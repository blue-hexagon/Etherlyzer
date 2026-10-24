from __future__ import annotations

from etherlyzer.lib.analytics.mac_classifier import (
    Administration,
    DeliveryType,
)
from etherlyzer.terminal.commands.inspect.branches.mac.broadcast import inspect_broadcast_address
from etherlyzer.terminal.commands.inspect.branches.mac.local_group import inspect_local_group
from etherlyzer.terminal.commands.inspect.branches.mac.local_individual import (
    inspect_local_individual,
)
from etherlyzer.terminal.commands.inspect.branches.mac.universal_group import (
    inspect_universal_group,
)
from etherlyzer.terminal.commands.inspect.branches.mac.universal_individual import (
    inspect_universal_individual,
)
from etherlyzer.terminal.commands.inspect.branches.mac.zero import inspect_zero_address
from etherlyzer.terminal.commands.inspect.common import InspectionParams
from etherlyzer.terminal.commands.inspect.display import (
    display_ieee_identity,
    display_mac_autopsy,
)


def inspect_ieee_quadrants(
    params: InspectionParams,
) -> int:

    _, _, _, classified_mac = params.to_vars()
    display_ieee_identity(params)
    if params.inspect_flags.show_mac_autopsy:
        display_mac_autopsy(params)
    if params.classified_mac.is_zero:
        inspect_zero_address(params)
    elif params.classified_mac.is_broadcast:
        inspect_broadcast_address(params)
    else:
        match (classified_mac.administration, classified_mac.delivery):
            case (Administration.UNIVERSAL, DeliveryType.INDIVIDUAL):
                inspect_universal_individual(params)

            case (Administration.UNIVERSAL, DeliveryType.GROUP):
                inspect_universal_group(params)

            case (Administration.LOCAL, DeliveryType.INDIVIDUAL):
                inspect_local_individual(params)

            case (Administration.LOCAL, DeliveryType.GROUP):
                inspect_local_group(params)
            case _:
                raise ValueError("Unsupported MAC classification")

    return 0
