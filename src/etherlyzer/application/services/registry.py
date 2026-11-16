from etherlyzer.infrastructure.registry.provider import RegistryProvider
from etherlyzer.presentation.reporting.model import Item, Section


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
