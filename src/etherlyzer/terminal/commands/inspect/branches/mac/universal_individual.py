import argparse

from etherlyzer.ieee.index.store import IndexStore
from etherlyzer.ieee.registry.provider import RegistryProvider
from etherlyzer.lib.analytics.analyze_mac import MACClassification
from etherlyzer.terminal.commands.inspect.common import TerminalInspectFlags
from etherlyzer.terminal.commands.inspect.display import (
    display_all_vendor_blocks,
    display_associated_block_counts,
    display_organization,
    display_registration,
)


def inspect_universal_individual(
    args: argparse.Namespace,
    index: IndexStore,
    inspect_flags: TerminalInspectFlags,
    classified_mac: MACClassification,
) -> bool | None:
    entry = index.get_single(index.mac, args.value)

    if entry is not None:
        short_orgname = entry.short_name()
        reg = RegistryProvider.get(str(entry.registry).lower().replace("-", ""))
        display_registration(entry, reg)

        if inspect_flags.show_vendor_stats or inspect_flags.show_vendor_blocks:
            # vendor_index: VendorIndex = index.vendor_index
            vendor_correlated_entries = index.vendor.lookup_many(entry.organization_name)

            if vendor_correlated_entries:
                if inspect_flags.show_vendor_stats:
                    display_associated_block_counts(vendor_correlated_entries)

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
