from etherlyzer.lib.analytics.mac_classifier import SLAPQuadrant
from etherlyzer.terminal.commands.inspect.common import InspectionParams
from etherlyzer.terminal.commands.inspect.display import (
    display_mac_autopsy,
    show_cid_registration,
)


def inspect_local_individual(params: InspectionParams) -> None:
    print("Local-Individual: SLAP branch")

    _, _, _, classified_mac = params.to_vars()
    match classified_mac.slap_quadrant:
        case SLAPQuadrant.ELI:
            display_mac_autopsy(params)
            show_cid_registration(params)

        case SLAPQuadrant.AAI:
            display_mac_autopsy(params)

        case SLAPQuadrant.SAI:
            display_mac_autopsy(params)

        case SLAPQuadrant.RESERVED:
            display_mac_autopsy(params)

        case _:
            raise ValueError(f"Unexpected SLAP quadrant: {classified_mac.slap_quadrant}")
