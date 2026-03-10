import ast


class ClassDiagramGenerator(ast.NodeVisitor):
    def __init__(self):
        self.classes = []

    def visit_ClassDef(self, node):
        class_info = {"name": node.name, "methods": [], "attributes": [], "docstring": ast.get_docstring(node)}

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                class_info["methods"].append(item.name)
                for function_item in item.body:
                    if isinstance(function_item, ast.Assign):
                        for target in function_item.targets:
                            if isinstance(target, ast.Attribute):
                                class_info["attributes"].append(target.attr)

            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        class_info["attributes"].append(target.id)

        self.classes.append(class_info)
        self.generic_visit(node)


def generate_markdown_output(classes):
    markdown_lines = []
    for cls in classes:
        # H1 heading for class name
        markdown_lines.append(f"# {cls['name']}")

        # Docstring as summary
        if cls["docstring"]:
            markdown_lines.append(f"{cls['docstring']}")
        else:
            markdown_lines.append("No documentation provided.")

        # UML diagram section
        markdown_lines.append("```mermaid")
        markdown_lines.append("classDiagram")
        markdown_lines.append(f"    class {cls['name']}")

        # Add attributes with private check
        for attr in cls["attributes"]:
            if attr.startswith("_"):
                markdown_lines.append(f"    {cls['name']} : -{attr}")
            else:
                markdown_lines.append(f"    {cls['name']} : +{attr}")

        # Add methods with private check
        for method in cls["methods"]:
            if method.startswith("_"):
                markdown_lines.append(f"    {cls['name']} : -{method}()")
            else:
                markdown_lines.append(f"    {cls['name']} : +{method}()")

        markdown_lines.append("```")
        markdown_lines.append("")  # Empty line for separation
    return "\n".join(markdown_lines)


def main():
    # Read the Python file containing classes
    with open("mermaidgenerator/test.py", "r") as f:
        source_code = f.read()

    # Parse the source code
    tree = ast.parse(source_code)

    # Generate class diagram
    generator = ClassDiagramGenerator()
    generator.visit(tree)

    # Create markdown output
    markdown_content = generate_markdown_output(generator.classes)

    # Save to file
    with open("UML-Diagram.md", "w") as f:
        f.write(markdown_content)


if __name__ == "__main__":
    main()
