from __future__ import annotations

from etherlyzer.formatters import MACFormatter


def run(args) -> int:
    print(
        MACFormatter.format_custom(
            mac=args.mac,
            separator=args.separator,
            block_size=args.block_size,
            case=args.casing,
            fix_typos=args.fix_typos,
        )
    )

    return 0


def register(subparsers):
    parser = subparsers.add_parser(
        "format",
        help="Format MAC address",
    )

    parser.add_argument("mac", nargs="?")
    parser.add_argument("-p", "--separator", type=str, default=":", help="Separator for mac address")
    parser.add_argument("-b", "--block-size", type=int, default=2, help="Block size for mac address")
    parser.add_argument(
        "-c",
        "--casing", type=str, default="lower", help="Use upper case (lower is default)"
    )
    parser.add_argument(
        "-f",
        "--fix-typos",
        action="store_true",
        default=False,
        dest="fix_typos",
        help="Fix typo-candidates like o/O/ø/Ø instead of 0, 1 instead of i/I et cetera (see docs for specifics).",
    )

    parser.set_defaults(func=run)
