import pytest

from etherlyzer.core.formatting import MACFormatter


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("001122334455", "00:11:22:33:44:55"),
        ("00-11-22-33-44-FF", "00:11:22:33:44:ff"),
        ("0011.  2233.4455", "00:11:22:33:44:55"),
        ("00 11 ab 33 44 55", "00:11:ab:33:44:55"),
        (" 00.11.22.33.44.55", "00:11:22:33:44:55"),
        ("00.1122 33.44-FF   ", "00:11:22:33:44:ff"),
        (" --00.11__  22 33.44.-.--FF   ", "00:11:22:33:44:ff"),
    ],
)
def test_normalizes_mac_formats(value: str, expected: str) -> None:
    assert (
        MACFormatter.format(mac=value, block_size=2, separator=":", case="lower", fix_typos=False)
        == expected
    )
