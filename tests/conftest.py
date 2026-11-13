import pytest

from etherlyzer.infrastructure.registry.provider import RegistryProvider


@pytest.fixture
def registry() -> RegistryProvider:
    provider = RegistryProvider()
    return provider
