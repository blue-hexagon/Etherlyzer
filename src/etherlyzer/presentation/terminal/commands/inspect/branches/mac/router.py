from __future__ import annotations

from etherlyzer.core.analytics.mac_classifier import (
    Administration,
    DeliveryType,
)
from etherlyzer.presentation.reporting.renderers.text import TextRenderer
from etherlyzer.presentation.terminal.commands.inspect.branches.mac.broadcast import (
    inspect_broadcast_address,
)
from etherlyzer.presentation.terminal.commands.inspect.branches.mac.local_group import (
    inspect_local_group,
)
from etherlyzer.presentation.terminal.commands.inspect.branches.mac.local_individual import (
    inspect_local_individual,
)
from etherlyzer.presentation.terminal.commands.inspect.branches.mac.universal_group import (
    inspect_universal_group,
)
from etherlyzer.presentation.terminal.commands.inspect.branches.mac.universal_individual import (
    inspect_universal_individual,
)
from etherlyzer.presentation.terminal.commands.inspect.branches.mac.zero import inspect_zero_address
from etherlyzer.presentation.terminal.commands.inspect.common import InspectionParams
from etherlyzer.presentation.terminal.commands.inspect.presentation.sections import (
    build_mac_autopsy_section,
)


def inspect_mac_router(
    params: InspectionParams,
) -> int:

    _, _, _, classified_mac, report = params.to_vars()

    report.sections.append(build_mac_autopsy_section(params))

    if params.classified_mac.is_zero:
        inspect_zero_address(params)
    elif params.classified_mac.is_broadcast:
        inspect_broadcast_address(params)
    else:
        match (classified_mac.administration, classified_mac.delivery):
            case (Administration.UNIVERSAL, DeliveryType.INDIVIDUAL):
                found_uaa_i = inspect_universal_individual(params)

            case (Administration.UNIVERSAL, DeliveryType.GROUP):
                found_uaa_g = inspect_universal_group(params)

            case (Administration.LOCAL, DeliveryType.INDIVIDUAL):
                found_laa_i = inspect_local_individual(params)

            case (Administration.LOCAL, DeliveryType.GROUP):
                found_laa_g = inspect_local_group(params)
            case _:
                raise ValueError("Unsupported MAC classification")  # Never..
    print(TextRenderer().render(report))
    return 0
