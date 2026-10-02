from __future__ import annotations

import time

from etherlyzer.ieee.catalog import Catalog


def run(args):
    manager = Catalog()
    start = time.perf_counter()
    print("Synchronizing IEEE registries...\n")
    updated = manager.get_all_registries(check_for_updates=True)
    elapsed = time.perf_counter() - start
    print()
    print(f"Finished in {elapsed:.2f} seconds.")
    return 0


def register(subparsers):
    parser = subparsers.add_parser(
        "update",
        help="Synchronize IEEE registries",
    )

    parser.set_defaults(func=run)
