import re

from etherlyzer.formatters import MACFormatter
from etherlyzer.ieee.index import IEEEIndex
from etherlyzer.ieee.catalog import Catalog
from etherlyzer.ieee.registry import RegCategory, EtherTypeEntry


def run(args):
    registry = Catalog()
    index = IEEEIndex.from_registries(registry.get_all_registries(check_for_updates=False))
    if args.type.lower() == RegCategory.MAC.value:
        entry = index.get_single(index.mac_index, args.mac)
    elif args.type.lower() == RegCategory.PROTOCOL.value:
        entry = index.get_single(index.protocol_index, args.mac)
    elif args.type.lower() == RegCategory.IDENTIFIER.value:
        entry = index.get_single(index.identifier_index, args.mac)
    else:
        print(f"No valid type ({args.type}) selected.")
        return 1
    if entry is None:
        print("No matching entry found.")
        return 1
    print(f"")
    print(f"Organization")
    short = re.sub(r"(,.*|Co.*)$", "", entry.organization_name).strip()  # TODO: Test
    print(f"  Name         : {short}")
    print(f"  Full Name    : {entry.organization_name}")
    print(f"  Address")

    for addr in entry.organization_address.split(","):
        addr = addr.split("  ")
        for line in addr:
            if line:
                print(f"    {line.strip()}")

    print()
    reg = Catalog.get_registry(str(entry.registry).lower().replace("-", ""))
    print("Registry")
    print(f"  IEEE Type    : {entry.registry} [{reg.full_name}]")
    print(f"  Assignment   : {MACFormatter.format_default(entry.assignment)}")
    print(
        f"  Range        : {MACFormatter.format_with_stuffed_hex(entry.assignment, "0")} - {MACFormatter.format_with_stuffed_hex(entry.assignment, "f")}")
    try:
        # @formatter:off
        print(f"  Legacy       : {reg.legacy}")
        if reg.legacy:
            print(f"  Legacy Name  : {reg.legacy_name}")

        print(f"  Prefix Bits  : {reg.prefix_bits} bits")
        print(f"  Address Bits : {reg.address_bits} bits")
        print(f"  Addresses    : {reg.address_count:,}") # noqa
        # @formatter:on
    except KeyError:
        pass
    other_bloks = index.vendor_index.lookup(entry.organization_name)
    # print(f"  {index.vendor_index.lookup(entry.organization_name)}")
    fmt_counter = 0
    if other_bloks:
        print(f"  Other Blocks : {len(other_bloks)}")  # TODO
        for assignment in other_bloks:
            fmt_counter += 9
            print(f"    {MACFormatter.format_default(assignment.assignment)}", end=" ")
            if fmt_counter > 90+45:
                fmt_counter = 0
                print()
    print()
    if isinstance(entry, EtherTypeEntry):
        print(f"  Protocol    : {entry.protocol}")

    print()

    return 0


def register(subparsers):
    parser = subparsers.add_parser("identify", help="Search vendors, protocols or assignments")
    parser.add_argument(
        "-t",
        "--type",
        type=str,
        choices=list(RegCategory),
        default="mac",
        metavar="{mac|protocol|identifier}",
    )
    parser.add_argument("mac", help="Search string", type=str)
    parser.set_defaults(func=run)
