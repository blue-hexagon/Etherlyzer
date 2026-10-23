from __future__ import annotations

from collections.abc import Iterable

from etherlyzer.ieee.index.store import IndexStore
from etherlyzer.ieee.registry.category import RegistryCategory
from etherlyzer.ieee.registry.ieee_registry import IEEERegistry


class IndexBuilder:
    @staticmethod
    def build(registries: Iterable[IEEERegistry]) -> IndexStore:
        indexes = IndexStore()

        for registry in registries:
            entries = registry.load()

            match registry.category:
                case RegistryCategory.MAC_REGISTRY:
                    indexes.mac.insert(registry, entries)

                case RegistryCategory.ETHERTYPE_REGISTRY:
                    indexes.ethertype.insert(entries)

                case RegistryCategory.IDENTIFIER_REGISTRY:
                    indexes.identifier.insert(registry, entries)

                case _:
                    raise ValueError(f"Unsupported registry category: {registry.category}")

        for mac in indexes.mac.walk():
            entry = indexes.mac.lookup(mac)
            if entry is not None:
                indexes.vendor.insert(entry)

        return indexes
