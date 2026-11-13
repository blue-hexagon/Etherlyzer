from __future__ import annotations

from etherlyzer.application.cli.commands.inspect.branch_macaddr_presentation import (
    build_cid_registration_section,
    build_mac_autopsy_section,
)
from etherlyzer.application.cli.commands.inspect.branch_macaddr_uaa_ig import (
    inspect_universal,
)
from etherlyzer.application.cli.commands.inspect.common import (
    MacInspectionParams,
)
from etherlyzer.core.interpretation.mac.classifier import (
    Administration,
    DeliveryType,
    SLAPQuadrant,
)
from etherlyzer.core.interpretation.mac.identifier import analyze_mac_identity
from etherlyzer.presentation.reporting.renderers.text import TextRenderer


def mac_inspection_router(
    params: MacInspectionParams,
) -> int:
    """
    Orchestrate MAC address inspection in two stages:

    1. Analysis (Autopsy):
       Establish the address's structural properties, IEEE identity,
       classification, and registration status.

    2. Enrichment:
       Conditionally append additional information based on the
       address's classification and applicable IEEE allocation rules.

    Special addresses, such as all-zero and broadcast, require no
    further allocation-based enrichment.

    ELI addresses may be enriched with CID registration details,
    regardless of their individual/group designation. Universally
    administered addresses may be enriched with IEEE allocation
    metadata, vendor correlations, and associated address blocks.

    Group-address enrichment respects allocation-specific restrictions,
    including the exclusion of legacy IAB assignments.

    This function serves as the entry point for both stages.
    """
    classified_mac = params.classified_mac
    context = params.context
    report = params.report

    if classified_mac is None:
        raise ValueError("Unexpected MAC classification")

    mac_identity = analyze_mac_identity(
        classified_mac,
        context,
    )
    report.sections.append(
        build_mac_autopsy_section(
            params,
            mac_identity.identity,
            mac_identity.resolution,
            mac_identity.form,
            mac_identity.assessment,
        ),
    )

    if classified_mac.is_zero or classified_mac.is_broadcast:
        pass
    else:
        match (
            classified_mac.administration,
            classified_mac.delivery,
        ):
            case (Administration.UNIVERSAL, _):
                inspect_universal(params)  # U/G branch

            case (Administration.LOCAL, _) if classified_mac.slap_quadrant == SLAPQuadrant.ELI:
                report.previous_section.append(
                    build_cid_registration_section(params, clear_ig_bit=True),
                )
            case (Administration.LOCAL, DeliveryType.INDIVIDUAL):
                match classified_mac.slap_quadrant:
                    case SLAPQuadrant.AAI:
                        pass
                    case SLAPQuadrant.SAI:
                        pass

                    case SLAPQuadrant.RESERVED:
                        pass

                    case _:
                        raise ValueError(
                            f"Unexpected SLAP quadrant: {classified_mac.slap_quadrant}"
                        )

            case (Administration.LOCAL, DeliveryType.GROUP):
                pass
            case _:
                raise ValueError("Unsupported MAC classification")  # Never..

    print(TextRenderer().render(report))

    return 0
