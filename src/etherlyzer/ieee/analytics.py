from etherlyzer.ieee.ieee_registry import IEEEEntry


def get_vendor_block_totals(vendors_other_blocks: list[IEEEEntry]) -> tuple[int, int, int, int, int]:
    total_addresses = 0
    total_addresses_mal = 0
    total_addresses_mam = 0
    total_addresses_mas = 0
    total_addresses_iab = 0
    for ent in vendors_other_blocks:
        if ent.registry == "MA-L":
            total_addresses += 2 ** 24
            total_addresses_mal += 2 ** 24
        elif ent.registry == "MA-M":
            total_addresses += 2 ** 20
            total_addresses_mam += 2 ** 20
        elif ent.registry == "MA-S":
            total_addresses += 2 ** 12
            total_addresses_mas += 2 ** 12
        elif ent.registry == "IAB":
            total_addresses += 2 ** 12
            total_addresses_iab += 2 ** 12
        else:
            raise RuntimeError(f"Unexpected error occured because of a invalid registry identifier: {ent.registry}")
    return total_addresses, total_addresses_iab, total_addresses_mal, total_addresses_mam, total_addresses_mas
