import argparse

from etherlyzer.ieee.index.store import IndexStore
from etherlyzer.lib.analytics.analyze_mac import MACClassification
from etherlyzer.terminal.commands.inspect.common import TerminalInspectFlags


def inspect_local_individual_eli(
    args: argparse.Namespace,
    index: IndexStore,
    eval_flags: TerminalInspectFlags,
    classified_mac: MACClassification,
) -> None:
    print()
