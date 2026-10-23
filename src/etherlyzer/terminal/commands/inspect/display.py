from __future__ import annotations

import argparse

from etherlyzer.ieee.entry.mac import MACAllocationEntry
from etherlyzer.ieee.index.store import IndexStore
from etherlyzer.ieee.registry.ieee_registry import IEEERegistry
from etherlyzer.lib.analytics.allocations import summarize_vendor_allocations
from etherlyzer.lib.analytics.analyze_mac import (
    Administration,
    DeliveryType,
    MACClassification,
    SLAPQuadrant,
)
from etherlyzer.lib.formatting import MACFormatter
from etherlyzer.lib.normalization import normalize
from etherlyzer.lib.translation import PresentationTranslator
from etherlyzer.terminal.commands.inspect.common import TerminalInspectFlags


def display_associated_block_counts(vendor_correlated_entries: list[MACAllocationEntry]) -> None:
    total_alloc, iab_alloc, mal_alloc, mam_alloc, mas_alloc = summarize_vendor_allocations(
        vendor_correlated_entries
    )
    print("\nAssociated Allocations")
    print("  Total")
    print(f"    Blocks           : {total_alloc.total_blocks:,}")
    print(f"    Capacity         : {total_alloc.total_addresses:,}")
    print("  MA-L")
    print(f"    Blocks           : {mal_alloc.total_blocks:,}")
    print(f"    Capacity         : {mal_alloc.total_addresses:,}")
    print("  MA-M")
    print(f"    Blocks           : {mam_alloc.total_blocks:,}")
    print(f"    Capacity         : {mam_alloc.total_addresses:,}")
    print("  MA-S")
    print(f"    Blocks           : {mas_alloc.total_blocks:,}")
    print(f"    Capacity         : {mas_alloc.total_addresses:,}")
    print("  IAB")
    print(f"    Blocks           : {iab_alloc.total_blocks:,}")
    print(f"    Capacity         : {iab_alloc.total_addresses:,}")


def display_all_vendor_blocks(
    args: argparse.Namespace, vendor_correlated_entries: list[MACAllocationEntry]
) -> None:
    if args.show_vendor_blocks:
        fmt_vendorblocks_width_count = 0
        fmt_vendorblocks_max_width = 45
        fmt_vendorblocks_width_increment = 9
        print("  Registered Blocks (B=IAB, S=MA-S, M=MA-M, L=MA-L)")
        for entry in vendor_correlated_entries:
            fmt_vendorblocks_width_count += fmt_vendorblocks_width_increment
            print(
                f"      [{entry.registry_id()}] {MACFormatter.format_default(entry.assignment)}",
                end="",
            )
            if fmt_vendorblocks_width_count >= fmt_vendorblocks_max_width:  # max width
                fmt_vendorblocks_width_count = 0
                print()  # Required exactly here.
        else:
            print()  # Required exactly here.


def display_registration(entry: MACAllocationEntry, reg: IEEERegistry) -> None:
    stuffed_input_0 = MACFormatter.format_default(entry.assignment, "0")
    sutffed_input_f = MACFormatter.format_default(entry.assignment, "f")
    print("\nIEEE Registry")
    print(f"  IEEE Type           : {entry.registry} [{reg.full_name}]")
    print(f"  Assignment          : {MACFormatter.format_default(entry.assignment)}")
    print(f"  Range               : {stuffed_input_0} - {sutffed_input_f}")
    print(f"  Prefix Bits         : {reg.prefix_bits} bits")
    print(f"  Address Bits        : {reg.address_bits} bits")
    print(f"  Legacy              : {reg.legacy}")
    print(f"  Legacy Name         : {reg.legacy_name or 'NA'}")
    if reg.address_count is not None:
        print(f"  Address Capacity    : {reg.address_count:,}")


def display_organization(entry: MACAllocationEntry, short_orgname: str) -> None:
    print("\nOrganization")
    print(f"  Name              : {short_orgname}")
    print(f"  Full Name         : {entry.organization_name}")
    print("  Address")
    for addr_piece in entry.format_vendor_address():
        print(f"    {addr_piece}")


def display_ieee_identifier(
    args: argparse.Namespace,
    index: IndexStore,
    eval_flags: TerminalInspectFlags,
    classified_mac: MACClassification,
) -> None:
    normalized = normalize(args.value)
    is_complete = len(normalized) == 12
    mac_entry = None
    cid_entry = None

    if classified_mac.administration == Administration.UNIVERSAL:
        if classified_mac.delivery == DeliveryType.INDIVIDUAL:
            mac_entry = index.get_single(index.mac, normalized)

    elif classified_mac.slap_quadrant == SLAPQuadrant.ELI and len(normalized) >= 6:
        cid_entry = index.get_single(
            index.identifier,
            normalized[:6],
        )
    if classified_mac.is_zero and is_complete:
        assignment = "Not Applicable (Zero Address)"

    elif classified_mac.is_broadcast and is_complete:
        assignment = "Not Applicable (Broadcast Address)"

    elif classified_mac.delivery == DeliveryType.GROUP:
        assignment = "Not Applicable (Group Address)"

    elif classified_mac.administration == Administration.UNIVERSAL:
        if is_complete:
            assignment = (
                "EUI-48 Candidate (Registered Block)"
                if mac_entry is not None
                else "Universal Individual (Unverified)"
            )
        else:
            assignment = (
                "Universal Individual Prefix (Registered Block)"
                if mac_entry is not None
                else "Universal Individual Prefix (Unverified)"
            )

    elif classified_mac.slap_quadrant == SLAPQuadrant.ELI:
        if is_complete:
            assignment = (
                "ELI-48 Candidate (Registered CID)"
                if cid_entry is not None
                else "ELI-48 Candidate (Unregistered CID)"
                if len(normalized) >= 6
                else "ELI-48 Candidate (CID Not Evaluated)"
            )
        else:
            assignment = (
                "ELI Prefix (Registered CID)"
                if cid_entry is not None
                else "ELI Prefix (Unregistered CID)"
                if len(normalized) >= 6
                else "ELI Prefix (Incomplete CID)"
            )

    elif classified_mac.slap_quadrant == SLAPQuadrant.AAI:
        assignment = "AAI Quadrant"

    elif classified_mac.slap_quadrant == SLAPQuadrant.SAI:
        assignment = "SAI Quadrant"

    elif classified_mac.slap_quadrant == SLAPQuadrant.RESERVED:
        assignment = "Reserved SLAP Quadrant"

    else:
        assignment = "Unknown"
    print("\nIEEE Identifier")
    print(f"  Type                : {assignment}")
    print(f"  SLAP Quadrant       : {classified_mac.slap_quadrant}")


def display_mac_autopsy(
    args: argparse.Namespace,
    index: IndexStore,
    eval_flags: TerminalInspectFlags,
    classified_mac: MACClassification,
) -> None:
    cid_length = 6  # noqa: F841 ; TODO
    normalized = normalize(args.value)
    canonical_mac = MACFormatter.format(args.value, block_size=2, separator="-", case="upper")
    try:
        bit_reversed_mac = PresentationTranslator.to_bit_reversed(normalized)
    except ValueError:
        bit_reversed_mac = "NA"

    mac_int = int(normalized, 16)
    mac_int_padded = int(normalized.ljust(12, "0"), 16)
    mac_decimals = list(bytes.fromhex(normalized.replace(":", "")))

    first_octet = mac_int_padded >> 40
    ul_bit = (first_octet >> 1) & 1
    ul_bit_addon = (
        "Local / Locally Administered" if ul_bit else "Universal / Universally Administered"
    )
    ig_bit = first_octet & 1
    ig_bit_addon = "Group / Multicast" if ig_bit else "Individual / Unicast"
    bit_width = len(normalized) * 4
    octal_width = (bit_width + 2) // 3
    binary = f"{mac_int:0{bit_width}b}"
    binary = ".".join(binary[i : i + 4] for i in range(0, len(binary), 4))

    print("MAC Address Autopsy")
    print("  Input")
    print(f"    Value             : {args.value}")
    print(f"    Length            : {len(normalized) * 4} bits")
    print("  Representations")
    print(f"    Canonical         : {canonical_mac}")
    print(f"    Bit-Reversed      : {bit_reversed_mac}")
    print(f"    To Hex            : {mac_int:0{len(normalized)}X}")
    print(f"    To Integer        : {mac_int:,}")
    print(f"    To Decimals       : {' '.join(map(str, mac_decimals))}")
    print(f"    To Octal          : {mac_int:0{octal_width}o}")
    print(f"    To Binary         : {binary}")
    print(f"    To Bytes          : {mac_int.to_bytes(bit_width // 8, 'big').hex(' ').upper()}")
    print("  Address Properties")
    print(f"    Null Address      : {classified_mac.is_zero}")
    print(f"    Broadcast         : {classified_mac.is_broadcast}")
    print("    Special Bits")
    print(f"      U/L             : {ul_bit} {ul_bit_addon}")
    print(f"      I/G             : {ig_bit} {ig_bit_addon}")


def show_cid_registration(index: IndexStore, normalized: str, slap: SLAPQuadrant) -> None:
    cid_length = 6
    if slap == SLAPQuadrant.ELI:
        cid_entry = index.get_single(indextype=index.identifier, mac=normalized[:cid_length])
        print("    CID")
        if cid_entry is not None:
            print(f"      Organization   : {cid_entry.organization_name}")
            print("      Address")
            for address_piece in cid_entry.format_vendor_address():
                print(f"        {address_piece}")

        else:
            print("      Organization   : Not Registered")
