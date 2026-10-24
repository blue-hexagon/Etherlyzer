import argparse
from typing import cast
from unittest.mock import Mock

import pytest

from etherlyzer.core.analytics.mac_classifier import classify_mac
from etherlyzer.ieee.initialize import EtherlyzerContext
from etherlyzer.presentation.reporting.model import Report, Section
from etherlyzer.presentation.terminal.commands.inspect.branches.mac import router
from etherlyzer.presentation.terminal.commands.inspect.common import (
    InspectionParams,
    TerminalInspectFlags,
)


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
        ("000000000000", "inspect_zero_address"),
        ("ffffffffffff", "inspect_broadcast_address"),
    ],
)
def test_all_major_branches(
    monkeypatch: pytest.MonkeyPatch,
    value: str,
    destination: str,
) -> None:
    report = Report()

    params = InspectionParams(
        args=argparse.Namespace(value=value),
        context=cast(EtherlyzerContext, Mock()),
        inspect_flags=TerminalInspectFlags(
            show_mac_autopsy=False,
            show_vendor_stats=False,
            show_vendor_blocks=False,
        ),
        classified_mac=classify_mac(value),
        report=report,
    )

    # Isolate routing from the actual IEEE identity analysis.
    identity_section = Section(title="IEEE Identity")

    monkeypatch.setattr(
        router,
        "build_ieee_identity_section",
        Mock(return_value=identity_section),
    )

    mocked_handler = Mock()
    monkeypatch.setattr(router, destination, mocked_handler)

    result = router.inspect_mac_router(params)

    assert result == 0
    mocked_handler.assert_called_once_with(params)

    assert report.sections == [identity_section]
