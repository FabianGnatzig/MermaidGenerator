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


**Inherits:** [TestClass](#testclass)
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

# Engine
Represents a car engine.
```mermaid
classDiagram
    class Engine {
+ int horsepower
- \_\_init\_\_(horsepower: int) None
+ start() None
+ stop() None
}
```

# Vehicle
Base class for all vehicles.
```mermaid
classDiagram
    class Vehicle {
+ str make
+ int year
- \_\_init\_\_(make: str, year: int) None
+ describe() str
}
```

# Car
A car — demonstrates inheritance from Vehicle and association with Engine.


**Inherits:** [Vehicle](#vehicle)


**Uses:** [Engine](#engine)
```mermaid
classDiagram
Vehicle <|-- Car
Car --> Engine : engine
    class Car {
+ str model
+ Engine engine
- \_\_init\_\_(make: str, year: int, model: str, engine: Engine) None
+ drive() None
}
```
