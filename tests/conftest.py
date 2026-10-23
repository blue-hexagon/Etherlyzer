import pytest

from etherlyzer.ieee.registry.provider import RegistryProvider


@pytest.fixture
def registry() -> RegistryProvider | None:
    if RegistryProvider.all_caches_exist():
        return RegistryProvider
    return None
