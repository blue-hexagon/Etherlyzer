from typing import ClassVar

from etherlyzer.ieee.entry.ethertype import EtherTypeEntry
from etherlyzer.ieee.entry.mac import MACAllocationEntry
from etherlyzer.ieee.registry.category import RegistryCategory
from etherlyzer.ieee.registry.ieee_registry import IEEERegistry


class Catalog:
    IEEE_REGISTRIES: ClassVar[dict[str, IEEERegistry]] = {
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
    def db_is_initialized(cls) -> bool:
        db_init_checks: list[bool] = []
        for registry in cls.IEEE_REGISTRIES.values():
            db_init_checks.append(registry.registry_cache.filepath.exists())
        return all(list(db_init_checks))

    @staticmethod
    def get_registry(registry_name: str) -> IEEERegistry:
        reg = Catalog.IEEE_REGISTRIES.get(registry_name, None)
        if reg is None:
            raise RuntimeError(f"Unknown registry {registry_name}")
        return reg

    def get_all_registries_and_ensure_cache_is_synced(
        self, check_for_updates: bool = True, inform_if_synced_about_expiration: bool = False
    ) -> list[IEEERegistry]:
        for registry in self.IEEE_REGISTRIES.values():
            # If not checking for updates, we still need a present dataset.
            if (
                check_for_updates
                and registry.registry_cache.need_updates(inform_if_synced_about_expiration)
            ) or not self.db_is_initialized():
                status = registry.registry_downloader.fetch_online()
                if status is False:
                    break
        return list(self.IEEE_REGISTRIES.values())

    def get_registries(self) -> list[IEEERegistry]:
        return list(self.IEEE_REGISTRIES.values())

    def __getitem__(self, key: str) -> IEEERegistry:
        return self.IEEE_REGISTRIES[key]
