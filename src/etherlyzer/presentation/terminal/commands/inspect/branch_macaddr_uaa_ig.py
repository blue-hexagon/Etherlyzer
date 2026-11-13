from etherlyzer.application.analysis.mac_classifier import DeliveryType
from etherlyzer.domain.registry.provider import Registry, is_mac_registry
from etherlyzer.presentation.terminal.commands.inspect.branch_macaddr_presentation import (
    build_associated_block_count_section,
    build_ieee_registration_section,
    build_vendor_blocks_section,
)
from etherlyzer.presentation.terminal.commands.inspect.common import (
    MacInspectionParams,
)


def inspect_universal(params: MacInspectionParams) -> bool | None:
    context, args, inspect_flags, report, cmac = (
        params.context,
        params.args,
        params.inspect_flags,
        params.report,
        params.classified_mac,
    )

    if cmac.delivery == DeliveryType.INDIVIDUAL:
        entry = context.indexes.mac.lookup(args.value)
    else:
        entry = context.indexes.mac.lookup_group_allocation(args.value)

    if entry is not None:
        registry: Registry = context.provider.get_by_name(entry.registry)
        if True and is_mac_registry(registry):
            ieee_registry_section = build_ieee_registration_section(entry, registry)

        if inspect_flags.show_vendor_stats or inspect_flags.show_vendor_blocks:
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
    return None
