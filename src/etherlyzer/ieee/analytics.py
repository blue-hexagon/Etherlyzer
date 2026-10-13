from dataclasses import dataclass

from etherlyzer.ieee.ieee_registry import IEEEEntry


@dataclass
class IEEEAllocation:
    registry: str
    total_addresses: int = 0
    total_blocks: int = 0

    def add_addresses(self, added: int) -> None:
        self.total_addresses += added

    def increment_blocks(self) -> None:
        self.total_blocks += 1


def get_vendor_total_addr_space(
    vendors_other_blocks: list[IEEEEntry],
) -> tuple[int, int, IEEEAllocation, IEEEAllocation, IEEEAllocation, IEEEAllocation]:
    mal = IEEEAllocation("MA-L")
    mam = IEEEAllocation("MA-M")
    mas = IEEEAllocation("MA-S")
    iab = IEEEAllocation("IAB")
    for ent in vendors_other_blocks:
        if ent.registry == "MA-L":
            mal.add_addresses(2**24)
            mal.increment_blocks()
        elif ent.registry == "MA-M":
            mal.add_addresses(2**20)
            mal.increment_blocks()
        elif ent.registry == "MA-S":
            mal.add_addresses(2**12)
            mal.increment_blocks()
        elif ent.registry == "IAB":
            iab.add_addresses(2**12)
            iab.increment_blocks()
        else:
            raise RuntimeError(
                f"Unexpected error occured because of a invalid registry identifier: {ent.registry}"
            )
    tot_blocks = mal.total_blocks + mam.total_blocks + mas.total_blocks + iab.total_blocks
    tot_addrs = (
        mal.total_addresses + mam.total_addresses + mas.total_addresses + iab.total_addresses
    )
    return tot_blocks, tot_addrs, iab, mal, mam, mas
