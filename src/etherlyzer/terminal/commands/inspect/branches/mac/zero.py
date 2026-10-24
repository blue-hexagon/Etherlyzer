import argparse

from etherlyzer.ieee.index.store import IndexStore
from etherlyzer.lib.analytics.analyze_mac import MACClassification
from etherlyzer.terminal.commands.inspect.common import TerminalInspectFlags


def inspect_zero_address(
    args: argparse.Namespace,
    index: IndexStore,
    inspect_flags: TerminalInspectFlags,
    classified_mac: MACClassification,
) -> None:
    print("Zero")
