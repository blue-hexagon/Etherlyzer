from etherlyzer.bootstrap import EtherlyzerContext
from etherlyzer.infrastructure.registry.provider import RegistryProvider
from etherlyzer.presentation.reporting.model import Item, Section


def get_mac_assignment(eth_ctx: EtherlyzerContext, macaddr: str):
    entry = eth_ctx.indexes.mac.lookup(macaddr)
    if entry is None:
        return Section(title="IEEE Assignment", items=[Item(key="Result", value="No match found.")])

    return Section(
        title="IEEE Assignment",
        items=[
            Item(key="Registry", value=entry.registry),
            Item(key="Assignment", value=entry.assignment),
            Item(key="Name", value=entry.organization_name),
            Item(key="Address", value=entry.organization_address),
        ],
    )


def get_registry_entries():
    manager = RegistryProvider()
    reg_sections = []

    for registry in manager.get_all(require_cache=True):
        reg_sections.append(  # noqa: PERF401
            Section(
                title=f"{registry.name} ({registry.full_name})",
                items=[
                    Item(key="Legacy Name", value=registry.legacy_name),
                    Item(key="Category", value=registry.family),
                    Item(key="Description", value=registry.description),
                    Item(key="Legacy", value=registry.legacy),
                    Item(key="File", value=str(registry.registry_cache.filepath)),
                    Item(key="Source URL", value=str(registry.url)),
                    Item(key="Prefix Bits", value=str(registry.prefix_bits)),
                    Item(key="Last Retrieved", value=str(registry.registry_cache.last_retrieved)),
                    Item(
                        key="Update Interval",
                        value=str(registry.registry_cache.update_interval),
                    ),
                ],
            )
        )

    return Section(title="Registries", items=reg_sections)
