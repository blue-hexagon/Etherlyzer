import pytest

from etherlyzer.ieee.catalog import Catalog


@pytest.fixture
def registry():
    if Catalog.db_is_initialized():
        return Catalog
