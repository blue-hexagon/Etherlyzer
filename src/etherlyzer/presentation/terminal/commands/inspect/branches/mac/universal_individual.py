from etherlyzer.presentation.terminal.commands.inspect.common import InspectionParams
from etherlyzer.presentation.terminal.commands.inspect.presentation.sections import (
    build_associated_block_count_section,
    build_ieee_registration_section,
    build_vendor_blocks_section,
)


def inspect_universal_individual(params: InspectionParams) -> bool | None:
    args, context, inspect_flags, _, report = params.to_vars()
    entry = context.indexes.mac.lookup(args.value)
    if entry is not None:
        registry = context.provider.get_by_name(entry.registry)
        if True:
            ieee_registry_section = build_ieee_registration_section(entry, registry)

        if params.inspect_flags.show_vendor_stats or inspect_flags.show_vendor_blocks:
            vendor_correlated_entries = context.indexes.vendor.lookup_many(entry.organization_name)

            if vendor_correlated_entries:
                if inspect_flags.show_vendor_stats:
                    ieee_registry_section.items.append(
                        build_associated_block_count_section(vendor_correlated_entries),
                    )

                if inspect_flags.show_vendor_blocks:
                    ieee_registry_section.items.append(
                        build_vendor_blocks_section(vendor_correlated_entries),
                    )
        report.previous_section.append(ieee_registry_section)
        return True
    if entry is None:
        return False
    return False
