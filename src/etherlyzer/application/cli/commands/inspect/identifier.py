from etherlyzer.application.cli.commands.inspect.common import (
    MacInspectionParams,
)
from etherlyzer.presentation.reporting.renderers.text import TextRenderer

from .macaddr_presentation import build_cid_registration_section


def inspect_identifier(
    params: MacInspectionParams,
) -> int:
    section = build_cid_registration_section(params)
    params.report.sections.append(section)
    print(TextRenderer().render(params.report))
    return 0
