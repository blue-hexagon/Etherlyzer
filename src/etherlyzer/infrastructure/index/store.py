from __future__ import annotations

from dataclasses import dataclass, field

from etherlyzer.infrastructure.index.implementation.ethertype import EthertypeIndex
from etherlyzer.infrastructure.index.implementation.identifier import IdentifierIndex
from etherlyzer.infrastructure.index.implementation.mac_allocation import MACAllocationIndex
from etherlyzer.infrastructure.index.implementation.vendor import VendorIndex


@dataclass(slots=True)
class IndexStore:
    mac: MACAllocationIndex = field(default_factory=MACAllocationIndex)
    ethertype: EthertypeIndex = field(default_factory=EthertypeIndex)
    identifier: IdentifierIndex = field(default_factory=IdentifierIndex)
    vendor: VendorIndex = field(default_factory=VendorIndex)
