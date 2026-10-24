from etherlyzer.core.analytics.mac_classifier import SLAPQuadrant
from etherlyzer.presentation.terminal.commands.inspect.common import InspectionParams
from etherlyzer.presentation.terminal.commands.inspect.presentation.sections import (
    build_cid_registration_section,
    build_mac_autopsy_section,
)


def inspect_local_individual(params: InspectionParams) -> None:
    print("Local-Individual: SLAP branch")
    _, _, _, classified_mac, report = params.to_vars()
    report.sections.append(
        build_mac_autopsy_section(params),
    )
    match classified_mac.slap_quadrant:
        case SLAPQuadrant.ELI:
            report.sections.append(
                build_cid_registration_section(params),
            )

        case SLAPQuadrant.AAI:
            pass
        case SLAPQuadrant.SAI:
            pass

        case SLAPQuadrant.RESERVED:
            pass

        case _:
            raise ValueError(f"Unexpected SLAP quadrant: {classified_mac.slap_quadrant}")
