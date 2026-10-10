from typing import Any

from etherlyzer.formatters import MACFormatter
from etherlyzer.ieee.analytics import get_vendor_total_addr_space
from etherlyzer.ieee.eui48_classifier import DeliveryType, Administration, SLAPQuadrant
from etherlyzer.ieee.ieee_registry import IEEEEntry, IEEERegistry


def show_associated_block_counts(vendor_correlated_entries: list[IEEEEntry]):
    tot_blocks, tot_addr, iab_alloc, mal_alloc, mam_alloc, mas_alloc = get_vendor_total_addr_space(
        vendor_correlated_entries)
    print(f"\nAssociated Allocations")
    print(f"  Total")
    print(f"    Blocks           : {tot_blocks:,}")
    print(f"    Capacity         : {tot_addr:,}")
    print(f"  MA-L")
    print(f"    Blocks           : {mal_alloc.total_blocks:,}")
    print(f"    Capacity         : {mal_alloc.total_addresses:,}")
    print(f"  MA-M")
    print(f"    Blocks           : {mam_alloc.total_blocks:,}")
    print(f"    Capacity         : {mam_alloc.total_addresses:,}")
    print(f"  MA-S")
    print(f"    Blocks           : {mas_alloc.total_blocks:,}")
    print(f"    Capacity         : {mas_alloc.total_addresses:,}")
    print(f"  IAB")
    print(f"    Blocks           : {iab_alloc.total_blocks:,}")
    print(f"    Capacity         : {iab_alloc.total_addresses:,}")


def show_all_vendor_blocks(args, vendor_correlated_entries: list[IEEEEntry]):
    if args.show_vendor_blocks:
        fmt_vendorblocks_width_count = 0
        fmt_vendorblocks_max_width = 45
        fmt_vendorblocks_width_increment = 9
        print(f"  Registered Blocks (B=IAB, S=MA-S, M=MA-M, L=MA-L)")
        for entry in vendor_correlated_entries:
            fmt_vendorblocks_width_count += fmt_vendorblocks_width_increment
            print(f"      [{entry.registry_short_str()}] {MACFormatter.format_default(entry.assignment)}",
                  end="")
            if fmt_vendorblocks_width_count >= fmt_vendorblocks_max_width:  # max width
                fmt_vendorblocks_width_count = 0
                print()  # Required exactly here.
        else:
            print()  # Required exactly here.


def show_registration(entry, reg: IEEERegistry):
    stuffed_input_0 = MACFormatter.format_with_stuffed_hex(entry.assignment, "0")
    sutffed_input_f = MACFormatter.format_with_stuffed_hex(entry.assignment, "f")
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


def show_organization(entry, short_orgname):
    print(f"\nOrganization")
    print(f"  Name              : {short_orgname}")
    print(f"  Full Name         : {entry.organization_name}")
    print(f"  Address")
    for addr_piece in entry.format_vendor_addr():
        print(f"    {addr_piece}")


def show_mac_autopsy(args, classified_mac, index, no_valid_entry: bool):
    cid_length = 6
    normalized = MACFormatter.normalize(args.value)
    mac_int = int(normalized, 16)
    mac_int_padded = int(normalized.ljust(12, "0"), 16)
    first_octet = mac_int_padded >> 40
    ul_bit = (first_octet >> 1) & 1
    ul_bit_addon = 'Local / Locally Administered' if ul_bit else 'Universal / Universally Administered'
    ig_bit = first_octet & 1
    ig_bit_addon = 'Group / Multicast' if ig_bit else 'Individual / Unicast'
    bit_width = len(normalized) * 4
    octal_width = (bit_width + 2) // 3
    binary = f"{mac_int:0{bit_width}b}"
    binary = ".".join(binary[i:i + 4] for i in range(0, len(binary), 4))
    if classified_mac.slap_quadrant is not None:
        slap = classified_mac.slap_quadrant
    elif classified_mac.delivery == DeliveryType.GROUP:
        slap = "Not Applicable (Group Address)"
    else:
        slap = "Not Applicable (Universal Address)"

    if classified_mac.is_zero:
        assignment = "Not Applicable (Zero Address)"
    elif classified_mac.is_broadcast:
        assignment = "Not Applicable (Broadcast Address)"
    elif classified_mac.delivery == DeliveryType.GROUP:
        assignment = "Not Applicable (Group Address)"
    elif classified_mac.administration == Administration.LOCAL:
        assignment = "Not Applicable (Local Address)"
    elif no_valid_entry:
        assignment = "Not Found"
    else:
        assignment = "EUI-48 Candidate"

    print(f"MAC Address Autopsy")
    print(f"  Input")
    print(f"    Value             : {args.value}")
    print(f"    Length            : {len(normalized) * 4} bits")
    print(f"    To Hex            : {mac_int:0{len(normalized)}X}")
    print(f"    To Decimal        : {mac_int:,}")
    print(f"    To Octal          : {mac_int:0{octal_width}o}")
    print(f"    To Binary         : {binary}")
    print(f"    To Bytes          : {mac_int.to_bytes(bit_width // 8, 'big').hex(' ').upper()}")
    print(f"    Special Bits")
    print(f"      U/L             : {ul_bit} {ul_bit_addon}")
    print(f"      I/G             : {ig_bit} {ig_bit_addon}")
    print(f"  Address Properties")
    print(f"    Broadcast         : {classified_mac.is_broadcast}")

    show_cid_registration(index, normalized, slap)

    print(f"\nIEEE Identifier")
    print(f"  SLAP Quadrant    : {slap}")
    print(f"  Type             : {assignment}")
    return 0


def show_cid_registration(index, normalized: str, slap: str | Any):
    cid_length = 6
    if slap == SLAPQuadrant.ELI:
        cid_entry = index.get_single(indextype=index.identifier_index, mac=normalized[:cid_length])
        print("    CID")
        if cid_entry is not None:
            print(f"      Organization   : {cid_entry.organization_name}")
            print(f"      Address")
            for address_piece in cid_entry.format_vendor_addr():
                print(f"        {address_piece}")

        else:
            print(f"      Organization   : Not Registered")
