from __future__ import annotations

from collections.abc import Generator, Iterable
from dataclasses import dataclass, field

from etherlyzer.ieee.entry.mac import MACAllocationEntry
from etherlyzer.ieee.index.base import HEX_DIGITS, IEEEIndexProtocol
from etherlyzer.ieee.registry.ieee_registry import IEEERegistry


@dataclass(slots=True)
class MACAllocationIndex(IEEEIndexProtocol):
    prefixes_36: dict[str, MACAllocationEntry] = field(default_factory=dict)
    prefixes_28: dict[str, MACAllocationEntry] = field(default_factory=dict)
    prefixes_24: dict[str, MACAllocationEntry] = field(default_factory=dict)

    def insert(self, registry: IEEERegistry, entries: Iterable[MACAllocationEntry]) -> None:
        match registry.prefix_bits:
            case 36:
                target = self.prefixes_36
            case 28:
                target = self.prefixes_28
            case 24:
                target = self.prefixes_24
            case _:
                raise ValueError(f"Unsupported prefix length: {registry.prefix_bits}")

        target.update({entry.assignment.upper(): entry for entry in entries})

    def get_one(self, identifier: str) -> MACAllocationEntry | None:
        mac = "".join(c for c in identifier.upper() if c in HEX_DIGITS)

        # longest prefix match
        return (
            self.prefixes_36.get(mac[:9])
            or self.prefixes_28.get(mac[:7])
            or self.prefixes_24.get(mac[:6])
        )

    def walk(self) -> Generator[str]:
        yield from self.prefixes_36
        yield from self.prefixes_28
        yield from self.prefixes_24
