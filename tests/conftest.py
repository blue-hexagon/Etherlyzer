import pytest

from etherlyzer.ieee.registry.provider import RegistryProvider


@pytest.fixture
def registry() -> RegistryProvider:
    provider = RegistryProvider()
    return provider
