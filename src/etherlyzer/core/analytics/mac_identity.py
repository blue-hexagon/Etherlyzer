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
    mac_is_complete = mac.is_complete()
    kind = "Unknown"
    identity = "Unknown"
    registration = "Not Applicable"

    if mac.is_zero:  # Zero
        kind = "Special"
        identity = "Null Address"

    elif mac.is_broadcast:  # Broadcast
        kind = "Special"
        identity = "Broadcast Address"

    elif mac.administration == Administration.UNIVERSAL:  # UAA
        kind = "UAA"
        if mac.delivery == DeliveryType.GROUP:
            identity = "Group Address" if mac_is_complete else "Group Prefix"

            if mac_is_complete:
                first_octet = int(normalized[:2], 16)

                individual_form = f"{first_octet & 0xFE:02X}{normalized[2:]}"

                # NOTE: MA-L, MA-M, MA-S (not IAB) can flip the I/G bit of an assignment to create a multicast address (per IEEE)
                entry = context.indexes.mac.lookup_group_allocation(individual_form)
                if entry is not None and entry.registry in {
                    "MA-L",
                    "MA-M",
                    "MA-S",
                }:  # It is in, if it is.
                    identity = "Group Address (Registered Block)"
                    registration = f"Registered Block ({entry.registry})"
                elif entry:
                    registration = "No Matching IEEE Group Allocation"
            else:
                registration = "Not Evaluated (Incomplete Address)"

        # UAA Individual: EUI-48 Prefix
        elif not mac_is_complete and mac.delivery == DeliveryType.INDIVIDUAL:
            kind = "UAA"
            identity = "EUI-48 Prefix"
            registration = "Not Evaluated (Incomplete Address)"

        # UAA Individual: EUI-48 Candidate / EUI-48 Structure
        elif mac_is_complete:
            entry = context.indexes.mac.lookup(normalized)
            if entry is not None:
                identity = "EUI-48 Candidate"
                registration = f"Registered Block ({entry.registry})"
            else:
                identity = "EUI-48 Structure"
                registration = "No Matching IEEE Registry Block"
    elif mac.slap_quadrant == SLAPQuadrant.ELI:  # LAA: ELI
        # ELI Prefix
        kind = "LAA"
        if len(normalized) < 6:
            identity = "ELI Prefix"
            registration = "CID Not Evaluated (Incomplete Prefix)"

        # ELI Prefix / ELI-48 Candidate / ELI-48 Structure
        elif len(normalized) >= 6:
            # Clear I/G to obtain the registered CID for group addresses.
            cid = f"{int(normalized[:2], 16) & 0xFE:02X}{normalized[2:6]}".upper()
            entry = context.indexes.identifier.lookup(cid)

            if mac_is_complete:
                if entry is not None:
                    identity = (
                        "Individual ELI-48 Candidate"
                        if (int(normalized[:2], 16) & 0x01) == 0
                        else "Group ELI-48 Candidate"
                    )
                else:
                    identity = (
                        "Individual ELI-48 Structure (No Matching CID)"
                        if (int(normalized[:2], 16) & 0x01) == 0
                        else "Group ELI-48 Structure (No Matching CID)"
                    )
            else:
                identity = "ELI Prefix"

            registration = "Registered CID" if entry is not None else "No Matching IEEE CID"
    # AAI
    elif mac.slap_quadrant == SLAPQuadrant.AAI:
        kind = "LAA"
        if normalized.startswith("3333"):
            identity = "IPv6 Multicast Address" if mac_is_complete else "IPv6 Multicast Prefix"
            registration = "IETF IPv6 Multicast Mapping (RFC 2464)"
        else:
            identity = "AAI Quadrant" if mac_is_complete else "AAI Quadrant Prefix"
            registration = "SLAP Administrative Assignment Space"

    # SAI
    elif mac.slap_quadrant == SLAPQuadrant.SAI:
        kind = "LAA"
        identity = "SAI Quadrant" if mac_is_complete else "SAI Quadrant Prefix"
        registration = "SLAP Protocol-Defined Assignment Space"

    # RESERVED
    elif mac.slap_quadrant == SLAPQuadrant.RESERVED:
        kind = "LAA"
        identity = "Reserved SLAP Quadrant" if mac_is_complete else "Reserved SLAP Quadrant Prefix"
        registration = "Reserved by SLAP"

    return identity, registration, kind
