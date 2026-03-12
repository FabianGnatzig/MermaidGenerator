"""Generator class for mermaid UML-Diagramm generation."""

import ast
from pathlib import Path

DOCSTRING_FILLER = "No documentation provided."


class ClassDiagramGenerator(ast.NodeVisitor):
    """Generator class for UML-Diagramm generation."""

    def __init__(self) -> None:
        """Initialisation of the generator."""
        self._classes = []
        self._markdown_lines = []
        self._seen_classes = set()

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Analysed the class definition.

        Gets called for each class that is defined in a sourcecode.

        Args:
            node (ast.ClassDef): ClassDef object of the class to analyse.
        """
        if node.name in self._seen_classes:
            return

        self._seen_classes.add(node.name)

        class_info = {
            "name": node.name,
            "decorator": "",
            "methods": [],
            "arguments": [],
            "returns": [],
            "attributes": [],
            "docstring": ast.get_docstring(node),
            "parent": None if not node.bases else f"{node.bases[0].id}",
        }

        if node.decorator_list:
            class_info["decorator"] = node.decorator_list[0].id

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                class_info["methods"].append(item.name)
                class_info["arguments"].append(self._get_arguments(item))
                class_info["returns"].append(self._get_return_types(item))

                if item.name != "__init__":
                    continue

                for function_item in item.body:
                    if not isinstance(function_item, ast.Assign):
                        continue

                    for target in function_item.targets:
                        if not isinstance(target, ast.Attribute):
                            continue

                    if target.attr in class_info["attributes"]:
                        continue

                    class_info["attributes"].append(target.attr)

            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if not isinstance(target, ast.Name):
                        continue

                    class_info["attributes"].append(target.id)

        self._classes.append(class_info)

    @staticmethod
    def _get_arguments(item: ast.FunctionDef) -> list[str]:
        """Generates a list of arguments.

        Args:
            item (ast.FunctionDef): Function definition item.

        Returns:
            list[str]: List of arguments as strings.
        """
        return [arg.arg for arg in item.args.args]

    @staticmethod
    def _get_return_types(item: ast.FunctionDef) -> str:
        """Generates a string with all return values.

        Args:
            item (ast.FunctionDef): Function definition item.

        Returns:
            str: Return type string.
        """
        if isinstance(item.returns, ast.Name):
            return item.returns.id

        if isinstance(item.returns, ast.Subscript):
            return_types = f"{item.returns.value.id}["

            tuple_items = item.returns.slice.elts

            for type in tuple_items:
                return_types += type.id
                if type != tuple_items[-1]:
                    return_types += ", "

            return_types += "]"
            return return_types

        else:
            return "None"

    def generate_markdown_output(self) -> None:
        """Generates the markdown / mermaid out of the analysed classes."""
        for cls in self._classes:
            docstring = cls["docstring"] if cls["docstring"] else DOCSTRING_FILLER

            self._create_mermaid_header(cls["name"], docstring, cls["decorator"], cls["parent"])

            for attr in cls["attributes"]:
                self.add_class_item(attr)

            for method in cls["methods"]:
                index = cls["methods"].index(method)
                self.add_class_item(method, True, cls["arguments"][index], cls["returns"][index])

            self._markdown_lines.append("}")
            self._markdown_lines.append("```")
            self._markdown_lines.append("")

    def _create_mermaid_header(self, name: str, docstring: str, decorator: str, parent: str = "") -> None:
        """Creates a header for the mermaid diagramm.

        Creates a heading, adds the docstring and creates the mermaid start.

        Args:
            name (str): Name of the class.
            docstring (str): Docstring of the class.
            decorator (str): Decorator of the class.
            parent (str): Name of the parent class. Default is "".
        """
        self._markdown_lines.append(f"# {name}")
        if docstring:
            self._markdown_lines.append(docstring)

        if parent:
            self._markdown_lines.append(f"[Parent class](#{parent.lower()})")

        self._markdown_lines.append("```mermaid")
        self._markdown_lines.append("classDiagram")

        if parent:
            self._markdown_lines.append(f"{parent} <|-- {name}")

        self._markdown_lines.append(f"    class {name}" + " {")

        if decorator:
            self._markdown_lines.append(f"<<{decorator}>>")

    def _create_mermaid_footer(self) -> None:
        """Adds a footer for the mermaid diagram."""
        self._markdown_lines.append("}")
        self._markdown_lines.append("```")
        self._markdown_lines.append("")

    def add_class_item(
        self, item_name: str, is_method: bool = False, argument: str = "", return_types: str = "None"
    ) -> None:
        """Adds a class item to the mermaid diagram.

        Class items are methods and attributes.

        Args:
            item_name (str): Defined name of the item.
            is_method (bool, optional): Flag if the item is a Method to add '()' to the name. Defaults to False.
            argument (str, optional): Argument of method. Defaults to "".
            return_types (str, optional): Return type hints. Defaults to "None".
        """
        if is_method:
            args_str = ", ".join(argument) if isinstance(argument, list) else argument
            item_name += f"({args_str}) -> {return_types}"

        if item_name.startswith("_"):
            item_name = item_name.replace("_", "\\_")
            self._markdown_lines.append(f"- {item_name}")
            return

        self._markdown_lines.append(f"+ {item_name}")

    def write_to_json(self, save_path: Path) -> None:
        """Writes the created markdown lines to a .md file.

        Args:
            save_path (Path): Path to save the markdown file.
        """
        with open(save_path, "w", encoding="utf-8") as file:
            file.write("\n".join(self._markdown_lines))


def main() -> None:
    """Main function for testing."""
    with open("mermaidgenerator/test.py") as f:
        source_code = f.read()

    tree = ast.parse(source_code)
    generator = ClassDiagramGenerator()
    generator.visit(tree)
    generator.generate_markdown_output()
    generator.write_to_json("class_diagrams.md")


if __name__ == "__main__":
    main()
