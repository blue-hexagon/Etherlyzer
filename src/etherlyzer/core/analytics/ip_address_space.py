from dataclasses import dataclass, field
from enum import Enum, auto
from typing import ClassVar


def ip_to_int(ip: str) -> int:
    """Converts an IP address from dot notation to an integer."""
    octets = map(int, ip.split('.'))
    return sum(octet << (8 * (3 - idx)) for idx, octet in enumerate(octets))


def int_to_ip(ip_int: int) -> str:
    """Converts an IP address from an integer to dot notation."""
    return '.'.join(str((ip_int >> (8 * i)) & 0xFF) for i in reversed(range(4)))


def is_private_ip(ip_decimal: int) -> bool:
    """Checks if the given IP in decimal format is a private IP."""
    for ip_range in PrivateAddressSpace.PRIVATE_IP_RANGES:
        if ip_range.start_ip_decimal < ip_decimal < ip_range.end_ip_decimal:
            return True
    return False


def is_public_ip(ip_decimal: int) -> bool:
    """Checks if the given IP in decimal format is a public IP."""
    for ip_range in PublicAddressSpace.PUBLIC_IP_RANGES:
        if ip_range.start_ip_decimal < ip_decimal < ip_range.end_ip_decimal:
            return True
    return False


def is_special_ip(ip_decimal: int) -> bool:
    """Checks if the given IP in decimal format is a special IP (e.g., APIPA, loopback, multicast, reserved)."""
    for ip_range in SpecialAddressSpace.SPECIAL_IP_RANGES:
        if ip_range.start_ip_decimal < ip_decimal < ip_range.end_ip_decimal:
            return True
    return False


def calculate_subnet_mask(start_ip_int, end_ip_int):
    """Calculates the subnet mask for a given IP range."""
    range_size = end_ip_int - start_ip_int
    total_ipv4_bits = 32
    subnet_bits = 0
    while range_size:
        subnet_bits += range_size & 1
        range_size >>= 1
    return total_ipv4_bits - subnet_bits


class AddressSpace(Enum):
    PRIVATE = auto()
    PUBLIC = auto()
    SPECIAL = auto()
    ANY = auto()


@dataclass
class IPRange:
    """Represents an IP range with start and end addresses in both dot notation and decimal."""
    start_ip: str
    end_ip: str
    start_ip_decimal: int = field(init=False)
    end_ip_decimal: int = field(init=False)
    cidr_mask: int = field(init=False)

    def __post_init__(self):
        self.start_ip_decimal = ip_to_int(self.start_ip)
        self.end_ip_decimal = ip_to_int(self.end_ip)
        self.cidr_mask = calculate_subnet_mask(self.start_ip_decimal, self.end_ip_decimal)


class PrivateAddressSpace:
    CLASS_A: IPRange = IPRange('10.0.0.0', '10.255.255.255')
    CLASS_B: IPRange = IPRange('172.16.0.0', '172.31.255.255')
    CLASS_C: IPRange = IPRange('192.168.0.0', '192.168.255.255')

    PRIVATE_IP_RANGES: ClassVar[list[IPRange]] = [CLASS_A, CLASS_B, CLASS_C]


class PublicAddressSpace:
    CLASS_A_1: IPRange = IPRange('1.0.0.0', '9.255.255.255')
    CLASS_A_2: IPRange = IPRange('11.0.0.0', '100.63.255.255')
    CLASS_A_3: IPRange = IPRange('100.128.0.0', '126.255.255.255')

    CLASS_B_1: IPRange = IPRange('128.0.0.0', '169.253.255.255')
    CLASS_B_2: IPRange = IPRange('169.255.0.0', '172.15.255.255')
    CLASS_B_3: IPRange = IPRange('172.32.0.0', '191.255.255.255')

    CLASS_C_1: IPRange = IPRange('192.0.0.0', '192.167.255.255')
    CLASS_C_2: IPRange = IPRange('192.169.0.0', '223.255.255.255')

    PUBLIC_IP_RANGES: ClassVar[list[IPRange]] = [
        CLASS_A_1, CLASS_A_2, CLASS_A_3,
        CLASS_B_1, CLASS_B_2, CLASS_B_3,
        CLASS_C_1, CLASS_C_2
    ]


class SpecialAddressSpace:
    ZERO_NET: IPRange = IPRange('0.0.0.0', '0.255.255.255')  # Non-routable
    CG_NAT: IPRange = IPRange('100.64.0.0', ' 100.127.255.255')  # RFC 6598
    APIPA: IPRange = IPRange('169.254.0.0', '169.254.255.255')
    LOOPBACK: IPRange = IPRange('127.0.0.0', '127.255.255.255')
    MULTICAST: IPRange = IPRange('224.0.0.0', '239.255.255.255')  # Class D
    RESERVED: IPRange = IPRange('240.0.0.0', '255.255.255.255')  # Class E

    SPECIAL_IP_RANGES: ClassVar[list[IPRange]] = [ZERO_NET, CG_NAT, APIPA, LOOPBACK, MULTICAST, RESERVED]


if __name__ == '__main__':
    print(int_to_ip(2851995648))
