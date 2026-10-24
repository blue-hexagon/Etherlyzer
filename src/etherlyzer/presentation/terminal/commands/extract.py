from __future__ import annotations

import argparse
from pathlib import Path

from etherlyzer.core.extraction import MACExtractor
from etherlyzer.core.formatting import MACFormatter
from etherlyzer.core.normalization import normalize
from etherlyzer.presentation.terminal.utility import read_multiline


def run(args: argparse.Namespace) -> int:
    is_pcap = not args.bulk and args.file.suffix.lower() in {".pcap", ".pcapng"}

    if args.bulk:
        lines = read_multiline(
            linetype="text",
            skip_empty_lines=False,
        )
        data = "\n".join(lines).encode("utf-8")
        matches = MACExtractor.extract_macs(data)

    else:
        matches = MACExtractor.extract_file(args.file)

    seen: set[str] = set()
    count = 0

    for position, mac in matches:
        normalized = normalize(mac)

        if args.unique:
            if normalized in seen:
                continue
            seen.add(normalized)

        formatted = MACFormatter.format(
            mac=normalized,
            separator=args.separator,
            block_size=args.block_size,
            case=args.casing,
            fix_typos=False,
        )

        if args.offsets:
            label = "Packet" if is_pcap else "Offset"
            location = str(position) if is_pcap else f"0x{position:08X}"
            print(f"{label} {location}  {formatted}")
        else:
            print(formatted)

        count += 1

    return 0 if count else 1


def register(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    parser = subparsers.add_parser(
        "extract",
        help="Extract MAC address candidates from text or binary files.",
        description=(
            "Extract MAC addresses from packet captures or hexadecimal "
            "representations embedded in text. Supports PCAP, PCAPNG, "
            "and arbitrary text files."
        ),
        epilog=r"""
Examples:
  etherlyzer extract -f capture.txt
  etherlyzer extract -f capture.bin
  etherlyzer extract -b
  etherlyzer extract -f capture.txt -l
  etherlyzer extract -f capture.txt -u
  etherlyzer extract -f capture.txt -p . -s 4
  etherlyzer extract -f capture.txt -c upper
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    source = parser.add_mutually_exclusive_group(required=True)

    source.add_argument(
        "-f",
        "--file",
        type=Path,
        help="Read and scan a text or binary file.",
    )

    source.add_argument(
        "-b",
        "--bulk",
        action="store_true",
        help="Read text interactively for MAC extraction.",
    )

    parser.add_argument(
        "-l",
        "--offsets",
        action="store_true",
        help="Show byte offsets for text or packet numbers for packet captures.",
    )

    parser.add_argument(
        "-u",
        "--unique",
        action="store_true",
        help="Only output the first occurrence of each MAC address.",
    )

    parser.add_argument(
        "-p",
        "--separator",
        default=":",
        help="Output separator (default: ':').",
    )

    parser.add_argument(
        "-s",
        "--block-size",
        type=int,
        default=2,
        help="Number of hexadecimal characters per block (default: 2).",
    )

    parser.add_argument(
        "-c",
        "--casing",
        choices=["lower", "upper"],
        default="lower",
        help="Output casing (default: lower).",
    )

    parser.set_defaults(func=run)
