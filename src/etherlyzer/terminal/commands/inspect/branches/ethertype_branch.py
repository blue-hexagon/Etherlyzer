import argparse

from etherlyzer.ieee.entry.ethertype import EtherTypeEntry
from etherlyzer.ieee.entry.mac import MACAllocationEntry
from etherlyzer.ieee.index.store import IndexStore


def inspect_ethertype(
    args: argparse.Namespace, entry: MACAllocationEntry, index: IndexStore
) -> None:
    if isinstance(entry, EtherTypeEntry):
        print(f"  Protocol    : {entry.protocol}")
