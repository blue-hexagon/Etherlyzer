from pathlib import Path

import pytest

from etherlyzer.ieee.entry.mac import MACAllocationEntry
from etherlyzer.ieee.registry.cache import RegistryCache
from etherlyzer.ieee.registry.category import RegistryCategory
from etherlyzer.ieee.registry.downloader import RegistryDownloader
from etherlyzer.ieee.registry.ieee_registry import IEEERegistry


@pytest.fixture
def ieee_registry(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> IEEERegistry:
    # Redirect registry files to pytest's temporary directory.
    monkeypatch.setattr(
        "etherlyzer.ieee.registry.cache.DEFAULT_CACHE_DIR",
        tmp_path,
    )

    return IEEERegistry(
        enabled=True,
        name="MA-L",
        model=MACAllocationEntry,
        full_name="Test IEEE Registry",
        url="https://example.com/registry.csv",
        category=RegistryCategory.MAC_REGISTRY,
        legacy=False,
        description="Testing Registry",
    )


@pytest.fixture
def registry_cache(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> RegistryCache:
    monkeypatch.setattr(
        "etherlyzer.ieee.registry.cache.DEFAULT_CACHE_DIR",
        tmp_path,
    )

    return RegistryCache(name="MA-L")


@pytest.fixture
def registry_downloader(
    registry_cache: RegistryCache,
) -> RegistryDownloader:
    return RegistryDownloader(
        url="https://example.com/registry.csv",
        name="MA-L",
        cache=registry_cache,
    )
