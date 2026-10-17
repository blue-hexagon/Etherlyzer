from __future__ import annotations

import argparse

from etherlyzer.formatters import MACFormatter
from etherlyzer.terminal.utility import read_multiline


def run(args: argparse.Namespace) -> int:
    if args.linenumbers and not args.bulk:
        raise argparse.ArgumentError(None, "--linenumbers requires --bulk")
    linenumber = 0

    macs = (
        read_multiline(linetype="MAC addresses", skip_empty_lines=False)
        if args.bulk
        else [args.mac]
    )
    padding = (
        len(
            str(len(macs)),
        )
        + 2
    )  # Decimal count + spacing

    for mac in macs:
        if args.linenumbers:
            linenumber += 1
            print(f"{linenumber}.".ljust(padding, " "), end="")
        print(
            MACFormatter.format_custom(
                mac=mac,
                separator=args.separator,
                block_size=args.block_size,
                case=args.casing,
                fix_typos=args.fix_typos,
            )
        )

    return 0


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser(
        "format",
        help="Correct and normalize MAC address formatting.",
        description=(
            "Format MAC addresses using a selected separator, block size, and casing. "
            "Optional typo correction can repair supported character substitutions. "
            "This command formats input without performing MAC address validation."
        ),
        epilog=r"""
Examples:
  etherlyzer format 001122334455
  etherlyzer format 00-11-22-33-44-55 -p :
  etherlyzer format 001122334455 -p . -s 4
  etherlyzer format 00:11:22:33:44:55 -c upper
  etherlyzer format O0:1i:22:33:44:s5 --fix-typos
  etherlyzer format -b -p . -s 4 --fix-typos
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    source = parser.add_mutually_exclusive_group(required=True)

    source.add_argument(
        "mac",
        nargs="?",
        help="MAC address to format.",
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
        help="Prefix output lines with their corresponding input line number.",
    )

    parser.add_argument(
        "-p",
        "--separator",
        type=str,
        default=":",
        help="Output separator: ':', '-', '.', or empty (default: ':').",
    )

    parser.add_argument(
        "-s",
        "--block-size",
        type=int,
        default=2,
        help="Number of hexadecimal characters per block (default: 2).",
    )

    parser.add_argument(
        "-c",
        "--casing",
        type=str,
        choices=["lower", "upper"],
        default="lower",
        help="Output hexadecimal casing (default: lower).",
    )

    parser.add_argument(
        "-f",
        "--fix-typos",
        action="store_true",
        help="Correct supported typo-like character substitutions before formatting.",
    )

    parser.set_defaults(func=run)
