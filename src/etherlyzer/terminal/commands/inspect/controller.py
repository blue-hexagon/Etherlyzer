from __future__ import annotations

import argparse

from etherlyzer.ieee.initialize import (
    initialize_etherlyzer,
)
from etherlyzer.ieee.registry.category import RegistryCategory
from etherlyzer.lib.analytics.analyze_mac import analyze_mac_address
from etherlyzer.lib.normalization import normalize
from etherlyzer.terminal.commands.inspect.arg_validation import validate_inspect_args
from etherlyzer.terminal.commands.inspect.branches.ethertype_branch import inspect_ethertype
from etherlyzer.terminal.commands.inspect.branches.mac.router import inspect_ieee_quadrants
from etherlyzer.terminal.commands.inspect.common import TerminalInspectFlags
from etherlyzer.terminal.commands.inspect.display import show_cid_registration


def run(args: argparse.Namespace) -> int:
    validate_inspect_args(args)

    indexes = initialize_etherlyzer()

    inspect_flags = TerminalInspectFlags(
        show_mac_autopsy=args.all or args.show_mac_autopsy,
        show_vendor_stats=(args.all or args.show_vendor_stats or args.show_vendor_blocks),
        show_vendor_blocks=args.all or args.show_vendor_blocks,
    )

    match args.type.lower():
        case RegistryCategory.MAC_REGISTRY.value:
            return inspect_ieee_quadrants(args, indexes, inspect_flags)
        case RegistryCategory.ETHERTYPE_REGISTRY.value:
            entry = indexes.get_single(indexes.ethertype, args.value)
            inspect_ethertype(args, entry, indexes)
        case RegistryCategory.IDENTIFIER_REGISTRY.value:
            entry = indexes.get_single(indexes.identifier, args.value)
            norm = normalize(args.value)
            slap = analyze_mac_address(args.value).slap_quadrant
            if slap is None:
                return 2
            show_cid_registration(indexes, norm, slap)
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
        choices=list(RegistryCategory),
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
