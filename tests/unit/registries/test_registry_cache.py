import datetime
from datetime import timedelta

import pytest
from _pytest.monkeypatch import MonkeyPatch

from etherlyzer.ieee.registry.cache import RegistryCache


@pytest.mark.parametrize(
    ("age", "expected"),
    [
        (datetime.timedelta(microseconds=0), False),
        (datetime.timedelta(microseconds=1), False),
        (datetime.timedelta(seconds=2), False),
        (datetime.timedelta(hours=0), False),
        (datetime.timedelta(hours=1), False),
        (datetime.timedelta(hours=12), False),
        (datetime.timedelta(hours=23), False),
        (datetime.timedelta(hours=23, minutes=59, seconds=59), False),
        (datetime.timedelta(hours=24, minutes=0, seconds=1), True),
        (datetime.timedelta(hours=25), True),
        (datetime.timedelta(days=7), True),
    ],
)
def test_cache_expiration(
    monkeypatch: MonkeyPatch,
    registry_cache: RegistryCache,
    age: datetime.timedelta,
    expected: bool,
) -> None:
    monkeypatch.setattr(
        registry_cache,
        "update_interval",
        timedelta(hours=24),
    )
    registry_cache.filepath.touch()

    registry_cache.last_retrieved = datetime.datetime.now(datetime.UTC) - age

    assert registry_cache.need_updates() is expected


def test_missing_file_causes_update_required(
    registry_cache: RegistryCache,
) -> None:
    assert not registry_cache.filepath.exists()
    assert registry_cache.need_updates() is True
