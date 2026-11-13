def flip_ig_bit(mac: str) -> str:
    first = int(mac[:2], 16) ^ 0x01
    return f"{first:02X}{mac[2:]}"
