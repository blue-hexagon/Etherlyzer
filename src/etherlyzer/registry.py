import datetime
from dataclasses import astuple, dataclass, fields
from enum import StrEnum
from pathlib import Path

import requests
from requests import ConnectTimeout

from etherlyzer.configuration import config
from etherlyzer.importer import CSVImporter
from etherlyzer.dirs import DATA_ROOT


class RegistryCategory(StrEnum):
    MAC = "mac"
    PROTOCOL = "protocol"
    IDENTIFIER = "identifier"


@dataclass(frozen=True, slots=True)
class BaseEntry:
    @classmethod
    def get_header(cls) -> list[str]:
        return [f.name for f in fields(cls)]

    def get_row(self) -> tuple:
        return astuple(self)

    def __hash__(self):
        return hash(astuple(self))


@dataclass(frozen=True, slots=True)
class IEEEEntry(BaseEntry):
    registry: str
    assignment: str
    organization_name: str
    organization_address: str


@dataclass(frozen=True, slots=True)
class EtherTypeEntry(IEEEEntry):
    protocol: str


@dataclass(slots=True)
class IEEERegistry:
    """
    Metadata describing an IEEE Registration Authority registry.
    """

    enabled: bool
    name: str
    model: type[IEEEEntry] | type[EtherTypeEntry]
    full_name: str
    url: str

    description: str = ""

    category: RegistryCategory = RegistryCategory.IDENTIFIER

    legacy_name: str | None = None

    prefix_bits: int | None = None
    address_bits: int | None = None
    address_count: int | None = None

    legacy: bool = False

    update_interval: datetime.timedelta = datetime.timedelta(days=1)
    last_retrieved: datetime.datetime = None  # noqa; set in post-init

    def __post_init__(self):
        # Check that filepath exists
        # Get file mod ts if, else set to 0.0 (epoch zero)
        # Modify stateful variable that is used later to ensure a (recent) copy exists.
        f_mod_ts = self.filepath.stat().st_mtime if self.filepath.exists() else 0.0
        self.last_retrieved = datetime.datetime.fromtimestamp(
            f_mod_ts,
            tz=datetime.UTC,
        )

    @property
    def is_mac_registry(self) -> bool:
        return self.category is RegistryCategory.MAC

    @property
    def is_protocol_registry(self) -> bool:
        return self.category is RegistryCategory.PROTOCOL

    @property
    def is_identifier_registry(self) -> bool:
        return self.category is RegistryCategory.IDENTIFIER

    @property
    def filepath(self) -> Path:
        return DATA_ROOT / Path("".join([self.name, ".csv"]))

    @property
    def assignment_length(self) -> int:
        return self.prefix_bits // 4 if self.prefix_bits else 0

    @staticmethod
    def req_headers() -> dict[str, str]:
        return {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/137.0.0.0 Safari/537.36"
            )
        }

    def load(self):
        if not self.filepath.exists():
            self.save()
        return CSVImporter.load(self.filepath, self.model)

    def need_updates(self):
        expires = self.last_retrieved + self.update_interval
        expires_humanized = expires.replace(microsecond=0)
        now = datetime.datetime.now(datetime.UTC)
        f_not_exists = not self.filepath.exists()

        if f_not_exists and config.show_sync_messages:
            print(f"Cache for {self.name} not found.")
        elif expires <= now and config.show_sync_messages:
            print(f"Cache for {self.name} has expired.")
        elif config.show_sync_messages:
            print(f"Cache for {self.name} expires at: {expires_humanized} UTC")

        return f_not_exists or expires <= now

    def save(self) -> bool | None:
        times = 1
        max = 3
        res = None
        loop = True
        while loop and times <= max:
            try:
                if config.show_sync_messages:
                    print(f"Saving Registry: {self.name}")
                res = requests.get(headers=self.req_headers(), url=self.url, timeout=20)
                res.raise_for_status()
                loop = False
            except ConnectTimeout:
                if config.show_sync_messages:
                    print(f"Request timed out on {times}. attempt out of {max} attempts.")
                times += 1
                if times == max + 1:
                    print(f"Unable to retrieve the registry '{self.name}' from {self.url}. Maximum attempts exceeded.")
                    return False
        with open(self.filepath, "w", encoding="utf-8", newline="") as f:
            f.write(res.content.decode("utf-8"))
        return None


class Registry:
    IEEE_REGISTRIES = {  # noqa
        "mal": IEEERegistry(
            enabled=True,
            name="MA-L",
            model=IEEEEntry,
            full_name="MAC Address Block Large",
            legacy_name="OUI",
            category=RegistryCategory.MAC,
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
            model=IEEEEntry,
            full_name="MAC Address Block Medium",
            legacy_name="OUI-28",
            category=RegistryCategory.MAC,
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
            model=IEEEEntry,
            full_name="MAC Address Block Small",
            legacy_name="OUI-36",
            category=RegistryCategory.MAC,
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
        "manid": IEEERegistry(
            enabled=False,
            name="MANID",
            model=IEEEEntry,
            full_name="Manufacturer Identifier",
            legacy_name=None,
            category=RegistryCategory.IDENTIFIER,
            legacy=False,
            description=(
                "Manufacturer identifier registry maintained by the IEEE "
                "Registration Authority. Used to uniquely identify "
                "manufacturers rather than allocating MAC addresses."
            ),
            url="https://standards-oui.ieee.org/manid/manid.csv",
        ),
        "opid": IEEERegistry(
            enabled=False,
            name="OPID",
            model=IEEEEntry,
            full_name="OUI-based Protocol Identifier",
            legacy_name=None,
            category=RegistryCategory.IDENTIFIER,
            legacy=False,
            description=(
                "Registry of protocol identifiers based on IEEE-assigned "
                "organizational identifiers. Used by vendor-specific and "
                "IEEE protocols."
            ),
            url="https://standards-oui.ieee.org/bopid/opid.csv",
        ),
        "cid": IEEERegistry(
            enabled=False,
            name="CID",
            model=IEEEEntry,
            full_name="Company Identifier",
            legacy_name=None,
            category=RegistryCategory.IDENTIFIER,
            legacy=False,
            description=(
                "Unique company identifiers assigned by IEEE. Identifies "
                "organizations independently of MAC address allocations."
            ),
            url="https://standards-oui.ieee.org/cid/cid.csv",
        ),
        "iab": IEEERegistry(
            enabled=False,
            name="IAB",
            model=IEEEEntry,
            full_name="Individual Address Block",
            legacy_name=None,
            category=RegistryCategory.MAC,
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
            category=RegistryCategory.PROTOCOL,
            legacy=False,
            description=(
                "Registry mapping EtherType values to Ethernet protocols, "
                "including IPv4, IPv6, ARP, VLAN tagging, LLDP, MPLS, "
                "802.1X, and many vendor-specific protocols."
            ),
            url="https://standards-oui.ieee.org/ethertype/eth.csv",
        ),
    }

    @staticmethod
    def get_registry(name: str) -> IEEERegistry | None:
        return Registry.IEEE_REGISTRIES.get(name, None)

    def get_registries(self, update=True) -> list[IEEERegistry]:
        for registry in self.IEEE_REGISTRIES.values():
            if update and registry.need_updates():

                status = registry.save()
                if status is False:
                    break
        return list(self.IEEE_REGISTRIES.values())

    def __getitem__(self, key):
        return self.IEEE_REGISTRIES[key]
