from __future__ import annotations

from collections.abc import Generator, Iterable
from dataclasses import dataclass, field

from etherlyzer.core.constants import HEX_DIGITS
from etherlyzer.ieee.entry.mac import MACAllocationEntry, MACLookupResult, classify_mac
from etherlyzer.ieee.index.children.proto import IndexService
from etherlyzer.ieee.registry.ieee_registry import RegistrySource


@dataclass(slots=True)
class MACAllocationIndex(IndexService):
    prefixes_36: dict[str, MACAllocationEntry] = field(default_factory=dict)
    prefixes_28: dict[str, MACAllocationEntry] = field(default_factory=dict)
    prefixes_24: dict[str, MACAllocationEntry] = field(default_factory=dict)
    IAB_ENCLOSING_IEEE_RAS = frozenset({"0050C2", "40D855"})
    # IAB-Based Identifiers
    # 2026-11-04: https://standards-support.ieee.org/hc/en-us/articles/4888705676564-Guidelines-for-Use-of-Extended-Unique-Identifier-EUI-Organizationally-Unique-Identifier-OUI-and-Company-ID-CID
    # While the IEEE RA did not guarantee that the 36-bit IAB identifier
    # would always be created from the same OUI, all IAB assignments were
    # in fact created from two particular OUIs: 00-50-C2hex and 40-D8-55hex.
    # The former was used until all the IABs based on it were assigned [(200X)], after which the latter was used [(201X)].
    # TODO: That should be the obly two enclosing IEEE-RA's but I'm slightly uncertain.

    def insert(self, registry: RegistrySource, entries: Iterable[MACAllocationEntry]) -> None:
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

    def lookup_group_allocation(self, identifier: str) -> MACAllocationEntry | None:
        """This is a special lookup only used once in the entire program.
        It fixes an edge-case where IAB will take precendence over the MAM and MAL registry
        because it is more specific. But that is an error in this specific instance for the following reason:
        MA-L, MA-M, MA-S (not IAB) can flip the I/G bit of an assignment to create a multicast address (per IEEE)
        Hence IAB must be excluded in this very lookup."""

        m = "".join(c for c in identifier.upper() if c in HEX_DIGITS)
        mac = self.clear_ig_bit(m)
        entry_36 = self.prefixes_36.get(mac[:9])
        entry_24 = self.prefixes_24.get(mac[:6])
        return (
            (entry_36 if entry_36 is not None and entry_36.registry != "IAB" else None)
            or self.prefixes_28.get(mac[:7])
            or (
                entry_24
                if entry_24 is not None and mac[:6] not in self.IAB_ENCLOSING_IEEE_RAS
                else None
            )
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
