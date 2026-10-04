import datetime
from dataclasses import dataclass, fields, astuple
from enum import StrEnum
from pathlib import Path

import requests
from requests import RequestException
from tqdm import tqdm

from etherlyzer.ieee.csv_parser import IEEERegistryReader
from etherlyzer.util.dirs import DATA_PLATFORM_DIR
from etherlyzer.util.knobs import etherlyzer_knobs


class RegCategory(StrEnum):
    MAC = "mac"  # IAB, MA-L, MA-M, MA-S
    PROTOCOL = "protocol"  # Ethertype
    IDENTIFIER = "identifier"  # CID


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

    category: RegCategory

    legacy: bool

    description: str = ""

    legacy_name: str | None = None

    prefix_bits: int | None = None
    address_bits: int | None = None
    address_count: int | None = None

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
        return self.category is RegCategory.MAC

    @property
    def is_protocol_registry(self) -> bool:
        return self.category is RegCategory.PROTOCOL

    @property
    def is_identifier_registry(self) -> bool:
        return self.category is RegCategory.IDENTIFIER

    @property
    def filepath(self) -> Path:
        return DATA_PLATFORM_DIR / Path("".join([self.name, ".csv"]))

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
        return IEEERegistryReader.load(self.filepath, self.model)

    def need_updates(self, inform_if_synced_about_expiration=False):
        expires = self.last_retrieved + self.update_interval
        expires_humanized = expires.replace(microsecond=0)
        now = datetime.datetime.now(datetime.UTC)
        f_not_exists = not self.filepath.exists()

        if f_not_exists and etherlyzer_knobs.show_sync_messages:
            print(f"Cache for {self.name} not found.")
        elif expires <= now and etherlyzer_knobs.show_sync_messages:
            print(f"Cache for {self.name} has expired.")
        elif etherlyzer_knobs.show_sync_messages and inform_if_synced_about_expiration:
            namelen = len("EtherType") - len(self.name)
            print(f"Cache for {self.name} expires at: {' '*namelen} {expires_humanized} UTC")

        return f_not_exists or expires <= now

    def save(self) -> bool | None:
        attempts = 1
        max_attempts = 3

        while attempts <= max_attempts:
            try:
                if etherlyzer_knobs.show_sync_messages:
                    print(f"Saving Registry: {self.name}")

                res = requests.get(
                    headers=self.req_headers(),
                    url=self.url,
                    timeout=20,
                    stream=True,
                )
                res.raise_for_status()

                total_size = int(res.headers.get("content-length", 0)) or None

                with open(self.filepath, "wb") as f:
                    with tqdm(
                            total=total_size or None,
                            unit="B",
                            unit_scale=True,
                            unit_divisor=1024,
                            desc=f"Saving {self.name}",
                            disable=not etherlyzer_knobs.show_sync_messages,
                    ) as progress:
                        for chunk in res.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                progress.update(len(chunk))

                return None

            except RequestException as exc:
                if etherlyzer_knobs.show_sync_messages:
                    print(
                        f"Request timed out on attempt "
                        f"{attempts} of {max_attempts}."
                    )

                attempts += 1

        print(
            f"Unable to retrieve the registry '{self.name}' "
            f"from {self.url}. Maximum attempts exceeded."
        )

        return False
