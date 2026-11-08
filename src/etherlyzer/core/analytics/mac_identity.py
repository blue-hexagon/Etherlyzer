from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, StrEnum

from etherlyzer.core.analytics.mac_classifier import (
    Administration,
    DeliveryType,
    MACClassification,
    SLAPQuadrant,
)
from etherlyzer.ieee.initialize import EtherlyzerContext


class MacForm(StrEnum):
    UAA_PREFIX = "UAA Prefix"
    UAA_ADDRESS = "UAA Address"
    LAA_PREFIX = "LAA Prefix"
    LAA_ADDRESS = "LAA Address"

    SPECIAL_FIXED_ADDRESS = "Special (Fixed Address)"
    SPECIAL_PROTOCOL_PREFIX = "Special (Protocol-Defined Prefix)"
    SPECIAL_PROTOCOL_ADDRESS = "Special (Protocol-Defined Address)"


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
    IPV6_MULTICAST_PREFIX = "IPv6 Multicast Prefix"
    IPV6_MULTICAST_ADDRESS = "IPv6 Multicast Address"
    ALL_ZERO = "All-Zero / Null Address"
    BROADCAST = "Ethernet Broadcast"


class MacResolution(StrEnum):
    # IEEE registered allocations
    REGISTERED_MAL = "Registered Block (MA-L)"
    REGISTERED_MAM = "Registered Block (MA-M)"
    REGISTERED_MAS = "Registered Block (MA-S)"
    REGISTERED_IAB = "Registered Block (IAB)"
    REGISTERED_CID = "Registered CID"

    # Unresolved allocations
    NO_REGISTRY_MATCH = "No Matching Eligible IEEE Allocation"
    NO_CID_MATCH = "No Matching IEEE CID"

    # SLAP assignment mechanisms
    SLAP_AAI = "SLAP Administrative Assignment Space"
    SLAP_SAI = "SLAP Standard Assignment Space"
    SLAP_RESERVED = "Reserved SLAP Assignment Space"

    # Standards-defined special purposes
    IPV6_MULTICAST = "IETF IPv6 Multicast Mapping (RFC 2464)"
    IEEE_RA_RESERVED = "IEEE RA Reserved"
    IEEE_8023_DEFINED = "IEEE 802.3 Defined"


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
        MacResolution.IPV6_MULTICAST,
        MacResolution.IEEE_8023_DEFINED,
    }
)

RESERVED_RESOLUTIONS = frozenset(
    {
        MacResolution.SLAP_RESERVED,
        MacResolution.IEEE_RA_RESERVED,
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

    def __post_init__(self):
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
