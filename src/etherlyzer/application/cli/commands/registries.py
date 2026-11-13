from __future__ import annotations

import argparse

from etherlyzer.application.services.get import get_registry_entries
from etherlyzer.presentation.reporting.model import Report
from etherlyzer.presentation.reporting.renders import get_render


def run(args: argparse.Namespace) -> int:  # noqa; keep standard params.
    report = Report(sections=[get_registry_entries()])
    print(report.render(get_render("text")))
    return 0


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser(
        "registries",
        help="Show local IEEE registry metadata and synchronization status.",
        description=(
            "Display metadata for the locally configured IEEE registries, "
            "including category, source, prefix size, retrieval time, and "
            "update interval."
        ),
        epilog="""
Example:
  etherlyzer registries
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.set_defaults(func=run)
