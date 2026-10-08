import pytest

from etherlyzer.formatters import MACFormatter


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("001122334455", "00:11:22:33:44:55"),
        ("00-11-22-33-44-55", "00:11:22:33:44:55"),
        ("0011.2233.4455", "00:11:22:33:44:55"),
        ("00 11 22 33 44 55", "00:11:22:33:44:55"),
    ],
)
def test_normalizes_mac_formats(value, expected):
    assert MACFormatter.format_custom(mac=value, block_size=2, separator=":", case="lower", fix_typos=False) == expected
