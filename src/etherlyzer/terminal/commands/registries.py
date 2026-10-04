from __future__ import annotations

import argparse

from etherlyzer.ieee.catalog import Catalog
from etherlyzer import __version__


def run(args):
    manager = Catalog()

    print()

    print(f"EtherLyzer {__version__}")
    print()

    print("Registries")

    for registry in manager.get_all_registries(check_for_updates=False):
        print(
            f"Name            : {registry.name} ({registry.full_name})"
            f"\nLegacy Name     : {registry.legacy_name}"
            f"\nCategory        : {registry.category}"
            f"\nDescription     : {registry.description}"
            f"\nLegacy          : {registry.legacy}"
            f"\nFile            : {registry.filepath}"
            f"\nSource URL      : {registry.url}"
            f"\nPrefix Bits     : {registry.prefix_bits}"
            f"\nLast Retrieved  : {registry.last_retrieved}"
            f"\nUpdate Interval : {registry.update_interval}"
        )
        print()

    print()

    return 0


def register(subparsers):
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
