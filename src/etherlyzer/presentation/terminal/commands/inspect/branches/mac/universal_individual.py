from etherlyzer.core.reporting.model import Report
from etherlyzer.presentation.terminal.commands.inspect.common import InspectionParams
from etherlyzer.presentation.terminal.commands.inspect.presentation.display import (
    build_associated_block_count_section,
    display_all_vendor_blocks,
    display_organization,
    display_registration,
)


def inspect_universal_individual(
    params: InspectionParams,
) -> bool | None:
    args, context, inspect_flags, _ = params.to_vars()
    entry = context.indexes.mac.lookup(args.value)
    report = Report()
    if entry is not None:
        short_orgname = entry.short_name()
        registry = context.provider.get_by_name(entry.registry)
        display_registration(entry, registry)

        if params.inspect_flags.show_vendor_stats or inspect_flags.show_vendor_blocks:
            # vendor_index: VendorIndex = index.vendor_index
            vendor_correlated_entries = context.indexes.vendor.lookup_many(entry.organization_name)

            if vendor_correlated_entries:
                if inspect_flags.show_vendor_stats:
                    report.sections.append(
                        build_associated_block_count_section(vendor_correlated_entries),
                    )

                if inspect_flags.show_vendor_blocks:
                    display_all_vendor_blocks(args, vendor_correlated_entries)

        display_organization(entry, short_orgname)
        print()  # Required exactly here.
        return True
    if entry is None:
        print("IEEE Registry")
        print("  Status            : Not Found")
        return False
    return False
