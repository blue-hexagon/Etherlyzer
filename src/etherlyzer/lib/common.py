HEX_DIGITS = frozenset("0123456789ABCDEFabcdef")
VALID_SEPERATORS = frozenset(" -.:")
STRICT_TYPOS: dict[str, str] = {" ": "", "\t": ""}
RELAXED_TYPOS: dict[str, str] = {
    **STRICT_TYPOS,
    "o": "0",
    "O": "0",
}

LENIENT_TYPOS: dict[str, str] = {
    **RELAXED_TYPOS,
    "i": "1",
    "I": "1",
    "l": "1",
    "L": "1",
    "s": "5",
    "S": "5",
    "ø": "0",
    "Ø": "0",
}
