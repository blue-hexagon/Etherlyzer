from enum import StrEnum


class RegistryFamily(StrEnum):
    MAC_REGISTRY = "mac"  # IAB, MA-L, MA-M, MA-S
    ETHERTYPE_REGISTRY = "ethertype"  # Ethertype
    IDENTIFIER_REGISTRY = "identifier"  # CID
    IP_MULTICAST_REGISTRY = "ip_multicast"
    IP_UNICAST_REGISTRY = "ip_unicast"
