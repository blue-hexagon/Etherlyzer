from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Protocol

type ReportValue = str | int | float | bool | None


@dataclass(frozen=True, slots=True)
class Item:
    key: str
    value: ReportValue


@dataclass(slots=True)
class Section:
    title: str
    items: list[Item | Section] = field(default_factory=list)
    layout: Literal["default", "grid"] = "default"


@dataclass(slots=True)
class Report:
    sections: list[Section] = field(default_factory=list)

    def render(self, renderer: ReportRenderer) -> str:
        return renderer.render(self)


class ReportRenderer(Protocol):
    def render(self, report: Report) -> str: ...
