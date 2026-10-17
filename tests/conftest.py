import pytest

from etherlyzer.ieee.registry.catalog import Catalog


@pytest.fixture
def registry() -> Catalog | None:
    if Catalog.db_is_initialized():
        return Catalog
    return None
