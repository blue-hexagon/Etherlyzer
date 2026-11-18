from dataclasses import dataclass
from enum import StrEnum

from etherlyzer.core.interpretation.mac.constants import HEX_DIGITS
from etherlyzer.core.interpretation.mac.formatting import RecognizedMacFormat, custom_format
from etherlyzer.core.interpretation.mac.normalization import normalize


class AttributionStrength(StrEnum):
    DISTINCTIVE = "Distinctive"
    INDICATIVE = "Indicative"
    COMMON = "Common"


@dataclass(frozen=True)
class MacFormatAttribution:
    sources: tuple[str, ...]
    strength: AttributionStrength


@dataclass(frozen=True, slots=True)
class MacFormatInspection:
    original: str
    recognized_formats: tuple[RecognizedMacFormat, ...]
    attributions: tuple[MacFormatAttribution, ...]


MAC_FORMAT_ATTRIBUTION = {
    RecognizedMacFormat.DOTTED_TRIPLETS_LOWER: MacFormatAttribution(
        sources=("Cisco IOS/IOS XE", "Arista EOS"),
        strength=AttributionStrength.INDICATIVE,
    ),
    RecognizedMacFormat.HYPHENATED_HALVES_LOWER: MacFormatAttribution(
        sources=("HPE", "Aruba"),
        strength=AttributionStrength.INDICATIVE,
    ),
    RecognizedMacFormat.HYPHENATED_TRIPLETS_LOWER: MacFormatAttribution(
        sources=("Huawei", "H3C"),
        strength=AttributionStrength.INDICATIVE,
    ),
    RecognizedMacFormat.COLON_SEPARATED_LOWER: MacFormatAttribution(
        sources=("Linux", "UNIX", "MacOS", "Tooling", "Human"),
        strength=AttributionStrength.COMMON,
    ),
    RecognizedMacFormat.DASH_SEPARATED_UPPER: MacFormatAttribution(
        sources=("Windows OS", "Tooling"),
        strength=AttributionStrength.INDICATIVE,
    ),
}


def _infer_formats(mac: str) -> tuple[RecognizedMacFormat, ...]:
    """Identify known formatting conventions matching a MAC address.

    The original representation is compared against each formatting
    rule. Case, separators, and hexadecimal grouping must match.

    Returns:
        Matching formatting conventions, or an empty tuple.
    """
    normalized = "".join(c for c in mac if c in HEX_DIGITS)

    if len(normalized) != 12:
        return ()

    matches = []

    for format_ in RecognizedMacFormat:
        rule = format_.value

        formatted = custom_format(
            normalized,
            block_size=rule.mac_block_size,
            separator=rule.separator,
            case=rule.mac_case,
        )

        if formatted == mac:
            matches.append(format_)

    return tuple(matches)


def _get_attributions(mac: str) -> tuple[MacFormatAttribution, ...]:
    """Return possible source attributions based on MAC formatting.

    An attribution is a heuristic, not proof of the originating
    vendor, operating system, or tool.
    """
    return tuple(
        dict.fromkeys(
            MAC_FORMAT_ATTRIBUTION[format_]
            for format_ in _infer_formats(mac)
            if format_ in MAC_FORMAT_ATTRIBUTION
        )
    )


def inspect_format(mac: str) -> MacFormatInspection:
    """Inspect a MAC address's formatting and possible origins."""

    if len(normalize(mac)) != 12:
        return MacFormatInspection(
            original=mac,
            recognized_formats=(),
            attributions=(),
        )

    recognized = _infer_formats(mac)

    attributions = tuple(
        dict.fromkeys(
            MAC_FORMAT_ATTRIBUTION[format_]
            for format_ in recognized
            if format_ in MAC_FORMAT_ATTRIBUTION
        )
    )

    return MacFormatInspection(
        original=mac,
        recognized_formats=recognized,
        attributions=attributions,
    )


if __name__ == "__main__":
    print(inspect_format("abcd.0101.defa"))
