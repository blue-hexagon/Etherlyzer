from etherlyzer.lib.analytics.analyze_mac import SLAPQuadrant
from etherlyzer.terminal.commands.inspect.common import InspectionParams
from etherlyzer.terminal.commands.inspect.display import (
    display_ieee_identifier,
    display_mac_autopsy,
)


def inspect_local_individual(params: InspectionParams) -> None:
    print("Local-Individual: SLAP branch")
    classified_mac = params.get("classified_mac")
    match classified_mac.slap_quadrant:
        case SLAPQuadrant.ELI:
            display_ieee_identifier(**params)
            display_mac_autopsy(**params)

        case SLAPQuadrant.AAI:
            display_ieee_identifier(**params)
            display_mac_autopsy(**params)

        case SLAPQuadrant.SAI:
            display_ieee_identifier(**params)
            display_mac_autopsy(**params)

        case SLAPQuadrant.RESERVED:
            display_ieee_identifier(**params)
            display_mac_autopsy(**params)

        case _:
            raise ValueError(f"Unexpected SLAP quadrant: {classified_mac.slap_quadrant}")
