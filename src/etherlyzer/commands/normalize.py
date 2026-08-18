from etherlyzer.formatters import MACFormatter


def run(args):
    print(MACFormatter.normalize(args.mac))
    return 0


def register(subparsers):

    parser = subparsers.add_parser(
        "normalize",
        help="Normalize MAC address",

    )
    parser.add_argument("mac")
    parser.set_defaults(func=run)
