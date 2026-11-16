from __future__ import annotations

from collections.abc import Generator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from scapy.layers.l2 import Ether
from scapy.utils import PcapReader

from etherlyzer.core.interpretation.mac.normalization import normalize_strict


@dataclass(slots=True, frozen=True)
class ExtractedMac:
    packet_or_linenumber: int
    src: str
    dst: str | None = None


def extract_unique_pcap_macs(pcap_fp: Path) -> set[str]:
    return {
        address
        for packet in _extract_pcap_macs(pcap_fp)
        for address in (packet.src, packet.dst)
        if address is not None
    }


def _extract_pcap_macs(path: Path) -> Generator[ExtractedMac, Any]:
    with PcapReader(str(path)) as capture:
        for packet_number, packet in enumerate(capture, start=1):
            if Ether not in packet:
                continue

            ethernet = packet[Ether]
            yield ExtractedMac(
                packet_number, normalize_strict(ethernet.src), normalize_strict(ethernet.dst)
            )


def extract_file(path: Path) -> Generator[ExtractedMac, Any]:
    if path.suffix.lower() in {".pcap", ".pcapng"}:
        yield from _extract_pcap_macs(path)
    else:
        yield from extract_from_bytestream(path.read_bytes())


def hex_value(byte: int) -> int:
    if 48 <= byte <= 57:
        return byte - 48
    if 65 <= byte <= 70:
        return byte - 55
    if 97 <= byte <= 102:
        return byte - 87
    return -1


def extract_from_bytestream(data: bytes) -> Generator[ExtractedMac, Any]:
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
        yield ExtractedMac(start, normalize_strict(mac))
