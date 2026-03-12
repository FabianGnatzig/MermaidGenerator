"""Example file with test classes."""

from dataclasses import dataclass


class TestClass:
    """This is a test class."""

    def __init__(self) -> None:
        """Init method."""
        self._private_var = True
        self.public_var = False

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


class AnotherClass(TestClass):
    """Its just a class with inhertation."""

    def __init__(self, name: str) -> None:
        """Another init method.

        Args:
            name (str): A random name.
        """
        super().__init__()
        self._name = name


@dataclass
class TestDataClass:
    """This is a docstring."""

    _value = False
    value = True
