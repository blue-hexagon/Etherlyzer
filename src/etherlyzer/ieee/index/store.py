from __future__ import annotations

from dataclasses import dataclass, field

from etherlyzer.ieee.index.children.ethertype import EthertypeIndex
from etherlyzer.ieee.index.children.identifier import IdentifierIndex
from etherlyzer.ieee.index.children.mac_allocation import MACAllocationIndex
from etherlyzer.ieee.index.children.vendor import VendorIndex


@dataclass(slots=True)
class IndexStore:
    mac: MACAllocationIndex = field(default_factory=MACAllocationIndex)
    ethertype: EthertypeIndex = field(default_factory=EthertypeIndex)
    identifier: IdentifierIndex = field(default_factory=IdentifierIndex)
    vendor: VendorIndex = field(default_factory=VendorIndex)
