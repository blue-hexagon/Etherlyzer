from __future__ import annotations

import argparse



def run(args: argparse.Namespace) -> int:
    entry = Registrylookup(args.mac)

    if entry is None:
        print("No match.")
        return 1

    print()

    print(f"Registry     : {entry.registry}")
    print(f"Assignment   : {entry.assignment}")
    print(f"Organization : {entry.organization_name}")
    print(f"Address      : {entry.organization_address}")

    if hasattr(entry, "protocol"):
        print(f"Protocol     : {entry.protocol}")

    print()

    return 0


def register(subparsers):
    parser = subparsers.add_parser(
        "lookup",
        help="Lookup a MAC address",
    )

    parser.add_argument(
        "mac",
        help="MAC address",
    )

    parser.set_defaults(func=run)
