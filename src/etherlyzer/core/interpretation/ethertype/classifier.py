import string
from dataclasses import dataclass
from enum import StrEnum

from etherlyzer.domain.entry.ethertype import EtherTypeEntry


class EtherTypeFieldType(StrEnum):
    LENGTH = "IEEE 802.3 Length Field"
    UNDEFINED = "Undefined Length/Type"
    ETHERTYPE = "EtherType"


@dataclass(frozen=True, slots=True)
class EtherTypeStruct:
    normalized: str
    value: int
    field_type: EtherTypeFieldType
    entry: EtherTypeEntry | None = None

    @property
    def assignment(self) -> str:
        return self.normalized

    @property
    def is_ethertype(self) -> bool:
        return self.field_type is EtherTypeFieldType.ETHERTYPE

    @property
    def is_length(self) -> bool:
        return self.field_type is EtherTypeFieldType.LENGTH

    @property
    def is_undefined(self) -> bool:
        return self.field_type is EtherTypeFieldType.UNDEFINED

    @property
    def length_value(self) -> str | None:
        if self.is_length:
            return f"{self.value} bytes"
        return None

    @property
    def has_match(self) -> bool:
        return self.entry is not None

    @property
    def match_status(self) -> str:
        if not self.is_ethertype:
            return "Not Applicable"
        return "Match" if self.has_match else "No Match"

    @property
    def registry(self) -> str | None:
        return self.entry.registry if self.entry else None

    @property
    def description(self) -> str | None:
        return self.entry.protocol if self.entry else None

    @property
    def organization_name(self) -> str | None:
        return self.entry.organization_name if self.entry else None

    @property
    def organization_address(self) -> str | None:
        if self.entry and self.entry.organization_address:
            return self.entry.organization_address.strip()
        return None

    @property
    def requires_oui_pid(self) -> bool:
        return self.value == 0x88B7


def get_ethertype_struct(
    ethertype: str,
    entry: EtherTypeEntry | None = None,
) -> EtherTypeStruct:
    normalized = ethertype.strip()

    if normalized.lower().startswith("0x"):
        normalized = normalized[2:]

    if len(normalized) != 4 or any(c not in string.hexdigits for c in normalized):
        raise ValueError(f"Expected a 16-bit hexadecimal value: {ethertype!r}")

    normalized = normalized.upper()
    value = int(normalized, 16)

    if value <= 0x05DC:
        field_type = EtherTypeFieldType.LENGTH
    elif value < 0x0600:
        field_type = EtherTypeFieldType.UNDEFINED
    else:
        field_type = EtherTypeFieldType.ETHERTYPE

    if entry is not None:
        if field_type is not EtherTypeFieldType.ETHERTYPE:
            raise ValueError("Registry entry provided for a non-EtherType value.")

        registered = entry.assignment.upper().removeprefix("0X")
        if registered != normalized:
            raise ValueError("Registry assignment does not match the supplied EtherType.")

    return EtherTypeStruct(
        normalized=normalized,
        value=value,
        field_type=field_type,
        entry=entry,
    )
