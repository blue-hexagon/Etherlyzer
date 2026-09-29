from etherlyzer.cliutil import read_multiline
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
            print("ERR".ljust(4, " "), end="")
            if len(validated_mac) > 14:
                print(f"{validated_mac.ljust(14, ' ')[:14]}. >> {validation_mask}")
            else:
                print(f"{validated_mac.ljust(15, ' ')[:15]} >> {validation_mask}")
            continue

        if MACFormatter.mask_is_valid(validation_mask):
            normalized_mac = MACFormatter.normalize(mac)
            print("OK".ljust(4, " "), end="")
            if args.show_originals:
                print(f"{normalized_mac.ljust(15, ' ')} >> {mac}")
            else:
                print(f"{normalized_mac}")
            normalized_count += 1
        else:
            invalid_count += 1

    print()
    print(
        f"Normalized {normalized_count}/{len(macs)} MAC addresses. Invalid MAC addresses identified: {invalid_count}/{len(macs)}")
    return 0


def register(subparsers):
    parser = subparsers.add_parser(
        "validize",
        help="Validates and normalizes MAC addresses",
    )

    parser.add_argument(
        "mac",
        nargs="?",
        help="MAC address to normalize",
    )

    parser.add_argument(
        "--bulk",
        action="store_true",
        help="Read multiple MAC addresses interactively",
    )
    parser.add_argument(
        "--linenumbers",
        action="store_true",
        help="Show linenumbers corresponding to each MAC address (kind of only useful when validizing in bulk)",
        dest="linenumbers"
    )

    parser.add_argument(
        "--strict",
        dest="strict",
        action="store_true",
        help="Return normalized output even for invalid MAC addresses",
    )

    parser.add_argument(
        "--include-originals",
        dest="show_originals",
        action="store_true",
        help="Displays the original MAC addresses after the normalized MAC address on each line.",
    )

    parser.set_defaults(
        func=run,
        strict=False,
        show_originals=False,
    )
