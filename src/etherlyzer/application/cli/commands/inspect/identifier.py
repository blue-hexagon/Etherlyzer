from etherlyzer.application.cli.commands.inspect.common import (
    MacInspectionParams,
)
from etherlyzer.application.services.mac import build_cid_registration
from etherlyzer.presentation.reporting.renderers.text import TextRenderer


def inspect_identifier(
    params: MacInspectionParams,
) -> int:
    section = build_cid_registration(params)
    params.report.sections.append(section)
    print(TextRenderer().render(params.report))
    return 0
