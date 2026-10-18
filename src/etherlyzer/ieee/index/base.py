from __future__ import annotations

from typing import Protocol

from etherlyzer.ieee.entry.ethertype import EtherTypeEntry
from etherlyzer.ieee.entry.mac import MACAllocationEntry

HEX_DIGITS = frozenset("0123456789ABCDEF")


class IEEEIndexProtocol(Protocol):
    def get_many(self, identifier: str) -> list[MACAllocationEntry | EtherTypeEntry] | None: ...
    def get_one(self, identifier: str) -> MACAllocationEntry | EtherTypeEntry | None: ...
