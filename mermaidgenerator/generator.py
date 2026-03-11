"""Generator class for mermaid UML-Diagramm generation."""

import ast

DOCSTRING_FILLER = "No documentation provided."


class ClassDiagramGenerator(ast.NodeVisitor):
    """Generator class for UML-Diagramm generation."""

    def __init__(self) -> None:
        """Initialisation of the generator."""
        self._classes = []
        self._markdown_lines = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Analysed the class definition.

        Gets called for each class that is defined in a sourcecode.

        Args:
            node (ast.ClassDef): ClassDef object of the class to analyse.
        """
        class_info = {
            "name": node.name,
            "decorator": "",
            "methods": [],
            "attributes": [],
            "docstring": ast.get_docstring(node),
        }
        if node.decorator_list:
            class_info["decorator"] = node.decorator_list[0].id

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                class_info["methods"].append(item.name)
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
        self.generic_visit(node)

    def generate_markdown_output(self) -> None:
        """Generates the markdown / mermaid out of the analysed classes."""
        for cls in self._classes:
            docstring = cls["docstring"] if cls["docstring"] else DOCSTRING_FILLER

            self._create_mermaid_header(cls["name"], docstring, cls["decorator"])

            for attr in cls["attributes"]:
                self.add_class_item(attr)

            for method in cls["methods"]:
                self.add_class_item(method, True)

            self._markdown_lines.append("}")
            self._markdown_lines.append("```")
            self._markdown_lines.append("")

        self._write_to_json()

    def _create_mermaid_header(self, name: str, docstring: str, decorator: str) -> None:
        """Creates a header for the mermaid diagramm.

        Creates a heading, adds the docstring and creates the mermaid start.

        Args:
            name (str): Name of the class.
            docstring (str): Docstring of the class.
            decorator (str): Decorator of the class.
        """
        self._markdown_lines.append(f"# {name}")
        if docstring:
            self._markdown_lines.append(docstring)

        self._markdown_lines.append("```mermaid")
        self._markdown_lines.append("classDiagram")
        self._markdown_lines.append(f"    class {name}" + " {")

        if decorator:
            self._markdown_lines.append(f"<<{decorator}>>")

    def _create_mermaid_footer(self) -> None:
        """Adds a footer for the mermaid diagram."""
        self._markdown_lines.append("}")
        self._markdown_lines.append("```")
        self._markdown_lines.append("")

    def add_class_item(self, item_name: str, is_method: bool = False) -> None:
        """Adds a class item to the mermaid diagram.

        Class items are methods and attributes.

        Args:
            item_name (str): Defined name of the item.
            is_method (bool, optional): Flag if the item is a Method to add '()' to the name. Defaults to False.
        """
        if is_method:
            item_name += "()"

        if item_name.startswith("_"):
            item_name = item_name.replace("_", "\\_")
            self._markdown_lines.append(f"- {item_name}")
            return

        self._markdown_lines.append(f"+ {item_name}")

    def _write_to_json(self) -> None:
        """Writes the created markdown lines to a .md file."""
        with open("UML-Diagram.md", "w", encoding="utf-8") as file:
            file.write("\n".join(self._markdown_lines))


def main() -> None:
    """Main function for testing."""
    with open("mermaidgenerator/test.py") as f:
        source_code = f.read()

    tree = ast.parse(source_code)
    generator = ClassDiagramGenerator()
    generator.visit(tree)
    generator.generate_markdown_output()


if __name__ == "__main__":
    main()
