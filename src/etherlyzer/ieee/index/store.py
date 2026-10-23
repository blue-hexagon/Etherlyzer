from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

from etherlyzer.ieee.entry.mac import MACAllocationEntry, MACLookupResult, classify_mac
from etherlyzer.ieee.index.children.ethertype import EthertypeIndex
from etherlyzer.ieee.index.children.identifier import IdentifierIndex
from etherlyzer.ieee.index.children.mac_allocation import MACAllocationIndex
from etherlyzer.ieee.index.children.vendor import VendorIndex


@dataclass(slots=True)
class IndexStore:
    mac: MACAllocationIndex = field(default_factory=MACAllocationIndex)
    ethertype: EthertypeIndex = field(default_factory=EthertypeIndex)
    identifier: IdentifierIndex = field(default_factory=IdentifierIndex)
    vendor: VendorIndex = field(default_factory=VendorIndex)


    class MACLookupService:
        def __init__(self, index: MACAllocationIndex) -> None:
            self.index = index

        def lookup(self, mac: str) -> MACLookupResult: ...

        def lookup_many(
            self,
            values: Iterable[str],
            include_unsuccessful: bool = False,
        ) -> list[MACLookupResult]: ...

    @staticmethod
    def get_single(
        indextype: VendorIndex | MACAllocationIndex | IdentifierIndex | EthertypeIndex, mac: str
    ) -> MACAllocationEntry | list[MACAllocationEntry] | None:
        ieee_entry = indextype.lookup(mac)
        if ieee_entry:
            return ieee_entry
        else:
            return None
