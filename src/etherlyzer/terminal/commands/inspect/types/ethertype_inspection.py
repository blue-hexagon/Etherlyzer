import argparse

from etherlyzer.ieee.entry.ethertype import EtherTypeEntry
from etherlyzer.ieee.entry.mac import MACAllocationEntry
from etherlyzer.ieee.index.ieee_index import IEEEIndex


def inspect_ethertype(
    args: argparse.Namespace, entry: MACAllocationEntry, index: IEEEIndex
) -> None:
    if isinstance(entry, EtherTypeEntry):
        print(f"  Protocol    : {entry.protocol}")
