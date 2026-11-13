from __future__ import annotations

from typing import Protocol

from etherlyzer.domain.entry.ethertype import EtherTypeEntry
from etherlyzer.domain.entry.mac import MACAllocationEntry


class IndexService(Protocol):
    def lookup_many(self, identifier: str) -> list[MACAllocationEntry | EtherTypeEntry] | None: ...
    def lookup(self, identifier: str) -> MACAllocationEntry | EtherTypeEntry | None: ...

    @staticmethod
    def flip_ig_bit(mac: str) -> str:
        first = int(mac[:2], 16) ^ 0x01
        return f"{first:02X}{mac[2:]}"

    @staticmethod
    def clear_ig_bit(mac: str) -> str:
        first = int(mac[:2], 16) & 0xFE
        individual_form = f"{first:02X}{mac[2:]}"
        return individual_form
