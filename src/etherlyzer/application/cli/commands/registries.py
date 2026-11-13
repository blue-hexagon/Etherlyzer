from __future__ import annotations

import argparse

from etherlyzer.infrastructure.registry.provider import RegistryProvider
from etherlyzer.presentation.reporting.model import Item, Report, Section
from etherlyzer.presentation.reporting.renders import get_render


def run(args: argparse.Namespace) -> int:
    manager = RegistryProvider()

    registries = manager.get_all(require_cache=True)
    reg_sections = []
    if not args.verbose:
        for registry in registries:
            reg_sections.append(  # noqa: PERF401
                Section(
                    title=f"{registry.name} ({registry.full_name})",
                    items=[
                        Item(key="Category", value=registry.family),
                        Item(key="Description", value=registry.description),
                        Item(key="File", value=str(registry.registry_cache.filepath)),
                        Item(key="Source URL", value=str(registry.url)),
                        Item(
                            key="Last Retrieved", value=str(registry.registry_cache.last_retrieved)
                        ),
                    ],
                )
            )
    else:
        for registry in manager.get_all(require_cache=True):
            reg_sections.append(  # noqa: PERF401
                Section(
                    title=f"{registry.name} ({registry.full_name})",
                    items=[
                        Item(key="Legacy Name", value=registry.legacy_name),
                        Item(key="Category", value=registry.family),
                        Item(key="Description", value=registry.description),
                        Item(key="Legacy", value=registry.legacy),
                        Item(key="File", value=str(registry.registry_cache.filepath)),
                        Item(key="Source URL", value=str(registry.url)),
                        Item(key="Prefix Bits", value=str(registry.prefix_bits)),
                        Item(
                            key="Last Retrieved", value=str(registry.registry_cache.last_retrieved)
                        ),
                        Item(
                            key="Update Interval",
                            value=str(registry.registry_cache.update_interval),
                        ),
                    ],
                )
            )

    main_section = Section(title="Registries", items=reg_sections)
    report = Report(sections=[main_section])
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
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print verbose output",
    )

    parser.set_defaults(func=run)
