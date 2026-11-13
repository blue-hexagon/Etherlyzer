from __future__ import annotations

from etherlyzer.application.cli.commands.inspect.common import (
    MacInspectionParams,
)
from etherlyzer.core.interpretation.mac.allocation_analysis import summarize_vendor_allocations
from etherlyzer.core.interpretation.mac.formatting import MACFormatter
from etherlyzer.core.interpretation.mac.identifier import MacAssessment
from etherlyzer.core.interpretation.mac.translation import MacTranslation
from etherlyzer.domain.entry.mac import MACAllocationEntry
from etherlyzer.infrastructure.registry.registry_source import RegistrySource
from etherlyzer.presentation.reporting.model import Item, Section


def build_associated_block_count_section(
    vendor_correlated_entries: list[MACAllocationEntry],
) -> Section:
    total_alloc, iab_alloc, mal_alloc, mam_alloc, mas_alloc = summarize_vendor_allocations(
        vendor_correlated_entries
    )
    mal, mam, mas, iab = None, None, None, None
    if mal_alloc.total_blocks > 0:
        mal = Section(
            title="MA-L",
            items=[
                Item(key="Blocks", value=f"{mal_alloc.total_blocks:,}"),
                Item(key="Capacity", value=f"{mal_alloc.total_addresses:,}"),
            ],
        )

    if mam_alloc.total_blocks > 0:
        mam = Section(
            title="MA-M",
            items=[
                Item(key="Blocks", value=f"{mam_alloc.total_blocks:,}"),
                Item(key="Capacity", value=f"{mam_alloc.total_addresses:,}"),
            ],
        )
    if mas_alloc.total_blocks > 0:
        mas = Section(
            title="MA-S",
            items=[
                Item(key="Blocks", value=f"{mas_alloc.total_blocks:,}"),
                Item(key="Capacity", value=f"{mas_alloc.total_addresses:,}"),
            ],
        )
    if iab_alloc.total_blocks > 0:
        iab = Section(
            title="IAB",
            items=[
                Item(key="Blocks", value=f"{iab_alloc.total_blocks:,}"),
                Item(key="Capacity", value=f"{iab_alloc.total_addresses:,}"),
            ],
        )
    stats_for_each_registry: list[Item | Section] = [
        s for s in [mal, mam, mas, iab] if s is not None
    ]
    return Section(
        title="Associated Allocations",
        items=[
            Section(
                title="Summary",
                items=[
                    Item(key="Blocks", value=f"{total_alloc.total_blocks:,}"),
                    Item(key="Capacity", value=f"{total_alloc.total_addresses:,}"),
                ],
            ),
            Section(
                title="By Registry",
                items=stats_for_each_registry,
            ),
        ],
    )


def build_vendor_blocks_section(
    vendor_correlated_entries: list[MACAllocationEntry],
) -> Section:
    return Section(
        title="Registered Blocks",
        layout="grid",
        items=[
            Item(
                key=entry.registry_id(),
                value=MACFormatter.format_default(entry.assignment),
            )
            for entry in vendor_correlated_entries
        ],
        legend="B=IAB, S=MA-S, M=MA-M, L=MA-L",
    )


def build_ieee_registration_section(
    entry: MACAllocationEntry,
    reg: RegistrySource[MACAllocationEntry],
) -> Section:
    range_start = MACFormatter.format_default(entry.assignment, "0")
    range_end = MACFormatter.format_default(entry.assignment, "f")
    address = entry.format_vendor_address()

    allocation_items: list[Item | Section] = [
        Item(
            key="Registry",
            value=f"{entry.registry} [{reg.full_name}]",
        ),
        Item(
            key="Assignment",
            value=MACFormatter.format_default(entry.assignment),
        ),
        Item(
            key="Range",
            value=f"{range_start} - {range_end}",
        ),
        Item(
            key="Prefix Bits",
            value=f"{reg.prefix_bits} bits",
        ),
        Item(
            key="Address Bits",
            value=f"{reg.address_bits} bits",
        ),
    ]

    if reg.address_count is not None:
        allocation_items.append(Item(key="Address Capacity", value=f"{reg.address_count:,}"))

    allocation_items.append(Item(key="Legacy", value="Yes" if reg.legacy else "No"))

    if reg.legacy and reg.legacy_name:
        allocation_items.append(Item(key="Legacy Name", value=reg.legacy_name))

    return Section(
        title="IEEE Registry",
        layout="default",
        items=[
            Section(
                title="Organization",
                layout="default",
                items=[
                    Item(key="Name", value=entry.short_name()),
                    Item(key="Full Name", value=entry.organization_name),
                    Item(key="Address", value="".join(address)),
                ],
            ),
            Section(
                title="Allocation",
                layout="default",
                items=allocation_items,
            ),
        ],
    )


def build_mac_autopsy_section(
    params: MacInspectionParams,
    identity: str,
    registration: str,
    kind: str,
    assessment: frozenset[MacAssessment],
) -> Section:
    normalized = params.classified_mac.normalized

    mac_int_padded = int(normalized.ljust(12, "0"), 16)

    first_octet = mac_int_padded >> 40

    ul_bit = (first_octet >> 1) & 1
    ul_bit_addon = (
        "Local / Locally Administered" if ul_bit else "Universal / Universally Administered"
    )

    ig_bit = first_octet & 1
    ig_bit_addon = "Group / Multicast" if ig_bit else "Individual / Unicast"

    pt = MacTranslation
    pt.strict = False  # len != 12

    return Section(
        title="MAC Address Autopsy",
        items=[
            Section(
                title="Input",
                items=[
                    Item(key="Value", value=params.args.value),
                    Item(key="Length", value=f"{len(normalized) * 4} bits"),
                ],
            ),
            Section(
                title="IEEE Identity",
                items=[
                    Item("Kind", kind),
                    Item("Type", identity),
                    Item("Registration", registration),
                    Item(
                        "SLAP Quadrant",
                        params.classified_mac.slap_quadrant.value
                        if params.classified_mac.slap_quadrant is not None
                        else "None",
                    ),
                    Section(
                        title="Assessment",
                        items=[Item(ass.label, ass.description) for ass in assessment],
                    )
                    if len(assessment) > 0
                    else Item("No Observations", "Zero Assessments Made"),
                ],
            ),
            Section(
                title="Representations",
                items=[
                    Item(key="Canonical", value=str(pt.to_canonical(normalized))),
                    Item(key="Bit-Reversed", value=str(pt.to_bit_reversed(normalized))),
                    Item(key="To Hex", value=str(pt.to_hex(normalized))),
                    Item(key="To Integer", value=str(pt.to_decimal(normalized))),
                    Item(key="To Decimals", value=str(pt.to_decimal_bytes(normalized))),
                    Item(key="To Binary", value=str(pt.to_binary(normalized))),
                    Item(key="To Bytes", value=str(pt.to_bytes(normalized))),
                ],
            ),
            Section(
                title="Address Properties",
                items=[
                    Item(key="Null Address", value=params.classified_mac.is_zero),
                    Item(key="Broadcast", value=params.classified_mac.is_broadcast),
                    Section(
                        title="Special Bits",
                        items=[
                            Item(key="U/L", value=f"{ul_bit} {ul_bit_addon}"),
                            Item(key="I/G", value=f"{ig_bit} {ig_bit_addon}"),
                        ],
                    ),
                ],
            ),
        ],
    )


def build_cid_registration_section(
    params: MacInspectionParams, clear_ig_bit: bool = False
) -> Section:
    context = params.context
    classified_mac = params.classified_mac
    CID_LENGTH = 6
    if clear_ig_bit:
        cid_entry = context.indexes.identifier.lookup_with_ig_bit_cleared(
            classified_mac.normalized[:CID_LENGTH]
        )
    else:
        cid_entry = context.indexes.identifier.lookup(classified_mac.normalized[:CID_LENGTH])
    if cid_entry is None:
        section = Section(
            title="CID",
            items=[
                Section(
                    title="Assignment",
                    items=[
                        Item(key="Organization", value="Not Found"),
                    ],
                )
            ],
        )
    else:
        section = Section(
            title="CID",
            items=[
                Section(
                    title="Assignment",
                    items=[
                        Item(key="Organization", value=cid_entry.organization_name),
                        Section(
                            title="Address",
                            items=[
                                Item(key=f"Line {i}", value=piece)
                                for i, piece in enumerate(
                                    cid_entry.format_vendor_address(), start=1
                                )
                            ],
                        ),
                    ],
                ),
            ],
        )

    return section
