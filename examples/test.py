"""Example file with test classes."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


class TestClass:
    """This is a test class."""

    def __init__(self) -> None:
        """Init method."""
        self._private_var: bool = True
        self.public_var: bool = False

    def _privatemethod(self, value: bool) -> bool:
        """A private method.

        Args:
            value (bool): A value.
        """
        self._private_var = value
        return True

    def publicmethod(self, value: bool) -> tuple[str, bool]:
        """A public method.

        Args:
            value (bool): A value.
        """
        self.public_var = value

    @staticmethod
    def static_helper(text: str) -> str:
        """A static helper method.

        Args:
            text (str): Input text.
        """
        return text.upper()

    @property
    def private_var(self) -> bool:
        """Getter for private_var."""
        return self._private_var

    @private_var.setter
    def private_var(self, value: bool) -> None:
        """Setter for private_var."""
        self._private_var = value


class AnotherClass(TestClass):
    """Its just a class with inhertation."""

    _class_count: int = 0

    def __init__(self, name: str) -> None:
        """Another init method.

        Args:
            name (str): A random name.
        """
        super().__init__()
        self._name: str = name

    @classmethod
    def create(cls, name: str) -> "AnotherClass":
        """Factory class method.

        Args:
            name (str): A random name.
        """
        return cls(name)

    @staticmethod
    def _do_something(name: str) -> list[str]:
        """Does something.

        Args:
            name (str): A random name.
        """
        return [name.capitalize()]


class AbstractShape(ABC):
    """Abstract base class for shapes."""

    def __init__(self, color: str) -> None:
        """Init method.

        Args:
            color (str): The shape color.
        """
        self.color: str = color

    @abstractmethod
    def area(self) -> float:
        """Calculate the area."""

    @abstractmethod
    def perimeter(self) -> float:
        """Calculate the perimeter."""

    def describe(self) -> str:
        """Describe the shape."""
        return f"A {self.color} shape"


@dataclass
class TestDataClass:
    """This is a docstring."""

    _value: bool = False
    value: bool = True
    label: str = "default"


class Engine:
    """Represents a car engine."""

    def __init__(self, horsepower: int) -> None:
        """Init method.

        Args:
            horsepower (int): Engine power in HP.
        """
        self.horsepower: int = horsepower

    def start(self) -> None:
        """Start the engine."""

    def stop(self) -> None:
        """Stop the engine."""


class Vehicle:
    """Base class for all vehicles."""

    def __init__(self, make: str, year: int) -> None:
        """Init method.

        Args:
            make (str): Manufacturer name.
            year (int): Production year.
        """
        self.make: str = make
        self.year: int = year

    def describe(self) -> str:
        """Return a description of the vehicle."""


class Car(Vehicle):
    """A car — demonstrates inheritance from Vehicle and association with Engine."""

    def __init__(self, make: str, year: int, model: str, engine: Engine) -> None:
        """Init method.

        Args:
            make (str): Manufacturer name.
            year (int): Production year.
            model (str): Car model name.
            engine (Engine): The engine instance.
        """
        super().__init__(make, year)
        self.model: str = model
        self.engine: Engine = engine

    def drive(self) -> None:
        """Start the engine and drive."""
        self.engine.start()
