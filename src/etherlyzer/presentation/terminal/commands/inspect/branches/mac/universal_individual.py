from etherlyzer.presentation.reporting.renderers.text import TextRenderer
from etherlyzer.presentation.terminal.commands.inspect.common import InspectionParams
from etherlyzer.presentation.terminal.commands.inspect.presentation.sections import (
    build_associated_block_count_section,
    build_ieee_registration_section,
    build_organization_section,
    build_vendor_blocks_section,
)


def inspect_universal_individual(params: InspectionParams) -> bool | None:
    args, context, inspect_flags, _, report = params.to_vars()
    entry = context.indexes.mac.lookup(args.value)
    if entry is not None:
        short_orgname = entry.short_name()
        registry = context.provider.get_by_name(entry.registry)
        if True:
            report.sections.append(
                build_ieee_registration_section(entry, registry),
            )

        if params.inspect_flags.show_vendor_stats or inspect_flags.show_vendor_blocks:
            vendor_correlated_entries = context.indexes.vendor.lookup_many(entry.organization_name)

            if vendor_correlated_entries:
                if inspect_flags.show_vendor_stats:
                    report.sections.append(
                        build_associated_block_count_section(vendor_correlated_entries),
                    )

                if inspect_flags.show_vendor_blocks:
                    report.sections.append(
                        build_vendor_blocks_section(vendor_correlated_entries),
                    )

        report.sections.append(
            build_organization_section(entry, short_orgname),
        )
        print(TextRenderer().render(report))
        return True
    if entry is None:
        print("IEEE Registry")
        print("  Status            : Not Found")
        return False
    return False
