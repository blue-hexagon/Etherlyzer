from pathlib import Path
from typing import TypeVar

import pytest

from etherlyzer.domain.entry.mac import MACAllocationEntry
from etherlyzer.domain.registry.cache import RegistryCache
from etherlyzer.domain.registry.downloader import RegistryDownloader
from etherlyzer.domain.registry.family import RegistryFamily
from etherlyzer.domain.registry.ieee_registry import RegistrySource, SourceFormat

T = TypeVar("T")


@pytest.fixture
def ieee_registry(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> RegistrySource[T]:
    # Redirect registry files to pytest's temporary directory.
    monkeypatch.setattr(
        "etherlyzer.ieee.registry.cache.DEFAULT_CACHE_DIR",
        tmp_path,
    )

    return RegistrySource(
        name="MA-L",
        model=MACAllocationEntry,
        full_name="Test IEEE Registry",
        url="https://example.com/registry.csv",
        family=RegistryFamily.MAC_REGISTRY,
        legacy=False,
        description="Testing Registry",
        authority="IEEE",
        format=SourceFormat.CSV,
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
