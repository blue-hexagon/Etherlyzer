from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import TypeVar

from etherlyzer.ieee.registry import RegCategory, IEEEEntry, EtherTypeEntry, IEEERegistry

HEX_DIGITS = frozenset("0123456789ABCDEF")

T = TypeVar("T")


@dataclass(slots=True)
class MACIndex:
    prefixes_36: dict[str, IEEEEntry] = field(default_factory=dict)
    prefixes_28: dict[str, IEEEEntry] = field(default_factory=dict)
    prefixes_24: dict[str, IEEEEntry] = field(default_factory=dict)

    def insert(self, registry: IEEERegistry, entries: Iterable[IEEEEntry]) -> None:
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

    def lookup(self, mac: str) -> IEEEEntry | None:
        mac = "".join(c for c in mac.upper() if c in HEX_DIGITS)

        # Order is important - longest prefix match
        return (
                self.prefixes_36.get(mac[:9])
                or self.prefixes_28.get(mac[:7])
                or self.prefixes_24.get(mac[:6])
        )


@dataclass(slots=True)
class ProtocolIndex:
    ethertype: dict[str, EtherTypeEntry] = field(default_factory=dict)

    def insert(
            self,
            registry: IEEERegistry,
            entries: Iterable[EtherTypeEntry],
    ) -> None:
        self.ethertype.update({entry.assignment.upper(): entry for entry in entries})

    def lookup(self, ethertype: str) -> EtherTypeEntry | None:
        ethertype = "".join(c for c in ethertype.upper() if c in HEX_DIGITS)
        return self.ethertype.get(ethertype)


@dataclass(slots=True)
class IdentifierIndex:
    cid: dict[str, IEEEEntry] = field(default_factory=dict)
    opid: dict[str, IEEEEntry] = field(default_factory=dict)
    manid: dict[str, IEEEEntry] = field(default_factory=dict)

    def insert(self, registry: IEEERegistry, entries: Iterable[IEEEEntry]) -> None:
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

    def lookup(self, identifier: str) -> IEEEEntry | None:
        identifier = identifier.upper()

        return self.cid.get(identifier) or self.opid.get(identifier) or self.manid.get(identifier)


@dataclass(slots=True)
class IEEEIndex:
    mac_index: MACIndex = field(default_factory=MACIndex)
    protocol_index: ProtocolIndex = field(default_factory=ProtocolIndex)
    identifier_index: IdentifierIndex = field(default_factory=IdentifierIndex)

    @classmethod
    def from_registries(
            cls,
            registries: Iterable[IEEERegistry],
    ) -> IEEEIndex:

        index = cls()

        for registry in registries:
            entries = registry.load()

            match registry.category:
                case RegCategory.MAC:
                    index.mac_index.insert(registry, entries)

                case RegCategory.PROTOCOL:
                    index.protocol_index.insert(registry, entries)

                case RegCategory.IDENTIFIER:
                    index.identifier_index.insert(registry, entries)

                case _:
                    raise ValueError(f"Unsupported registry category: {registry.category}")

        return index

    def get_from_mac_index(self, mac: str) -> IEEEEntry | None:
        return self.mac_index.lookup(mac)

    def get_from_ethertype_index(self, ethertype: str) -> EtherTypeEntry | None:
        return self.protocol_index.lookup(ethertype)

    def get_identifier(self, identifier: str) -> IEEEEntry | None:
        return self.identifier_index.lookup(identifier)

    @staticmethod
    def get_bulk(
            ieee_index: MACIndex | IdentifierIndex | ProtocolIndex,
            path_or_text: Path | list[str],
    ) -> list[IEEEEntry]:
        # Pass a list[str] from interactive or pass a Path
        if isinstance(path_or_text, Path):
            with open(path_or_text) as f:
                text_data = f.readlines()
        else:
            text_data = path_or_text
        ieee_entries: set[IEEEEntry] = set()
        for line in text_data:
            ieee_entry = ieee_index.lookup(line)
            if ieee_entry:
                ieee_entries.add(ieee_entry)

        ieee_entries: list[IEEEEntry] = list(ieee_entries)
        # Sort by name, and then by registry-name reversed
        ieee_entries = sorted(ieee_entries, key=lambda e: e.organization_name)
        ieee_entries = sorted(ieee_entries, key=lambda e: e.registry, reverse=True)

        return ieee_entries

    @staticmethod
    def get_single(indextype: MACIndex | IdentifierIndex | ProtocolIndex, mac: str):
        ieee_entry = indextype.lookup(mac)
        if ieee_entry:
            return ieee_entry
        else:
            return None
