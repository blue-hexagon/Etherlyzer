from __future__ import annotations

import argparse

from etherlyzer import __version__
from etherlyzer.terminal.commands import (
    format,
    inspect,
    registries,
    sync,
    validate,
    whois,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="etherlyzer",
        description=(
            "EtherLyzer - Ethernet identifier lookup, validation, formatting, "
            "and IEEE registry analysis toolkit."
        ),
        epilog=r"""
Examples:
  etherlyzer whois 00:11:22:33:44:55
  etherlyzer inspect 00:11:22:33:44:55
  etherlyzer validate 00-11-22-33-44-55
  etherlyzer format 001122334455
  etherlyzer registries
  etherlyzer sync

Run `etherlyzer <command> --help` for command-specific options and examples.
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"EtherLyzer {__version__}",
        help="Show the installed EtherLyzer version and exit.",
    )

    subparsers = parser.add_subparsers(
        title="Commands",
        metavar="COMMAND",
        required=True,
    )

    whois.register(subparsers)
    validate.register(subparsers)
    format.register(subparsers)
    inspect.register(subparsers)
    registries.register(subparsers)
    sync.register(subparsers)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        return args.func(args)

    except KeyboardInterrupt:
        print("\nInterrupted.")
        return 130

    except Exception as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
