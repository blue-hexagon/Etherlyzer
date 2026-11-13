import pytest

from etherlyzer.domain.registry.provider import RegistryProvider


@pytest.fixture
def registry() -> RegistryProvider:
    provider = RegistryProvider()
    return provider
