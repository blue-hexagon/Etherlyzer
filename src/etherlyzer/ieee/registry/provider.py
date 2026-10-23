from typing import ClassVar

from etherlyzer.ieee.entry.ethertype import EtherTypeEntry
from etherlyzer.ieee.entry.mac import MACAllocationEntry
from etherlyzer.ieee.registry.category import RegistryCategory
from etherlyzer.ieee.registry.ieee_registry import IEEERegistry


class RegistryProvider:
    REGISTRIES: ClassVar[dict[str, IEEERegistry]] = {
        "mal": IEEERegistry(
            enabled=True,
            name="MA-L",
            model=MACAllocationEntry,
            full_name="MAC Address Block Large",
            legacy_name="OUI",
            category=RegistryCategory.MAC_REGISTRY,
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
        ),
        "mam": IEEERegistry(
            enabled=True,
            name="MA-M",
            model=MACAllocationEntry,
            full_name="MAC Address Block Medium",
            legacy_name="OUI-28",
            category=RegistryCategory.MAC_REGISTRY,
            prefix_bits=28,
            address_bits=20,
            address_count=1_048_576,
            legacy=False,
            description=(
                "Medium-sized IEEE MAC address allocation intended for "
                "organizations requiring fewer addresses than MA-L."
            ),
            url="https://standards-oui.ieee.org/oui28/mam.csv",
        ),
        "mas": IEEERegistry(
            enabled=True,
            name="MA-S",
            model=MACAllocationEntry,
            full_name="MAC Address Block Small",
            legacy_name="OUI-36",
            category=RegistryCategory.MAC_REGISTRY,
            prefix_bits=36,
            address_bits=12,
            address_count=4_096,
            legacy=False,
            description=(
                "Small IEEE MAC address allocation for embedded devices, "
                "IoT, industrial equipment, and smaller manufacturers."
            ),
            url="https://standards-oui.ieee.org/oui36/oui36.csv",
        ),
        "cid": IEEERegistry(
            enabled=True,
            name="CID",
            model=MACAllocationEntry,
            full_name="Company Identifier",
            legacy_name=None,
            category=RegistryCategory.IDENTIFIER_REGISTRY,
            legacy=False,
            description=(
                "Unique company identifiers assigned by IEEE. Identifies "
                "organizations independently of MAC address allocations."
            ),
            url="https://standards-oui.ieee.org/cid/cid.csv",
        ),
        "iab": IEEERegistry(
            enabled=True,
            name="IAB",
            model=MACAllocationEntry,
            full_name="Individual Address Block",
            legacy_name=None,
            category=RegistryCategory.MAC_REGISTRY,
            prefix_bits=36,
            address_bits=12,
            address_count=4_096,
            legacy=True,
            description=(
                "Legacy IEEE MAC address allocation scheme superseded by "
                "MA-S. Retained for compatibility with older hardware."
            ),
            url="https://standards-oui.ieee.org/iab/iab.csv",
        ),
        "ethertype": IEEERegistry(
            enabled=True,
            name="EtherType",
            model=EtherTypeEntry,
            full_name="EtherType Registry",
            legacy_name=None,
            category=RegistryCategory.ETHERTYPE_REGISTRY,
            legacy=False,
            description=(
                "Registry mapping EtherType values to Ethernet protocols, "
                "including IPv4, IPv6, ARP, VLAN tagging, LLDP, MPLS, "
                "802.1X, and many vendor-specific protocols."
            ),
            url="https://standards-oui.ieee.org/ethertype/eth.csv",
        ),
    }

    @classmethod
    def get(cls, registry_name: str, require_cache: bool = False) -> IEEERegistry:
        registry = cls.REGISTRIES.get(registry_name)

        if registry is None:
            raise KeyError(f"Unknown registry: {registry_name!r}. Choices: {list(cls.REGISTRIES)}")

        if require_cache:
            cls.ensure_cache_exists(registry_name)

        return registry

    @classmethod
    def get_all(cls, require_cache: bool = False) -> list[IEEERegistry]:
        if require_cache:
            cls.ensure_all_caches_exist()

        return list(cls.REGISTRIES.values())

    @classmethod
    def cache_exists(cls, registry_name: str) -> bool:
        registry = cls.get(registry_name)
        return registry.registry_cache.filepath.exists()

    @classmethod
    def all_caches_exist(cls) -> bool:
        return all(cls.cache_exists(name) for name in cls.REGISTRIES)

    @classmethod
    def ensure_cache_exists(cls, registry_name: str) -> None:
        if not cls.cache_exists(registry_name):
            raise RuntimeError(f"Registry cache for {registry_name!r} is missing.")

    @classmethod
    def ensure_all_caches_exist(cls) -> None:
        if not cls.all_caches_exist():
            raise RuntimeError("One or more registry caches are missing.")

    def __getitem__(self, key: str) -> IEEERegistry:
        return self.REGISTRIES[key]
