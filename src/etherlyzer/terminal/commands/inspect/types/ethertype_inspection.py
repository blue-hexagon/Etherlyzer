from etherlyzer.ieee.ieee_registry import EtherTypeEntry


def inspect_ethertype(args, entry, index):
    if isinstance(entry, EtherTypeEntry):
        print(f"  Protocol    : {entry.protocol}")
