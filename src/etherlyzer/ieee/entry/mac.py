import re
from dataclasses import dataclass

from etherlyzer.ieee.entry.base import BaseEntry


@dataclass(frozen=True, slots=True)
class MACAllocationEntry(BaseEntry):
    registry: str
    assignment: str
    organization_name: str
    organization_address: str

    def registry_id(self) -> str:
        """Instead of MA-L, MA-M, then MAL, MAM, IAB"""
        return self.registry.replace("-", "")[2:]

    def short_name(self) -> str:
        """Get the proper organization name by removing identifiers such as Co, Ltd."""
        return re.sub(r"(,.*|Co.*)$", "", self.organization_name).strip()

    def format_vendor_address(self) -> list[str]:
        """Format the vendors registered compnay address"""
        addr_representation = []
        for addr_outer in self.organization_address.split(","):
            addr = addr_outer.split("  ")
            for line in addr:
                if line:
                    addr_representation.append(line.strip())
        return addr_representation
