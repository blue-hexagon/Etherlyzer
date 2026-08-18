from typing import Literal

from etherlyzer.conf import config


class MACFormatter:
    HEX_DIGITS = frozenset("0123456789ABCDEFabcdef")
    STRICT_TYPOS: dict[str, str] = {" ": ""}
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
            mac[i : i + config.mac_block_size] for i in range(0, len(mac), config.mac_block_size)
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
        mac = separator.join(mac[i : i + block_size] for i in range(0, len(mac), block_size))
        if case == "upper":
            return mac.upper()
        return mac.lower()

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
            no_strict=False,
        )
    )
