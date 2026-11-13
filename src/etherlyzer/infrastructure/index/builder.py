from __future__ import annotations

from collections.abc import Iterable
from typing import TypeVar

from etherlyzer.infrastructure.index.store import IndexStore
from etherlyzer.infrastructure.registry.family import RegistryFamily
from etherlyzer.infrastructure.registry.provider import (
    Registry,
    is_ethertype_registry,
    is_mac_registry,
)

T = TypeVar("T")


class IndexBuilder:
    @staticmethod
    def build(registries: Iterable[Registry]) -> IndexStore:
        indexes = IndexStore()

        for registry in registries:
            match registry.family:
                case RegistryFamily.MAC_REGISTRY:
                    if is_mac_registry(registry):
                        mac_registry = registry.load()
                        indexes.mac.insert(registry, mac_registry)

                case RegistryFamily.ETHERTYPE_REGISTRY:
                    if is_ethertype_registry(registry):
                        ethertype_registry = registry.load()
                        indexes.ethertype.insert(ethertype_registry)

                case RegistryFamily.IDENTIFIER_REGISTRY:
                    if is_mac_registry(registry):
                        mac_registry = registry.load()
                        indexes.identifier.insert(registry, mac_registry)

                case _:
                    raise ValueError(f"Unsupported registry category: {registry.family}")

        for mac in indexes.mac.walk():
            entry = indexes.mac.lookup(mac)
            if entry is not None:
                indexes.vendor.insert(entry)

        return indexes
