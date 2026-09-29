from etherlyzer.configuration import config
from etherlyzer.formatters import MACFormatter

from etherlyzer.registry import IEEEEntry


class RegistryMatchExporter:
    @staticmethod
    def export_csv_to_console(entries: list[IEEEEntry]):
        for entry in entries:
            try:
                print(
                    f"{entry.registry}{config.field_separator}"
                    f"{MACFormatter.format_default(entry.assignment)}{config.field_separator}"
                    f"{entry.organization_name}{config.field_separator}"
                    f"{entry.organization_address}"
                    f""
                )
            except AttributeError():
                # Lookup not found.
                pass

    @staticmethod
    def export_humanized_to_console(entries: list[IEEEEntry]):
        for entry in entries:
            mac = MACFormatter.format_default(entry.assignment)
            try:
                print(f"{entry.registry}: {mac} {entry.organization_name}")
            except AttributeError():
                # Lookup not found.
                pass
