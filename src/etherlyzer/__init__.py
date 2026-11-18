from functools import cache
from importlib.metadata import PackageNotFoundError, version

from etherlyzer.bootstrap import EtherlyzerContext, initialize_etherlyzer
from etherlyzer.core.interpretation.ethertype.classifier import (
    EtherTypeFieldType,
    EtherTypeStruct,
    get_ethertype_struct,
)
from etherlyzer.core.interpretation.mac import extraction, formatting, translation
from etherlyzer.core.interpretation.mac.classifier import (
    MacStructure,
    get_mac_structure,
)
from etherlyzer.core.interpretation.mac.constants import (
    HEX_DIGITS,
    LENIENT_TYPOS,
    RELAXED_TYPOS,
    STRICT_TYPOS,
)
from etherlyzer.core.interpretation.mac.inspection import (
    MacForm,
    MacIdentity,
    MacIdentityResult,
    MacResolution,
    inspect,
)
from etherlyzer.core.interpretation.mac.normalization import normalize, normalize_strict
from etherlyzer.domain.entry.ethertype import EtherTypeEntry
from etherlyzer.domain.entry.mac import MACAllocationEntry

try:
    __version__ = version("etherlyzer")
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"


@cache
def _get_context() -> EtherlyzerContext:
    return initialize_etherlyzer()


def inspect_mac(mac: str) -> MacIdentityResult:
    """Inspect the structure and identity of an Ethernet MAC address.

    Performs standards-aware analysis of a hexadecimal MAC
    address or prefix, combining structural classification,
    IEEE registry information, and recognized protocol-defined
    address identities.

    Unlike lookup_mac(), this function does more than resolve
    an IEEE registration. It examines the address itself and
    explains its addressing form, identity, and resolution.

    The inspection considers:

    - Individual versus group addressing (I/G).
    - Universal versus local administration (U/L).
    - IEEE 802c SLAP quadrants where applicable.
    - Special, reserved, and protocol-defined addresses.
    - Applicable IEEE registration information.
    - Structural and registration-related assessments.

    Args:
        mac: Hexadecimal MAC address or supported prefix.
            Supported input representations depend on the
            underlying normalization and parsing rules.

    Returns:
        MacIdentityResult: A structured inspection containing:

        - structure: Normalized address and structural properties.
        - form: Address form classification.
        - identity: Identified address identity.
        - resolution: Basis for the identity resolution.
        - assessment: Classification and evidence assessments.

    Notes:
        A matching IEEE allocation does not establish that the
        address was legitimately assigned to a particular device.

        Likewise, an address without an ordinary vendor
        registration may still have a standards-defined identity.

    Examples:
        Inspect an IPv6 multicast address:

        >>> result = inspect_mac("33:33:00:00:00:01")
        >>> result.identity.value
        'IPv6 Multicast Address'

        Inspect an individual address:

        >>> result = inspect_mac("00:00:0C:12:34:56")
        >>> result.structure.is_complete
        True

        >>> result.structure.is_broadcast
        False

    See Also:
        lookup_mac: Resolve the corresponding IEEE allocation.
        inspect_ethertype: Inspect an Ethernet Type/Length field.
    """
    return inspect(get_mac_structure(mac), _get_context())


def lookup_mac(mac: str) -> MACAllocationEntry | None:
    """Resolve a MAC address or prefix against IEEE MAC allocations.

    Performs a registry-backed lookup using EtherLyzer's
    locally indexed IEEE allocation datasets.

    Resolution considers supported IEEE assignment scopes,
    including MA-L, MA-M, MA-S, and legacy IAB allocations.

    This operation is concerned with registration information.
    It does not independently establish the protocol-defined
    identity or legitimacy of an observed MAC address.

    Args:
        mac: MAC address or supported hexadecimal prefix
            to resolve against the local IEEE registries.

    Returns:
        MACAllocationEntry | None: The matching IEEE allocation
        entry, including registry information, assignment,
        organization name, and associated metadata.

        Returns None when no eligible allocation is found.

    Notes:
        A matching IEEE allocation identifies the registered
        allocation holder, not necessarily the manufacturer,
        owner, or identity of an observed network device.

        Registry lookup requires the corresponding datasets
        to be available in the local EtherLyzer context.

    Examples:
        >>> allocation = lookup_mac("00:00:0C:12:34:56")
        >>> if allocation:
        ...     print(allocation.registry)
        MA-L

    See Also:
        inspect_mac: Inspect MAC address structure and identity.
    """
    return _get_context().indexes.mac.lookup(mac)


def lookup_ethertype(ethertype: str) -> EtherTypeEntry | None:
    """Look up an Ethernet protocol identifier in the IEEE registry.

    Resolves a hexadecimal EtherType identifier against the
    locally indexed IEEE EtherType registration dataset.

    Unlike inspect_ethertype(), this function performs only
    registry resolution and does not independently classify
    the Ethernet Length/Type field.

    Args:
        ethertype: Hexadecimal EtherType identifier to look up.
            Leading and trailing whitespace is stripped,
            and alphabetic hexadecimal digits are normalized
            to uppercase before registry lookup.

    Returns:
        EtherTypeEntry | None: The matching IEEE EtherType
        registration, including available protocol and
        organization metadata.

        Returns None if no matching registration exists.

    Notes:
        An absent registration does not by itself establish
        whether a numeric value is a valid EtherType.

        For structural classification of the complete
        16-bit Length/Type field, use inspect_ethertype().

    Examples:
        >>> entry = lookup_ethertype("0800")
        >>> if entry:
        ...     print(entry.assignment)
        0800

    See Also:
        inspect_ethertype: Classify a Length/Type value and
            enrich it with available registry information.
    """
    return _get_context().indexes.ethertype.lookup(ethertype.strip().upper())


def inspect_ethertype(ethertype: str) -> EtherTypeStruct:
    """Inspect an Ethernet 16-bit Length/Type field.

    Performs structural classification of the supplied
    hexadecimal value and enriches recognized EtherType
    values with locally available IEEE registration data.

    The IEEE 802.3 Length/Type field is interpreted using
    the following numeric boundaries:

        0x0000-0x05DC: IEEE 802.3 length field (0-1500).

        0x05DD-0x05FF: Undefined Length/Type values.

        0x0600-0xFFFF: EtherType value space.

    For values classified as EtherTypes, the function
    attempts to resolve the identifier against the local
    IEEE EtherType registry.

    The inspection also recognizes the OUI Extended
    EtherType (0x88B7), which requires additional OUI
    and protocol identifier fields for complete
    protocol identification.

    Args:
        ethertype: Hexadecimal representation of a
            16-bit Ethernet Length/Type field.

    Returns:
        EtherTypeStruct: Structured interpretation containing
        the normalized identifier, numeric value, field
        classification, and applicable registry metadata.

        For IEEE 802.3 length values, the result exposes
        the interpreted payload length.

        For EtherTypes, available fields include registry
        match status, protocol description, organization
        information, and OUI-extension requirements.

    Notes:
        A value within the EtherType range does not
        necessarily have an IEEE registry assignment.

        Registry resolution is not attempted for values
        classified as length fields or undefined values.

    Examples:
        Inspect an IEEE 802.3 length field:

        >>> result = inspect_ethertype("05DC")
        >>> result.is_ethertype
        False
        >>> result.length_value
        1500

        Inspect an EtherType:

        >>> result = inspect_ethertype("0800")
        >>> result.is_ethertype
        True

        Inspect an OUI Extended EtherType:

        >>> result = inspect_ethertype("88B7")
        >>> result.requires_oui_pid
        True

    See Also:
        lookup_ethertype: Retrieve IEEE registration
            information without structural classification.
    """
    structure = get_ethertype_struct(ethertype)

    if not structure.is_ethertype:
        return structure

    entry = lookup_ethertype(ethertype)

    return get_ethertype_struct(
        structure.normalized,
        entry=entry,
    )


__all__ = [  # noqa: RUF022
    "HEX_DIGITS",
    "LENIENT_TYPOS",
    "RELAXED_TYPOS",
    "STRICT_TYPOS",
    "EtherTypeStruct",
    "MacForm",
    "MacIdentity",
    "MacIdentityResult",
    "MacResolution",
    "MacStructure",
    "extraction",
    "formatting",
    "inspect_ethertype",
    "EtherTypeFieldType",
    "inspect_mac",
    "lookup_mac",
    "normalize",
    "normalize_strict",
    "translation",
]
