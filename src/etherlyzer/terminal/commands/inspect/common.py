from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import TypedDict

from etherlyzer.ieee.index.store import IndexStore
from etherlyzer.lib.analytics.analyze_mac import MACClassification


@dataclass(frozen=True)
class TerminalInspectFlags:
    show_mac_autopsy: bool
    show_vendor_stats: bool
    show_vendor_blocks: bool


class InspectionParams(TypedDict):
    args: argparse.Namespace
    index: IndexStore
    inspect_flags: TerminalInspectFlags
    classified_mac: MACClassification
