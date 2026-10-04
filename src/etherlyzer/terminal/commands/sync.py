from __future__ import annotations

import argparse
import time

from etherlyzer.ieee.catalog import Catalog


def run(args):
    manager = Catalog()
    start = time.perf_counter()
    print("Synchronizing IEEE registries...\n")
    manager.get_all_registries(check_for_updates=True,inform_if_synced_about_expiration=True)
    elapsed = time.perf_counter() - start
    print()
    print(f"Synchronization completed in {elapsed:.2f} seconds.")
    return 0


def register(subparsers):
    parser = subparsers.add_parser(
        "sync",
        help="Synchronize the local IEEE registry database with upstream sources.",
        description=(
            "Check upstream IEEE registry sources and refresh the local "
            "database when updates are available."
        ),
        epilog="""
Example:
  etherlyzer sync
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.set_defaults(func=run)
