from dataclasses import dataclass, field
from pathlib import Path

from etherlyzer.ieee.registry.cache import RegistryCache
from etherlyzer.ieee.registry.category import RegistryCategory
from etherlyzer.ieee.registry.downloader import RegistryDownloader
from etherlyzer.ieee.registry.parser import RegistryParser


@dataclass
class IEEERegistry[T]:
    """
    Metadata describing an IEEE Registration Authority registry.
    """

    enabled: bool
    name: str
    model: type[T]
    full_name: str
    url: str

    category: RegistryCategory

    legacy: bool

    description: str = ""

    legacy_name: str | None = None

    prefix_bits: int | None = None
    address_bits: int | None = None
    address_count: int | None = None

    cache_dir: Path | None = None

    registry_cache: RegistryCache = field(init=False)
    registry_downloader: RegistryDownloader = field(init=False)
    registry_parser: RegistryParser = field(default_factory=RegistryParser)

    def __post_init__(self):
        self.registry_cache = RegistryCache(
            name=self.name,
            cache_dir=self.cache_dir,
        )
        self.registry_downloader = RegistryDownloader(
            url=self.url, name=self.name, cache=self.registry_cache
        )

    def load(self) -> list[T]:
        if not self.registry_cache.filepath.is_file():
            raise FileNotFoundError(f"Missing registry cache: {self.registry_cache.filepath}")

        return self.registry_parser.load_file(
            self.registry_cache.filepath,
            self.model,
        )

    @property
    def is_mac_registry(self) -> bool:
        return self.category is RegistryCategory.MAC_REGISTRY

    @property
    def is_protocol_registry(self) -> bool:
        return self.category is RegistryCategory.ETHERTYPE_REGISTRY

    @property
    def is_identifier_registry(self) -> bool:
        return self.category is RegistryCategory.IDENTIFIER_REGISTRY

    @property
    def assignment_length(self) -> int:
        return self.prefix_bits // 4 if self.prefix_bits else 0
