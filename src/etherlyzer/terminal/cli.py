from __future__ import annotations

import argparse
from pathlib import Path

from etherlyzer.terminal.commands import info, format, normalize, identify, update, bulk
from etherlyzer.util.dirs import DATA_PLATFORM_DIR
from etherlyzer.util.knobs import etherlyzer_knobs


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="etherlyzer",
        description="EtherLyzer - Ethernet lookup and analysis toolkit",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="EtherLyzer 0.1.0",
    )

    subparsers = parser.add_subparsers(
        title="Commands",
        required=True,
    )

    bulk.register(subparsers)
    normalize.register(subparsers)
    format.register(subparsers)
    update.register(subparsers)
    info.register(subparsers)
    identify.register(subparsers)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()

    args = parser.parse_args(argv)

    if not hasattr(args, "func"):
        parser.print_help()
        return 1

    try:
        return args.func(args)

    except KeyboardInterrupt:
        print("Interrupted.")
        return 130

    except Exception as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
