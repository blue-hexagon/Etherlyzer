from pathlib import Path
from typing import TypeVar

from etherlyzer.ieee.entry.ethertype import EtherTypeEntry
from etherlyzer.ieee.entry.mac import MACAllocationEntry
from etherlyzer.ieee.registry.family import RegistryFamily
from etherlyzer.ieee.registry.ieee_registry import IEEERegistry

T = TypeVar("T")


class RegistryProvider:
    def __init__(self, cache_dir: Path | None = None):
        self.cache_dir = cache_dir
        self.registries = self._create_registries()

    def _create_registries(self) -> dict[str, IEEERegistry[T]]:
        return {
            "mal": IEEERegistry(
                enabled=True,
                name="MA-L",
                model=MACAllocationEntry,
                full_name="MAC Address Block Large",
                legacy_name="OUI",
                family=RegistryFamily.MAC_REGISTRY,
                prefix_bits=24,
                address_bits=24,
                address_count=16_777_216,
                legacy=False,
                description=(
                    "Large IEEE MAC address allocation. Formerly known as the "
                    "Organizationally Unique Identifier (OUI). Used by vendors "
                    "requiring large address spaces."
                ),
                url="https://standards-oui.ieee.org/oui/oui.csv",
                cache_dir=self.cache_dir,
            ),
            "mam": IEEERegistry(
                enabled=True,
                name="MA-M",
                model=MACAllocationEntry,
                full_name="MAC Address Block Medium",
                legacy_name="OUI-28",
                family=RegistryFamily.MAC_REGISTRY,
                prefix_bits=28,
                address_bits=20,
                address_count=1_048_576,
                legacy=False,
                description=(
                    "Medium-sized IEEE MAC address allocation intended for "
                    "organizations requiring fewer addresses than MA-L."
                ),
                url="https://standards-oui.ieee.org/oui28/mam.csv",
                cache_dir=self.cache_dir,
            ),
            "mas": IEEERegistry(
                enabled=True,
                name="MA-S",
                model=MACAllocationEntry,
                full_name="MAC Address Block Small",
                legacy_name="OUI-36",
                family=RegistryFamily.MAC_REGISTRY,
                prefix_bits=36,
                address_bits=12,
                address_count=4_096,
                legacy=False,
                description=(
                    "Small IEEE MAC address allocation for embedded devices, "
                    "IoT, industrial equipment, and smaller manufacturers."
                ),
                url="https://standards-oui.ieee.org/oui36/oui36.csv",
                cache_dir=self.cache_dir,
            ),
            "cid": IEEERegistry(
                enabled=True,
                name="CID",
                model=MACAllocationEntry,
                full_name="Company Identifier",
                legacy_name=None,
                family=RegistryFamily.IDENTIFIER_REGISTRY,
                legacy=False,
                description=(
                    "Unique company identifiers assigned by IEEE. Identifies "
                    "organizations independently of MAC address allocations."
                ),
                url="https://standards-oui.ieee.org/cid/cid.csv",
                cache_dir=self.cache_dir,
            ),
            "iab": IEEERegistry(
                enabled=True,
                name="IAB",
                model=MACAllocationEntry,
                full_name="Individual Address Block",
                legacy_name=None,
                family=RegistryFamily.MAC_REGISTRY,
                prefix_bits=36,
                address_bits=12,
                address_count=4_096,
                legacy=True,
                description=(
                    "Legacy IEEE MAC address allocation scheme superseded by "
                    "MA-S. Retained for compatibility with older hardware."
                ),
                url="https://standards-oui.ieee.org/iab/iab.csv",
                cache_dir=self.cache_dir,
            ),
            "ethertype": IEEERegistry(
                enabled=True,
                name="EtherType",
                model=EtherTypeEntry,
                full_name="EtherType Registry",
                legacy_name=None,
                family=RegistryFamily.ETHERTYPE_REGISTRY,
                legacy=False,
                description=(
                    "Registry mapping EtherType values to Ethernet protocols, "
                    "including IPv4, IPv6, ARP, VLAN tagging, LLDP, MPLS, "
                    "802.1X, and many vendor-specific protocols."
                ),
                url="https://standards-oui.ieee.org/ethertype/eth.csv",
                cache_dir=self.cache_dir,
            ),
        }

    def get(self, registry_name: str, require_cache: bool = False) -> IEEERegistry[T]:
        registry = self.registries.get(registry_name)

        if registry is None:
            raise KeyError(f"Unknown registry: {registry_name!r}. Choices: {list(self.registries)}")

        if require_cache:
            self.ensure_cache_exists(registry_name)

        return registry

    def get_by_name(self, name: str) -> IEEERegistry[T]:
        for registry in self.registries.values():
            if registry.name.casefold() == name.casefold():
                return registry

        raise KeyError(f"Unknown registry: {name!r}")

    def get_all(self, require_cache: bool = False) -> list[IEEERegistry[T]]:
        if require_cache:
            self.ensure_all_caches_exist()

        return list(self.registries.values())

    def cache_exists(self, registry_name: str) -> bool:
        registry = self.get(registry_name)
        return registry.registry_cache.filepath.exists()

    def all_caches_exist(self) -> bool:
        return all(self.cache_exists(name) for name in self.registries)

    def ensure_cache_exists(self, registry_name: str) -> None:
        if not self.cache_exists(registry_name):
            raise RuntimeError(f"Registry cache for {registry_name!r} is missing.")

    def ensure_all_caches_exist(self) -> None:
        if not self.all_caches_exist():
            raise RuntimeError("One or more registry caches are missing.")

    def __getitem__(self, key: str) -> IEEERegistry[T]:
        return self.registries[key]
