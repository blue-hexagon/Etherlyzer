from dataclasses import dataclass
from enum import StrEnum

from etherlyzer.core.normalization import normalize


class Administration(StrEnum):
    UNIVERSAL = "Universally Administered Address (UAA)"
    LOCAL = "Locally Administered Address (LAA)"


class DeliveryType(StrEnum):
    INDIVIDUAL = "Individual Address"
    GROUP = "Group Address"


class SLAPQuadrant(StrEnum):
    AAI = "Administratively Assigned (AAI)"
    ELI = "Extended Local (ELI)"
    RESERVED = "Reserved"
    SAI = "Standard Assigned (SAI)"


@dataclass(frozen=True, slots=True)
class MACClassification:
    normalized: str
    administration: Administration
    delivery: DeliveryType
    is_broadcast: bool
    is_zero: bool
    slap_quadrant: SLAPQuadrant | None

    def is_complete(self) -> bool:
        return len(self.normalized) == 12

    def is_all_zero(self) -> bool:
        value = int(self.normalized, 16)
        is_all_zeros = value == 0
        return is_all_zeros

    def is_all_ones(self) -> bool:
        value = int(self.normalized, 16)
        bits = len(self.normalized) * 4

        is_all_ones = value == (1 << bits) - 1
        return is_all_ones


def classify_mac(mac: str) -> MACClassification:
    normalized = normalize(mac)

    if not normalized or len(normalized) > 12 or len(normalized) < 6:
        raise ValueError("Expected a full or partial MAC address of 6-12 hexadecimal digits")

    normalized_padded = normalized.ljust(12, "0")
    mac_int = int(normalized_padded, 16)

    first = mac_int >> 40

    is_local = bool(first & 0x02)
    is_group = bool(first & 0x01)

    quadrant = None
    # RFC 9542 : 2.1.1: Setting I/G does not affect the Y/Z bit
    # RFC 9542 : 2.3.1: explicitly identifies 33:33:XX:XX:XX:XX as IPv6 multicast addresses within the Administratively Assigned SLAP quadrant.
    # RFC 8947 : explicitly describes CID-derived ELI addresses as supporting group M-bit = 0 and 1 (furthermore MA-L, MA-M and MA-S supports M-bit)
    # Hence: AAI, SAI and ELI supports the M-bit.
    if is_local:
        quadrant = {
            0x00: SLAPQuadrant.AAI,
            0x08: SLAPQuadrant.ELI,
            0x04: SLAPQuadrant.RESERVED,
            0x0C: SLAPQuadrant.SAI,
        }[first & 0x0C]

    return MACClassification(
        normalized=normalized,
        administration=(Administration.LOCAL if is_local else Administration.UNIVERSAL),
        delivery=(DeliveryType.GROUP if is_group else DeliveryType.INDIVIDUAL),
        is_broadcast=mac_int == 0xFFFFFFFFFFFF and len(normalized) == 12,
        is_zero=mac_int == 0 and len(normalized) == 12,
        slap_quadrant=quadrant,
    )
