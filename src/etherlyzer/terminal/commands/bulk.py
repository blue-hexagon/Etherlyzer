from __future__ import annotations

from pathlib import Path

from etherlyzer.ieee.database import IEEEIndex
from etherlyzer.ieee.catalog import Catalog
from etherlyzer.terminal.utility import read_multiline


def run(args):
    index = IEEEIndex.from_registries(
        Catalog().get_all_registries()
    )
    if args.interactive:
        data = read_multiline()
        entries = (IEEEIndex.get_bulk(
            ieee_index=index.mac_index,
            path_or_text=data,
        ))
    else:  # elif args.file:
        entries = (IEEEIndex.get_bulk(
            ieee_index=index.mac_index,
            path_or_text=Path(args.file),
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
