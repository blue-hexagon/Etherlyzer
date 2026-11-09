from __future__ import annotations

import argparse
from dataclasses import dataclass

from etherlyzer.core.application.analytics.mac_classifier import MACClassification
from etherlyzer.ieee.initialize import EtherlyzerContext
from etherlyzer.presentation.reporting.model import Report


@dataclass(frozen=True)
class TerminalInspectFlags:
    show_mac_autopsy: bool
    show_vendor_stats: bool
    show_vendor_blocks: bool


@dataclass(slots=True, frozen=True)
class CommonInspectionParams:
    args: argparse.Namespace
    context: EtherlyzerContext
    inspect_flags: TerminalInspectFlags
    report: Report


@dataclass(frozen=True)
class MacInspectionParams(CommonInspectionParams):
    classified_mac: MACClassification
