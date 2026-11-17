
import pytest

from etherlyzer.core.interpretation.ethertype.classifier import (
    EtherTypeFieldType,
    get_ethertype_struct,
)


@pytest.mark.parametrize(
    ("hexval", "resolved"),
    [
        (0x0000, EtherTypeFieldType.LENGTH),
        (0x0000 + 1, EtherTypeFieldType.LENGTH),
        (0x05DC - 1, EtherTypeFieldType.LENGTH),
        (0x05DC, EtherTypeFieldType.LENGTH),
        (0x05DC + 1, EtherTypeFieldType.UNDEFINED),
        (0x0600 - 1, EtherTypeFieldType.UNDEFINED),
        (0x0600, EtherTypeFieldType.ETHERTYPE),
        (0x0600 + 1, EtherTypeFieldType.ETHERTYPE),
        (0xFFFF, EtherTypeFieldType.ETHERTYPE),
    ],
)
def test_ethertype_fieldtype(
    hexval: int,
    resolved: EtherTypeFieldType,
) -> None:
    value = f"{hexval:04X}"
    struct = get_ethertype_struct(value)

    assert struct.field_type == resolved
