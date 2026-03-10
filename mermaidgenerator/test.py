from dataclasses import dataclass


class TestClass:
    """This is a test class."""

    def __init__(self):
        self._private_var = True
        self.public_var = False

    def _privatemethod(self, value: bool):
        self._private_var = value

    def publicmethod(self, value: bool):
        self.public_var = value


@dataclass
class TestDataClass:
    _value = False
    value = True
