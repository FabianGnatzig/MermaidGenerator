# MermaidGenerator
Generates Mermaid Diagrams from Python classes.
[Look at an example](/class_diagrams.md)

The tool parses Python source code and generates Mermaid class diagrams based on the class structure, inheritance relationships, and method signatures found in your Python files. It supports both single-file and multi-file projects, making it easy to visualize complex Python architectures.

**Made by Fabian Gnatzig in 2026.**

## Usage
```
python -m mermaidgenerator [-h] --src-folder SRC_FOLDER [--doc-path DOC_PATH]
```

To use the generator, simply run the command with the appropriate arguments:
- `--src-folder`: The path to the root directory of your Python project
- `--doc-path`: Optional path to save the generated Mermaid diagrams (defaults to current directory)

Example usage:
```
python -m mermaidgenerator [-h] --src-folder C:\Users\user\python_project\src --doc-path C:\Users\user\python_project\docs
```
