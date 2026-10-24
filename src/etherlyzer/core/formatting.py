from typing import Literal

from etherlyzer.config.knobs import etherlyzer_knobs
from etherlyzer.core.constants import HEX_DIGITS, LENIENT_TYPOS
from etherlyzer.core.normalization import normalize


class MACFormatter:
    @classmethod
    def format_default(cls, mac: str, stuff_char: str | None = None) -> str:
        """Formats a MAC address according to how etherlyze_knobs is configured ."""
        if stuff_char:
            mac = (normalize(mac) + 12 * stuff_char)[:12]
        mac = normalize(mac)
        mac = etherlyzer_knobs.mac_separator.join(
            mac[i : i + etherlyzer_knobs.mac_block_size]
            for i in range(0, len(mac), etherlyzer_knobs.mac_block_size)
        )

        return str(getattr(mac, etherlyzer_knobs.mac_case.value)())

    @classmethod
    def format(
        cls,
        mac: str,
        block_size: int,
        separator: Literal[".", ":", "-"],
        case: Literal["upper", "lower"],
        fix_typos: bool = False,
    ) -> str:
        """Custom MAC address formatting"""
        if fix_typos:
            mac = cls.fix_typos(mac)
        mac = normalize(mac)
        mac = separator.join(mac[i : i + block_size] for i in range(0, len(mac), block_size))
        if case == "upper":
            return mac.upper()
        return mac.lower()

    @classmethod
    def fix_typos(cls, mac: str) -> str:
        for c in mac:
            if c in LENIENT_TYPOS:
                mac = mac.replace(c, LENIENT_TYPOS[c])
            elif c not in HEX_DIGITS:
                mac = mac.replace(c, "#")
        return mac
