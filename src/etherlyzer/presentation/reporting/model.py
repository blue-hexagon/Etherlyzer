from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Protocol

type ReportValue = str | int | float | bool | None


@dataclass(frozen=True, slots=True)
class Item:
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
    title: str | None = None
    items: list[Item | Section | Table] = field(default_factory=list)
    layout: Literal["default", "grid"] = "default"
    legend: str | None = None

    def append(self, item: Item | Section) -> None:
        self.items.append(item)


@dataclass(slots=True)
class Report:
    sections: list[Section] = field(default_factory=list)

    def render(self, selected: ReportRenderer) -> str:
        return selected.render(self)

    @property
    def previous_section(self) -> Section:
        return self.sections[-1]


class ReportRenderer(Protocol):
    def render(self, report: Report) -> str: ...
