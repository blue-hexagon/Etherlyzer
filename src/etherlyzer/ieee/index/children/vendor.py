from __future__ import annotations

import re
from dataclasses import dataclass, field

from etherlyzer.ieee.entry.mac import MACAllocationEntry
from etherlyzer.ieee.index.children.proto import IndexService


def normalize_vendor_name(name: str) -> str:
    name = name.casefold()
    name = re.sub(r"[.,/\\()\-_'\"&]+", " ", name)
    name = re.sub(r"\s+", " ", name)
    return name.strip()


@dataclass(slots=True)
class VendorIndex(IndexService):
    vendors: dict[str, list[MACAllocationEntry]] = field(default_factory=dict)

    def insert(self, entry: MACAllocationEntry) -> None:
        key = normalize_vendor_name(
            entry.organization_name,
        )
        self.vendors.setdefault(key, []).append(entry)

    def lookup_many(self, identifier: str) -> list[MACAllocationEntry] | None:
        ieee_mac_entries = self.vendors.get(
            normalize_vendor_name(identifier),
        )
        if ieee_mac_entries is not None:
            ieee_mac_entries.sort(
                key=lambda entry: int(
                    "".join(c for c in entry.assignment if c in "0123456789ABCDEFabcdef"),
                    16,
                )
            )
        return ieee_mac_entries
