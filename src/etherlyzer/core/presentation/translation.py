import string
from dataclasses import dataclass
from typing import Any, ClassVar


def get_arrlen_chwidth(arr: list[Any]) -> int:
    return len(str(len(arr)))  # 0-9 = 1; 10-99 = 2; 100-999 = 3 etc..


@dataclass(slots=True)
class PresentationTranslator:
    strict: ClassVar[bool] = True  # Strict validation means len == 12

    @classmethod
    def validate(cls, normalized: str) -> None:
        if (
            len(normalized) != 12 or not all(c in string.hexdigits for c in normalized)
        ) and cls.strict:
            raise ValueError(f"{normalized} is not a valid 6-12-ch hex string")

    @classmethod
    def _raw(cls, normalized: str) -> bytes:
        if not len(normalized) % 2 == 0:
            raise ValueError(f"Invalid hexadecimal input '{normalized}': odd number of digits")
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
        ln = len(normalized)

        return f"0x{val:0{ln}X}"

    @classmethod
    def to_hex_bytes(cls, normalized: str) -> str:
        return " ".join(f"0x{byte:02X}" for byte in cls._raw(normalized))

    @classmethod
    def to_bytes(cls, normalized: str) -> str:
        return cls._raw(normalized).hex(" ").upper()
