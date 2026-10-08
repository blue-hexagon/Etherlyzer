from dataclasses import dataclass
from enum import StrEnum


class Administration(StrEnum):
    UNIVERSAL = "universal"
    LOCAL = "local"


class DeliveryType(StrEnum):
    INDIVIDUAL = "individual"
    GROUP = "group"


class SLAPQuadrant(StrEnum):
    AAI = "administratively_assigned"
    ELI = "extended_local"
    RESERVED = "reserved"
    SAI = "standard_assigned"


@dataclass(frozen=True, slots=True)
class MACClassification:
    administration: Administration
    delivery: DeliveryType
    is_broadcast: bool
    is_zero: bool
    slap_quadrant: SLAPQuadrant | None


def classify_mac(mac: str) -> MACClassification:
    mac = int(mac.replace(":", "").replace("-", ""), 16)
    if not 0 <= mac < (1 << 48):
        raise ValueError("Expected a 48-bit MAC address")

    first = mac >> 40

    is_local = bool(first & 0x02)
    is_group = bool(first & 0x01)

    quadrant = None

    if is_local:
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
        is_broadcast=mac == (1 << 48) - 1,
        is_zero=mac == 0,
        slap_quadrant=quadrant,
    )
