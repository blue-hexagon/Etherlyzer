from __future__ import annotations

import argparse
from dataclasses import dataclass

from etherlyzer.formatters import MACFormatter
from etherlyzer.ieee.catalog import Catalog
from etherlyzer.ieee.eui48_classifier import classify_mac
from etherlyzer.ieee.ieee_registry import RegCategory
from etherlyzer.ieee.index import IEEEIndex
from etherlyzer.terminal.commands.inspect.types.display import show_cid_registration
from etherlyzer.terminal.commands.inspect.types.ethertype_inspection import inspect_ethertype
from etherlyzer.terminal.commands.inspect.types.mac_inspection import inspect_ieee_quadrants
from etherlyzer.terminal.commands.inspect.validation import validate_args


@dataclass
class EvaluatedFlags:
    show_mac_autopsy: bool
    show_vendor_stats: bool
    show_vendor_blocks: bool


def run(args: argparse.Namespace) -> int:
    validate_args(args)

    registry = Catalog()
    index = IEEEIndex.from_registries(registry.get_all_registries(check_for_updates=False))
    eval_flags = EvaluatedFlags(
        show_mac_autopsy=args.all or args.show_mac_autopsy,
        show_vendor_stats=(args.all or args.show_vendor_stats or args.show_vendor_blocks),
        show_vendor_blocks=args.all or args.show_vendor_blocks,
    )

    match args.type.lower():
        case RegCategory.MAC.value:
            return inspect_ieee_quadrants(args, index, eval_flags)
        case RegCategory.PROTOCOL.value:
            entry = index.get_single(index.protocol_index, args.value)
            inspect_ethertype(args, entry, index)
        case RegCategory.IDENTIFIER.value:
            entry = index.get_single(index.identifier_index, args.value)
            show_cid_registration(
                index, MACFormatter.normalize(args.value), classify_mac(args.value)
            )
        case _:
            print(f"No valid type ({args.type}) selected.")
            return 1

    print()

    return 0


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser(
        "inspect",
        help="Inspect an IEEE assignment and display registry, organization, range, and allocation details.",
        description=(
            "Inspect a single IEEE assignment and display detailed registry metadata, "
            "organization information, address range, and related vendor allocations."
        ),
        epilog=r"""
Examples:
  etherlyzer inspect 00:11:22:33:44:55
  etherlyzer inspect 000001 --show-vendor-blocks
  etherlyzer inspect -t mac 00:11:22:33:44:55
  etherlyzer inspect -t protocol 0800
  etherlyzer inspect -t identifier <identifier>
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-t",
        "--type",
        type=str,
        choices=list(RegCategory),
        default="mac",
        metavar="{mac|protocol|identifier}",
        help="IEEE registry category to search (default: mac).",
    )
    parser.add_argument(
        "-x",
        "--show-mac-autopsy",
        action="store_true",
        help="Show MAC address structure, representations, and IEEE identifier classification.",
    )

    parser.add_argument(
        "-s",
        "--show-vendor-stats",
        action="store_true",
        help="Show associated vendor allocation counts and address capacities.",
    )

    parser.add_argument(
        "-b",
        "--show-vendor-blocks",
        action="store_true",
        help="List associated IEEE-registered vendor blocks.",
    )

    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Display all available inspection details.",
    )
    parser.add_argument(
        "value",
        type=str,
        help="IEEE assignment or identifier to inspect.",
    )

    parser.set_defaults(func=run)
