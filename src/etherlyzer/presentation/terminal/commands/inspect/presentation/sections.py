from __future__ import annotations

from etherlyzer.core.analytics.allocation_stats import summarize_vendor_allocations
from etherlyzer.core.analytics.mac_identity import analyze_mac_identity
from etherlyzer.core.formatting import MACFormatter
from etherlyzer.core.translation import PresentationTranslator
from etherlyzer.ieee.entry.mac import MACAllocationEntry
from etherlyzer.ieee.registry.ieee_registry import IEEERegistry
from etherlyzer.presentation.reporting.model import Item, Section
from etherlyzer.presentation.terminal.commands.inspect.common import InspectionParams


def build_associated_block_count_section(
    vendor_correlated_entries: list[MACAllocationEntry],
) -> Section:
    total_alloc, iab_alloc, mal_alloc, mam_alloc, mas_alloc = summarize_vendor_allocations(
        vendor_correlated_entries
    )
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
                title="MA-L",
                items=[
                    Item(key="Blocks", value=f"{mal_alloc.total_blocks:,}"),
                    Item(key="Capacity", value=f"{mal_alloc.total_addresses:,}"),
                ],
            ),
            Section(
                title="MA-M",
                items=[
                    Item(key="Blocks", value=f"{mam_alloc.total_blocks:,}"),
                    Item(key="Capacity", value=f"{mam_alloc.total_addresses:,}"),
                ],
            ),
            Section(
                title="MA-S",
                items=[
                    Item(key="Blocks", value=f"{mas_alloc.total_blocks:,}"),
                    Item(key="Capacity", value=f"{mas_alloc.total_addresses:,}"),
                ],
            ),
            Section(
                title="IAB",
                items=[
                    Item(key="Blocks", value=f"{iab_alloc.total_blocks:,}"),
                    Item(key="Capacity", value=f"{iab_alloc.total_addresses:,}"),
                ],
            ),
        ],
    )


def build_vendor_blocks_section(
    vendor_correlated_entries: list[MACAllocationEntry],
) -> Section:
    return Section(
        title="Registered Blocks (B=IAB, S=MA-S, M=MA-M, L=MA-L)",
        layout="grid",
        items=[
            Item(
                key=entry.registry_id(),
                value=MACFormatter.format_default(entry.assignment),
            )
            for entry in vendor_correlated_entries
        ],
    )


def build_ieee_registration_section(entry: MACAllocationEntry, reg: IEEERegistry) -> Section:
    stuffed_input_0 = MACFormatter.format_default(entry.assignment, "0")
    sutffed_input_f = MACFormatter.format_default(entry.assignment, "f")

    return Section(
        title="IEEE Registry",
        layout="default",
        items=[
            Item(
                key="IEEE Type",
                value=f"{entry.registry} [{reg.full_name}]",
            ),
            Item(
                key="Assignment",
                value=f"{MACFormatter.format_default(entry.assignment)}",
            ),
            Item(
                key="Range",
                value=f"{stuffed_input_0} - {sutffed_input_f}",
            ),
            Item(
                key="Prefix Bits",
                value=f"{reg.prefix_bits} bits",
            ),
            Item(
                key="Address Bits",
                value=f"{reg.address_bits} bits",
            ),
            Item(
                key="Legacy",
                value=f"{reg.legacy}",
            ),
            Item(
                key="Legacy Name",
                value=f"{reg.legacy_name or 'NA'}",
            ),
            *(
                [Item(key="Address Capacity", value=reg.address_count)]
                if reg.address_count is not None
                else []
            ),
        ],
    )


def build_organization_section(entry: MACAllocationEntry, short_orgname: str) -> Section:
    address = entry.format_vendor_address()
    return Section(
        title="Organization",
        layout="default",
        items=[
            Item(
                key="Name",
                value=f"{short_orgname}",
            ),
            Item(
                key="Full Name",
                value=f"{entry.organization_name}",
            ),
            Item(
                key="Address",
                value=f"{''.join(address)}",
            ),
        ],
    )


def build_ieee_identity_section(params: InspectionParams) -> Section:
    _, context, _, mac, _ = params.to_vars()

    identity, registration = analyze_mac_identity(mac, context)
    return Section(
        title="IEEE Identity",
        items=[
            Item("Type", identity),
            Item("Registration", registration),
            Item(
                "SLAP Quadrant",
                mac.slap_quadrant.value if mac.slap_quadrant is not None else "None",
            ),
        ],
    )


def build_mac_autopsy_section(params: InspectionParams) -> Section:
    args, _, _, classified_mac, _ = params.to_vars()
    normalized = classified_mac.normalized
    mac_int_padded = int(normalized.ljust(12, "0"), 16)

    first_octet = mac_int_padded >> 40

    ul_bit = (first_octet >> 1) & 1
    ul_bit_addon = (
        "Local / Locally Administered" if ul_bit else "Universal / Universally Administered"
    )

    ig_bit = first_octet & 1
    ig_bit_addon = "Group / Multicast" if ig_bit else "Individual / Unicast"

    pt = PresentationTranslator

    return Section(
        title="MAC Address Autopsy",
        items=[
            Section(
                title="Input",
                items=[
                    Item(key="Value", value=args.value),
                    Item(key="Length", value=f"{len(normalized) * 4} bits"),
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
                    Item(key="Null Address", value=classified_mac.is_zero),
                    Item(key="Broadcast", value=classified_mac.is_broadcast),
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


def build_cid_registration_section(params: InspectionParams) -> Section:
    CID_LENGTH = 6
    _, context, _, classified_mac, _ = params.to_vars()

    cid_entry = context.indexes.identifier.lookup(classified_mac.normalized[:CID_LENGTH])

    if cid_entry is None:
        return Section(
            title="CID",
            items=[
                Item(key="Organization", value="Not Registered"),
            ],
        )

    return Section(
        title="CID",
        items=[
            Item(key="Organization", value=cid_entry.organization_name),
            Section(
                title="Address",
                items=[
                    Item(key=f"Line {i}", value=piece)
                    for i, piece in enumerate(cid_entry.format_vendor_address(), start=1)
                ],
            ),
        ],
    )
