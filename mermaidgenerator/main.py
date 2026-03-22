"""Main script for using the MermaidGenerator."""

import ast
import fnmatch
from argparse import ArgumentParser
from pathlib import Path

from .generator import ClassDiagramGenerator


def _is_excluded(file: Path, src_folder: Path, patterns: list[str]) -> bool:
    """Returns True if the file matches any of the exclude glob patterns.

    Args:
        file (Path): The file to check.
        src_folder (Path): The source root, used to compute relative paths.
        patterns (list[str]): Glob patterns to match against (e.g. '**/test_*.py').

    Returns:
        bool: True if the file should be excluded.
    """
    relative = str(file.relative_to(src_folder)).replace("\\", "/")
    return any(fnmatch.fnmatch(relative, pattern) for pattern in patterns)


def main() -> None:
    """Main function for Class analyser."""
    parser = ArgumentParser(description="Generate Mermaid diagrams")
    parser.add_argument("--src-folder", required=True, help="Source folder path")
    parser.add_argument("--doc-path", required=False, help="Documentation path")
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="PATTERN",
        help="Glob pattern of files to exclude, relative to --src-folder (can be repeated)",
    )

    args = parser.parse_args()
    src_folder = Path(args.src_folder)

    doc_path = Path(args.doc_path) if args.doc_path else src_folder.parent / "class_diagrams.md"

    generator = ClassDiagramGenerator()

    for python_file in src_folder.rglob("*.py"):
        if _is_excluded(python_file, src_folder, args.exclude):
            continue

        with open(python_file, encoding="utf-8") as f:
            source_code = f.read()

        tree = ast.parse(source_code)
        generator.visit(tree)

    generator.generate_markdown_output()
    generator.write_to_markdown(doc_path)


if __name__ == "__main__":
    main()
