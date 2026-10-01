from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import TypeVar

import etherlyzer.misc.dirs as pathman
from etherlyzer.misc.settings import config
from etherlyzer.ieee.registry import EtherTypeEntry, IEEEEntry, IEEERegistry, RegistryCategory

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
class RegistryIndex:
    mac_index: MACIndex = field(default_factory=MACIndex)
    protocol_index: ProtocolIndex = field(default_factory=ProtocolIndex)
    identifier_index: IdentifierIndex = field(default_factory=IdentifierIndex)

    @classmethod
    def from_registries(
            cls,
            registries: Iterable[IEEERegistry],
    ) -> RegistryIndex:

        index = cls()

        for registry in registries:
            entries = registry.load()

            match registry.category:
                case RegistryCategory.MAC:
                    index.mac_index.insert(registry, entries)

                case RegistryCategory.PROTOCOL:
                    index.protocol_index.insert(registry, entries)

                case RegistryCategory.IDENTIFIER:
                    index.identifier_index.insert(registry, entries)

                case _:
                    raise ValueError(f"Unsupported registry category: {registry.category}")

        return index

    def lookup_mac(self, mac: str) -> IEEEEntry | None:
        return self.mac_index.lookup(mac)

    def lookup_ethertype(self, ethertype: str) -> EtherTypeEntry | None:
        return self.protocol_index.lookup(ethertype)

    def lookup_identifier(self, identifier: str) -> IEEEEntry | None:
        return self.identifier_index.lookup(identifier)

    @staticmethod
    def lookup_bulk_from_file(
            indextype: MACIndex | IdentifierIndex | ProtocolIndex,
            stream: Path | str | list[str],
    ) -> list[IEEEEntry]:
        # Pass a list[str] from interactive or pass a Path|str`Path`
        if not isinstance(stream, list):
            with open(stream) as f:
                macdata = f.readlines()
        else:
            macdata = stream
        entries: set[IEEEEntry] = set()
        for line in macdata:
            ieee_entry = indextype.lookup(line)
            if ieee_entry:
                entries.add(ieee_entry)

        entries: list[IEEEEntry] = list(entries)
        # Sort by name, and then by registry-name reversed
        entries = sorted(entries, key=lambda e: e.organization_name)
        entries = sorted(entries, key=lambda e: e.registry, reverse=True)

        return entries

    @staticmethod
    def lookup_single_from_console(indextype: MACIndex | IdentifierIndex | ProtocolIndex, mac: str):
        ieee_entry = indextype.lookup(mac)
        if ieee_entry:
            return ieee_entry
        else:
            return None
