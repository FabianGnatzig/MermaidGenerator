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
