from dataclasses import dataclass
from enum import Enum
from typing import Literal

from etherlyzer.config.knobs import etherlyzer_knobs
from etherlyzer.core.interpretation.mac.normalization import normalize


@dataclass(slots=True, frozen=True)
class MacFormatRule:
    mac_block_size: int = 2
    mac_case: Literal["upper", "lower"] = "upper"
    separator: str = "-"

    def __post_init__(self):
        if len(self.separator) > 1:
            raise ValueError("Mac separator can only be 1ch")


class RecognizedMacFormat(Enum):
    HYPHENATED_TRIPLETS_LOWER = MacFormatRule(
        mac_block_size=4,
        mac_case="lower",
        separator="-",
    )
    HYPHENATED_TRIPLETS_UPPER = MacFormatRule(
        mac_block_size=4,
        mac_case="upper",
        separator="-",
    )
    DOTTED_TRIPLETS_LOWER = MacFormatRule(
        mac_block_size=4,
        mac_case="lower",
        separator=".",
    )
    DOTTED_TRIPLETS_UPPER = MacFormatRule(
        mac_block_size=4,
        mac_case="upper",
        separator=".",
    )
    HYPHENATED_HALVES_LOWER = MacFormatRule(
        mac_block_size=6,
        mac_case="lower",
        separator="-",
    )
    HYPHENATED_HALVES_UPPER = MacFormatRule(
        mac_block_size=6,
        mac_case="upper",
        separator="-",
    )
    COLON_SEPARATED_LOWER = MacFormatRule(
        mac_block_size=2,
        mac_case="lower",
        separator=":",
    )
    COLON_SEPARATED_UPPER = MacFormatRule(
        mac_block_size=2,
        mac_case="upper",
        separator=":",
    )
    DASH_SEPARATED_LOWER = MacFormatRule(
        mac_block_size=2,
        mac_case="lower",
        separator="-",
    )
    DASH_SEPARATED_UPPER = MacFormatRule(
        mac_block_size=2,
        mac_case="upper",
        separator="-",
    )
    NORMALIZED_LOWER = MacFormatRule(
        mac_block_size=12,
        mac_case="lower",
        separator="",
    )
    NORMALIZED_UPPER = MacFormatRule(
        mac_block_size=12,
        mac_case="upper",
        separator="",
    )
    SPACE_SEPARATED_LOWER = MacFormatRule(
        mac_block_size=2,
        mac_case="lower",
        separator=" ",
    )
    SPACE_SEPARATED_UPPER = MacFormatRule(
        mac_block_size=2,
        mac_case="upper",
        separator=" ",
    )
    SPACE_SEPARATED_TRIPLETS_LOWER = MacFormatRule(
        mac_block_size=4,
        mac_case="lower",
        separator=" ",
    )

    SPACE_SEPARATED_TRIPLETS_UPPER = MacFormatRule(
        mac_block_size=4,
        mac_case="upper",
        separator=" ",
    )


def default_format(
    mac: str,
    stuff_char: str | None = None,
) -> str:
    """Format a MAC address using EtherLyzer's configured preferences.

    Normalizes the input and applies the MAC address formatting
    settings defined in ``etherlyzer_knobs``, including the
    separator, hexadecimal block size, and letter casing.

    Optionally pads the normalized input to a maximum of
    12 hexadecimal characters before formatting.

    Args:
        mac: MAC address or hexadecimal prefix to format.
        stuff_char: Optional character used to right-pad the
            normalized input to 12 characters. When omitted,
            the original normalized length is preserved.

    Returns:
        The formatted MAC address according to the active
        EtherLyzer configuration.

    Notes:
        The output depends on the current configuration.
        Identical inputs may produce different representations
        when formatting preferences differ.

        Padding does not validate or guarantee that the
        resulting address represents a valid EUI-48 assignment.
    """
    if stuff_char:
        mac = (normalize(mac) + 12 * stuff_char)[:12]
    mac = normalize(mac)
    mac = etherlyzer_knobs.mac_separator.join(
        mac[i : i + etherlyzer_knobs.mac_block_size]
        for i in range(0, len(mac), etherlyzer_knobs.mac_block_size)
    )

    return str(getattr(mac, etherlyzer_knobs.mac_case.value)())


def custom_format(
    mac: str,
    block_size: int,
    separator: Literal[".", ":", "-"],
    case: Literal["upper", "lower"],
) -> str:
    """Format a MAC address using explicitly specified preferences.

    Normalizes the input and groups its hexadecimal characters
    into blocks of the requested size, separated by the specified
    delimiter and converted to the requested letter casing.

    Unlike ``to_default_format()``, this function does not
    depend on EtherLyzer's global formatting configuration.

    Args:
        mac: MAC address or hexadecimal prefix to format.
        block_size: Number of hexadecimal characters per block.
            Must be a positive integer.
        separator: Character inserted between hexadecimal blocks.
            Supported values are ``.``, ``:``, and ``-``.
        case: Letter casing of hexadecimal characters.
            Either ``upper`` or ``lower``.

    Returns:
        The normalized MAC address formatted according to
        the supplied preferences.

    Examples:
        >>> custom_format(
        ...     "001122334455", 4, ".", "lower"
        ... )
        '0011.2233.4455'

        >>> custom_format(
        ...     "001122334455", 2, ":", "upper"
        ... )
        '00:11:22:33:44:55'
    """
    mac = normalize(mac)
    mac = separator.join(mac[i : i + block_size] for i in range(0, len(mac), block_size))
    if case == "upper":
        return mac.upper()
    return mac.lower()


def canonical_format(
    mac: str,
) -> str:
    """Convert a MAC address to its canonical hexadecimal representation.

    Normalizes the input and formats it using uppercase
    hexadecimal octets separated by hyphens.

    The function preserves the length of the normalized input,
    allowing incomplete MAC addresses and prefixes to be
    formatted without requiring a complete 48-bit address.

    Args:
        mac: MAC address or hexadecimal prefix to format.

    Returns:
        The canonical representation using uppercase hexadecimal
        characters and hyphen-separated octets.

    Examples:
        >>> canonical_format("001122334455")
        '00-11-22-33-44-55'

        >>> canonical_format("001122")
        '00-11-22'

    Notes:
        Canonical formatting changes the textual representation
        only. It does not verify whether the address is registered,
        assigned, or structurally valid.
    """
    return custom_format(mac, block_size=2, separator="-", case="upper")
