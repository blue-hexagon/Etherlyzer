from etherlyzer.terminal.utility import read_multiline
from etherlyzer.formatters import MACFormatter


def run(args):
    if args.bulk:
        macs = read_multiline(linetype="MAC addresses")
    else:
        macs = args.mac

    linenumber = 1
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
        "validize",
        help="Validates and normalizes MAC addresses (this command does not perform any sort of typo-correction - use `format` for that purpose).",
    )

    parser.add_argument(
        "mac",
        nargs="?",
        help="MAC address to normalize",
    )

    parser.add_argument(
        "-b",
        "--bulk",
        action="store_true",
        help="Read multiple MAC addresses interactively",
    )
    parser.add_argument(
        "-l",
        "--linenumbers",
        action="store_true",
        help="Show linenumbers corresponding to each MAC address (kind of only useful when validizing in bulk)",
        dest="linenumbers"
    )

    parser.add_argument(
        "-s",
        "--strict",
        dest="strict",
        action="store_true",
        help="Only return MAC's that can be normalized without errors.",
    )

    parser.add_argument(
        "-o",
        "--show-originals",
        dest="show_originals",
        action="store_true",
        help="Displays the original MAC addresses after the normalized MAC address on each line.",
    )
    parser.add_argument(
        "-i",
        "--show-info",
        dest="show_info",
        action="store_true",
        help="Displays an OK or ERR before each line depending on whether the outout succeeded normalization.",
    )

    parser.set_defaults(
        func=run,
        strict=False,
        show_info=False,
        show_originals=False,
    )
