from __future__ import annotations

from typing import Protocol

from etherlyzer.ieee.entry.ethertype import EtherTypeEntry
from etherlyzer.ieee.entry.mac import MACAllocationEntry


class IndexService(Protocol):
    def lookup_many(self, identifier: str) -> list[MACAllocationEntry | EtherTypeEntry] | None: ...
    def lookup(self, identifier: str) -> MACAllocationEntry | EtherTypeEntry | None: ...
