from __future__ import annotations

from typing import TYPE_CHECKING, Literal

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


def get_renderer(kind: Literal["text", "json", "csv"] = "text") -> ReportRenderer:
    """Create a renderer for the specified report output format.

    Args:
        kind: Defaults to ``text`` if no argument is given.

    Returns:
        A new renderer instance implementing the ReportRenderer interface.
        Unknown formats fall back to TextRenderer.

    Examples:
        Create a report::

            >>> from etherlyzer.presentation import Item, Report, Section
            >>> report = Report(
            ...     sections=[
            ...         Section(
            ...             title="MAC Analysis",
            ...             items=[Item("Address", "00:11:22:33:44:55")],
            ...         )
            ...     ]
            ... )

        Render directly using a renderer::

            >>> output = get_renderer("text").render(report)

        Alternatively, render through the report interface::

            >>> output = report.render(get_renderer("json"))
    """
    try:
        return RENDERERS[kind]()
    except KeyError:
        return TextRenderer()
