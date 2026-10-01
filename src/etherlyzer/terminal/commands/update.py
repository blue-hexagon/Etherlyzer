from __future__ import annotations

import time

from etherlyzer.ieee.registry import Registry


def run(args):
    manager = Registry()
    start = time.perf_counter()
    print("Synchronizing IEEE registries...\n")
    updated = manager.get_registries(update=True)
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
