from __future__ import annotations

from etherlyzer.formatters import MACFormatter


def run(args) -> int:

    print(
        MACFormatter.format(
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

    parser.add_argument("mac")
    parser.add_argument("--separator", type=str, default=":", help="Separator for mac address")
    parser.add_argument("--block-size", type=int, default=2, help="Block size for mac address")
    parser.add_argument(
        "--casing", type=str, default="lower", help="Use upper case (lower is default)"
    )
    parser.add_argument(
        "--fix-typos",
        action="store_true",
        default=False,
        dest="fix_typos",
        help="Fix typos like O instead of 0",
    )

    parser.set_defaults(func=run)
