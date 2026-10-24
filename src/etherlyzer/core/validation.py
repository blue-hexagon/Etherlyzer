from enum import StrEnum
from string import punctuation

from etherlyzer.core.constants import HEX_DIGITS, LENIENT_TYPOS, RELAXED_TYPOS, VALID_SEPARATORS


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


class MACValidator:
    @classmethod
    def validate(cls, in_addr: str) -> tuple[str, str]:
        normalized_mac = ""
        validation_mask = ""
        valid_letter_count = 0
        typo_count = 0

        def valid_norm_mac_check() -> bool:
            return valid_letter_count + typo_count < 12

        for _, ch in enumerate(in_addr):
            if ch in HEX_DIGITS:
                if valid_norm_mac_check():
                    normalized_mac += ch.lower()
                    validation_mask += MacMaskLetter.HEX
                else:
                    normalized_mac += ch.lower()
                    validation_mask += MacMaskLetter.EXCESS_HEX
                valid_letter_count += 1
            elif ch in VALID_SEPARATORS or ch in punctuation:
                pass
            elif ch in RELAXED_TYPOS:
                if valid_norm_mac_check():
                    normalized_mac += ch
                    validation_mask += MacMaskLetter.RELAXED_TYPO
                else:
                    normalized_mac += ch
                    validation_mask += MacMaskLetter.EXCESS_RELAXED_TYPO
                typo_count += 1
            elif ch in LENIENT_TYPOS:
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
        return len(mask) == 12 and all([ch == "v" for ch in mask])  # noqa
