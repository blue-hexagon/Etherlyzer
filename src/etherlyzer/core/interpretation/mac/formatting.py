from typing import Literal

from etherlyzer.config.knobs import etherlyzer_knobs
from etherlyzer.core.interpretation.mac.normalization import normalize


def to_default_format(
    mac: str,
    stuff_char: str | None = None,
) -> str:
    """Formats a MAC address according to how etherlyze_knobs is configured ."""
    if stuff_char:
        mac = (normalize(mac) + 12 * stuff_char)[:12]
    mac = normalize(mac)
    mac = etherlyzer_knobs.mac_separator.join(
        mac[i : i + etherlyzer_knobs.mac_block_size]
        for i in range(0, len(mac), etherlyzer_knobs.mac_block_size)
    )

    return str(getattr(mac, etherlyzer_knobs.mac_case.value)())


def to_customized_format(
    mac: str,
    block_size: int,
    separator: Literal[".", ":", "-"],
    case: Literal["upper", "lower"],
) -> str:
    """Custom MAC address formatting"""
    mac = normalize(mac)
    mac = separator.join(mac[i : i + block_size] for i in range(0, len(mac), block_size))
    if case == "upper":
        return mac.upper()
    return mac.lower()


def to_canonical_format(
    mac: str,
) -> str:
    """Canonical MAC address formatting"""
    return to_customized_format(mac, block_size=2, separator="-", case="upper")
