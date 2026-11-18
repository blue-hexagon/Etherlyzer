import string
from typing import Any


def get_arrlen_chwidth(arr: list[Any]) -> int:
    """Return the character width needed to display an array's length.

    Useful for determining the width of sequential row numbers.

    Args:
        arr: Array whose length determines the character width.

    Returns:
        Number of decimal digits in the array's length.

    Examples:
        >>> get_arrlen_chwidth([1, 2, 3])
        1
        >>> get_arrlen_chwidth(list(range(100)))
        3
    """
    return len(str(len(arr)))  # 0-9 = 1; 10-99 = 2; 100-999 = 3 etc..


def _raw(normalized: str, *, strict: bool = True) -> bytes:
    """Convert normalized hexadecimal input into raw bytes.

    Args:
        normalized: Hexadecimal string without separators or prefixes.
        strict: Require exactly 12 hexadecimal digits (48 bits).
            When False, any even number of hexadecimal digits is accepted.

    Returns:
        The decoded byte sequence.

    Raises:
        ValueError: If strict mode requires a different length, the
            hexadecimal digit count is odd, or invalid characters
            are encountered.
    """
    if strict and len(normalized) != 12:
        raise ValueError("Expected a complete 48-bit MAC address")

    if len(normalized) % 2:
        raise ValueError("Hexadecimal input must have an even number of digits")

    if not all(c in string.hexdigits for c in normalized):
        raise ValueError(f"Invalid hexadecimal input: {normalized!r}")

    return bytes.fromhex(normalized)


def to_canonical(normalized: str, *, strict: bool = True) -> str:
    """Convert a hexadecimal MAC address to canonical octet notation.

    Args:
        normalized: Hexadecimal address without separators.
        strict: Require a complete 48-bit address. Defaults to True.

    Returns:
        Uppercase hexadecimal octets separated by hyphens.

    Examples:
        >>> to_canonical("001122334455")
        '00-11-22-33-44-55'
    """
    return _raw(normalized, strict=strict).hex("-").upper()


def to_bit_reversed(normalized: str, *, strict: bool = True) -> str:
    """Reverse the bit order within each octet of a MAC address.

    Bit reversal is performed independently for each octet, not
    across the entire address. The octet order remains unchanged.

    Args:
        normalized: Hexadecimal address without separators.
        strict: Require a complete 48-bit address. Defaults to True.

    Returns:
        Bit-reversed octets in uppercase colon-separated notation.

    Examples:
        >>> to_bit_reversed("001122334455")
        '00:88:44:CC:22:AA'
    """
    raw = _raw(normalized, strict=strict)
    reversed_bytes = bytes(int(f"{byte:08b}"[::-1], 2) for byte in raw)
    return reversed_bytes.hex(":").upper()


def to_decimal_octets(
    normalized: str,
    *,
    padding: bool = False,
    strict: bool = True,
) -> str:
    """Represent each MAC address octet as a decimal integer.

    Args:
        normalized: Hexadecimal address without separators.
        padding: Left-align each decimal value within a
            three-character field, adding trailing spaces as needed.
        strict: Require a complete 48-bit address. Defaults to True.

    Returns:
        Space-separated decimal octet values in the range 0–255.

    Examples:
        >>> to_decimal_octets("001122334455")
        '0 17 34 51 68 85'
    """
    raw = _raw(normalized, strict=strict)

    return " ".join(f"{byte:<3}" if padding else str(byte) for byte in raw)


def to_decimal(normalized: str, *, strict: bool = True) -> str:
    """Convert a hexadecimal MAC address to its decimal integer value.

    The address is interpreted as an unsigned big-endian integer.

    Args:
        normalized: Hexadecimal address without separators.
        strict: Require a complete 48-bit address. Defaults to True.

    Returns:
        Decimal integer representation with comma thousands separators.

    Examples:
        >>> to_decimal("000000000001")
        '1'
    """
    raw = _raw(normalized, strict=strict)
    return f"{int.from_bytes(raw, 'big'):,}"


def to_binary(normalized: str, *, strict: bool = True) -> str:
    """Convert a MAC address to octet-grouped binary notation.

    Args:
        normalized: Hexadecimal address without separators.
        strict: Require a complete 48-bit address. Defaults to True.

    Returns:
        Eight-bit binary octets separated by periods.

    Examples:
        >>> to_binary("001122334455")
        '00000000.00010001.00100010.00110011.01000100.01010101'
    """
    return ".".join(f"{byte:08b}" for byte in _raw(normalized, strict=strict))


def to_binary_raw(normalized: str, *, strict: bool = True) -> str:
    """Convert a MAC address to a continuous binary string.

    Unlike to_binary(), the result contains no octet separators.

    Args:
        normalized: Hexadecimal address without separators.
        strict: Require a complete 48-bit address. Defaults to True.

    Returns:
        Binary representation without separators.

    Examples:
        >>> to_binary_raw("000000000001")
        '000000000000000000000000000000000000000000000001'
    """
    raw = _raw(normalized, strict=strict)
    return "".join(f"{byte:08b}" for byte in raw)


def to_hex(normalized: str, *, strict: bool = True) -> str:
    """Convert a MAC address to a prefixed hexadecimal string.

    Args:
        normalized: Hexadecimal address without separators.
        strict: Require a complete 48-bit address. Defaults to True.

    Returns:
        Uppercase hexadecimal representation prefixed with ``0x``.

    Examples:
        >>> to_hex("001122334455")
        '0x001122334455'
    """
    raw = _raw(normalized, strict=strict)
    return f"0x{raw.hex().upper()}"


def to_hex_bytes(normalized: str, *, strict: bool = True) -> str:
    """Represent each MAC address octet as a prefixed hexadecimal byte.

    Args:
        normalized: Hexadecimal address without separators.
        strict: Require a complete 48-bit address. Defaults to True.

    Returns:
        Space-separated uppercase hexadecimal octets, each prefixed
        with ``0x``.

    Examples:
        >>> to_hex_bytes("001122334455")
        '0x00 0x11 0x22 0x33 0x44 0x55'
    """
    return " ".join(f"0x{byte:02X}" for byte in _raw(normalized, strict=strict))


def to_bytes(normalized: str, *, strict: bool = True) -> str:
    """Represent a MAC address as space-separated hexadecimal octets.

    This function returns a formatted string, not a bytes object.

    Args:
        normalized: Hexadecimal address without separators.
        strict: Require a complete 48-bit address. Defaults to True.

    Returns:
        Space-separated uppercase hexadecimal octets without prefixes.

    Examples:
        >>> to_bytes("001122334455")
        '00 11 22 33 44 55'
    """
    return _raw(normalized, strict=strict).hex(" ").upper()
