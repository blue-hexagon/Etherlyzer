from __future__ import annotations

from pathlib import Path

from etherlyzer.ieee.database import RegistryIndex
from etherlyzer.ieee.registry import Registry
from etherlyzer.terminal.cliutil import read_multiline


def run(args):
    index = RegistryIndex.from_registries(
        Registry().get_registries()
    )
    if args.interactive:
        data = read_multiline()
        entries = (RegistryIndex.lookup_bulk_from_file(
            indextype=index.mac_index,
            stream=data,
        ))
    else:  # elif args.file:
        entries = (RegistryIndex.lookup_bulk_from_file(
            indextype=index.mac_index,
            stream=Path(args.file),
        ))

    for entry in entries:
        print(
            entry.registry,
            entry.assignment,
            entry.organization_name,
            sep="\t",
        )

    return 0


def register(subparsers):
    parser = subparsers.add_parser(
        "bulk",
        help="Bulk lookup",
    )

    parser.add_argument(
        "file",
        nargs="?",
        help="Input file",
    )
    parser.add_argument(
        "-i",
        "--interactive",
        dest="interactive",
        action="store_true",
        help="Read multiple MAC addresses interactively",
    )

    parser.set_defaults(func=run)
