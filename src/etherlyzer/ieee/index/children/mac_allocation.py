from __future__ import annotations

from collections.abc import Generator, Iterable
from dataclasses import dataclass, field

from etherlyzer.core.constants import HEX_DIGITS
from etherlyzer.ieee.entry.mac import MACAllocationEntry, MACLookupResult, classify_mac
from etherlyzer.ieee.index.children.proto import IndexService
from etherlyzer.ieee.registry.ieee_registry import IEEERegistry


@dataclass(slots=True)
class MACAllocationIndex(IndexService):
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

    def lookup(self, identifier: str) -> MACAllocationEntry | None:
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

    @staticmethod
    def get_bulk(
        ieee_index: MACAllocationIndex,
        values: Iterable[str],
        include_unsuccessful: bool = False,
    ) -> list[MACLookupResult]:
        results = []

        for line_number, mac in enumerate(values, start=1):
            mac = mac.strip()
            reason = classify_mac(mac)

            if reason is not None:
                result = MACLookupResult(
                    line_number=line_number,
                    mac=mac,
                    reason=reason,
                )
            else:
                entry = ieee_index.lookup(mac)

                result = MACLookupResult(
                    line_number=line_number,
                    mac=mac,
                    entry=entry,
                    reason=None if entry is not None else "Not found",
                )

            if result.entry is not None or include_unsuccessful:
                results.append(result)

        return results
