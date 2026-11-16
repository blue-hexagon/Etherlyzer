from __future__ import annotations

import argparse

from etherlyzer.application.cli.multiline_stdin import read_multiline
from etherlyzer.core.interpretation.mac.validation import MACValidator
from etherlyzer.presentation.reporting.model import Report, Section, Table
from etherlyzer.presentation.reporting.renders import get_renderer


def run(args: argparse.Namespace) -> int:
    macs = (
        read_multiline(linetype="MAC addresses", skip_empty_lines=False)
        if args.bulk
        else [args.mac]
    )
    table = Table(
        columns=(
            "Line",
            "Input",
            "Validity",
            "Mask",
            "Normalized",
        )
    )
    summary = Table(
        columns=(
            "Empty Lines",
            "Valid Lines",
            "Invalid Lines",
            "Total Lines",
        )
    )
    report = Report(
        [
            Section(
                title="",
                items=[table, summary],
            ),
        ],
    )
    total_empty_lines: int = 0
    total_lines: int = len(macs)
    total_valid: int = 0
    total_invalid: int = 0
    for linenumber, mac in enumerate(macs, start=1):
        normalized_mac, validation_mask = MACValidator.validate(mac)
        is_valid = "Valid" if MACValidator.mask_is_valid(validation_mask) else "Invalid"
        if args.skip_empty_lines and validation_mask == "MMMMMMMMMMMM":
            total_empty_lines += 1
            continue
        if args.only_valid:
            if MACValidator.mask_is_valid(validation_mask):
                total_valid += 1
                table.append(
                    linenumber,
                    mac,
                    is_valid,
                    validation_mask,
                    "",
                )
                continue
            total_invalid += 1
            continue

        elif args.only_invalid:
            if not MACValidator.mask_is_valid(validation_mask):
                total_invalid += 1
                table.append(
                    linenumber,
                    mac,
                    is_valid,
                    validation_mask,
                    normalized_mac,
                )
                continue
            total_valid += 1
            continue

        table.append(
            linenumber,
            mac,
            is_valid,
            validation_mask,
            normalized_mac,
        )

    summary.append(
        total_empty_lines,
        total_valid,
        total_invalid,
        total_lines,
    )
    print(report.render(get_renderer("text")))
    return 0


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser(
        "validate",
        help="Validate and normalize MAC addresses with optional diagnostics and filtering.",
        description=(
            "Validate and normalize MAC addresses without typo correction. "
            "Malformed input is reported rather than corrected; use `format` "
            "for corrective formatting."
        ),
        epilog=r"""
Examples:
  etherlyzer validate 00:11:22:33:44:55
  etherlyzer validate -b
  etherlyzer validate -b --strict
  etherlyzer validate -b --linenumbers --show-info
  etherlyzer validate -b --show-originals
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "mac",
        nargs="?",
        help="MAC address to validate and normalize.",
    )

    source.add_argument(
        "-b",
        "--bulk",
        action="store_true",
        help="Read multiple MAC addresses interactively.",
    )

    parser.add_argument(
        "-l",
        "--skip-empty-lines",
        action="store_true",
        help="Skips reporting of invalid empty lines.",
    )
    validity_display = parser.add_mutually_exclusive_group(required=False)
    validity_display.add_argument(
        "-i",
        "--only-invalid",
        action="store_true",
        help="Only report invalid MAC addresses.",
    )

    validity_display.add_argument(
        "-v",
        "--only-valid",
        action="store_true",
        help="Only report valid MAC addresses.",
    )

    parser.set_defaults(
        func=run,
        strict=False,
        show_info=False,
        show_originals=False,
    )
