from etherlyzer.presentation.reporting.renderers.text import TextRenderer
from etherlyzer.presentation.terminal.commands.inspect.branch_macaddr_presentation import (
    build_cid_registration_section,
)
from etherlyzer.presentation.terminal.commands.inspect.common import (
    MacInspectionParams,
)


def inspect_identifier(
    params: MacInspectionParams,
) -> int:
    section = build_cid_registration_section(params)
    params.report.sections.append(section)
    print(TextRenderer().render(params.report))
    return 0
