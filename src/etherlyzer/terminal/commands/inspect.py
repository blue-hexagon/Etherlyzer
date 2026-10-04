import argparse
import re

from etherlyzer.formatters import MACFormatter
from etherlyzer.ieee.index import IEEEIndex
from etherlyzer.ieee.catalog import Catalog
from etherlyzer.ieee.ieee_registry import RegCategory, EtherTypeEntry


def run(args):
    registry = Catalog()
    index = IEEEIndex.from_registries(registry.get_all_registries(check_for_updates=False))
    if args.type.lower() == RegCategory.MAC.value:
        entry = index.get_single(index.mac_index, args.value)
    elif args.type.lower() == RegCategory.PROTOCOL.value:
        entry = index.get_single(index.protocol_index, args.value)
    elif args.type.lower() == RegCategory.IDENTIFIER.value:
        entry = index.get_single(index.identifier_index, args.value)
    else:
        print(f"No valid type ({args.type}) selected.")
        return 1
    if entry is None:
        print("No matching entry found.")
        return 1
    print(f"")
    print(f"Organization")
    short = re.sub(r"(,.*|Co.*)$", "", entry.organization_name).strip()  # TODO: Test
    print(f"  Name            : {short}")
    print(f"  Full Name       : {entry.organization_name}")
    print(f"  Address")

    for addr in entry.organization_address.split(","):
        addr = addr.split("  ")
        for line in addr:
            if line:
                print(f"    {line.strip()}")

    print()
    reg = Catalog.get_registry(str(entry.registry).lower().replace("-", ""))
    print("Registry")
    print(f"  IEEE Type       : {entry.registry} [{reg.full_name}]")
    print(f"  Assignment      : {MACFormatter.format_default(entry.assignment)}")
    print(
        f"  Range           : {MACFormatter.format_with_stuffed_hex(entry.assignment, "0")} - {MACFormatter.format_with_stuffed_hex(entry.assignment, "f")}")
    try:
        # @formatter:off
        print(f"  Legacy          : {reg.legacy}")
        if reg.legacy:
            print(f"  Legacy Name     : {reg.legacy_name}")

        print(f"  Prefix Bits     : {reg.prefix_bits} bits")
        print(f"  Address Bits    : {reg.address_bits} bits")
        print(f"  Addresses       : {reg.address_count:,}") # noqa
        # @formatter:on
    except KeyError:
        pass
    other_bloks = index.vendor_index.lookup(entry.organization_name)
    # print(f"  {index.vendor_index.lookup(entry.organization_name)}")
    fmt_counter = 0
    if other_bloks:
        total_addresses = 0
        total_addresses_mal = 0
        total_addresses_mam = 0
        total_addresses_mas = 0
        total_addresses_iab = 0
        for ent in other_bloks:
            if ent.registry == "MA-L":
                total_addresses += 2 ** 24
                total_addresses_mal += 2 ** 24
            elif ent.registry == "MA-M":
                total_addresses += 2 ** 20
                total_addresses_mam += 2 ** 20
            elif ent.registry == "MA-S":
                total_addresses += 2 ** 12
                total_addresses_mas += 2 ** 12
            elif ent.registry == "IAB":
                total_addresses += 2 ** 12
                total_addresses_iab += 2 ** 12
        print(f"")
        print(f"Vendor Blocks")
        print(f"  Total Blocks    : {len(other_bloks)}")
        print(f"  Address Capacity")
        print(f"    Total         : {total_addresses:,}")
        print(f"    MA-L          : {total_addresses_mal:,}")
        print(f"    MA-M          : {total_addresses_mam:,}")
        print(f"    MA-S          : {total_addresses_mas:,}")
        print(f"    IAB           : {total_addresses_iab:,}")
        print(f"    Registered Blocks (B=IAB, S=MA-S, M=MA-M, L=MA-L)")
        for entry in other_bloks:
            fmt_counter += 9
            print(f"      [{entry.registry.replace("-", "")[2:]}] {MACFormatter.format_default(entry.assignment)}",
                  end="")
            if fmt_counter >= 45:
                fmt_counter = 0
                print()
    print()
    if isinstance(entry, EtherTypeEntry):
        print(f"  Protocol    : {entry.protocol}")

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
        "value",
        type=str,
        help="IEEE assignment or identifier to inspect.",
    )

    parser.set_defaults(func=run)
