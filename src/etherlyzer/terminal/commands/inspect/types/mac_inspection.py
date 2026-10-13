from typing import TYPE_CHECKING

from etherlyzer.ieee.catalog import Catalog
from etherlyzer.ieee.eui48_classifier import (
    Administration,
    DeliveryType,
    MACClassification,
    SLAPQuadrant,
    classify_mac,
)
from etherlyzer.ieee.index import IEEEIndex

if TYPE_CHECKING:
    from etherlyzer.terminal.commands.inspect.controller import EvaluatedFlags
from etherlyzer.terminal.commands.inspect.types.display import (
    display_all_vendor_blocks,
    display_associated_block_counts,
    display_ieee_identifier,
    display_mac_autopsy,
    display_organization,
    display_registration,
)


def inspect_universal_individual(
    args, index: IEEEIndex, eval_flags: EvaluatedFlags, classified_mac: MACClassification
) -> bool | None:
    entry = index.get_single(index.mac_index, args.value)

    if entry is not None:
        short_orgname = entry.short_name()
        reg = Catalog.get_registry(str(entry.registry).lower().replace("-", ""))
        display_registration(entry, reg)

        if eval_flags.show_vendor_stats or eval_flags.show_vendor_blocks:
            # vendor_index: VendorIndex = index.vendor_index
            vendor_correlated_entries = index.vendor_index.lookup(entry.organization_name)

            if vendor_correlated_entries:
                if eval_flags.show_vendor_stats:
                    display_associated_block_counts(vendor_correlated_entries)

                if eval_flags.show_vendor_blocks:
                    display_all_vendor_blocks(args, vendor_correlated_entries)

        display_organization(entry, short_orgname)
        print()  # Required exactly here.
        return True
    if entry is None:
        print("IEEE Registry")
        print("  Status            : Not Found")
        return False
    return False


def inspect_universal_group(
    args, index: IEEEIndex, eval_flags: EvaluatedFlags, classified_mac: MACClassification
):
    print("UG")


def inspect_local_individual(
    args,
    index: IEEEIndex,
    eval_flags: EvaluatedFlags,
    classified_mac: MACClassification,
) -> None:
    print("LI")
    params = {
        "args": args,
        "index": index,
        "eval_flags": eval_flags,
        "classified_mac": classified_mac,
    }

    match classified_mac.slap_quadrant:
        case SLAPQuadrant.ELI:
            inspect_local_individual_eli(**params)

        case SLAPQuadrant.AAI:
            inspect_local_individual_aai(**params)

        case SLAPQuadrant.SAI:
            inspect_local_individual_sai(**params)

        case SLAPQuadrant.RESERVED:
            inspect_local_individual_reserved(**params)

        case _:
            raise ValueError(f"Unexpected SLAP quadrant: {classified_mac.slap_quadrant}")


def inspect_local_individual_eli(
    args, index: IEEEIndex, eval_flags: EvaluatedFlags, classified_mac: MACClassification
):
    print()


def inspect_local_individual_reserved(
    args, index: IEEEIndex, eval_flags: EvaluatedFlags, classified_mac: MACClassification
):
    print()


def inspect_local_individual_sai(
    args, index: IEEEIndex, eval_flags: EvaluatedFlags, classified_mac: MACClassification
):
    print()


def inspect_local_individual_aai(
    args, index: IEEEIndex, eval_flags: EvaluatedFlags, classified_mac: MACClassification
):
    print()


def inspect_local_group(
    args, index: IEEEIndex, eval_flags: EvaluatedFlags, classified_mac: MACClassification
):
    print("LG")


def inspect_zero_address(
    args, index: IEEEIndex, eval_flags: EvaluatedFlags, classified_mac: MACClassification
):
    print("Zero")


def inspect_broadcast_address(
    args, index: IEEEIndex, eval_flags: EvaluatedFlags, classified_mac: MACClassification
):
    print("Broadcast")


def inspect_ieee_quadrants(args, index: IEEEIndex, eval_flags: EvaluatedFlags) -> int:
    classified_mac = classify_mac(args.value)
    params = {
        "args": args,
        "index": index,
        "eval_flags": eval_flags,
        "classified_mac": classified_mac,
    }

    if eval_flags.show_mac_autopsy:
        display_mac_autopsy(**params)
        display_ieee_identifier(**params)
    match (classified_mac.administration, classified_mac.delivery):
        case (Administration.UNIVERSAL, DeliveryType.INDIVIDUAL):
            inspect_universal_individual(**params)

        case (Administration.UNIVERSAL, DeliveryType.GROUP):
            inspect_universal_group(**params)

        case (Administration.LOCAL, DeliveryType.INDIVIDUAL):
            inspect_local_individual(**params)

        case (Administration.LOCAL, DeliveryType.GROUP):
            inspect_local_group(**params)
        case _:
            raise ValueError("Unsupported MAC classification")

    return 0
