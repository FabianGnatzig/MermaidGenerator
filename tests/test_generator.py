"""Tests for ClassDiagramGenerator."""

import ast

from mermaidgenerator.generator import ClassDiagramGenerator, _annotation_to_str


def _parse(source: str) -> ClassDiagramGenerator:
    """Parse source code and return a visited generator."""
    generator = ClassDiagramGenerator()
    generator.visit(ast.parse(source))
    generator.generate_markdown_output()
    return generator


def _output(source: str) -> str:
    """Return the full markdown output for the given source."""
    return "\n".join(_parse(source)._markdown_lines)


class TestAnnotationToStr:
    """Tests for the _annotation_to_str helper."""

    def test_none(self) -> None:
        """Returns empty string for None."""
        assert _annotation_to_str(None) == ""

    def test_simple_name(self) -> None:
        """Handles simple type names."""
        node = ast.parse("x: str").body[0].annotation
        assert _annotation_to_str(node) == "str"

    def test_generic(self) -> None:
        """Handles generic types like list[str]."""
        node = ast.parse("x: list[str]").body[0].annotation
        assert _annotation_to_str(node) == "list[str]"

    def test_union(self) -> None:
        """Handles union types like int | None."""
        node = ast.parse("x: int | None").body[0].annotation
        assert _annotation_to_str(node) == "int | None"

    def test_qualified(self) -> None:
        """Handles qualified types like typing.Optional."""
        node = ast.parse("x: typing.Optional").body[0].annotation
        assert _annotation_to_str(node) == "typing.Optional"

    def test_multi_generic(self) -> None:
        """Handles multi-param generics like dict[str, int]."""
        node = ast.parse("x: dict[str, int]").body[0].annotation
        assert _annotation_to_str(node) == "dict[str, int]"


class TestClassParsing:
    """Tests for visit_ClassDef and output generation."""

    def test_simple_class_header(self) -> None:
        """Class name appears as markdown heading."""
        out = _output('class Foo:\n    """A foo."""\n    pass')
        assert "# Foo" in out
        assert "A foo." in out

    def test_no_docstring_uses_filler(self) -> None:
        """Classes without docstrings get the filler text."""
        out = _output("class Foo:\n    pass")
        assert "No documentation provided." in out

    def test_public_attribute(self) -> None:
        """Public attributes get + visibility."""
        out = _output("class Foo:\n    def __init__(self) -> None:\n        self.name: str = ''")
        assert "+ str name" in out

    def test_private_attribute(self) -> None:
        """Private attributes get - visibility."""
        out = _output("class Foo:\n    def __init__(self) -> None:\n        self._value: int = 0")
        assert "- int \\_value" in out

    def test_static_method_suffix(self) -> None:
        """Static methods are marked with $."""
        source = "class Foo:\n    @staticmethod\n    def helper(x: str) -> str: ..."
        out = _output(source)
        assert "+ helper(x: str) str $" in out

    def test_classmethod_suffix(self) -> None:
        """Class methods are marked with $."""
        source = "class Foo:\n    @classmethod\n    def create(cls) -> 'Foo': ..."
        out = _output(source)
        assert "+ create() Foo $" in out

    def test_abstract_method_suffix(self) -> None:
        """Abstract methods are marked with *."""
        source = "from abc import abstractmethod\nclass Foo:\n    @abstractmethod\n    def run(self) -> None: ..."
        out = _output(source)
        assert "+ run() None *" in out

    def test_abc_stereotype(self) -> None:
        """Classes inheriting ABC get the abstract stereotype."""
        source = "from abc import ABC\nclass Foo(ABC):\n    pass"
        out = _output(source)
        assert "<<abstract>>" in out

    def test_dataclass_stereotype(self) -> None:
        """Dataclasses get the dataclass stereotype."""
        source = "from dataclasses import dataclass\n@dataclass\nclass Foo:\n    x: int = 0"
        out = _output(source)
        assert "<<dataclass>>" in out

    def test_property_rendered_as_attribute(self) -> None:
        """@property methods are rendered as attributes."""
        source = (
            "class Foo:\n"
            "    def __init__(self) -> None:\n"
            "        self._x: int = 0\n"
            "    @property\n"
            "    def x(self) -> int: ...\n"
        )
        out = _output(source)
        assert "+ int x" in out

    def test_property_suppresses_backing_field(self) -> None:
        """The private backing field is removed when a @property is defined."""
        source = (
            "class Foo:\n"
            "    def __init__(self) -> None:\n"
            "        self._x: int = 0\n"
            "    @property\n"
            "    def x(self) -> int: ...\n"
        )
        out = _output(source)
        assert "\\_x" not in out

    def test_property_setter_not_rendered(self) -> None:
        """@property.setter methods are not rendered."""
        source = (
            "class Foo:\n"
            "    @property\n"
            "    def x(self) -> int: ...\n"
            "    @x.setter\n"
            "    def x(self, value: int) -> None: ...\n"
        )
        out = _output(source)
        assert out.count("x") == 1  # only the attribute, not the setter


class TestInheritance:
    """Tests for parent class link generation."""

    def test_internal_parent_gets_anchor_link(self) -> None:
        """A parent defined in the same scan gets a markdown anchor link."""
        source = "class Base:\n    pass\nclass Child(Base):\n    pass"
        out = _output(source)
        assert "[Parent class](#base)" in out

    def test_external_parent_gets_plain_text(self) -> None:
        """A parent not found in the scan gets plain text."""
        source = "class Child(SomeExternalBase):\n    pass"
        out = _output(source)
        assert "Parent class: SomeExternalBase" in out
        assert "[Parent class]" not in out

    def test_abc_base_is_skipped(self) -> None:
        """ABC is in _SKIP_BASES and produces no parent entry."""
        source = "from abc import ABC\nclass Foo(ABC):\n    pass"
        out = _output(source)
        assert "Parent class" not in out

    def test_inheritance_arrow_in_diagram(self) -> None:
        """The Mermaid inheritance arrow is always rendered."""
        source = "class Base:\n    pass\nclass Child(Base):\n    pass"
        out = _output(source)
        assert "Base <|-- Child" in out

    def test_duplicate_class_is_skipped(self) -> None:
        """A class name seen twice is only rendered once."""
        source = "class Foo:\n    pass\nclass Foo:\n    pass"
        gen = _parse(source)
        assert len(gen._classes) == 1
