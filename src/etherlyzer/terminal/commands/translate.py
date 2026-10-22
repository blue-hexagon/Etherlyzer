from __future__ import annotations

import argparse
import sys
from enum import StrEnum

from etherlyzer.formatters import MACFormatter
from etherlyzer.presentation.translate import PresentationTranslator, get_arrlen_chwidth
from etherlyzer.terminal.utility import read_multiline


class Status(StrEnum):
    OK = "OK"
    INVALID = "ERR"


REPRESENTATIONS = (
    "canonical",
    "bit_reversed",
    "hex",
    "decimal",
    "decimal_bytes",
    "binary",
    "binary_raw",
    "hex_bytes",
    "bytes",
    "all",
)


def translate_to_all_representations(mac: str) -> tuple[dict[str, str], Status]:
    try:
        normalized = MACFormatter.normalize_semi_strict(mac).upper()
    except ValueError:
        return {}, Status.INVALID

    pt = PresentationTranslator()
    return (
        {
            "canonical": pt.to_canonical(normalized),
            "bit_reversed": pt.to_bit_reversed(normalized),
            "decimal": pt.to_decimal(normalized),
            "decimal_bytes": pt.to_decimal_bytes(normalized, padding=True),
            "binary": pt.to_binary(normalized),
            "binary_raw": pt.to_binary_raw(normalized),
            "hex": pt.to_hex(normalized),
            "hex_bytes": pt.to_hex_bytes(normalized),
            "bytes": pt.to_bytes(normalized),
        },
        Status.OK,
    )


def run(args: argparse.Namespace) -> int:
    if args.linenumbers and not args.bulk:
        print("error: --linenumbers requires --bulk", file=sys.stderr)
        return 2
    macs = (
        read_multiline(
            linetype="MAC addresses",
            skip_empty_lines=False,
        )
        if args.bulk
        else [args.mac]
    )

    padding = get_arrlen_chwidth(macs) + 1
    invalid_lines: list[int] = []
    for linenumber, mac in enumerate(macs, start=1):
        prefix = f"{linenumber}.".ljust(padding) if args.linenumbers else ""

        representations, status = translate_to_all_representations(mac)

        if args.to == "all" and status is not Status.INVALID:
            print(f"Line {linenumber}")
            print(f"  Input          : {mac}")
            for name, value in representations.items():
                label = name.replace("_", " ").title()
                print(f"  {label:<14} : {value}")

            if linenumber < len(macs):
                print()
        else:
            if status == Status.INVALID:
                invalid_lines.append(linenumber)
            else:
                print(f"{prefix} {representations[args.to]}")

    print()
    print(
        f"{len(invalid_lines)} invalid lines{':' if len(invalid_lines) > 0 else '!'} {', '.join([str(linum) for linum in invalid_lines])}"
    )

    return 0


def register(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    parser = subparsers.add_parser(
        "translate",
        help="Translate MAC addresses into different representations.",
        description=(
            "Translate MAC addresses into canonical, bit-reversed, "
            "hexadecimal, decimal, binary, or byte "
            "representations. Supports individual and bulk input."
        ),
        epilog=r"""
Examples:
  etherlyzer translate 40:06:AF:F1:08:08
  etherlyzer translate 40:06:AF:F1:08:08 -t decimal_bytes
  etherlyzer translate 40:06:AF:F1:08:08 -t binary
  etherlyzer translate 40:06:AF:F1:08:08 -t bit_reversed
  etherlyzer translate 40:06:AF:F1:08:08 -t hex_bytes
  etherlyzer translate -b
  etherlyzer translate -bl -t decimal
  etherlyzer translate -bl -t all
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    source = parser.add_mutually_exclusive_group(required=True)

    source.add_argument(
        "mac",
        nargs="?",
        help="MAC address to translate.",
    )

    source.add_argument(
        "-b",
        "--bulk",
        action="store_true",
        help="Read multiple MAC addresses interactively.",
    )

    parser.add_argument(
        "-l",
        "--linenumbers",
        action="store_true",
        help="Prefix output with the original input line number.",
    )
    parser.add_argument(
        "--parse-invalid-macs",
        action="store_true",
        help="Allow parsing of invalid MAC addresses (using semi-strict normalization).",
    )

    parser.add_argument(
        "-t",
        "--to",
        choices=REPRESENTATIONS,
        default="all",
        metavar="FORMAT",
        help=("Target representation: " + ", ".join(REPRESENTATIONS) + " (default: all)."),
    )

    parser.set_defaults(func=run)
