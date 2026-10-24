from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

from scapy.layers.l2 import Ether
from scapy.utils import PcapReader


@dataclass(slots=True)
class MACExtractor:
    @staticmethod
    def extract_pcap_macs(path: Path) -> Iterator[tuple[int, str]]:
        with PcapReader(str(path)) as capture:
            for packet_number, packet in enumerate(capture, start=1):
                if Ether not in packet:
                    continue

                ethernet = packet[Ether]

                yield packet_number, ethernet.src
                yield packet_number, ethernet.dst

    @classmethod
    def extract_file(cls, path: Path) -> Iterator[tuple[int, str]]:
        if path.suffix.lower() in {".pcap", ".pcapng"}:
            yield from cls.extract_pcap_macs(path)
        else:
            yield from cls.extract_macs(path.read_bytes())

    @staticmethod
    def hex_value(byte: int) -> int:
        if 48 <= byte <= 57:
            return byte - 48
        if 65 <= byte <= 70:
            return byte - 55
        if 97 <= byte <= 102:
            return byte - 87
        return -1

    @classmethod
    def extract_macs(cls, data: bytes) -> Iterator[tuple[int, str]]:
        """Extract 48-bit MAC candidates from byte-oriented text."""

        for start in range(len(data)):
            if cls.hex_value(data[start]) < 0:
                continue

            # Reject candidates embedded in longer hex sequences.
            if start > 0 and cls.hex_value(data[start - 1]) >= 0:
                continue

            digits: list[int] = []
            pos = start

            while pos < len(data) and len(digits) < 12:
                value = cls.hex_value(data[pos])

                if value >= 0:
                    digits.append(value)
                    pos += 1
                    continue

                # Skip at most one non-hexadecimal byte.
                if digits and pos + 1 < len(data) and cls.hex_value(data[pos + 1]) >= 0:
                    pos += 1
                    continue

                break

            if len(digits) != 12:
                continue

            # Reject candidates embedded in longer hex sequences.
            if pos < len(data) and cls.hex_value(data[pos]) >= 0:
                continue

            mac = "".join(f"{digit:X}" for digit in digits)
            yield start, mac
