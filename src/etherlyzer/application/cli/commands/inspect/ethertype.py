from etherlyzer.application.cli.commands.inspect.common import CommonInspectionParams
from etherlyzer.application.services.ethertype import build_ethertype_analysis
from etherlyzer.presentation.reporting.renderers.text import TextRenderer


def inspect_ethertype(
    params: CommonInspectionParams,
) -> int:
    section = build_ethertype_analysis(params.args.value, params.context)
    params.report.sections.append(section)
    print(TextRenderer().render(params.report))
    return 0
