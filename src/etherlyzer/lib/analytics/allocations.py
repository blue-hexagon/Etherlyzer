from dataclasses import dataclass

from etherlyzer.ieee.entry.mac import MACAllocationEntry


@dataclass
class VendorAllocation:
    registry: str | None
    total_addresses: int = 0
    total_blocks: int = 0

    def add_block(self, capacity: int) -> None:
        self.total_addresses += capacity
        self.total_blocks += 1


def summarize_vendor_allocations(
    vendors_other_blocks: list[MACAllocationEntry],
) -> tuple[
    VendorAllocation, VendorAllocation, VendorAllocation, VendorAllocation, VendorAllocation
]:
    capacities = {
        "MA-L": 2**24,
        "MA-M": 2**20,
        "MA-S": 2**12,
        "IAB": 2**12,
    }

    allocations = {registry: VendorAllocation(registry) for registry in capacities}

    for entry in vendors_other_blocks:
        registry = entry.registry

        if registry not in allocations:
            raise ValueError(f"Unknown IEEE registry: {registry!r}")

        allocations[registry].add_block(capacities[registry])

    total = VendorAllocation(
        registry=None,
        total_addresses=sum(allocation.total_addresses for allocation in allocations.values()),
        total_blocks=sum(allocation.total_blocks for allocation in allocations.values()),
    )

    return (
        total,
        allocations["IAB"],
        allocations["MA-L"],
        allocations["MA-M"],
        allocations["MA-S"],
    )
