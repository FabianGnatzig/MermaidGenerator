# ClassDiagramGenerator
Generator class for UML-Diagramm generation.
[Parent class](#ast.nodevisitor)
```mermaid
classDiagram
ast.NodeVisitor <|-- ClassDiagramGenerator
    class ClassDiagramGenerator {
- \_classes
- \_markdown\_lines
- \_seen\_classes
- \_\_init\_\_() None
+ visit\_ClassDef(node: ast.ClassDef) None
- \_get\_stereotype(node: ast.ClassDef) str $
- \_process\_method(item: ast.FunctionDef, class_info: dict) None
- \_add\_attribute(class_info: dict, name: str, type_str: str) None
+ generate\_markdown\_output() None
- \_create\_mermaid\_header(name: str, docstring: str, stereotype: str, parents: list[str]) None
- \_create\_mermaid\_footer() None
- \_add\_attribute\_line(name: str, type_str: str) None
- \_add\_method\_line(method: dict) None
+ write\_to\_markdown(save_path: Path) None
}
```

# TestClass
This is a test class.
```mermaid
classDiagram
    class TestClass {
- bool \_private\_var
+ bool public\_var
+ bool private\_var
- \_\_init\_\_() None
- \_privatemethod(value: bool) bool
+ publicmethod(value: bool) tuple[str, bool]
+ static\_helper(text: str) str $
}
```

# AnotherClass
Its just a class with inhertation.
[Parent class](#testclass)
```mermaid
classDiagram
TestClass <|-- AnotherClass
    class AnotherClass {
- int \_class\_count
- str \_name
- \_\_init\_\_(name: str) None
+ create(name: str) AnotherClass $
- \_do\_something(name: str) list[str] $
}
```

# AbstractShape
Abstract base class for shapes.
```mermaid
classDiagram
    class AbstractShape {
<<abstract>>
+ str color
- \_\_init\_\_(color: str) None
+ area() float *
+ perimeter() float *
+ describe() str
}
```

# TestDataClass
This is a docstring.
```mermaid
classDiagram
    class TestDataClass {
<<dataclass>>
- bool \_value
+ bool value
+ str label
}
```
