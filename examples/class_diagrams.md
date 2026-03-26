# TestClass
This is a test class.
```mermaid
classDiagram
    class TestClass {
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
