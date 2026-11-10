from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import TypeVar

from etherlyzer.ieee.index.builder import IndexBuilder
from etherlyzer.ieee.index.store import IndexStore
from etherlyzer.ieee.registry.provider import Registry, RegistryProvider

T = TypeVar("T")


@dataclass(slots=True)
class EtherlyzerContext:
    provider: RegistryProvider
    indexes: IndexStore


def initialize_etherlyzer(
    cache_dir: Path | None = None,
    registry_exemptions: list[str] | None = None,
    registry_inclusions: list[str] | None = None,
) -> EtherlyzerContext:
    provider = RegistryProvider(cache_dir=cache_dir)

    registries: list[Registry] = select_registries(
        provider,
        inclusions=registry_inclusions,
        exemptions=registry_exemptions,
    )

    initialize_registry_caches(registries=registries)
    indexes = initialize_indexes(registries=registries)
    return EtherlyzerContext(provider=provider, indexes=indexes)


def select_registries(
    provider: RegistryProvider,
    inclusions: list[str] | None = None,
    exemptions: list[str] | None = None,
) -> list[Registry]:
    included = {name.casefold() for name in (inclusions or [])}
    excluded = {name.casefold() for name in (exemptions or [])}

    return [
        registry
        for registry in provider.get_all()
        if (not included or registry.name.casefold() in included)
        and registry.name.casefold() not in excluded
    ]


def initialize_registry_caches(registries: list[Registry]) -> None:

    for registry in registries:
        if registry.registry_cache.filepath.exists():
            continue

        if not registry.registry_downloader.fetch_online():
            raise RuntimeError(f"Failed to synchronize registry cache: {registry.name}")


def initialize_indexes(registries: Iterable[Registry]) -> IndexStore:
    return IndexBuilder.build(registries)
