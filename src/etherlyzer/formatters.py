from enum import StrEnum
from typing import Literal

from etherlyzer.misc.settings import config
from string import punctuation


class MacMaskLetter(StrEnum):
    EXCESS_INVALID = "I"
    INVALID = "i"
    EXCESS_HEX = "V"
    HEX = "v"
    EXCESS_RELAXED_TYPO = "R"
    RELAXED_TYPO = "r"
    EXCESS_LENIENT_TYPO = "L"
    LENIENT_TYPO = "l"
    PUNCTUATION = "p"
    SEPERATOR = "-"


class MACFormatter:
    HEX_DIGITS = frozenset("0123456789ABCDEFabcdef")
    VALID_SEPERATORS = frozenset(" -.:")
    STRICT_TYPOS: dict[str, str] = {" ": "", "\t": ""}
    RELAXED_TYPOS: dict[str, str] = {  # noqa: RUF012
        **STRICT_TYPOS,
        "o": "0",
        "O": "0",
    }

    LENIENT_TYPOS: dict[str, str] = {  # noqa: RUF012
        **RELAXED_TYPOS,
        "i": "1",
        "I": "1",
        "l": "1",
        "L": "1",
        "s": "5",
        "S": "5",
    }

    @classmethod
    def format_default(cls, mac: str) -> str:
        mac = cls.normalize(mac)
        mac = config.mac_separator.join(
            mac[i: i + config.mac_block_size] for i in range(0, len(mac), config.mac_block_size)
        )

        return getattr(mac, config.mac_case.value)()

    @classmethod
    def format(
            cls,
            mac: str,
            block_size: int,
            separator: Literal[".", ":", "-"],
            case: Literal["upper", "lower"],
            fix_typos: bool,
    ) -> str:
        if fix_typos:
            mac = cls.fix_typos(mac)
        mac = cls.normalize(mac)
        if len(mac) > 12:
            raise ValueError(f"Malformed MAC address is of length: {len(mac)}!")
        mac = separator.join(mac[i: i + block_size] for i in range(0, len(mac), block_size))
        if case == "upper":
            return mac.upper()
        return mac.lower()

    @classmethod
    def validate(cls, in_addr: str) -> tuple[str, str]:
        normalized_mac = ""
        validation_mask = ""
        valid_letter_count = 0
        typo_count = 0

        def valid_norm_mac_check():
            return valid_letter_count + typo_count < 12

        for idx, ch in enumerate(in_addr):
            if ch in cls.HEX_DIGITS:
                if valid_norm_mac_check():
                    normalized_mac += ch.lower()
                    validation_mask += MacMaskLetter.HEX
                else:
                    normalized_mac += ch.lower()
                    validation_mask += MacMaskLetter.EXCESS_HEX
                valid_letter_count += 1
            elif ch in cls.VALID_SEPERATORS:
                pass
            elif ch in punctuation:
                pass
            elif ch in cls.RELAXED_TYPOS:
                if valid_norm_mac_check():
                    normalized_mac += ch
                    validation_mask += MacMaskLetter.RELAXED_TYPO
                else:
                    normalized_mac += ch
                    validation_mask += MacMaskLetter.EXCESS_RELAXED_TYPO
                typo_count += 1
            elif ch in cls.LENIENT_TYPOS:
                if valid_norm_mac_check():
                    normalized_mac += ch
                    validation_mask += MacMaskLetter.LENIENT_TYPO
                else:
                    normalized_mac += ch
                    validation_mask += MacMaskLetter.EXCESS_LENIENT_TYPO
                typo_count += 1
            else:
                if valid_norm_mac_check():
                    normalized_mac += ch
                    validation_mask += MacMaskLetter.INVALID
                else:
                    normalized_mac += ch
                    validation_mask += MacMaskLetter.EXCESS_INVALID
        if len(validation_mask) < 12:
            validation_mask = validation_mask.ljust(12, "M")
        return normalized_mac, validation_mask

    @classmethod
    def mask_is_valid(cls, mask: str) -> bool:
        return len(mask) == 12 and all([ch == "v" for ch in mask])

    @classmethod
    def normalize(cls, mac: str) -> str:
        mac = "".join(c for c in mac.lower() if c in cls.HEX_DIGITS)
        return mac

    @classmethod
    def fix_typos(cls, mac: str) -> str:
        for c in mac:
            if c in cls.LENIENT_TYPOS:
                mac = mac.replace(c, cls.LENIENT_TYPOS[c])
            elif c not in cls.HEX_DIGITS:
                mac = mac.replace(c, "#")
        return mac


if __name__ == "__main__":
    print(
        MACFormatter().format(
            mac="ab:cd:ef:fg:de:dd",
            separator=":",
            block_size=2,
            case="upper",
            fix_typos=False,
        )
    )
