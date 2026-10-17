import contextlib

from etherlyzer.formatters import MACFormatter
from etherlyzer.ieee.entry.mac import MACAllocationEntry
from etherlyzer.util.knobs import etherlyzer_knobs


class RegistryMatchExporter:
    @staticmethod
    def export_csv_to_console(entries: list[MACAllocationEntry]) -> None:
        for entry in entries:
            with contextlib.suppress(AttributeError):
                print(
                    f"{entry.registry}{etherlyzer_knobs.field_separator}"
                    f"{MACFormatter.format_default(entry.assignment)}{etherlyzer_knobs.field_separator}"
                    f"{entry.organization_name}{etherlyzer_knobs.field_separator}"
                    f"{entry.organization_address}"
                    f""
                )

    @staticmethod
    def export_humanized_to_console(entries: list[MACAllocationEntry]) -> None:
        for entry in entries:
            mac = MACFormatter.format_default(entry.assignment)
            with contextlib.suppress(AttributeError):
                print(f"{entry.registry}: {mac} {entry.organization_name}")
