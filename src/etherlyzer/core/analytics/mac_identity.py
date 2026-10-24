from etherlyzer.core.analytics.mac_classifier import (
    Administration,
    DeliveryType,
    MACClassification,
    SLAPQuadrant,
)
from etherlyzer.ieee.initialize import EtherlyzerContext


def analyze_mac_identity(classified_mac: MACClassification, context: EtherlyzerContext):
    mac = classified_mac

    normalized = mac.normalized
    complete = mac.is_complete()

    identity = "Unknown"
    registration = "Not Applicable"

    if mac.is_zero and complete:
        identity = "Null Address"

    elif mac.is_broadcast and complete:
        identity = "Broadcast Address"

    elif mac.administration == Administration.UNIVERSAL:
        if mac.delivery == DeliveryType.GROUP:
            identity = "Universal Group Address" if complete else "Universal Group Prefix"
            registration = "Not an EUI-48"

        elif not complete:
            identity = "EUI-48 Prefix"
            registration = "Not Evaluated (Incomplete Address)"

        else:
            entry = context.indexes.mac.lookup(normalized)

            identity = "EUI-48 Candidate" if entry is not None else "EUI-48 Structure (Unverified)"
            registration = (
                f"Registered Block ({entry.registry})"
                if entry is not None
                else "No Matching IEEE Registry Block"
            )

    elif mac.slap_quadrant == SLAPQuadrant.ELI:
        if len(normalized) < 6:
            identity = "ELI Prefix"
            registration = "CID Not Evaluated (Incomplete Prefix)"

        else:
            # Clear I/G to obtain the registered CID for group addresses.
            cid = f"{int(normalized[:2], 16) & 0xFE:02X}{normalized[2:6]}".upper()
            entry = context.indexes.identifier.lookup(cid)

            if complete:
                identity = (
                    "ELI-48 Candidate" if entry is not None else "ELI-48 Structure (Unverified)"
                )
            else:
                identity = "ELI Prefix"

            registration = "Registered CID" if entry is not None else "No Matching IEEE CID"

    elif mac.slap_quadrant == SLAPQuadrant.AAI:
        identity = "AAI" if complete else "AAI Prefix"
        registration = "SLAP Administrative Assignment Space"

    elif mac.slap_quadrant == SLAPQuadrant.SAI:
        identity = "SAI" if complete else "SAI Prefix"
        registration = "SLAP Protocol-Defined Assignment Space"

    elif mac.slap_quadrant == SLAPQuadrant.RESERVED:
        identity = "Reserved SLAP Quadrant"
        registration = "Reserved by SLAP"

    return identity, registration
