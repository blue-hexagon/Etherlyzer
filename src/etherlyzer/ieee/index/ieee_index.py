from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path

from etherlyzer.ieee.entry.ethertype import EtherTypeEntry
from etherlyzer.ieee.entry.mac import MACAllocationEntry
from etherlyzer.ieee.index.ethertype import EthertypeIndex
from etherlyzer.ieee.index.identifier import IdentifierIndex
from etherlyzer.ieee.index.mac_allocation import MACAllocationIndex
from etherlyzer.ieee.index.vendor import VendorIndex
from etherlyzer.ieee.registry.category import RegistryCategory
from etherlyzer.ieee.registry.ieee_registry import IEEERegistry


@dataclass(slots=True)
class IEEEIndexCatalog:
    mac_index: MACAllocationIndex = field(default_factory=MACAllocationIndex)
    ethertype_index: EthertypeIndex = field(default_factory=EthertypeIndex)
    identifier_index: IdentifierIndex = field(default_factory=IdentifierIndex)
    vendor_index: VendorIndex = field(default_factory=VendorIndex)

    @classmethod
    def build(cls, registries: Iterable[IEEERegistry]) -> IEEEIndexCatalog:
        index = cls()

        for registry in registries:
            index._ingest(registry)

        index._build_vendor_index()
        return index

    def _ingest(self, registry: IEEERegistry) -> None:
        entries = registry.load()

        match registry.category:
            case RegistryCategory.MAC_REGISTRY:
                self.mac_index.insert(registry, entries)
            case RegistryCategory.ETHERTYPE_REGISTRY:
                self.ethertype_index.insert(entries)
            case RegistryCategory.IDENTIFIER_REGISTRY:
                self.identifier_index.insert(registry, entries)
            case _:
                raise ValueError(f"Unsupported registry category: {registry.category}")

    def _build_vendor_index(self) -> None:
        for mac in self.mac_index.walk():
            entry = self.mac_index.get_one(mac)
            if entry is not None:
                self.vendor_index.insert(entry)

    def get_from_mac_index(self, mac: str) -> MACAllocationEntry | None:
        return self.mac_index.get_one(mac)

    def get_from_ethertype_index(self, ethertype: str) -> EtherTypeEntry | None:
        ret = self.ethertype_index.get_one(ethertype)
        if not isinstance(ret, EtherTypeEntry) and not isinstance(ret, type(None)):
            raise RuntimeError()
        return ret

    def get_from_identifier_index(self, identifier: str) -> MACAllocationEntry | None:
        return self.identifier_index.get_one(identifier)

    @staticmethod
    def get_many(
        ieee_index: MACAllocationIndex | IdentifierIndex | EthertypeIndex | VendorIndex,
        path_or_text: Path | str | list[str],
    ) -> list[MACAllocationEntry]:
        # Pass a list[str] from interactive or pass a Path or str (path)
        ieee_entries_as_set: set[MACAllocationEntry] = set()

        if isinstance(path_or_text, Path):
            with open(path_or_text) as f:
                text_data = f.readlines()
        else:
            text_data = path_or_text
        for line in text_data:
            ieee_entry = ieee_index.get_one(line)
            if ieee_entry:
                ieee_entries_as_set.add(ieee_entry)

        ieee_entries: list[MACAllocationEntry] = list(ieee_entries_as_set)
        # Sort by name, and then by registry-name reversed
        ieee_entries = sorted(ieee_entries, key=lambda e: e.organization_name)
        ieee_entries = sorted(ieee_entries, key=lambda e: e.registry, reverse=True)

        return ieee_entries

    @staticmethod
    def get_single(
        indextype: VendorIndex | MACAllocationIndex | IdentifierIndex | EthertypeIndex, mac: str
    ) -> MACAllocationEntry | list[MACAllocationEntry] | None:
        ieee_entry = indextype.get_one(mac)
        if ieee_entry:
            return ieee_entry
        else:
            return None
