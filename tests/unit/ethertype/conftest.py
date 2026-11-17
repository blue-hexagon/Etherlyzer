import pytest

from etherlyzer.bootstrap import EtherlyzerContext, initialize_etherlyzer
from etherlyzer.infrastructure.index.implementation.identifier import IdentifierIndex


@pytest.fixture
def eth_ctx() -> EtherlyzerContext:
    context = initialize_etherlyzer(registry_exemptions=["MA-L", "MA-M", "MA-S", "IAB", "CID"])
    return context


@pytest.fixture
def identifier_index(eth_ctx: EtherlyzerContext) -> IdentifierIndex:
    return eth_ctx.indexes.identifier
