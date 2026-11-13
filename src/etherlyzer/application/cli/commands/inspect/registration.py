from __future__ import annotations

import argparse

from etherlyzer.application.cli.commands.inspect.dispatch import dispatch
from etherlyzer.infrastructure.registry.family import RegistryFamily


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser(
        "inspect",
        help="Inspect network addresses, identifiers, and protocols.",
        description=(
            "Inspect a single IEEE assignment and display detailed registry metadata, "
            "organization information, address range, and related vendor allocations."
        ),
        epilog=r"""
Examples:
  etherlyzer inspect mac 00:11:22:33:44:55
  etherlyzer inspect mac 000001 --show-vendor-blocks
  etherlyzer inspect mac 00:11:22:33:44:55
  etherlyzer inspect protocol 0800
  etherlyzer inspect ip_ucast 10.100.64.13
  etherlyzer inspect ip_ucast 192.32.67.0/21
  etherlyzer inspect ip_mcast 224.0.0.1
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    type_parsers = parser.add_subparsers(
        dest="type",
        required=True,
    )

    for family in RegistryFamily:
        if family == RegistryFamily.IDENTIFIER_REGISTRY:
            continue
        branch = type_parsers.add_parser(
            family.value,
            help=f"Inspect {family.value} assignments.",
        )

        branch.add_argument(
            "value",
            type=str,
            help="Address or identifier to inspect.",
        )

        branch.set_defaults(
            func=dispatch,
            show_mac_autopsy=False,
            show_vendor_stats=False,
            show_vendor_blocks=False,
            all=False,
        )

        if family == RegistryFamily.MAC_REGISTRY:
            branch.add_argument(
                "-x",
                "--show-mac-autopsy",
                action="store_true",
                help="Show MAC address structure and classification.",
            )

            branch.add_argument(
                "-s",
                "--show-vendor-stats",
                action="store_true",
                help="Show vendor allocation counts and capacities.",
            )

            branch.add_argument(
                "-b",
                "--show-vendor-blocks",
                action="store_true",
                help="List associated IEEE vendor blocks.",
            )

            branch.add_argument(
                "-a",
                "--all",
                action="store_true",
                help="Display all available MAC inspection details.",
            )

    parser.set_defaults(func=dispatch)
