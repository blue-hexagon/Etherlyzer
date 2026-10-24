from enum import StrEnum


class RegistryFamily(StrEnum):
    MAC_REGISTRY = "mac"  # IAB, MA-L, MA-M, MA-S
    ETHERTYPE_REGISTRY = "protocol"  # Ethertype
    IDENTIFIER_REGISTRY = "identifier"  # CID
