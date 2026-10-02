from __future__ import annotations

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
            f"IEEE Name: {registry.name} ({registry.full_name})"
            f"\nLegacy Name: {registry.legacy_name}"
            f"\nCategory: {registry.category}"
            f"\nDescription: {registry.description}"
            f"\nIs Legacy: {registry.legacy}"
            f"\nFilepath: {registry.filepath}"
            f"\nURL: {registry.url}"
            f"\nPrefix bits: {registry.prefix_bits}"
            f"\nLast retrieved: {registry.last_retrieved}"
            f"\nUpdate interval: {registry.update_interval}"
        )
        print()

    print()

    return 0


def register(subparsers):
    parser = subparsers.add_parser(
        "info",
        help="Show application information",
    )

    parser.set_defaults(func=run)
