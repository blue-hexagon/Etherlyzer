from dataclasses import dataclass

from etherlyzer.ieee.entry.mac import MACAllocationEntry


@dataclass(frozen=True, slots=True)
class EtherTypeEntry(MACAllocationEntry):
    protocol: str
