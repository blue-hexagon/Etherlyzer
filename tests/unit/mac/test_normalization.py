import pytest

from etherlyzer.lib.normalization import normalize


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("00 1a 2b 3c 4d 5e", "001a2b3c4d5e"),
        ("001a 2b3c 4d5e", "001a2b3c4d5e"),
        ("001a2b 3c4d5e", "001a2b3c4d5e"),
        ("001a2b3c 4d5e", "001a2b3c4d5e"),
        ("0 0 1 a 2 b 3 c 4 d 5 e", "001a2b3c4d5e"),
        (" 001a2b3c4d5e", "001a2b3c4d5e"),
        ("001a2b3c4d5e", "001a2b3c4d5e"),
        (" 001a2b3c4d5e", "001a2b3c4d5e"),
        ("  001a2b3c4d5e", "001a2b3c4d5e"),
        ("001a2b3c4d5e", "001a2b3c4d5e"),
        ("  001a2b3c4d5e", "001a2b3c4d5e"),
        ("00 : 1a : 2b : 3c : 4d : 5e", "001a2b3c4d5e"),
        ("00 - 1a - 2b - 3c - 4d - 5e", "001a2b3c4d5e"),
        ("001a . 2b3c . 4d5e", "001a2b3c4d5e"),
    ],
)
def test_normalizes_mac(value: str, expected: str) -> None:
    assert normalize(value) == expected
