import re
import string
from dataclasses import dataclass

from etherlyzer.ieee.entry.base import BaseEntry
from etherlyzer.lib.normalization import normalize


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


@dataclass(frozen=True, slots=True)
class MACLookupResult:
    line_number: int
    mac: str
    entry: MACAllocationEntry | None = None
    reason: str | None = None


def classify_mac(mac: str) -> str | None:
    normalized = normalize(mac)

    if len(normalized) != 12 or any(c not in string.hexdigits for c in normalized):
        return "Invalid format"

    first_octet = int(normalized[:2], 16)

    is_group = bool(first_octet & 0x01)
    is_local = bool(first_octet & 0x02)

    if not (is_group or is_local):
        return None

    administration = "Local" if is_local else "Universal"
    delivery = "Multicast" if is_group else "Unicast"

    return f"{administration} {delivery}"
