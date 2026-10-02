import re

from etherlyzer.formatters import MACFormatter
from etherlyzer.ieee.database import IEEEIndex
from etherlyzer.ieee.catalog import Catalog
from etherlyzer.ieee.registry import RegistryCategory, EtherTypeEntry


def run(args):
    registry = Catalog()
    index = IEEEIndex.from_registries(registry.get_all_registries(check_for_updates=False))
    if args.type.lower() == RegistryCategory.MAC.value:
        entry = index.get_single(index.mac_index, args.mac)
    elif args.type.lower() == RegistryCategory.PROTOCOL.value:
        entry = index.get_single(index.protocol_index, args.mac)
    elif args.type.lower() == RegistryCategory.IDENTIFIER.value:
        entry = index.get_single(index.identifier_index, args.mac)
    else:
        print("No valid type selected.")
        print(args.type)
        print(RegistryCategory.IDENTIFIER.value)
        return 1
    if entry is None:
        print("No matching entry found.")
        return 1
    print(f"")
    print(f"Organization")
    short = re.sub(r"(,.*|Co.*)$", "", entry.organization_name).strip()
    print(f"  Name     : {short}")
    print(f"  Full Name      : {entry.organization_name}")
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
    print(f"  Range        : {MACFormatter.format_with_stuffed_hex(entry.assignment, "0")} - {MACFormatter.format_with_stuffed_hex(entry.assignment, "f")}")
    try:
        # @formatter:off
        print(f"  Legacy       : {reg.legacy}")
        if reg.legacy:
            print(f"  Legacy Name  : {reg.legacy_name}")

        print(f"  Prefix Bits  : {reg.prefix_bits} bits")
        print(f"  Address Bits : {reg.address_bits} bits")
        print(f"  Addresses    : {reg.address_count:,}")
        # @formatter:on
    except KeyError:
        pass

    if isinstance(entry, EtherTypeEntry):
        print(f"  Protocol    : {entry.protocol}")

    print()



    return 0


def register(subparsers):
    parser = subparsers.add_parser("identify", help="Search vendors, protocols or assignments")
    parser.add_argument(
        "--type",
        type=str,
        choices=list(RegistryCategory),
        default="mac",
        metavar="{mac|protocol|identifier}",
    )
    parser.add_argument("mac", help="Search string", type=str)
    parser.set_defaults(func=run)
