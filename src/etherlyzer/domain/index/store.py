from __future__ import annotations

from dataclasses import dataclass, field

from etherlyzer.domain.index.type.ethertype import EthertypeIndex
from etherlyzer.domain.index.type.identifier import IdentifierIndex
from etherlyzer.domain.index.type.mac_allocation import MACAllocationIndex
from etherlyzer.domain.index.type.vendor import VendorIndex


@dataclass(slots=True)
class IndexStore:
    mac: MACAllocationIndex = field(default_factory=MACAllocationIndex)
    ethertype: EthertypeIndex = field(default_factory=EthertypeIndex)
    identifier: IdentifierIndex = field(default_factory=IdentifierIndex)
    vendor: VendorIndex = field(default_factory=VendorIndex)
