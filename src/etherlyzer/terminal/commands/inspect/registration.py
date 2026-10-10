import argparse

from etherlyzer.formatters import MACFormatter
from etherlyzer.ieee.catalog import Catalog
from etherlyzer.ieee.eui48_classifier import classify_mac, Administration, DeliveryType
from etherlyzer.ieee.ieee_registry import RegCategory
from etherlyzer.ieee.index import IEEEIndex, VendorIndex
from etherlyzer.terminal.commands.inspect.inspections import show_mac_autopsy, \
    show_cid_registration, show_registration, show_organization, show_all_vendor_blocks, show_associated_block_counts
from etherlyzer.terminal.commands.inspect.ethertype import inspect_ethertype
from etherlyzer.terminal.commands.inspect.validation import validate_args


def run(args):
    validate_args(args)

    show_mac_analysis = args.all or args.show_mac_analysis
    show_vendor_stats = (
            args.all
            or args.show_vendor_stats
            or args.show_vendor_blocks
    )
    show_vendor_blocks = args.all or args.show_vendor_blocks

    registry = Catalog()
    index = IEEEIndex.from_registries(registry.get_all_registries(check_for_updates=False))
    match args.type.lower():
        case RegCategory.MAC.value:
            no_valid_entry = False
            classified_mac = classify_mac(args.value)
            if (
                    classified_mac.administration == Administration.UNIVERSAL  # registered
                    and classified_mac.delivery == DeliveryType.INDIVIDUAL  # unicast
                    and not classified_mac.is_zero  # not all zeroes
            ):
                entry = index.get_single(index.mac_index, args.value)
                print(entry)
                if entry is not None:
                    short_orgname = entry.short_name()

                    reg = Catalog.get_registry(str(entry.registry).lower().replace("-", ""))

                    vendor_index: VendorIndex = index.vendor_index
                    vendor_correlated_entries = vendor_index.lookup(entry.organization_name)

                    show_registration(entry, reg)

                    if vendor_correlated_entries is not None:
                        if show_vendor_stats:
                            show_associated_block_counts(vendor_correlated_entries)
                        if show_vendor_blocks:
                            show_all_vendor_blocks(args, vendor_correlated_entries)

                    show_organization(entry, short_orgname)
                    print()  # Required exactly here.
            if show_mac_analysis or entry is None:
                show_mac_autopsy(args, classified_mac, index, no_valid_entry)
            return 0
        case RegCategory.PROTOCOL.value:
            entry = index.get_single(index.protocol_index, args.value)
            inspect_ethertype(args, entry, index)
        case RegCategory.IDENTIFIER.value:
            entry = index.get_single(index.identifier_index, args.value)
            show_cid_registration(index, MACFormatter.normalize(args.value), classify_mac(args.value))
        case _:
            print(f"No valid type ({args.type}) selected.")
            return 1

    print()

    return 0


def register(subparsers):
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
        "--show-mac-analysis",
        action="store_true",
        help="Show MAC address structure, representations, and IEEE identifier classification.",
    )

    parser.add_argument(
        "--show-vendor-stats",
        action="store_true",
        help="Show associated vendor allocation counts and address capacities.",
    )

    parser.add_argument(
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
