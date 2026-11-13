from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, StrEnum

from etherlyzer.bootstrap import EtherlyzerContext
from etherlyzer.core.interpretation.mac.classifier import (
    Administration,
    DeliveryType,
    MACClassification,
    SLAPQuadrant,
)


def fixed_address_lookup(
    cmac: MACClassification,
) -> MacIdentityResult | None:

    STANDARDS_GROUP_MAC_PUBLIC_LISTING: dict[str, dict[str, MacIdentityResult]] = {
        "01005E": {
            "000000-7FFFFF": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.IPV4_MULTICAST_ADDRESS,
                resolution=MacResolution.IPV4_MULTICAST,
                cmac=cmac,
            ),
            "800000-8FFFFF": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.MPLS_MULTICAST_ADDRESS,
                resolution=MacResolution.MPLS_MULTICAST,
                cmac=cmac,
            ),
        },
        # IEEE 802.1Q reserved addresses
        # 01:80:C2:00:00:00 - 01:80:C2:00:00:0F
        # Standard Group MAC addresses
        # 01:80:C2:00:00:10 - 01:80:C2:00:00:FF
        "0180C20000": {
            "00": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.NEAREST_CUSTOMER_BRIDGE_GROUP,
                resolution=MacResolution.IEEE_8021Q,
                cmac=cmac,
            ),
            "01": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.MAC_SPECIFIC_CONTROL_PROTOCOLS,
                resolution=MacResolution.IEEE_8021Q,
                cmac=cmac,
            ),
            "02": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.SLOW_PROTOCOLS_MULTICAST,
                resolution=MacResolution.IEEE_8021AX,
                cmac=cmac,
            ),
            "03": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.NEAREST_NON_TPMR_BRIDGE_PAE,
                resolution=MacResolution.IEEE_8021Q,
                cmac=cmac,
            ),
            "04": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.MAC_SPECIFIC_CONTROL_PROTOCOLS,
                resolution=MacResolution.IEEE_8021Q,
                cmac=cmac,
            ),
            "05": MacIdentityResult(
                form=MacForm.SPECIAL_RESERVED_ADDRESS,
                identity=MacIdentity.RESERVED_FUTURE_STANDARDIZATION,
                resolution=MacResolution.IEEE_8021Q,
                cmac=cmac,
            ),
            "06": MacIdentityResult(
                form=MacForm.SPECIAL_RESERVED_ADDRESS,
                identity=MacIdentity.RESERVED_FUTURE_STANDARDIZATION,
                resolution=MacResolution.IEEE_8021Q,
                cmac=cmac,
            ),
            "07": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.MEF_ELMI_GROUP,
                resolution=MacResolution.IEEE_8021Q,
                cmac=cmac,
            ),
            "08": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.PROVIDER_BRIDGE_GROUP,
                resolution=MacResolution.IEEE_8021Q,
                cmac=cmac,
            ),
            "09": MacIdentityResult(
                form=MacForm.SPECIAL_RESERVED_ADDRESS,
                identity=MacIdentity.RESERVED_FUTURE_STANDARDIZATION,
                resolution=MacResolution.IEEE_8021Q,
                cmac=cmac,
            ),
            "0A": MacIdentityResult(
                form=MacForm.SPECIAL_RESERVED_ADDRESS,
                identity=MacIdentity.RESERVED_FUTURE_STANDARDIZATION,
                resolution=MacResolution.IEEE_8021Q,
                cmac=cmac,
            ),
            "0B": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.EDE_SS_PEP,
                resolution=MacResolution.IEEE_8021X_8021AE,
                cmac=cmac,
            ),
            "0C": MacIdentityResult(
                form=MacForm.SPECIAL_RESERVED_ADDRESS,
                identity=MacIdentity.RESERVED_FUTURE_STANDARDIZATION,
                resolution=MacResolution.IEEE_8021Q,
                cmac=cmac,
            ),
            "0D": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.PROVIDER_BRIDGE_MVRP,
                resolution=MacResolution.IEEE_8021Q,
                cmac=cmac,
            ),
            "0E": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.NEAREST_BRIDGE_GROUP,
                resolution=MacResolution.IEEE_8021Q,
                cmac=cmac,
            ),
            "0F": MacIdentityResult(
                form=MacForm.SPECIAL_RESERVED_ADDRESS,
                identity=MacIdentity.RESERVED_FUTURE_STANDARDIZATION,
                resolution=MacResolution.IEEE_8021Q,
                cmac=cmac,
            ),
            # Individual Standard Group MAC addresses
            "10": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.ALL_LANS_BRIDGE_MANAGEMENT,
                resolution=MacResolution.IEEE_8021D,
                cmac=cmac,
            ),
            "11": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.LOAD_SERVER_GENERIC,
                resolution=MacResolution.IEEE_8021E,
                cmac=cmac,
            ),
            "12": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.LOADABLE_DEVICE_GENERIC,
                resolution=MacResolution.IEEE_8021E,
                cmac=cmac,
            ),
            "13": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.IEEE_1905_CONTROL,
                resolution=MacResolution.IEEE_1905_1,
                cmac=cmac,
            ),
            "14": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.ALL_LEVEL_1_INTERMEDIATE_SYSTEMS,
                resolution=MacResolution.ISO_IEC_10589,
                cmac=cmac,
            ),
            "15": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.ALL_LEVEL_2_INTERMEDIATE_SYSTEMS,
                resolution=MacResolution.ISO_IEC_10589,
                cmac=cmac,
            ),
            "16": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.ALL_CONS_END_SYSTEMS,
                resolution=MacResolution.ISO_IEC_10030,
                cmac=cmac,
            ),
            "17": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.ALL_CONS_SNARES,
                resolution=MacResolution.ISO_IEC_10030,
                cmac=cmac,
            ),
            "18": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.ALL_MANAGER_STATIONS,
                resolution=MacResolution.IEEE_8021B,
                cmac=cmac,
            ),
            "19": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.GROUPCAST_WITH_RETRIES,
                resolution=MacResolution.IEEE_80211AA,
                cmac=cmac,
            ),
            "1A": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.ALL_AGENT_STATIONS,
                resolution=MacResolution.IEEE_8021B,
                cmac=cmac,
            ),
            "1B": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.ALL_MULTICAST_CAPABLE_END_SYSTEMS,
                resolution=MacResolution.ISO_IEC_9542,
                cmac=cmac,
            ),
            "1C": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.ALL_MULTICAST_ANNOUNCEMENTS,
                resolution=MacResolution.ISO_IEC_9542,
                cmac=cmac,
            ),
            "1D": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.ALL_MULTICAST_CAPABLE_INTERMEDIATE_SYSTEMS,
                resolution=MacResolution.ISO_IEC_9542,
                cmac=cmac,
            ),
            "1E": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.ALL_DTR_CONCENTRATORS,
                resolution=MacResolution.ISO_IEC_8802_5,
                cmac=cmac,
            ),
            "1F": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.EDE_CC_PEP,
                resolution=MacResolution.IEEE_8021X_8021AE,
                cmac=cmac,
            ),
            # Inclusive ranges within 01:80:C2:00:00
            "20-2F": MacIdentityResult(
                form=MacForm.SPECIAL_RESERVED_ADDRESS,
                identity=MacIdentity.MRP_APPLICATION_RESERVED,
                resolution=MacResolution.IEEE_8021Q,
                cmac=cmac,
            ),
            "30-3F": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.CFM_CCM_LINKTRACE_GROUP,
                resolution=MacResolution.IEEE_8021Q,
                cmac=cmac,
            ),
            "40-4F": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.TRILL_GROUP,
                resolution=MacResolution.IETF_TRILL,
                cmac=cmac,
            ),
            "50-FF": MacIdentityResult(
                form=MacForm.UAA_ADDRESS,
                identity=MacIdentity.GROUP_ADDRESS,
                resolution=MacResolution.UNASSIGNED,
                cmac=cmac,
            ),
        },
        # ISO/IEC JTC1/SC25 allocated addresses
        # 01:80:C2:00:01:00 - 01:80:C2:00:01:FF
        "0180C20001": {
            "00": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.RING_MANAGEMENT_DIRECTED_BEACON,
                resolution=MacResolution.ISO_IEC_9314_6,
                cmac=cmac,
            ),
            "01-0F": MacIdentityResult(
                form=MacForm.SPECIAL_RESERVED_ADDRESS,
                identity=MacIdentity.ISO_SC25_FUTURE_USE,
                resolution=MacResolution.ISO_IEC_SC25,
                cmac=cmac,
            ),
            "10": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.STATUS_REPORT_PROTOCOL,
                resolution=MacResolution.ISO_IEC_9314_6,
                cmac=cmac,
            ),
            "11-1F": MacIdentityResult(
                form=MacForm.SPECIAL_RESERVED_ADDRESS,
                identity=MacIdentity.ISO_SC25_FUTURE_USE,
                resolution=MacResolution.ISO_IEC_SC25,
                cmac=cmac,
            ),
            "20": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.ALL_FDDI_CONCENTRATORS,
                resolution=MacResolution.ISO_IEC_9314_2,
                cmac=cmac,
            ),
            "21-2F": MacIdentityResult(
                form=MacForm.SPECIAL_RESERVED_ADDRESS,
                identity=MacIdentity.ISO_SC25_FUTURE_USE,
                resolution=MacResolution.ISO_IEC_SC25,
                cmac=cmac,
            ),
            "30": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.SYNCHRONOUS_BANDWIDTH_ALLOCATION,
                resolution=MacResolution.ISO_IEC_9314_6,
                cmac=cmac,
            ),
            "31-FF": MacIdentityResult(
                form=MacForm.SPECIAL_RESERVED_ADDRESS,
                identity=MacIdentity.ISO_SC25_FUTURE_USE,
                resolution=MacResolution.ISO_IEC_SC25,
                cmac=cmac,
            ),
        },
        # ETSI allocated address range
        # 01:80:C2:00:02:00 - 01:80:C2:00:02:FF
        "0180C20002": {
            "00-FF": MacIdentityResult(
                form=MacForm.SPECIAL_RESERVED_ADDRESS,
                identity=MacIdentity.ETSI_FUTURE_USE,
                resolution=MacResolution.ETSI_RESERVED,
                cmac=cmac,
            ),
        },
        # Unassigned range
        # 01:80:C2:00:03:00 - 01:80:C2:FF:FF:FF
        # Outer key contains only the first three octets.
        "0180C2": {
            "000300-FFFFFF": MacIdentityResult(
                form=MacForm.UAA_ADDRESS,
                identity=MacIdentity.GROUP_ADDRESS,
                resolution=MacResolution.UNASSIGNED,
                cmac=cmac,
            ),
        },
        # ISO/IEC 9542 ES-IS addresses
        # 09:00:2B:00:00:04 - 09:00:2B:00:00:05
        "09002B0000": {
            "04": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.ALL_END_SYSTEM_NETWORK_ENTITIES,
                resolution=MacResolution.ISO_IEC_9542,
                cmac=cmac,
            ),
            "05": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.ALL_INTERMEDIATE_SYSTEM_NETWORK_ENTITIES,
                resolution=MacResolution.ISO_IEC_9542,
                cmac=cmac,
            ),
        },
        # IEEE 802.5 locally administered functional addresses
        # Configuration Report Server, Ring Error Monitor,
        # and Ring Parameter Server
        "0300000000": {
            "08": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.CONFIGURATION_REPORT_SERVER,
                resolution=MacResolution.IEEE_8025,
                cmac=cmac,
            ),
            "10": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.RING_ERROR_MONITOR,
                resolution=MacResolution.IEEE_8025,
                cmac=cmac,
            ),
            "40": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.RING_PARAMETER_SERVER,
                resolution=MacResolution.IEEE_8025,
                cmac=cmac,
            ),
        },
        # 03:00:00:00:01:00
        "0300000001": {
            "00": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.ALL_INTERMEDIATE_SYSTEM_NETWORK_ENTITIES,
                resolution=MacResolution.ISO_IEC_9542,
                cmac=cmac,
            ),
        },
        # 03:00:00:00:02:00
        "0300000002": {
            "00": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.ALL_END_SYSTEMS_AND_LOBE_MEDIA_TEST,
                resolution=MacResolution.ISO_IEC_9542_IEEE_8025,
                cmac=cmac,
            ),
        },
        # 03:00:00:00:04:00
        "0300000004": {
            "00": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.ALL_MANAGER_STATIONS,
                resolution=MacResolution.IEEE_8021B,
                cmac=cmac,
            ),
        },
        # 03:00:00:00:08:00
        "0300000008": {
            "00": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.ALL_CONS_SNARES,
                resolution=MacResolution.ISO_IEC_10030,
                cmac=cmac,
            ),
        },
        # 03:00:00:00:10:00
        "0300000010": {
            "00": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.ALL_CONS_END_SYSTEMS,
                resolution=MacResolution.ISO_IEC_10030,
                cmac=cmac,
            ),
        },
        # 03:00:00:00:20:00
        "0300000020": {
            "00": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.LOADABLE_DEVICE_GENERIC,
                resolution=MacResolution.IEEE_8021E,
                cmac=cmac,
            ),
        },
        # 03:00:00:00:40:00
        "0300000040": {
            "00": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.LOAD_SERVER_GENERIC,
                resolution=MacResolution.IEEE_8021E,
                cmac=cmac,
            ),
        },
        # 03:00:00:40:00:00
        "0300004000": {
            "00": MacIdentityResult(
                form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
                identity=MacIdentity.ALL_AGENT_STATIONS,
                resolution=MacResolution.IEEE_8021B,
                cmac=cmac,
            ),
        },
    }

    # Normalize and validate input.
    mac = cmac.normalized

    # Convert the input into an inclusive 48-bit interval.
    start = int(mac.ljust(12, "0"), 16)
    end = int(mac.ljust(12, "F"), 16)

    # Collect all registry entries intersecting the input interval.
    matches: list[tuple[int, int, MacIdentityResult]] = []

    for prefix, entries in STANDARDS_GROUP_MAC_PUBLIC_LISTING.items():
        for suffix, result in entries.items():
            lower, separator, upper = suffix.partition("-")

            if not separator:
                upper = lower

            if len(prefix + lower) != 12 or len(prefix + upper) != 12:
                raise ValueError(f"Invalid registry entry: {prefix}/{suffix}")

            lower_bound = int(prefix + lower, 16)
            upper_bound = int(prefix + upper, 16)

            if lower_bound <= end and upper_bound >= start:
                matches.append((lower_bound, upper_bound, result))

    if not matches:
        return None

    # Divide the queried prefix into intervals at every registry
    # boundary, so no narrower classification is overlooked.
    boundaries = {start, end + 1}

    for lower, upper, _ in matches:
        boundaries.add(max(start, lower))
        boundaries.add(min(end, upper) + 1)

    boundaries = sorted(boundaries)

    resolved: MacIdentityResult | None = None

    for point in boundaries[:-1]:
        # Prefer the narrowest matching registry entry.
        match = min(
            (entry for entry in matches if entry[0] <= point <= entry[1]),
            key=lambda entry: entry[1] - entry[0],
            default=None,
        )

        if match is None:
            return None

        result = match[2]

        if resolved is None:
            resolved = result
            continue

        if (
            resolved.form,
            resolved.identity,
            resolved.resolution,
        ) != (
            result.form,
            result.identity,
            result.resolution,
        ):
            return None

    return resolved


class MacForm(StrEnum):
    UAA_PREFIX = "UAA Prefix"
    UAA_ADDRESS = "UAA Address"
    LAA_PREFIX = "LAA Prefix"
    LAA_ADDRESS = "LAA Address"

    SPECIAL_FIXED_ADDRESS = "Special (Fixed Address)"
    SPECIAL_PROTOCOL_PREFIX = "Special (Protocol-Defined Prefix)"
    SPECIAL_PROTOCOL_ADDRESS = "Special (Protocol-Defined Address)"
    SPECIAL_RESERVED_ADDRESS = "Special (Reserved Address)"


class MacIdentity(StrEnum):
    # Universally administered individual
    EUI48_PREFIX = "EUI-48-Compatible Prefix"
    EUI48_ADDRESS = "EUI-48-Compatible Individual Address"

    # Universally administered group
    GROUP_PREFIX = "Group Address Prefix"
    GROUP_ADDRESS = "Group Address"

    # Extended Local Identifier (ELI)
    ELI_INDIVIDUAL_PREFIX = "Individual ELI Prefix"
    ELI_INDIVIDUAL_ADDRESS = "Individual ELI-48-Compatible Address"
    ELI_GROUP_PREFIX = "Group ELI Prefix"
    ELI_GROUP_ADDRESS = "Group ELI-48-Compatible Address"

    # Structured Local Address Plan (SLAP)
    AAI_PREFIX = "AAI Prefix"
    AAI_ADDRESS = "AAI Address"
    SAI_PREFIX = "SAI Prefix"
    SAI_ADDRESS = "SAI Address"
    RESERVED_PREFIX = "Reserved SLAP Prefix"
    RESERVED_ADDRESS = "Reserved SLAP Address"

    # Special-purpose identifiers
    IPV4_MULTICAST_ADDRESS = "IPv4 Multicast Address"
    MPLS_MULTICAST_ADDRESS = "MPLS Multicast Address"
    IPV6_MULTICAST_PREFIX = "IPv6 Multicast Prefix"
    IPV6_MULTICAST_ADDRESS = "IPv6 Multicast Address"
    ALL_ZERO = "All-Zero / Null Address"
    BROADCAST = "Ethernet Broadcast"

    # IEEE 802.1Q reserved group addresses
    NEAREST_CUSTOMER_BRIDGE_GROUP = "Nearest Customer Bridge Group Address"
    MAC_SPECIFIC_CONTROL_PROTOCOLS = "MAC-Specific Control Protocols Group Address"
    SLOW_PROTOCOLS_MULTICAST = "Slow Protocols Multicast Address"
    NEAREST_NON_TPMR_BRIDGE_PAE = "Nearest Non-TPMR Bridge / PAE Address"
    MEF_ELMI_GROUP = "MEF ELMI Protocol Group Address"
    PROVIDER_BRIDGE_GROUP = "Provider Bridge Group Address"
    EDE_SS_PEP = "EDE-SS PEP Address"
    PROVIDER_BRIDGE_MVRP = "Provider Bridge MVRP Address"
    NEAREST_BRIDGE_GROUP = "Nearest Bridge Group Address"

    # IEEE 802.1D / IEEE 802.1E
    ALL_LANS_BRIDGE_MANAGEMENT = "All LANs Bridge Management Group Address"
    LOAD_SERVER_GENERIC = "Load Server Generic Address"
    LOADABLE_DEVICE_GENERIC = "Loadable Device Generic Address"

    # IEEE 1905.1
    IEEE_1905_CONTROL = "IEEE 1905.1 Control Address"

    # ISO/IEC 10589 (IS-IS)
    ALL_LEVEL_1_INTERMEDIATE_SYSTEMS = "All Level 1 Intermediate Systems Address"
    ALL_LEVEL_2_INTERMEDIATE_SYSTEMS = "All Level 2 Intermediate Systems Address"

    # ISO/IEC 10030
    ALL_CONS_END_SYSTEMS = "All CONS End Systems Address"
    ALL_CONS_SNARES = "All CONS SNARES Address"

    # IEEE 802.1B
    ALL_MANAGER_STATIONS = "All Manager Stations Address"
    ALL_AGENT_STATIONS = "All Agent Stations Address"

    # IEEE 802.11aa
    GROUPCAST_WITH_RETRIES = "Groupcast with Retries (GCR) MAC Group Address"

    # ISO/IEC 9542 (ES-IS)
    ALL_MULTICAST_CAPABLE_END_SYSTEMS = "All Multicast Capable End Systems Address"
    ALL_MULTICAST_ANNOUNCEMENTS = "All Multicast Announcements Address"
    ALL_MULTICAST_CAPABLE_INTERMEDIATE_SYSTEMS = (
        "All Multicast Capable Intermediate Systems Address"
    )
    ALL_END_SYSTEM_NETWORK_ENTITIES = "All End System Network Entities Address"
    ALL_INTERMEDIATE_SYSTEM_NETWORK_ENTITIES = "All Intermediate System Network Entities Address"

    # ISO/IEC 8802-5
    ALL_DTR_CONCENTRATORS = "All DTR Concentrators MAC Group Address"

    # IEEE 802.1X / IEEE 802.1AE
    EDE_CC_PEP = "EDE-CC PEP Address"

    # IEEE 802.1Q / MRP / CFM
    MRP_APPLICATION_RESERVED = "MRP Application Reserved Address"
    CFM_CCM_LINKTRACE_GROUP = "CFM Continuity Check / Linktrace Group Address"

    # IETF TRILL
    TRILL_GROUP = "TRILL Protocol Group Address"

    # ISO/IEC 9314 (FDDI)
    RING_MANAGEMENT_DIRECTED_BEACON = "Ring Management Directed Beacon Multicast Address"
    STATUS_REPORT_PROTOCOL = "Status Report Protocol Multicast Address"
    ALL_FDDI_CONCENTRATORS = "All FDDI Concentrator MACs"
    SYNCHRONOUS_BANDWIDTH_ALLOCATION = "Synchronous Bandwidth Allocation Address"

    # IEEE 802.5 (Token Ring)
    CONFIGURATION_REPORT_SERVER = "Configuration Report Server (CRS) MAC Group Address"
    RING_ERROR_MONITOR = "Ring Error Monitor (REM) MAC Group Address"
    RING_PARAMETER_SERVER = "Ring Parameter Server (RPS) MAC Group Address"
    ALL_END_SYSTEMS_AND_LOBE_MEDIA_TEST = "All End Systems / Lobe Media Test Address"

    # Reserved allocations
    RESERVED_FUTURE_STANDARDIZATION = "Reserved for Future Standardization"
    ISO_SC25_FUTURE_USE = "ISO/IEC JTC1/SC25 Reserved for Future Use"
    ETSI_FUTURE_USE = "ETSI Reserved for Future Use"


class MacResolution(StrEnum):
    # IEEE registered allocations
    REGISTERED_MAL = "Registered Block (MA-L)"
    REGISTERED_MAM = "Registered Block (MA-M)"
    REGISTERED_MAS = "Registered Block (MA-S)"
    REGISTERED_IAB = "Registered Block (IAB)"
    REGISTERED_CID = "Registered (CID)"

    # Unresolved allocations
    NO_REGISTRY_MATCH = "No Matching Eligible IEEE Allocation"
    NO_CID_MATCH = "No Matching IEEE CID"
    UNASSIGNED = "Unassigned IEEE Group Address"

    # SLAP assignment mechanisms
    SLAP_ELI = "SLAP Extended Local Identifier"
    SLAP_AAI = "SLAP Administrative Assignment Space"
    SLAP_SAI = "SLAP Standard Assignment Space"
    SLAP_RESERVED = "Reserved SLAP Assignment Space"

    # Standards-defined special purposes
    IPV4_MULTICAST = "IETF IPv4 Multicast Mapping (RFC 1112 + 9542)"
    MPLS_MULTICAST = "IETF MPLS Multicast (RFC 5332)"
    IPV6_MULTICAST = "IETF IPv6 Multicast Mapping (RFC 2464)"
    IEEE_RA_RESERVED = "IEEE RA Reserved"
    IEEE_8023_DEFINED = "IEEE 802.3 Defined"

    # IEEE 802.1
    IEEE_8021Q = "IEEE 802.1Q Defined"
    IEEE_8021D = "IEEE 802.1D Defined"
    IEEE_8021E = "IEEE 802.1E Defined"
    IEEE_8021B = "IEEE 802.1B Defined"
    IEEE_8021AX = "IEEE 802.1AX Defined"
    IEEE_8021X_8021AE = "IEEE 802.1X / 802.1AE Defined"

    # IEEE 802.5 / IEEE 802.11 / IEEE 1905
    IEEE_8025 = "IEEE 802.5 Defined"
    IEEE_80211AA = "IEEE 802.11aa Defined"
    IEEE_1905_1 = "IEEE 1905.1 Defined"

    # ISO/IEC standards
    ISO_IEC_10589 = "ISO/IEC 10589 Defined"
    ISO_IEC_10030 = "ISO/IEC 10030 Defined"
    ISO_IEC_9542 = "ISO/IEC 9542 Defined"
    ISO_IEC_8802_5 = "ISO/IEC 8802-5 Defined"
    ISO_IEC_9314_2 = "ISO/IEC 9314-2 Defined"
    ISO_IEC_9314_6 = "ISO/IEC 9314-6 Defined"
    ISO_IEC_9542_IEEE_8025 = "ISO/IEC 9542 / IEEE 802.5 Defined"

    # IETF
    IETF_TRILL = "IETF TRILL Protocol Defined"

    # Reserved organizational allocations
    ISO_IEC_SC25 = "ISO/IEC JTC1/SC25 Reserved Allocation"
    ETSI_RESERVED = "ETSI Reserved Allocation"


REGISTERED_RESOLUTIONS = frozenset(
    {
        MacResolution.REGISTERED_MAL,
        MacResolution.REGISTERED_MAM,
        MacResolution.REGISTERED_MAS,
        MacResolution.REGISTERED_IAB,
        MacResolution.REGISTERED_CID,
    }
)

STANDARD_RESOLUTIONS = frozenset(
    {
        # IETF
        MacResolution.IPV6_MULTICAST,
        MacResolution.IETF_TRILL,
        # IEEE
        MacResolution.IEEE_8023_DEFINED,
        MacResolution.IEEE_8021Q,
        MacResolution.IEEE_8021D,
        MacResolution.IEEE_8021E,
        MacResolution.IEEE_8021B,
        MacResolution.IEEE_8021AX,
        MacResolution.IEEE_8021X_8021AE,
        MacResolution.IEEE_8025,
        MacResolution.IEEE_80211AA,
        MacResolution.IEEE_1905_1,
        # ISO/IEC
        MacResolution.ISO_IEC_10589,
        MacResolution.ISO_IEC_10030,
        MacResolution.ISO_IEC_9542,
        MacResolution.ISO_IEC_8802_5,
        MacResolution.ISO_IEC_9314_2,
        MacResolution.ISO_IEC_9314_6,
        MacResolution.ISO_IEC_9542_IEEE_8025,
    }
)

RESERVED_RESOLUTIONS = frozenset(
    {
        MacResolution.SLAP_RESERVED,
        MacResolution.IEEE_RA_RESERVED,
        MacResolution.ISO_IEC_SC25,
        MacResolution.ETSI_RESERVED,
    }
)


class MacAssessment(Enum):
    # Structural analysis
    STRUCTURALLY_CONFORMANT = (
        "Structurally Conformant",
        "The identifier conforms to the applicable structural addressing "
        "rules. This does not establish that it has been registered or assigned.",
    )

    # IEEE registration analysis
    REGISTERED_PREFIX = (
        "Registered Prefix",
        "The supplied prefix matches an eligible IEEE-registered allocation. "
        "More-specific allocations may affect attribution of completed addresses.",
    )

    REGISTERED_CANDIDATE = (
        "Registered Candidate",
        "The complete identifier falls within an eligible IEEE-registered "
        "allocation, but assignment of the specific identifier has not been verified.",
    )

    ATTRIBUTION_AMBIGUOUS = (
        "Attribution Ambiguous",
        "The supplied prefix does not establish a unique allocation attribution. "
        "More-specific allocations may apply to addresses within its completion space.",
    )

    # Standards and reservations
    STANDARD_DEFINED = (
        "Standards-Defined",
        "The identifier or address pattern has a recognized purpose or assignment "
        "mechanism defined by an applicable technical standard.",
    )

    RESERVED = (
        "Reserved",
        "The identifier belongs to an address or identifier space reserved "
        "under the applicable addressing rules.",
    )

    # Unresolved analysis
    UNRESOLVED = (
        "Unresolved",
        "The available information is insufficient to establish the relevant "
        "assignment or interpretation.",
    )

    def __init__(self, label: str, description: str) -> None:
        self.label = label
        self.description = description

    def __str__(self) -> str:
        return self.label


@dataclass
class MacIdentityResult:
    form: MacForm
    identity: MacIdentity
    resolution: MacResolution
    cmac: MACClassification
    assessment: frozenset[MacAssessment] = field(init=False)

    def __post_init__(self) -> None:
        self.assessment = self.assess_mac_identity(self.cmac)

    def assess_mac_identity(
        self,
        cmac: MACClassification,
        *,
        attribution_ambiguous: bool = False,
    ) -> frozenset[MacAssessment]:

        assessments: set[MacAssessment] = set()

        # Structural interpretation
        assessments.add(MacAssessment.STRUCTURALLY_CONFORMANT)

        # Registry-backed identifiers
        if self.resolution in REGISTERED_RESOLUTIONS:
            if cmac.is_complete():
                assessments.add(MacAssessment.REGISTERED_CANDIDATE)
            else:
                assessments.add(MacAssessment.REGISTERED_PREFIX)

        # More-specific allocations may change attribution
        if attribution_ambiguous:
            assessments.add(MacAssessment.ATTRIBUTION_AMBIGUOUS)

        # Standards-defined address purposes
        if self.resolution in STANDARD_RESOLUTIONS:
            assessments.add(MacAssessment.STANDARD_DEFINED)

        # Reserved address space
        if self.resolution in RESERVED_RESOLUTIONS:
            assessments.add(MacAssessment.RESERVED)

        return frozenset(assessments)


BLOCK_REGISTRATIONS: dict[str, MacResolution] = {
    "MA-L": MacResolution.REGISTERED_MAL,
    "MA-M": MacResolution.REGISTERED_MAM,
    "MA-S": MacResolution.REGISTERED_MAS,
    "IAB": MacResolution.REGISTERED_IAB,
}


def _registered_block(registry: str) -> MacResolution:
    return BLOCK_REGISTRATIONS[registry]


# ---------------------------------------------------------------------------
# UNIVERSALLY ADMINISTERED — GROUP
# ---------------------------------------------------------------------------


def inspect_uaa_mcast_prefix(cmac: MACClassification, ctx: EtherlyzerContext) -> MacIdentityResult:
    entry = ctx.indexes.mac.lookup_group_allocation(cmac.normalized)

    if entry is not None:
        return MacIdentityResult(
            identity=MacIdentity.GROUP_PREFIX,
            resolution=_registered_block(entry.registry),
            form=MacForm.UAA_PREFIX,
            cmac=cmac,
        )

    return MacIdentityResult(
        identity=MacIdentity.GROUP_PREFIX,
        resolution=MacResolution.NO_REGISTRY_MATCH,
        form=MacForm.UAA_PREFIX,
        cmac=cmac,
    )


def inspect_uaa_mcast_complete(
    cmac: MACClassification, ctx: EtherlyzerContext
) -> MacIdentityResult:
    entry = ctx.indexes.mac.lookup_group_allocation(cmac.normalized)
    if entry is not None:
        return MacIdentityResult(
            identity=MacIdentity.GROUP_ADDRESS,
            resolution=_registered_block(entry.registry),
            form=MacForm.UAA_ADDRESS,
            cmac=cmac,
        )

    return MacIdentityResult(
        identity=MacIdentity.GROUP_ADDRESS,
        resolution=MacResolution.NO_REGISTRY_MATCH,
        form=MacForm.UAA_ADDRESS,
        cmac=cmac,
    )


# ---------------------------------------------------------------------------
# UNIVERSALLY ADMINISTERED — INDIVIDUAL
# ---------------------------------------------------------------------------


def inspect_uaa_unicast_prefix(
    cmac: MACClassification, ctx: EtherlyzerContext
) -> MacIdentityResult:
    entry = ctx.indexes.mac.lookup(cmac.normalized)

    return MacIdentityResult(
        identity=MacIdentity.EUI48_PREFIX,
        resolution=_registered_block(entry.registry)
        if entry is not None
        else MacResolution.NO_REGISTRY_MATCH,
        form=MacForm.UAA_PREFIX,
        cmac=cmac,
    )


def inspect_uaa_unicast_complete(
    cmac: MACClassification, ctx: EtherlyzerContext
) -> MacIdentityResult:
    entry = ctx.indexes.mac.lookup(cmac.normalized)

    if entry is not None:
        return MacIdentityResult(
            identity=MacIdentity.EUI48_ADDRESS,
            resolution=_registered_block(entry.registry),
            form=MacForm.UAA_ADDRESS,
            cmac=cmac,
        )
    return MacIdentityResult(
        identity=MacIdentity.EUI48_ADDRESS if cmac.is_complete() else MacIdentity.EUI48_PREFIX,
        resolution=MacResolution.NO_REGISTRY_MATCH,
        form=MacForm.UAA_ADDRESS,
        cmac=cmac,
    )


# ---------------------------------------------------------------------------
# LOCALLY ADMINISTERED — SHARED SLAP ANALYSIS
# ---------------------------------------------------------------------------


def _inspect_laa_slap(cmac: MACClassification, ctx: EtherlyzerContext) -> MacIdentityResult:
    complete = cmac.is_complete()
    kind = MacForm.LAA_ADDRESS if complete else MacForm.LAA_PREFIX

    match cmac.slap_quadrant:
        case SLAPQuadrant.ELI:
            first = int(cmac.normalized[:2], 16) & 0xFE
            cid = f"{first:02X}{cmac.normalized[2:6]}"
            entry = ctx.indexes.identifier.lookup(cid)

            if cmac.delivery == DeliveryType.GROUP:
                identity = (
                    MacIdentity.ELI_GROUP_ADDRESS
                    if cmac.is_complete()
                    else MacIdentity.ELI_GROUP_PREFIX
                )
            else:
                identity = (
                    MacIdentity.ELI_INDIVIDUAL_ADDRESS
                    if cmac.is_complete()
                    else MacIdentity.ELI_INDIVIDUAL_PREFIX
                )

            registration = (
                MacResolution.REGISTERED_CID if entry is not None else MacResolution.NO_CID_MATCH
            )
            return MacIdentityResult(
                identity=identity, resolution=registration, form=kind, cmac=cmac
            )

        case SLAPQuadrant.AAI:
            return MacIdentityResult(
                identity=MacIdentity.AAI_ADDRESS if complete else MacIdentity.AAI_PREFIX,
                resolution=MacResolution.SLAP_AAI,
                form=kind,
                cmac=cmac,
            )

        case SLAPQuadrant.SAI:
            return MacIdentityResult(
                identity=MacIdentity.SAI_ADDRESS if complete else MacIdentity.SAI_PREFIX,
                resolution=MacResolution.SLAP_SAI,
                form=kind,
                cmac=cmac,
            )

        case SLAPQuadrant.RESERVED:
            return MacIdentityResult(
                identity=MacIdentity.RESERVED_ADDRESS if complete else MacIdentity.RESERVED_PREFIX,
                resolution=MacResolution.SLAP_RESERVED,
                form=kind,
                cmac=cmac,
            )

        case _:
            raise ValueError(f"Unexpected SLAP quadrant: {cmac.slap_quadrant}")


# ---------------------------------------------------------------------------
# LOCALLY ADMINISTERED — GROUP
# ---------------------------------------------------------------------------


def inspect_laa_mcast_prefix(cmac: MACClassification, ctx: EtherlyzerContext) -> MacIdentityResult:
    if cmac.normalized.startswith("3333"):
        return MacIdentityResult(
            identity=MacIdentity.IPV6_MULTICAST_PREFIX,
            resolution=MacResolution.IPV6_MULTICAST,
            form=MacForm.SPECIAL_PROTOCOL_PREFIX,
            cmac=cmac,
        )

    return _inspect_laa_slap(cmac, ctx)


def inspect_laa_mcast_complete(
    cmac: MACClassification, ctx: EtherlyzerContext
) -> MacIdentityResult:
    if cmac.normalized.startswith("3333"):
        return MacIdentityResult(
            identity=MacIdentity.IPV6_MULTICAST_ADDRESS,
            resolution=MacResolution.IPV6_MULTICAST,
            form=MacForm.SPECIAL_PROTOCOL_ADDRESS,
            cmac=cmac,
        )

    return _inspect_laa_slap(cmac, ctx)


# ---------------------------------------------------------------------------
# LOCALLY ADMINISTERED — INDIVIDUAL
# ---------------------------------------------------------------------------


def inspect_laa_unicast_prefix(
    cmac: MACClassification, ctx: EtherlyzerContext
) -> MacIdentityResult:
    return _inspect_laa_slap(cmac, ctx)


def inspect_laa_unicast_complete(
    cmac: MACClassification, ctx: EtherlyzerContext
) -> MacIdentityResult:
    return _inspect_laa_slap(cmac, ctx)


# ---------------------------------------------------------------------------
# DISPATCH
# ---------------------------------------------------------------------------


def _analyze(cmac: MACClassification, ctx: EtherlyzerContext) -> MacIdentityResult:
    if cmac.is_zero:
        return MacIdentityResult(
            identity=MacIdentity.ALL_ZERO,
            resolution=MacResolution.IEEE_RA_RESERVED,
            form=MacForm.SPECIAL_FIXED_ADDRESS,
            cmac=cmac,
        )
    elif cmac.is_broadcast:
        return MacIdentityResult(
            identity=MacIdentity.BROADCAST,
            resolution=MacResolution.IEEE_8023_DEFINED,
            form=MacForm.SPECIAL_FIXED_ADDRESS,
            cmac=cmac,
        )

    special_lookup = fixed_address_lookup(cmac=cmac)
    if special_lookup is not None:
        return special_lookup

    match cmac.administration, cmac.delivery, cmac.is_complete():
        case (Administration.UNIVERSAL, DeliveryType.INDIVIDUAL, True):
            return inspect_uaa_unicast_complete(cmac, ctx)

        case (Administration.UNIVERSAL, DeliveryType.INDIVIDUAL, False):
            return inspect_uaa_unicast_prefix(cmac, ctx)

        case (Administration.UNIVERSAL, DeliveryType.GROUP, True):
            return inspect_uaa_mcast_complete(cmac, ctx)

        case (Administration.UNIVERSAL, DeliveryType.GROUP, False):
            return inspect_uaa_mcast_prefix(cmac, ctx)

        case (Administration.LOCAL, DeliveryType.INDIVIDUAL, True):
            return inspect_laa_unicast_complete(cmac, ctx)

        case (Administration.LOCAL, DeliveryType.INDIVIDUAL, False):
            return inspect_laa_unicast_prefix(cmac, ctx)

        case (Administration.LOCAL, DeliveryType.GROUP, True):
            return inspect_laa_mcast_complete(cmac, ctx)

        case (Administration.LOCAL, DeliveryType.GROUP, False):
            return inspect_laa_mcast_prefix(cmac, ctx)

        case _:
            raise ValueError("Unsupported MAC classification")


def analyze_mac_identity(
    classified_mac: MACClassification, context: EtherlyzerContext
) -> MacIdentityResult:
    return _analyze(classified_mac, context)
