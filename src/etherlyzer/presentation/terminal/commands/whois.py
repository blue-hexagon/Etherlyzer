from __future__ import annotations

import argparse
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from etherlyzer.application.analysis.mac_classifier import classify_mac
from etherlyzer.application.analysis.mac_identity import (
    MacForm,
    MacIdentity,
    MacResolution,
    analyze_mac_identity,
)
from etherlyzer.domain.entry.mac import MACAllocationEntry
from etherlyzer.domain.initialize import EtherlyzerContext, initialize_etherlyzer
from etherlyzer.presentation.reporting.model import Item, Report, Section, Table
from etherlyzer.presentation.reporting.renders import get_render, get_render_choices
from etherlyzer.presentation.terminal.utility import read_multiline


@dataclass(frozen=True, slots=True)
class MACTerminalLookupResult:
    line_number: int
    mac: str
    form: MacForm
    identity: MacIdentity
    resolution: MacResolution
    entry: MACAllocationEntry | None = None


def get_bulk(
    context: EtherlyzerContext,
    values: Iterable[str],
    include_unsuccessful: bool = False,
) -> list[MACTerminalLookupResult]:
    results = []

    for line_number, mac in enumerate(values, start=1):
        mac = mac.strip()
        reason = analyze_mac_identity(classify_mac(mac), context)

        entry = context.indexes.mac.lookup_group_allocation(mac)
        result = MACTerminalLookupResult(
            entry=entry,
            line_number=line_number,
            mac=mac,
            form=reason.form,
            resolution=reason.resolution,
            identity=reason.identity,
        )
        if result.entry is not None or include_unsuccessful:
            results.append(result)

    return results


def handle_single(context: EtherlyzerContext, report: Report, args: argparse.Namespace) -> int:
    entry = context.indexes.mac.lookup(args.mac)
    if entry is None:
        report.sections.append(
            Section(title="IEEE Assignment", items=[Item(key="Result", value="No match found.")])
        )
        return 1

    report.sections.append(
        Section(
            title="IEEE Assignment",
            items=[
                Item(key="Registry", value=entry.registry),
                Item(key="Assignment", value=entry.assignment),
                Item(key="Name", value=entry.organization_name),
                Item(key="Address", value=entry.organization_address),
            ],
        )
    )
    return 0


def handle_many(
    context: EtherlyzerContext, report: Report, args: argparse.Namespace, source: list[str]
) -> int:
    results = get_bulk(
        context=context,
        values=source,
        include_unsuccessful=True,
    )

    if not results:
        report.sections.append(
            Section(
                title="IEEE Assignment",
                items=[
                    Item(key="Results", value="No matches found."),
                ],
            )
        )
        return 0
    table = Table(
        columns=(
            "Line",
            "Input",
            "Registry",
            "Assignment",
            "Organization",
            "Form",
            "Identity",
            "Resolution",
        )
    )
    for result in results:
        if result.entry is None and args.preserve_bad_entries:
            table.append(
                result.line_number,
                result.mac,
                "-",
                "-",
                "-",
                result.form,
                result.identity,
                result.resolution,
            )

        elif result.entry is not None:
            table.append(
                result.line_number,
                result.mac,
                result.entry.registry,
                result.entry.assignment,
                result.entry.organization_name,
                result.form,
                result.identity,
                result.resolution,
            )

    report.sections.append(
        Section(
            items=[table],
        )
    )
    return 0


def run(args: argparse.Namespace) -> int:
    context = initialize_etherlyzer()
    report = Report()

    if args.mac:
        status = handle_single(context, report, args)
        return status
    if args.bulk:
        raw_input = read_multiline(skip_empty_lines=False)
    elif args.file:
        raw_input = args.file.read_text(encoding="utf-8").splitlines()
    else:
        return 2

    status = handle_many(context, report, args, raw_input)
    print(report.render(get_render(args.format)))
    return status


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser(
        "whois",
        help="Identify IEEE vendors and organizations for MAC addresses.",
        description="Identify IEEE vendors and organizations for one or more MAC addresses.",
        epilog=r"""
Examples:
  etherlyzer whois 00:11:22:33:44:55   Look up a single MAC address
  etherlyzer whois -b                  Enter MAC addresses interactively
  etherlyzer whois -f .\macs.txt       Look up MAC addresses from a file
  etherlyzer whois -bp                 Include unsuccessful lookups
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    source = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument(
        "-o",
        "--format",
        type=str,
        help="Select a format for the output",
        choices=get_render_choices(),
    )
    parser.add_argument(
        "-p",
        "--preserve-bad-entries",
        action="store_true",
        help=".",
    )
    source.add_argument(
        "mac",
        nargs="?",
        help="MAC address to identify",
    )

    source.add_argument(
        "-f",
        "--file",
        type=Path,
        help="Read multiple MAC addresses from a file",
    )

    source.add_argument(
        "-b",
        "--bulk",
        action="store_true",
        help="Read multiple MAC addresses interactively",
    )

    parser.set_defaults(func=run)
