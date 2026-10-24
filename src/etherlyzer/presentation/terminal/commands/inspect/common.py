from __future__ import annotations

import argparse
from dataclasses import dataclass

from etherlyzer.core.analytics.mac_classifier import MACClassification
from etherlyzer.ieee.initialize import EtherlyzerContext


@dataclass(frozen=True)
class TerminalInspectFlags:
    show_mac_autopsy: bool
    show_vendor_stats: bool
    show_vendor_blocks: bool


@dataclass(slots=True, frozen=True)
class InspectionParams:
    args: argparse.Namespace
    context: EtherlyzerContext
    inspect_flags: TerminalInspectFlags
    classified_mac: MACClassification

    def to_vars(
        self,
    ) -> tuple[argparse.Namespace, EtherlyzerContext, TerminalInspectFlags, MACClassification]:
        return self.args, self.context, self.inspect_flags, self.classified_mac
