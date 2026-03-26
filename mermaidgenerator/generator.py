"""Generator class for mermaid UML-Diagramm generation."""

import ast
from pathlib import Path

DOCSTRING_FILLER = "No documentation provided."
_SKIP_ARGS = {"self", "cls"}
_SKIP_BASES = {"ABC", "object"}
_PROPERTY_VARIANTS = {"setter", "deleter", "getter"}


def _annotation_to_str(node: ast.expr | None) -> str:
    """Converts an AST annotation node to a readable type string.

    Args:
        node (ast.expr | None): The annotation AST node.

    Returns:
        str: The type as a string, or empty string if unresolvable.
    """
    if node is None:
        return ""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{node.value.id}.{node.attr}"
    if isinstance(node, ast.Subscript):
        outer = _annotation_to_str(node.value)
        try:
            inner = ", ".join(_annotation_to_str(e) for e in node.slice.elts)
        except AttributeError:
            inner = _annotation_to_str(node.slice)
        return f"{outer}[{inner}]"
    if isinstance(node, ast.Constant):
        return str(node.value)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        return f"{_annotation_to_str(node.left)} | {_annotation_to_str(node.right)}"
    return ""


class ClassDiagramGenerator(ast.NodeVisitor):
    """Generator class for UML-Diagramm generation."""

    def __init__(self) -> None:
        """Initialisation of the generator."""
        self._classes = []
        self._markdown_lines = []
        self._seen_classes = set()

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Analyses the class definition.

        Gets called for each class that is defined in a sourcecode.

        Args:
            node (ast.ClassDef): ClassDef object of the class to analyse.
        """
        if node.name in self._seen_classes:
            return

        self._seen_classes.add(node.name)

        parents = []
        for base in node.bases:
            if isinstance(base, ast.Attribute):
                qualified = f"{base.value.id}.{base.attr}"
                if base.attr not in _SKIP_BASES:
                    parents.append(qualified)
            elif isinstance(base, ast.Name) and base.id not in _SKIP_BASES:
                parents.append(base.id)

        class_info = {
            "name": node.name,
            "stereotype": self._get_stereotype(node),
            "methods": [],
            "attributes": [],
            "docstring": ast.get_docstring(node),
            "parents": parents,
        }

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                self._process_method(item, class_info)
            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        self._add_attribute(class_info, target.id, "")
            elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                self._add_attribute(class_info, item.target.id, _annotation_to_str(item.annotation))

        self._classes.append(class_info)

    @staticmethod
    def _get_stereotype(node: ast.ClassDef) -> str:
        """Determines the Mermaid stereotype for a class node.

        Checks bases for ABC (abstract) and decorators (e.g. dataclass).

        Args:
            node (ast.ClassDef): ClassDef object of the class to analyse.

        Returns:
            str: Stereotype string (e.g. "dataclass", "abstract"), or empty string.
        """
        for base in node.bases:
            if (isinstance(base, ast.Name) and base.id == "ABC") or (
                isinstance(base, ast.Attribute) and base.attr == "ABC"
            ):
                return "abstract"

        for dec in node.decorator_list:
            if isinstance(dec, ast.Name):
                return dec.id
            if isinstance(dec, ast.Attribute):
                return dec.attr

        return ""

    def _process_method(self, item: ast.FunctionDef, class_info: dict) -> None:
        """Processes a method definition and updates class_info.

        Handles properties, static/class methods, abstract methods, and
        instance attribute assignments inside __init__.

        Args:
            item (ast.FunctionDef): The method AST node.
            class_info (dict): The class info dict to update.
        """
        dec_names = set()
        for dec in item.decorator_list:
            if isinstance(dec, ast.Name):
                dec_names.add(dec.id)
            elif isinstance(dec, ast.Attribute):
                dec_names.add(dec.attr)

        if dec_names & _PROPERTY_VARIANTS:
            return

        if "property" in dec_names:
            self._add_attribute(class_info, item.name, _annotation_to_str(item.returns))
            class_info["attributes"] = [a for a in class_info["attributes"] if a["name"] != f"_{item.name}"]
            return

        args = []
        for arg in item.args.args:
            if arg.arg in _SKIP_ARGS:
                continue
            type_str = _annotation_to_str(arg.annotation)
            args.append(f"{arg.arg}: {type_str}" if type_str else arg.arg)

        class_info["methods"].append(
            {
                "name": item.name,
                "args": args,
                "return_type": _annotation_to_str(item.returns) or "None",
                "is_static": "staticmethod" in dec_names or "classmethod" in dec_names,
                "is_abstract": "abstractmethod" in dec_names,
            }
        )

        if item.name == "__init__":
            for func_item in item.body:
                if isinstance(func_item, ast.Assign):
                    for target in func_item.targets:
                        if (
                            isinstance(target, ast.Attribute)
                            and isinstance(target.value, ast.Name)
                            and target.value.id == "self"
                        ):
                            self._add_attribute(class_info, target.attr, "")
                elif isinstance(func_item, ast.AnnAssign):
                    target = func_item.target
                    if (
                        isinstance(target, ast.Attribute)
                        and isinstance(target.value, ast.Name)
                        and target.value.id == "self"
                    ):
                        self._add_attribute(class_info, target.attr, _annotation_to_str(func_item.annotation))

    def _add_attribute(self, class_info: dict, name: str, type_str: str) -> None:
        """Adds an attribute to class_info if not already present.

        Args:
            class_info (dict): The class info dict to update.
            name (str): Attribute name.
            type_str (str): Attribute type as a string.
        """
        if not any(a["name"] == name for a in class_info["attributes"]):
            class_info["attributes"].append({"name": name, "type": type_str})

    def generate_markdown_output(self) -> None:
        """Generates the markdown / mermaid out of the analysed classes."""
        for cls in self._classes:
            docstring = cls["docstring"] if cls["docstring"] else DOCSTRING_FILLER
            self._create_mermaid_header(cls["name"], docstring, cls["stereotype"], cls["parents"])

            for attr in cls["attributes"]:
                self._add_attribute_line(attr["name"], attr["type"])

            for method in cls["methods"]:
                self._add_method_line(method)

            self._create_mermaid_footer()

    def _create_mermaid_header(self, name: str, docstring: str, stereotype: str, parents: list[str]) -> None:
        """Creates a header for the mermaid diagram.

        Args:
            name (str): Name of the class.
            docstring (str): Docstring of the class.
            stereotype (str): Mermaid stereotype (e.g. "dataclass", "abstract").
            parents (list[str]): Names of all parent classes.
        """
        self._markdown_lines.append(f"# {name}")
        if docstring:
            self._markdown_lines.append(docstring)

        for parent in parents:
            if parent in self._seen_classes:
                self._markdown_lines.append(f"[Parent class](#{parent.lower()})")
            else:
                self._markdown_lines.append(f"Parent class: {parent}")

        self._markdown_lines.append("```mermaid")
        self._markdown_lines.append("classDiagram")

        for parent in parents:
            self._markdown_lines.append(f"{parent} <|-- {name}")

        self._markdown_lines.append(f"    class {name}" + " {")

        if stereotype:
            self._markdown_lines.append(f"<<{stereotype}>>")

    def _create_mermaid_footer(self) -> None:
        """Adds a footer for the mermaid diagram."""
        self._markdown_lines.append("}")
        self._markdown_lines.append("```")
        self._markdown_lines.append("")

    def _add_attribute_line(self, name: str, type_str: str) -> None:
        """Adds an attribute line to the mermaid diagram.

        Args:
            name (str): Attribute name.
            type_str (str): Attribute type string, or empty if unknown.
        """
        visibility = "-" if name.startswith("_") else "+"
        escaped = name.replace("_", "\\_")
        type_part = f"{type_str} " if type_str else ""
        self._markdown_lines.append(f"{visibility} {type_part}{escaped}")

    def _add_method_line(self, method: dict) -> None:
        """Adds a method line to the mermaid diagram.

        Appends $ for static/classmethod and * for abstract methods.

        Args:
            method (dict): Method info with name, args, return_type, is_static, is_abstract.
        """
        name = method["name"]
        args_str = ", ".join(method["args"])
        return_type = method["return_type"]
        escaped = name.replace("_", "\\_")
        visibility = "-" if name.startswith("_") else "+"

        suffix = "$" if method["is_static"] else ("*" if method["is_abstract"] else "")
        line = f"{visibility} {escaped}({args_str}) {return_type}"
        if suffix:
            line += f" {suffix}"
        self._markdown_lines.append(line)

    def write_to_markdown(self, save_path: Path) -> None:
        """Writes the created markdown lines to a .md file.

        Args:
            save_path (Path): Path to save the markdown file.
        """
        with open(save_path, "w", encoding="utf-8") as file:
            file.write("\n".join(self._markdown_lines))
