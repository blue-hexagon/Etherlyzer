from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

from etherlyzer.ieee.entry.ethertype import EtherTypeEntry
from etherlyzer.ieee.index.base import HEX_DIGITS, IEEEIndexProtocol


@dataclass(slots=True)
class EthertypeIndex(IEEEIndexProtocol):
    ethertype: dict[str, EtherTypeEntry] = field(default_factory=dict)

    def insert(
        self,
        entries: Iterable[EtherTypeEntry],
    ) -> None:
        self.ethertype.update({entry.assignment.upper(): entry for entry in entries})

    def get_one(self, identifier: str) -> EtherTypeEntry | None:
        ethertype = "".join(c for c in identifier.upper() if c in HEX_DIGITS)
        return self.ethertype.get(ethertype)
