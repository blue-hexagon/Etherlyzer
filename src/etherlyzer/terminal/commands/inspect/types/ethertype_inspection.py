import argparse

from etherlyzer.ieee.ieee_registry import EtherTypeEntry, IEEEEntry
from etherlyzer.ieee.index import IEEEIndex


def inspect_ethertype(args: argparse.Namespace, entry: IEEEEntry, index: IEEEIndex) -> None:
    if isinstance(entry, EtherTypeEntry):
        print(f"  Protocol    : {entry.protocol}")
