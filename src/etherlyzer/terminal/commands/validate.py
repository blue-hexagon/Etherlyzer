import argparse

from etherlyzer.terminal.utility import read_multiline
from etherlyzer.formatters import MACFormatter


def run(args):
    if args.bulk:
        macs = read_multiline(linetype="MAC addresses")
    else:
        macs = [args.mac]

    linenumber = 0
    padding = len(str(len(macs))) + 2
    normalized_count = 0
    invalid_count = 0
    for mac in macs:
        validated_mac, validation_mask = MACFormatter.validate(mac)
        if args.linenumbers:
            linenumber += 1
            if MACFormatter.mask_is_valid(validation_mask):
                print(f"{linenumber}.".ljust(padding, " "), end="")
            elif not args.strict:
                print(f"{linenumber}.".ljust(padding, " "), end="")

        if not args.strict and not MACFormatter.mask_is_valid(validation_mask):
            if args.show_info is True:
                print("ERR".ljust(4, " "), end="")
            if len(validated_mac) > 14:
                print(f"{validated_mac.ljust(14, ' ')[:14]}. => {validation_mask}")
            else:
                print(f"{validated_mac.ljust(15, ' ')[:15]} => {validation_mask}")
            invalid_count += 1
            continue

        if MACFormatter.mask_is_valid(validation_mask):
            normalized_mac = MACFormatter.normalize(mac)
            if args.show_info is True:
                print("OK".ljust(4, " "), end="")
            if args.show_originals:
                print(f"{normalized_mac.ljust(15, ' ')} <~ {mac}")
            else:
                print(f"{normalized_mac}")
            normalized_count += 1

    print()
    print(
        f"Normalized {normalized_count}/{len(macs)} MAC addresses. Invalid MAC addresses identified: {invalid_count}/{len(macs)}")
    return 0



def register(subparsers):
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
        "--linenumbers",
        action="store_true",
        help="Prefix output lines with their corresponding input line number.",
    )

    parser.add_argument(
        "-s",
        "--strict",
        action="store_true",
        help="Suppress invalid entries and output only successfully normalized MAC addresses.",
    )

    parser.add_argument(
        "-o",
        "--show-originals",
        action="store_true",
        help="Show the original input alongside each normalized MAC address.",
    )

    parser.add_argument(
        "-i",
        "--show-info",
        action="store_true",
        help="Prefix each result with OK or ERR to indicate validation status.",
    )

    parser.set_defaults(
        func=run,
        strict=False,
        show_info=False,
        show_originals=False,
    )
