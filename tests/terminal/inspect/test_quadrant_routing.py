import argparse
from types import SimpleNamespace
from typing import cast
from unittest.mock import Mock

import pytest
from _pytest.monkeypatch import MonkeyPatch

from etherlyzer.lib.analytics.mac_classifier import classify_mac
from etherlyzer.terminal.commands.inspect.branches.mac import router
from etherlyzer.terminal.commands.inspect.branches.mac.router import inspect_ieee_quadrants
from etherlyzer.terminal.commands.inspect.common import TerminalInspectFlags


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
def test_all_major_branches(monkeypatch: MonkeyPatch, value: str, destination: str) -> None:
    """
    Verify that each valid MAC classification (U/L + I/G) is routed to its
    expected inspection handler without executing that handler.
    """
    args = SimpleNamespace(value=value)
    index = Mock()
    flags = SimpleNamespace(show_mac_autopsy=False)

    mocked_handler = Mock()

    monkeypatch.setattr(
        router,
        destination,
        mocked_handler,
    )  # Temporarily replace inspect_universal_individual with a Mock (mocked_handler)

    # Run the actual dispatch with `inspect_universal_individual` being temorarily replaced by mocked_handler
    result = inspect_ieee_quadrants(
        cast(argparse.Namespace, cast(object, args)),
        index,
        cast(TerminalInspectFlags, cast(object, flags)),
    )
    # Should exit with code 0
    assert result == 0

    # And mocked_handler has registered that `inspect_universal_individual` was eventually called.
    mocked_handler.assert_called_once_with(
        args=args,
        index=index,
        inspect_flags=flags,
        classified_mac=classify_mac(args.value),
    )
