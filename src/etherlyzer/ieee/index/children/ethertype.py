from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

from etherlyzer.ieee.entry.ethertype import EtherTypeEntry
from etherlyzer.ieee.index.children.proto import IndexService
from etherlyzer.lib.common import HEX_DIGITS


@dataclass(slots=True)
class EthertypeIndex(IndexService):
    ethertype: dict[str, EtherTypeEntry] = field(default_factory=dict)

    def insert(self, entries: Iterable[EtherTypeEntry]) -> None:
        self.ethertype.update({entry.assignment.upper(): entry for entry in entries})

    def lookup(self, identifier: str) -> EtherTypeEntry | None:
        ethertype = "".join(c for c in identifier.upper() if c in HEX_DIGITS)
        return self.ethertype.get(ethertype)
