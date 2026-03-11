"""Example file with test classes."""

from dataclasses import dataclass


class TestClass:
    """This is a test class."""

    def __init__(self) -> None:
        """Init method."""
        self._private_var = True
        self.public_var = False

    def _privatemethod(self, value: bool) -> None:
        """A private method.

        Args:
            value (bool): A value.
        """
        self._private_var = value

    def publicmethod(self, value: bool) -> None:
        """A public method.

        Args:
            value (bool): A value.
        """
        self.public_var = value


@dataclass
class TestDataClass:
    """This is a docstring."""

    _value = False
    value = True
