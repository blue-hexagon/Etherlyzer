from __future__ import annotations

import argparse
from collections.abc import Iterator
from pathlib import Path

from scapy.layers.l2 import Ether
from scapy.utils import PcapReader

from etherlyzer.formatters import MACFormatter
from etherlyzer.terminal.utility import read_multiline


def extract_pcap_macs(path: Path) -> Iterator[tuple[int, str]]:
    with PcapReader(str(path)) as capture:
        for packet_number, packet in enumerate(capture, start=1):
            if Ether not in packet:
                continue

            ethernet = packet[Ether]

            yield packet_number, ethernet.src
            yield packet_number, ethernet.dst


def extract_file(path: Path) -> Iterator[tuple[int, str]]:
    if path.suffix.lower() in {".pcap", ".pcapng"}:
        yield from extract_pcap_macs(path)
    else:
        yield from extract_macs(path.read_bytes())


def hex_value(byte: int) -> int:
    if 48 <= byte <= 57:
        return byte - 48
    if 65 <= byte <= 70:
        return byte - 55
    if 97 <= byte <= 102:
        return byte - 87
    return -1


def extract_macs(data: bytes) -> Iterator[tuple[int, str]]:
    """Extract 48-bit MAC candidates from byte-oriented text."""

    for start in range(len(data)):
        if hex_value(data[start]) < 0:
            continue

        # Reject candidates embedded in longer hex sequences.
        if start > 0 and hex_value(data[start - 1]) >= 0:
            continue

        digits: list[int] = []
        pos = start

        while pos < len(data) and len(digits) < 12:
            value = hex_value(data[pos])

            if value >= 0:
                digits.append(value)
                pos += 1
                continue

            # Skip at most one non-hexadecimal byte.
            if digits and pos + 1 < len(data) and hex_value(data[pos + 1]) >= 0:
                pos += 1
                continue

            break

        if len(digits) != 12:
            continue

        # Reject candidates embedded in longer hex sequences.
        if pos < len(data) and hex_value(data[pos]) >= 0:
            continue

        mac = "".join(f"{digit:X}" for digit in digits)
        yield start, mac


def run(args: argparse.Namespace) -> int:
    is_pcap = not args.bulk and args.file.suffix.lower() in {".pcap", ".pcapng"}

    if args.bulk:
        lines = read_multiline(
            linetype="text",
            skip_empty_lines=False,
        )
        data = "\n".join(lines).encode("utf-8")
        matches = extract_macs(data)
    else:
        matches = extract_file(args.file)

    seen: set[str] = set()
    count = 0

    for position, mac in matches:
        normalized = MACFormatter.normalize(mac)

        if args.unique:
            if normalized in seen:
                continue
            seen.add(normalized)

        formatted = MACFormatter.format_custom(
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
