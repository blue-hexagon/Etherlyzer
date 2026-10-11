from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from etherlyzer.terminal.commands.inspect.types import mac_inspection as mac_inspection_module


@pytest.mark.parametrize(
    ("value", "destination"),
    [
        ("00000dabcdef", "inspect_universal_individual"),
        ("00000dabcde", "inspect_universal_individual"),
        ("000000", "inspect_universal_individual"),
        ("01005e000001", "inspect_universal_group"),
        ("01005e", "inspect_universal_group"),
        ("021122334455", "inspect_local_individual"),
        ("021122334", "inspect_local_individual"),
        ("3333ff123456", "inspect_local_group"),
        ("3333ff1", "inspect_local_group"),
    ],
)
def test_all_major_branches(monkeypatch, value, destination):
    """
    Verify that each valid MAC classification (U/L + I/G) is routed to its
    expected inspection handler without executing that handler.
    """
    args = SimpleNamespace(value=value)
    index = Mock()
    flags = SimpleNamespace(show_mac_autopsy=False)

    mocked_handler = Mock()

    monkeypatch.setattr(
        mac_inspection_module,
        destination,
        mocked_handler,
    )  # Temporarily replace inspect_universal_individual with a Mock (mocked_handler)

    # Run the actual dispatch with `inspect_universal_individual` being temorarily replaced by mocked_handler
    result = mac_inspection_module.inspect_ieee_quadrants(
        args,
        index,
        flags,
    )
    # Should exit with code 0
    assert result == 0

    # And mocked_handler has registered that `inspect_universal_individual` was eventually called.
    mocked_handler.assert_called_once_with(
        args=args,
        index=index,
        eval_flags=flags,
        classified_mac=mac_inspection_module.classify_mac(args.value),
    )
