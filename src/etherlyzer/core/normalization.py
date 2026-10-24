from etherlyzer.core.constants import HEX_DIGITS


def normalize(mac: str) -> str:
    mac = "".join(c for c in mac.lower() if c in HEX_DIGITS)
    return mac


def normalize_semi_strict(mac: str) -> str:
    normalized = normalize(mac)

    if len(normalized) != 12 or any(
        c.lower() not in HEX_DIGITS and c not in VALID_SEPERATORS for c in mac
    ):
        raise ValueError(f"Invalid MAC address: {mac!r}")

    return normalized
