import string
from dataclasses import dataclass
from typing import Any


def get_arrlen_chwidth(arr: list[Any]) -> int:
    return len(str(len(arr)))


@dataclass(slots=True)
class PresentationTranslator:
    @staticmethod
    def validate(normalized: str) -> None:
        if len(normalized) != 12 or not all(c in string.hexdigits for c in normalized):
            raise ValueError(normalized)

    @classmethod
    def _raw(cls, normalized: str) -> bytes:
        cls.validate(normalized)
        return bytes.fromhex(normalized)

    @classmethod
    def to_canonical(cls, normalized: str) -> str:
        return cls._raw(normalized).hex("-").upper()

    @classmethod
    def to_bit_reversed(cls, normalized: str) -> str:
        reversed_bytes = bytes(int(f"{byte:08b}"[::-1], 2) for byte in cls._raw(normalized))
        return reversed_bytes.hex(":").upper()

    @classmethod
    def to_decimal_bytes(cls, normalized: str, padding: bool = False) -> str:
        return (
            " ".join(f"{str(byte).ljust(3, ' ')}" for byte in cls._raw(normalized))
            if padding
            else " ".join(str(byte) for byte in cls._raw(normalized))
        )

    @classmethod
    def to_decimal(cls, normalized: str) -> str:
        val = int.from_bytes(cls._raw(normalized), byteorder="big")
        return f"{val:,}"

    @classmethod
    def to_binary(cls, normalized: str) -> str:
        return ".".join(f"{byte:08b}" for byte in cls._raw(normalized))

    @classmethod
    def to_binary_raw(cls, normalized: str) -> str:
        return f"{int.from_bytes(cls._raw(normalized), byteorder='big'):048b}"

    @classmethod
    def to_hex(cls, normalized: str) -> str:
        val = int.from_bytes(cls._raw(normalized), byteorder="big")
        return f"0x{val:012X}"

    @classmethod
    def to_hex_bytes(cls, normalized: str) -> str:
        return " ".join(f"0x{byte:02X}" for byte in cls._raw(normalized))

    @classmethod
    def to_bytes(cls, normalized: str) -> str:
        return cls._raw(normalized).hex(" ").upper()
