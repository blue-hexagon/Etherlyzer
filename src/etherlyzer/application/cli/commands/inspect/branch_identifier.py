from etherlyzer.application.cli.commands.inspect.branch_macaddr_presentation import (
    build_cid_registration_section,
)
from etherlyzer.application.cli.commands.inspect.common import (
    MacInspectionParams,
)
from etherlyzer.presentation.reporting.renderers.text import TextRenderer


def inspect_identifier(
    params: MacInspectionParams,
) -> int:
    section = build_cid_registration_section(params)
    params.report.sections.append(section)
    print(TextRenderer().render(params.report))
    return 0
