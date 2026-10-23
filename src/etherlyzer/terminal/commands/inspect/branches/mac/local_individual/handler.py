from etherlyzer.lib.analytics.analyze_mac import SLAPQuadrant
from etherlyzer.terminal.commands.inspect.branches.mac.local_individual.aai import (
    inspect_local_individual_aai,
)
from etherlyzer.terminal.commands.inspect.branches.mac.local_individual.eli import (
    inspect_local_individual_eli,
)
from etherlyzer.terminal.commands.inspect.branches.mac.local_individual.reserved import (
    inspect_local_individual_reserved,
)
from etherlyzer.terminal.commands.inspect.branches.mac.local_individual.sai import (
    inspect_local_individual_sai,
)
from etherlyzer.terminal.commands.inspect.common import InspectionParams


def inspect_local_individual(params: InspectionParams) -> None:
    print("Local-Individual: SLAP branch")
    classified_mac = params.get("classified_mac")
    match classified_mac.slap_quadrant:
        case SLAPQuadrant.ELI:
            inspect_local_individual_eli(**params)

        case SLAPQuadrant.AAI:
            inspect_local_individual_aai(**params)

        case SLAPQuadrant.SAI:
            inspect_local_individual_sai(**params)

        case SLAPQuadrant.RESERVED:
            inspect_local_individual_reserved(**params)

        case _:
            raise ValueError(f"Unexpected SLAP quadrant: {classified_mac.slap_quadrant}")
