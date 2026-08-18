from __future__ import annotations

from etherlyzer.database import RegistryIndex
from etherlyzer.registry import EtherTypeEntry, Registry, RegistryCategory


def run(args):
    registry = Registry()
    index = RegistryIndex.from_registries(registry.get_registries(update=False))
    if args.type.lower() == RegistryCategory.MAC.value:
        entry = index.lookup_single_from_console(index.mac_index, args.query)
    elif args.type.lower() == RegistryCategory.PROTOCOL.value:
        entry = index.lookup_single_from_console(index.protocol_index, args.query)
    elif args.type.lower() == RegistryCategory.IDENTIFIER.value:
        entry = index.lookup_single_from_console(index.identifier_index, args.query)
    else:
        print("No valid type selected.")
        print(args.type)
        print(RegistryCategory.IDENTIFIER.value)
        return 1
    if entry is None:
        print("No matching entry found.")
        return 1

    print(f"Organization : {entry.organization_name}")
    print()

    print("Registry")
    print(f"  Name        : {entry.registry}")
    print(f"  Assignment  : {entry.assignment}")

    if isinstance(entry, EtherTypeEntry):
        print(f"  Protocol    : {entry.protocol}")

    print()

    print("Organization Address")

    for addr in entry.organization_address.split(","):
        addr = addr.split("  ")
        for line in addr:
            if line:
                print(f"  {line.strip()}")

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
