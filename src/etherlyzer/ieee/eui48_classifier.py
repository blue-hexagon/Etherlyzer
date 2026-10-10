from dataclasses import dataclass
from enum import StrEnum


class Administration(StrEnum):
    UNIVERSAL = "Universal"
    LOCAL = "Local"


class DeliveryType(StrEnum):
    INDIVIDUAL = "Individual"
    GROUP = "Group"


class SLAPQuadrant(StrEnum):
    AAI = "Administratively Assigned (AAI)"
    ELI = "Extended Local (ELI)"
    RESERVED = "Reserved"
    SAI = "Standard Assigned (SAI)"


@dataclass(frozen=True, slots=True)
class MACClassification:
    administration: Administration
    delivery: DeliveryType
    is_broadcast: bool
    is_zero: bool
    slap_quadrant: SLAPQuadrant | None


def classify_mac(mac: str) -> MACClassification:
    normalized = mac.replace(":", "").replace("-", "")

    if not normalized or len(normalized) > 12:
        raise ValueError("Expected a MAC address of 1–12 hexadecimal digits")

    if not all(c in "0123456789abcdefABCDEF" for c in normalized):
        raise ValueError("Invalid hexadecimal MAC address")

    normalized = normalized.ljust(12, "0")
    mac_int = int(normalized, 16)

    first = mac_int >> 40

    is_local = bool(first & 0x02)
    is_group = bool(first & 0x01)

    quadrant = None

    if is_local and not is_group:
        quadrant = {
            0x00: SLAPQuadrant.AAI,
            0x08: SLAPQuadrant.ELI,
            0x04: SLAPQuadrant.RESERVED,
            0x0C: SLAPQuadrant.SAI,
        }[first & 0x0C]

    return MACClassification(
        administration=(
            Administration.LOCAL
            if is_local else Administration.UNIVERSAL
        ),
        delivery=(
            DeliveryType.GROUP
            if is_group else DeliveryType.INDIVIDUAL
        ),
        is_broadcast=mac_int == 0xFFFFFFFFFFFF,
        is_zero=mac_int == 0,
        slap_quadrant=quadrant,
    )
