from __future__ import annotations

import argparse
import time

from etherlyzer.ieee.registry.catalog import Catalog


def normalize_name(name: str) -> str:
    return name.lower().replace("-", "")


def run(args: argparse.Namespace) -> int:
    manager = Catalog()
    start = time.perf_counter()

    if args.status is None and args.force is None:
        print("Checking and managing IEEE registry synchronization state...\n")
        manager.get_all_registries_and_ensure_cache_is_synced(
            check_for_updates=True,
            inform_if_synced_about_expiration=True,
        )
    else:
        registries = manager.get_registries()
        requested = {
            normalize_name(name)
            for name in (args.status if args.status is not None else args.force)
        }

        available = {normalize_name(registry.name) for registry in registries}

        if unknown := requested - available:
            print(f"Unknown registries: {', '.join(sorted(unknown))}")
            return 2

        for registry in registries:
            if requested and normalize_name(registry.name) not in requested:
                continue

            if args.status is not None:
                registry.registry_cache.need_updates(inform_if_synced_about_expiration=True)
            else:
                registry.registry_downloader.fetch_online()

    elapsed = time.perf_counter() - start

    print()
    print(f"Task completed in {elapsed:.2f} seconds.")
    return 0


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser(
        "sync",
        help="Synchronize the local IEEE registry database with upstream sources.",
        description=(
            "Check upstream IEEE registry sources and refresh the local "
            "database when updates are available."
        ),
        epilog="""
Examples:
  etherlyzer sync                  Check and synchronize expired registries
  etherlyzer sync --status         Show expiration status for all registries
  etherlyzer sync -s MA-L          Show expiration status for MA-L
  etherlyzer sync --force          Force synchronization of all registries
  etherlyzer sync -f MA-L MA-M     Force synchronization of selected registries
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    actions = parser.add_mutually_exclusive_group()

    actions.add_argument(
        "-s",
        "--status",
        nargs="*",
        metavar="REGISTRY",
        default=None,
        help="Get the expiration status of all or selected IEEE registries.",
    )

    actions.add_argument(
        "-f",
        "--force",
        nargs="*",
        metavar="REGISTRY",
        default=None,
        help="Force synchronization of all or selected IEEE registries.",
    )
    parser.set_defaults(func=run)
