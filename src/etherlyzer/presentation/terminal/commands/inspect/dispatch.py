from __future__ import annotations

import argparse

from etherlyzer.core.analytics.mac_classifier import classify_mac
from etherlyzer.ieee.initialize import (
    initialize_etherlyzer,
)
from etherlyzer.ieee.registry.family import RegistryFamily
from etherlyzer.presentation.reporting.model import Report
from etherlyzer.presentation.terminal.commands.inspect.branches.ethertype_branch import (
    inspect_ethertype,
)
from etherlyzer.presentation.terminal.commands.inspect.branches.mac.router import (
    inspect_mac_router,
)
from etherlyzer.presentation.terminal.commands.inspect.common import (
    InspectionParams,
    TerminalInspectFlags,
)
from etherlyzer.presentation.terminal.commands.inspect.presentation.sections import (
    build_cid_registration_section,
)


def run(args: argparse.Namespace) -> int:
    validate_inspect_args(args)
    context = initialize_etherlyzer()
    inspect_flags = TerminalInspectFlags(
        show_mac_autopsy=(args.all or args.show_mac_autopsy),
        show_vendor_stats=(args.all or args.show_vendor_stats),
        show_vendor_blocks=(args.all or args.show_vendor_blocks),
    )

    params = InspectionParams(
        args=args,
        context=context,
        inspect_flags=inspect_flags,
        classified_mac=classify_mac(args.value),
        report=Report(),
    )
    match args.type.lower():
        case RegistryFamily.MAC_REGISTRY.value:
            return inspect_mac_router(params)
        case RegistryFamily.ETHERTYPE_REGISTRY.value:
            return inspect_ethertype(params)
        case RegistryFamily.IDENTIFIER_REGISTRY.value:
            slap = classify_mac(args.value).slap_quadrant
            if slap is None:
                return 2
            build_cid_registration_section(params)
        case _:
            print(f"No valid type ({args.type}) selected.")
            return 1

    print()

    return 0


def validate_inspect_args(args: argparse.Namespace) -> None:
    if args.show_vendor_blocks and args.type != "mac":
        raise argparse.ArgumentError(
            None, "--show-vendor-blocks is only supported for MAC assignments."
        )
    elif args.show_vendor_stats and args.type != "mac":
        raise argparse.ArgumentError(
            None, "--show-vendor-stats is only supported for MAC assignments."
        )
    elif args.show_mac_autopsy and args.type != "mac":
        raise argparse.ArgumentError(
            None, "--show-mac-analysis is only supported for MAC assignments."
        )
    else:
        pass


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
        choices=list(RegistryFamily),
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
