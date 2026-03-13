"""Main script for using the MermaidGenerator."""

import ast
from argparse import ArgumentParser
from pathlib import Path

from .generator import ClassDiagramGenerator


def main() -> None:
    """Main function for Class analyser."""
    parser = ArgumentParser(description="Generate Mermaid diagrams")
    parser.add_argument("--src-folder", required=True, help="Source folder path")
    parser.add_argument("--doc-path", required=False, help="Documentation path")

    args = parser.parse_args()
    src_folder = Path(args.src_folder)

    doc_path = Path(args.doc_path) if args.doc_path else src_folder.parent / "class_diagrams.md"

    all_python_files = src_folder.rglob("*.py")
    generator = ClassDiagramGenerator()

    for python_file in all_python_files:
        with open(python_file) as f:
            source_code = f.read()

        tree = ast.parse(source_code)
        generator.visit(tree)

    generator.generate_markdown_output()
    generator.write_to_json(doc_path)


if __name__ == "__main__":
    main()
