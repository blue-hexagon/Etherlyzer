from pathlib import Path
from typing import TypeVar

import pytest

from etherlyzer import initialize_etherlyzer, EtherlyzerContext
from etherlyzer.domain.entry.mac import MACAllocationEntry
from etherlyzer.infrastructure.index.implementation.identifier import IdentifierIndex
from etherlyzer.infrastructure.registry.cache import RegistryCache
from etherlyzer.infrastructure.registry.downloader import RegistryDownloader
from etherlyzer.infrastructure.registry.family import RegistryFamily
from etherlyzer.infrastructure.registry.registry_source import RegistrySource, SourceFormat

T = TypeVar("T")


@pytest.fixture
def eth_ctx() -> EtherlyzerContext:
    context = initialize_etherlyzer(registry_exemptions=["MA-L", "MA-M", "MA-S", "IAB", "CID"])
    return context


@pytest.fixture
def identifier_index(
) -> IdentifierIndex:
    return eth_ctx().indexes.identifier
