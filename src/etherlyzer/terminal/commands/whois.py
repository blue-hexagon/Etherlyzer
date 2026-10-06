from __future__ import annotations

import argparse
from pathlib import Path

from etherlyzer.ieee.index import IEEEIndex
from etherlyzer.ieee.catalog import Catalog
from etherlyzer.terminal.utility import read_multiline


def run(args):
    index = IEEEIndex.from_registries(
        Catalog().get_all_registries()
    )
    if args.mac:
        entry = index.get_single(indextype=index.mac_index, mac=args.mac)
        if entry is None:
            print("No entry found.")
            return 1
        print(
            entry.registry,
            entry.assignment,
            entry.organization_name,
            sep="\t",
        )
        return 0

    elif args.interactive:
        data = read_multiline()
        entries = IEEEIndex.get_bulk(
            ieee_index=index.mac_index,
            path_or_text=data,
        )
    elif args.file:
        entries = IEEEIndex.get_bulk(
            ieee_index=index.mac_index,
            path_or_text=args.file,
        )
    else:
        return 1
    if entries:
        for entry in entries:
            print(
                entry.registry,
                entry.assignment,
                entry.organization_name,
                sep="\t",
            )
    else:
        print("No entries found.")

    return 0


def register(subparsers):
    parser = subparsers.add_parser(
        "whois",
        help="Identify IEEE vendors and organizations for MAC addresses.",
        description="Identify IEEE vendors and organizations for one or more MAC addresses.",
        epilog="""
Examples:
  etherlyzer whois 00:11:22:33:44:55
  etherlyzer whois -f .\\macs.txt
  etherlyzer whois -i
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    source = parser.add_mutually_exclusive_group(required=True)

    source.add_argument(
        "mac",
        nargs="?",
        help="MAC address to identify",
    )

    source.add_argument(
        "-f",
        "--file",
        type=Path,
        help="Read MAC addresses from a file",
    )

    source.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Read multiple MAC addresses interactively",
    )

    parser.set_defaults(func=run)
