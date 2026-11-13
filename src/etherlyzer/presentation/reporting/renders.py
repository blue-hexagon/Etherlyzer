from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from etherlyzer.presentation.reporting.model import ReportRenderer
from etherlyzer.presentation.reporting.renderers.csv import CSVRenderer
from etherlyzer.presentation.reporting.renderers.json import JSONRenderer
from etherlyzer.presentation.reporting.renderers.text import TextRenderer

RENDERERS: dict[str, type[ReportRenderer]] = {
    "text": TextRenderer,
    "json": JSONRenderer,
    "csv": CSVRenderer,
}


def get_render_choices() -> list[str]:
    return list(RENDERERS)


def get_render(kind: str = "text") -> ReportRenderer:
    try:
        return RENDERERS[kind]()
    except KeyError:
        return TextRenderer()
