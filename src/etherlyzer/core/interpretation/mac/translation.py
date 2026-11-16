import string
from typing import Any


def get_arrlen_chwidth(arr: list[Any]) -> int:
    return len(str(len(arr)))  # 0-9 = 1; 10-99 = 2; 100-999 = 3 etc..


def _raw(normalized: str, *, strict: bool = True) -> bytes:
    if strict and len(normalized) != 12:
        raise ValueError("Expected a complete 48-bit MAC address")

    if len(normalized) % 2:
        raise ValueError("Hexadecimal input must have an even number of digits")

    if not all(c in string.hexdigits for c in normalized):
        raise ValueError(f"Invalid hexadecimal input: {normalized!r}")

    return bytes.fromhex(normalized)


def to_canonical(normalized: str, *, strict: bool = True) -> str:
    return _raw(normalized, strict=strict).hex("-").upper()


def to_bit_reversed(normalized: str, *, strict: bool = True) -> str:
    raw = _raw(normalized, strict=strict)
    reversed_bytes = bytes(int(f"{byte:08b}"[::-1], 2) for byte in raw)
    return reversed_bytes.hex(":").upper()


def to_decimal_bytes(
    normalized: str,
    *,
    padding: bool = False,
    strict: bool = True,
) -> str:
    raw = _raw(normalized, strict=strict)

    return " ".join(f"{byte:<3}" if padding else str(byte) for byte in raw)


def to_decimal(normalized: str, *, strict: bool = True) -> str:
    raw = _raw(normalized, strict=strict)
    return f"{int.from_bytes(raw, 'big'):,}"


def to_binary(normalized: str, *, strict: bool = True) -> str:
    return ".".join(f"{byte:08b}" for byte in _raw(normalized, strict=strict))


def to_binary_raw(normalized: str, *, strict: bool = True) -> str:
    raw = _raw(normalized, strict=strict)
    return "".join(f"{byte:08b}" for byte in raw)


def to_hex(normalized: str, *, strict: bool = True) -> str:
    raw = _raw(normalized, strict=strict)
    return f"0x{raw.hex().upper()}"


def to_hex_bytes(normalized: str, *, strict: bool = True) -> str:
    return " ".join(f"0x{byte:02X}" for byte in _raw(normalized, strict=strict))


def to_bytes(normalized: str, *, strict: bool = True) -> str:
    return _raw(normalized, strict=strict).hex(" ").upper()
