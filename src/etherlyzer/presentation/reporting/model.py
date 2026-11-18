from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Protocol

type ReportValue = str | int | float | bool | None


@dataclass(frozen=True, slots=True)
class Item:
    """Represent a single key-value pair in a report."""

    key: str
    value: ReportValue


@dataclass(slots=True)
class Table:
    columns: tuple[str, ...]
    rows: list[tuple[ReportValue, ...]] = field(default_factory=list)

    def append(self, *values: ReportValue) -> None:
        if len(values) != len(self.columns):
            raise ValueError(f"Expected {len(self.columns)} values, received {len(values)}")

        self.rows.append(values)


@dataclass(slots=True)
class Section:
    """Represent a section containing report elements.

    Sections can contain individual items, tables, and nested
    sections, allowing hierarchical reports to be constructed.

    Examples:
        >>> section = Section(title="MAC Analysis")
        >>> section.append(Item("Address", "00:00:0C:12:34:56"))
        >>> section.append(Item("Vendor", "Cisco Systems, Inc"))

        Create a nested section:

        >>> details = Section(
        ...     title="Address Properties",
        ...     items=[
        ...         Item("Individual", True),
        ...         Item("Locally Administered", False),
        ...     ],
        ... )
        >>> section.append(details)
    """

    title: str | None = None
    items: list[Item | Section | Table] = field(default_factory=list)
    layout: Literal["default", "grid"] = "default"
    legend: str | None = None

    def append(self, item: Item | Section) -> None:
        self.items.append(item)


@dataclass(slots=True)
class Report:
    """Represent a structured report composed of sections.

    Reports are independent of their output format. They can
    be rendered using any compatible ReportRenderer implementation.

    Examples:
        Create a report:

        >>> report = Report()
        >>> report.sections.append(
        ...     Section(
        ...         title="MAC Analysis",
        ...         items=[
        ...             Item("Address", "00:00:0C:12:34:56"),
        ...             Item("Vendor", "Cisco Systems, Inc"),
        ...         ],
        ...     )
        ... )

        Render the report using the text renderer:

        >>> from etherlyzer.presentation import get_renderer
        >>> output = report.render(get_renderer("text"))

        Alternatively, render as JSON:

        >>> output = report.render(get_renderer("json"))
    """

    sections: list[Section] = field(default_factory=list)

    def render(self, selected: ReportRenderer) -> str:
        """Render the report using the selected renderer.

        Args:
            selected: Renderer implementing the ReportRenderer
                interface.

        Returns:
            The rendered report as a string.
        """
        return selected.render(self)

    @property
    def previous_section(self) -> Section:
        """Return the most recently added top-level section.

        Raises:
            IndexError: If the report contains no sections.
        """
        return self.sections[-1]


class ReportRenderer(Protocol):
    """Define the interface for report renderer implementations."""

    def render(self, report: Report) -> str:
        """Render a report into a string representation."""
        ...
