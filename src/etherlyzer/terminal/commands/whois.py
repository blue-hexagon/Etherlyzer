from __future__ import annotations

import argparse
from pathlib import Path

from etherlyzer.ieee.index.ieee_index import IEEEIndexCatalog
from etherlyzer.ieee.registry.catalog import Catalog
from etherlyzer.terminal.utility import print_table, read_multiline
from etherlyzer.util.knobs import etherlyzer_knobs


def run(args: argparse.Namespace) -> int:
    if args.linenumbers and not (args.bulk or args.file):
        print("error: --linenumbers requires --bulk or --file")
        return 2

    separator = args.delimiter if args.delimiter is not None else etherlyzer_knobs.field_separator

    index = IEEEIndexCatalog.build(Catalog().get_all_registries_and_ensure_cache_is_synced())

    if args.mac:
        entry = index.get_from_mac_index(args.mac)

        if entry is None:
            print("No entry found.")
            return 1

        print(
            entry.registry,
            entry.assignment,
            entry.organization_name,
            sep=separator,
        )
        return 0

    if args.bulk:
        source = read_multiline(skip_empty_lines=False)
    elif args.file:
        source = args.file.read_text(encoding="utf-8").splitlines()
    else:
        return 2

    results = IEEEIndexCatalog.get_bulk(
        ieee_index=index.mac_index,
        values=source,
        include_unsuccessful=True,
    )

    if not results:
        print("No entries found.")
        return 0

    rows: list[tuple[str, ...]] = []

    for result in results:
        if result.entry is None and not args.preserve_bad_entries:
            continue

        if result.entry is not None:
            fields = (
                "MATCH",
                str(result.entry.registry),
                str(result.entry.assignment),
                str(result.entry.organization_name),
            )
        else:
            fields = (
                result.reason.upper().replace(" ", "_"),
                "N/A",
                "N/A",
                "N/A",
            )

        if args.linenumbers:
            number = (
                str(result.line_number) if args.delimiter is not None else f"{result.line_number}."
            )
            fields = (number, *fields)
        rows.append(fields)

    headers = ("Result", "Registry", "Assignment", "Organization")

    if args.linenumbers:
        headers = ("Line", *headers)

    print_table(
        rows,
        headers=headers if args.column_names else None,
        delimiter=args.delimiter,
    )

    return 0


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser(
        "whois",
        help="Identify IEEE vendors and organizations for MAC addresses.",
        description="Identify IEEE vendors and organizations for one or more MAC addresses.",
        epilog=r"""
Examples:
  etherlyzer whois 00:11:22:33:44:55   Look up a single MAC address
  etherlyzer whois -b                  Enter MAC addresses interactively
  etherlyzer whois -f .\macs.txt       Look up MAC addresses from a file
  etherlyzer whois -bl                 Show original input line numbers
  etherlyzer whois -bp                 Include unsuccessful lookups
  etherlyzer whois -blcp               Show all results in an aligned table
  etherlyzer whois -blcp -d ";"        Output semicolon-delimited results
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    source = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument(
        "-d",
        "--delimiter",
        type=str,
        help="Select a delimiter, if none is chosen tabs is default",
    )
    parser.add_argument(
        "-p",
        "--preserve-bad-entries",
        action="store_true",
        help=".",
    )
    parser.add_argument(
        "-l",
        "--linenumbers",
        action="store_true",
        help="Prefix output lines with their corresponding input line number",
    )
    parser.add_argument(
        "-c",
        "--column-names",
        action="store_true",
        help="Write a header row on the first line of the output",
    )
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
        "-b",
        "--bulk",
        action="store_true",
        help="Read multiple MAC addresses interactively",
    )

    parser.set_defaults(func=run)
