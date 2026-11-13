from pathlib import Path
from typing import TypeGuard, TypeVar

from etherlyzer.domain.entry.ethertype import EtherTypeEntry
from etherlyzer.domain.entry.mac import MACAllocationEntry
from etherlyzer.domain.registry.family import RegistryFamily
from etherlyzer.domain.registry.ieee_registry import RegistrySource, SourceFormat

T = TypeVar("T")
type Registry = RegistrySource[MACAllocationEntry] | RegistrySource[EtherTypeEntry]


def is_mac_registry(
    registry: Registry,
) -> TypeGuard[RegistrySource[MACAllocationEntry]]:
    return registry.model is MACAllocationEntry


def is_ethertype_registry(
    registry: Registry,
) -> TypeGuard[RegistrySource[EtherTypeEntry]]:
    return registry.model is EtherTypeEntry


class RegistryProvider:
    def __init__(self, cache_dir: Path | None = None):
        self.cache_dir: Path | None = cache_dir
        self.registries: dict[str, Registry] = self._create_registries()

    def _create_registries(self) -> dict[str, Registry]:
        return {
            "mal": RegistrySource(
                authority="IEEE",
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
                format=SourceFormat.CSV,
                url="https://standards-oui.ieee.org/oui/oui.csv",
                cache_dir=self.cache_dir,
            ),
            "mam": RegistrySource(
                authority="IEEE",
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
                format=SourceFormat.CSV,
                url="https://standards-oui.ieee.org/oui28/mam.csv",
                cache_dir=self.cache_dir,
            ),
            "mas": RegistrySource(
                authority="IEEE",
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
                format=SourceFormat.CSV,
                url="https://standards-oui.ieee.org/oui36/oui36.csv",
                cache_dir=self.cache_dir,
            ),
            "cid": RegistrySource(
                authority="IEEE",
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
                format=SourceFormat.CSV,
                url="https://standards-oui.ieee.org/cid/cid.csv",
                cache_dir=self.cache_dir,
            ),
            "iab": RegistrySource(
                authority="IEEE",
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
                format=SourceFormat.CSV,
                url="https://standards-oui.ieee.org/iab/iab.csv",
                cache_dir=self.cache_dir,
            ),
            "ethertype": RegistrySource(
                authority="IEEE",
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
                format=SourceFormat.CSV,
                url="https://standards-oui.ieee.org/ethertype/eth.csv",
                cache_dir=self.cache_dir,
            ),
        }

        # "sgma": RegistrySource(
        #     authority="IEEE",
        #     name="SGMA",
        #     model=object,
        #     full_name="Standards Group MAC",
        #     legacy_name=None,
        #     family=RegistryFamily.MAC_REGISTRY,
        #     legacy=False,
        #     description="",
        #     format=SourceFormat.HTML,
        #     url="https://standards.ieee.org/products-programs/regauth/grpmac/public/",
        #     cache_dir=self.cache_dir,
        # ),
        # "iana-ucast": RegistrySource(
        #     authority="IANA",
        #     name="IANA-UCAST",
        #     model=object,
        #     full_name="IANA Unicast MAC Addresses",
        #     legacy_name=None,
        #     family=RegistryFamily.MAC_REGISTRY,
        #     legacy=False,
        #     description=(
        #         "IANA-managed unicast MAC address assignments under the "
        #         "00-00-5E OUI. Includes protocol-specific allocations "
        #         "for VRRP, BFD, TRILL, and other IETF protocols."
        #     ),
        #     format=SourceFormat.CSV,
        #     url="https://www.iana.org/assignments/ethernet-numbers/ethernet-numbers-2.csv",
        #     cache_dir=self.cache_dir,
        #     misc={"static_prefix": "00-00-5E"},
        # ),
        # "iana-mcast": RegistrySource(
        #     authority="IANA",
        #     name="IANA-MCAST",
        #     model=object,
        #     full_name="IANA Multicast MAC Addresses",
        #     legacy_name=None,
        #     family=RegistryFamily.MAC_REGISTRY,
        #     legacy=False,
        #     description=(
        #         "IANA-managed multicast MAC address assignments under the "
        #         "01-00-5E prefix. Includes IPv4 multicast, MPLS multicast, "
        #         "BFD, TRILL, and other IETF protocol-specific assignments."
        #     ),
        #     format=SourceFormat.CSV,
        #     url="https://www.iana.org/assignments/ethernet-numbers/ethernet-numbers-3.csv",
        #     cache_dir=self.cache_dir,
        # ),
        # "iana-ipv4-mcast": RegistrySource(
        #     authority="IANA",
        #     name="IANA-IPV4-MCAST",
        #     model=object,
        #     full_name="IPv4 Multicast Address Space",
        #     legacy_name=None,
        #     family=RegistryFamily.IP_MULTICAST_REGISTRY,
        #     legacy=False,
        #     description=(
        #         "IANA registry of IPv4 multicast group assignments within "
        #         "224.0.0.0/4. Includes routing, discovery, and application "
        #         "protocol multicast groups, which can be mapped to their "
        #         "corresponding Ethernet multicast addresses."
        #     ),
        #     format=SourceFormat.XML,
        #     url="https://www.iana.org/assignments/multicast-addresses/multicast-addresses.xml",
        #     cache_dir=self.cache_dir,
        # ),
        # "iana-ipv6-mcast": RegistrySource(
        #     authority="IANA",
        #     name="IANA-IPV6-MCAST",
        #     model=object,
        #     full_name="IPv6 Multicast Address Space",
        #     legacy_name=None,
        #     family=RegistryFamily.IP_MULTICAST_REGISTRY,
        #     legacy=False,
        #     description=(
        #         "IANA registry of IPv6 multicast group assignments, "
        #         "including protocol-specific groups, scope definitions, "
        #         "and reserved ranges. Supports derivation of corresponding "
        #         "33-33 Ethernet multicast addresses."
        #     ),
        #     format=SourceFormat.XML,
        #     url="https://www.iana.org/assignments/ipv6-multicast-addresses/ipv6-multicast-addresses.xml",
        #     cache_dir=self.cache_dir,
        # ),
        # "wireshark-wka": RegistrySource(
        #     authority="Wireshark",
        #     name="WKA",
        #     model=object,
        #     full_name="Well-Known MAC Addresses",
        #     legacy_name=None,
        #     family=RegistryFamily.MAC_REGISTRY,
        #     legacy=False,
        #     description=(
        #         "Wireshark-maintained collection of well-known MAC addresses "
        #         "and prefixes associated with network protocols, virtual "
        #         "devices, and vendor-specific implementations. Includes "
        #         "HSRP, VRRP, CDP, PVST+, and various legacy protocols."
        #     ),
        #     format=SourceFormat.TSV,
        #     url="https://raw.githubusercontent.com/wireshark/wireshark/master/wka",
        #     cache_dir=self.cache_dir,
        # ),

    def get(self, registry_name: str, require_cache: bool = False) -> Registry:
        registry = self.registries.get(registry_name)

        if registry is None:
            raise KeyError(f"Unknown registry: {registry_name!r}. Choices: {list(self.registries)}")

        if require_cache:
            self.ensure_cache_exists(registry_name)

        return registry

    def get_by_name(self, name: str) -> Registry:
        for registry in self.registries.values():
            if registry.name.casefold() == name.casefold():
                return registry

        raise KeyError(f"Unknown registry: {name!r}")

    def get_all(self, require_cache: bool = False) -> list[Registry]:
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

    def __getitem__(self, key: str) -> Registry:
        return self.registries[key]
