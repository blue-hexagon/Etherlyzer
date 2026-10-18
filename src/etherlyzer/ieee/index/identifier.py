from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

from etherlyzer.ieee.entry.mac import MACAllocationEntry
from etherlyzer.ieee.index.base import IEEEIndexProtocol
from etherlyzer.ieee.registry.ieee_registry import IEEERegistry


@dataclass(slots=True)
class IdentifierIndex(IEEEIndexProtocol):
    cid: dict[str, MACAllocationEntry] = field(default_factory=dict)
    opid: dict[str, MACAllocationEntry] = field(default_factory=dict)
    manid: dict[str, MACAllocationEntry] = field(default_factory=dict)

    def insert(self, registry: IEEERegistry, entries: Iterable[MACAllocationEntry]) -> None:
        match registry.name:
            case "CID":
                target = self.cid
            case "OPID":
                target = self.opid
            case "MANID":
                target = self.manid
            case _:
                raise ValueError(f"Unsupported identifier registry: {registry.name}")

        target.update({entry.assignment.upper(): entry for entry in entries})

    def get_one(self, identifier: str) -> MACAllocationEntry | None:
        identifier = identifier.upper()
        return self.cid.get(identifier) or self.opid.get(identifier) or self.manid.get(identifier)
