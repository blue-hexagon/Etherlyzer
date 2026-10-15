import re
from collections.abc import Generator, Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol, TypeVar

from etherlyzer.ieee.entry.ethertype import EtherTypeEntry
from etherlyzer.ieee.entry.mac import MACAllocationEntry
from etherlyzer.ieee.ieee_registry import IEEERegistry
from etherlyzer.ieee.registry.category import RegistryCategory

HEX_DIGITS = frozenset("0123456789ABCDEF")

T = TypeVar("T")


class IEEEIndexProtocol(Protocol):
    def get_many(self, identifier: str) -> list[MACAllocationEntry | EtherTypeEntry] | None: ...
    def get_one(self, identifier: str) -> MACAllocationEntry | EtherTypeEntry | None: ...


@dataclass(slots=True)
class MACAllocationIndex(IEEEIndexProtocol):
    prefixes_36: dict[str, MACAllocationEntry] = field(default_factory=dict)
    prefixes_28: dict[str, MACAllocationEntry] = field(default_factory=dict)
    prefixes_24: dict[str, MACAllocationEntry] = field(default_factory=dict)

    def insert(self, registry: IEEERegistry, entries: Iterable[MACAllocationEntry]) -> None:
        match registry.prefix_bits:
            case 36:
                target = self.prefixes_36
            case 28:
                target = self.prefixes_28
            case 24:
                target = self.prefixes_24
            case _:
                raise ValueError(f"Unsupported prefix length: {registry.prefix_bits}")

        target.update({entry.assignment.upper(): entry for entry in entries})

    def get_one(self, identifier: str) -> MACAllocationEntry | None:
        mac = "".join(c for c in identifier.upper() if c in HEX_DIGITS)

        # Order is important - longest prefix match
        return (
            self.prefixes_36.get(mac[:9])
            or self.prefixes_28.get(mac[:7])
            or self.prefixes_24.get(mac[:6])
        )

    def walk(self) -> Generator[str]:
        yield from self.prefixes_36
        yield from self.prefixes_28
        yield from self.prefixes_24


@dataclass(slots=True)
class VendorIndex(IEEEIndexProtocol):
    vendors: dict[str, list[MACAllocationEntry]] = field(default_factory=dict)

    @staticmethod
    def normalize_vendor_name(name: str) -> str:
        name = name.casefold()
        name = re.sub(r"[.,/\\()\-_'\"&]+", " ", name)
        name = re.sub(r"\s+", " ", name)
        return name.strip()

    def insert(self, entry: MACAllocationEntry) -> None:
        key = self.normalize_vendor_name(
            entry.organization_name,
        )
        self.vendors.setdefault(key, []).append(entry)

    def get_many(self, identifier: str) -> list[MACAllocationEntry] | None:
        ieee_mac_entries = self.vendors.get(
            self.normalize_vendor_name(identifier),
        )
        if ieee_mac_entries is not None:
            ieee_mac_entries.sort(
                key=lambda entry: int(
                    "".join(c for c in entry.assignment if c in "0123456789ABCDEFabcdef"),
                    16,
                )
            )
        return ieee_mac_entries


@dataclass(slots=True)
class ProtocolIndex(IEEEIndexProtocol):
    ethertype: dict[str, EtherTypeEntry] = field(default_factory=dict)

    def insert(
        self,
        entries: Iterable[EtherTypeEntry],
    ) -> None:
        self.ethertype.update({entry.assignment.upper(): entry for entry in entries})

    def get_one(self, identifier: str) -> EtherTypeEntry | None:
        ethertype = "".join(c for c in identifier.upper() if c in HEX_DIGITS)
        return self.ethertype.get(ethertype)


@dataclass(slots=True)
class IdentifierIndex(IEEEIndexProtocol):
    cid: dict[str, MACAllocationEntry] = field(default_factory=dict)
    opid: dict[str, MACAllocationEntry] = field(default_factory=dict)
    manid: dict[str, MACAllocationEntry] = field(default_factory=dict)

    def insert(self, registry: IEEERegistry, entries: Iterable[MACAllocationEntry]) -> None:
        match registry.name:
            case "CID":
                target = self.cid
            case "OPID":
                target = self.opid
            case "MANID":
                target = self.manid
            case _:
                raise ValueError(f"Unsupported identifier registry: {registry.name}")

        target.update({entry.assignment.upper(): entry for entry in entries})

    def get_one(self, identifier: str) -> MACAllocationEntry | None:
        identifier = identifier.upper()
        return self.cid.get(identifier) or self.opid.get(identifier) or self.manid.get(identifier)


@dataclass(slots=True)
class IEEEIndex:
    mac_index: MACAllocationIndex = field(default_factory=MACAllocationIndex)
    protocol_index: ProtocolIndex = field(default_factory=ProtocolIndex)
    identifier_index: IdentifierIndex = field(default_factory=IdentifierIndex)
    vendor_index: VendorIndex = field(default_factory=VendorIndex)

    @classmethod
    def from_registries(
        cls,
        registries: Iterable[IEEERegistry],
    ) -> IEEEIndex:

        index = cls()

        for registry in registries:
            entries = registry.load()

            match registry.category:
                case RegistryCategory.MAC_REGISTRY:
                    index.mac_index.insert(registry, entries)

                case RegistryCategory.PROTOCOL_REGISTRY:
                    index.protocol_index.insert(entries)

                case RegistryCategory.IDENTIFIER_REGISTRY:
                    index.identifier_index.insert(registry, entries)

                case _:
                    raise ValueError(f"Unsupported registry category: {registry.category}")
        mac_walker = index.mac_index.walk()
        v_index = VendorIndex()

        while True:
            try:
                entry = index.get_from_mac_index(next(mac_walker))
                if entry is not None:
                    v_index.insert(entry)
            except StopIteration:
                break
        index.vendor_index = v_index
        return index

    def get_from_mac_index(self, mac: str) -> MACAllocationEntry | None:
        return self.mac_index.get_one(mac)

    def get_from_ethertype_index(self, ethertype: str) -> EtherTypeEntry | None:
        ret = self.protocol_index.get_one(ethertype)
        if not isinstance(ret, EtherTypeEntry):
            raise RuntimeError()
        return ret

    def get_identifier(self, identifier: str) -> MACAllocationEntry | None:
        return self.identifier_index.get_one(identifier)

    @staticmethod
    def get_many(
        ieee_index: MACAllocationIndex | IdentifierIndex | ProtocolIndex | VendorIndex,
        path_or_text: Path | str | list[str],
    ) -> list[MACAllocationEntry]:
        # Pass a list[str] from interactive or pass a Path or str (path)
        ieee_entries_as_set: set[MACAllocationEntry] = set()

        if isinstance(path_or_text, Path):
            with open(path_or_text) as f:
                text_data = f.readlines()
        else:
            text_data = path_or_text
        for line in text_data:
            ieee_entry = ieee_index.get_one(line)
            if ieee_entry:
                ieee_entries_as_set.add(ieee_entry)

        ieee_entries: list[MACAllocationEntry] = list(ieee_entries_as_set)
        # Sort by name, and then by registry-name reversed
        ieee_entries = sorted(ieee_entries, key=lambda e: e.organization_name)
        ieee_entries = sorted(ieee_entries, key=lambda e: e.registry, reverse=True)

        return ieee_entries

    @staticmethod
    def get_single(
        indextype: VendorIndex | MACAllocationIndex | IdentifierIndex | ProtocolIndex, mac: str
    ) -> MACAllocationEntry | list[MACAllocationEntry] | None:
        ieee_entry = indextype.get_one(mac)
        if ieee_entry:
            return ieee_entry
        else:
            return None
