import pytest

from etherlyzer.lib.analytics.mac_classifier import (
    Administration,
    DeliveryType,
    SLAPQuadrant,
    classify_mac,
)


@pytest.mark.parametrize(
    ("value", "administration", "delivery"),
    [
        ("00000dabcdef", Administration.UNIVERSAL, DeliveryType.INDIVIDUAL),
        ("01005e000001", Administration.UNIVERSAL, DeliveryType.GROUP),
        ("021122334455", Administration.LOCAL, DeliveryType.INDIVIDUAL),
        ("3333ff123456", Administration.LOCAL, DeliveryType.GROUP),
    ],
)
def test_mac_classification(
    value: str, administration: Administration, delivery: DeliveryType
) -> None:
    result = classify_mac(value)

    assert result.administration == administration
    assert result.delivery == delivery


@pytest.mark.parametrize(
    ("value", "slap_quadrant"),
    [
        ("02:00:0d:ab:cd:ef:", SLAPQuadrant.AAI),
        ("02-da-bc-def--", SLAPQuadrant.AAI),
        ("02.12.34", SLAPQuadrant.AAI),
        ("121234", SLAPQuadrant.AAI),
        ("A21234", SLAPQuadrant.AAI),
        (".06000dabcdef", SLAPQuadrant.RESERVED),
        (":06dabcdef", SLAPQuadrant.RESERVED),
        ("-061234", SLAPQuadrant.RESERVED),
        ("161234", SLAPQuadrant.RESERVED),
        ("A61234", SLAPQuadrant.RESERVED),
        ("0A000dabcdef", SLAPQuadrant.ELI),
        ("0Adabcdef", SLAPQuadrant.ELI),
        ("0A1234", SLAPQuadrant.ELI),
        ("1A1234", SLAPQuadrant.ELI),
        ("AA1234", SLAPQuadrant.ELI),
        ("0E000dabcdef", SLAPQuadrant.SAI),
        ("0Edabcdef", SLAPQuadrant.SAI),
        ("0E1234", SLAPQuadrant.SAI),
        ("1E1234", SLAPQuadrant.SAI),
        ("AE1234", SLAPQuadrant.SAI),
    ],
)
def test_mac_classification_slap_quadrant(value: str, slap_quadrant: SLAPQuadrant) -> None:
    result = classify_mac(value)

    assert result.slap_quadrant == slap_quadrant


@pytest.mark.parametrize(
    "value",
    [
        "02000dabcdef1",
        "02dabcdefabc23",
        "06000",
        "02",
        "0a000",
        "0Ada",
        "00E000dabcdef",
    ],
)
def test_mac_classification_slap_quadrant_fails(value: str) -> None:
    with pytest.raises(ValueError):
        classify_mac(value)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("000000", False),
        ("00000000000", False),
        ("000000000000", True),
    ],
)
def test_zero_address(value: str, expected: bool) -> None:
    result = classify_mac(value)

    assert result.is_zero is expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("ffffff", False),
        ("fffffffffff", False),
        ("ffffffffffff", True),
    ],
)
def test_broadcast_address(value: str, expected: bool) -> None:
    result = classify_mac(value)

    assert result.is_broadcast is expected
