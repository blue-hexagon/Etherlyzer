from __future__ import annotations

import argparse

from etherlyzer import __version__
from etherlyzer.ieee.registry.provider import RegistryProvider


def run(args: argparse.Namespace) -> int:
    manager = RegistryProvider()

    print()

    print(f"EtherLyzer {__version__}")
    print()

    print("Registries")
    registries = manager.get_all(require_cache=True)
    if not args.verbose:
        for registry in registries:
            print(
                f"Name            : {registry.name} ({registry.full_name})"
                f"\nCategory        : {registry.category}"
                f"\nDescription     : {registry.description}"
                f"\nFile            : {registry.registry_cache.filepath}"
                f"\nSource URL      : {registry.url}"
                f"\nLast Retrieved  : {registry.registry_cache.last_retrieved}"
            )
            print()
    else:
        for registry in manager.get_all(require_cache=True):
            print(
                f"Name            : {registry.name} ({registry.full_name})"
                f"\nLegacy Name     : {registry.legacy_name}"
                f"\nCategory        : {registry.category}"
                f"\nDescription     : {registry.description}"
                f"\nLegacy          : {registry.legacy}"
                f"\nFile            : {registry.registry_cache.filepath}"
                f"\nSource URL      : {registry.url}"
                f"\nPrefix Bits     : {registry.prefix_bits}"
                f"\nLast Retrieved  : {registry.registry_cache.last_retrieved}"
                f"\nUpdate Interval : {registry.registry_cache.update_interval}"
            )
            print()

    print()

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
