import datetime
from pathlib import Path
from unittest.mock import Mock

import pytest
import requests

import etherlyzer.ieee.ieee_registry as registry_module
from etherlyzer.ieee.ieee_registry import (
    IEEEEntry,
    IEEERegistry,
    RegCategory,
)


@pytest.fixture
def ieee_registry(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> IEEERegistry:
    # Redirect registry files to pytest's temporary directory.
    monkeypatch.setattr(
        "etherlyzer.ieee.ieee_registry.DATA_PLATFORM_DIR",
        tmp_path,
    )

    return IEEERegistry(
        enabled=True,
        name="MA-L",
        model=IEEEEntry,
        full_name="Test IEEE Registry",
        url="https://example.com/registry.csv",
        category=RegCategory.MAC,
        legacy=False,
        description="Testing Registry",
        update_interval=datetime.timedelta(days=28),
    )


def test_database_automatically_synchronizes_if_one_file_is_not_found(
    ieee_registry: IEEERegistry, monkeypatch: pytest.MonkeyPatch
) -> None:
    assert not ieee_registry.filepath.exists()

    mocked_save = Mock()
    mocked_load = Mock(return_value=[])

    monkeypatch.setattr(ieee_registry, "fetch_online", mocked_save)
    monkeypatch.setattr(
        registry_module.IEEERegistryReader,
        "load_file",
        mocked_load,
    )

    result = ieee_registry.load()

    mocked_save.assert_called_once_with()
    mocked_load.assert_called_once_with(
        ieee_registry.filepath,
        IEEEEntry,
    )
    assert result == []


def test_database_automatically_synchronizes_if_update_interval_exceeds_fstamp(
    ieee_registry: IEEERegistry,
) -> None:
    ieee_registry.last_retrieved = (
        datetime.datetime.now(datetime.UTC)
        - ieee_registry.update_interval
        - datetime.timedelta(seconds=1)
    )

    assert ieee_registry.need_updates() is True


def test_database_can_load(
    ieee_registry: IEEERegistry,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    ieee_registry.filepath.write_text(
        """
Registry,Assignment,Organization Name,Organization Address
MA-L,9075DE,Zebra Technologies Inc.,ONE ZEBRA PLAZA HOLTSVILLE NY US 11742
MA-L,80BA16,Micas Networks Inc.," 250 Tasman Drive, Ste 170, San Jose, CA 95134 San Jose CA US 95134 "
MA-L,10E992,INGRAM MICRO SERVICES,100 CHEMIN DE BAILLOT MONTAUBAN  FR 82000
MA-L,78F276,Cyklop Fastjet Technologies (Shanghai) Inc.,"No 18?Lane 699, Zhang Wengmiao Rd,  Fengxian district, Shanghai China Shanghai  CN 201401 "
MA-L,20F83B,"Nabu Casa, Inc.","8 The Green, Suite 12630 Dover DE US 19901 "
MA-L,F01B24,zte corporation,"12/F.,zte R&D building ,kejinan Road,Shenzhen,P.R.China shenzhen  guangdong CN 518057 "
MA-L,B84C87,IEEE Registration Authority,445 Hoes Lane Piscataway NJ US 08554
MA-L,E4F14C,Private,
MA-L,E00630,"HUAWEI TECHNOLOGIES CO.,LTD","No.2 Xin Cheng Road, Room R6,Songshan Lake Technology Park Dongguan  CN 523808 "
MA-L,04D168,"Sunplus Technology Co., Ltd.","19, Innovation First Road, Hsinchu Science Park Hsinchu  TW 300 "
MA-L,644C69,CONPROVE,"75, Visconde de Ouro Preto St. Uberlândia Minas Gerais BR 38405-202 "
""".strip(),
        encoding="utf-8",
    )

    mocked_fetch = Mock()
    monkeypatch.setattr(ieee_registry, "fetch_online", mocked_fetch)

    entries: list[IEEEEntry] = ieee_registry.load()

    assert len(entries) == 11
    assert entries[4].assignment == "20F83B"
    assert entries[4].organization_name == "Nabu Casa, Inc."
    assert entries[4].organization_address == "8 The Green, Suite 12630 Dover DE US 19901 "
    assert entries[4].registry == "MA-L"

    mocked_fetch.assert_not_called()


def test_database_can_fetch(
    ieee_registry: IEEERegistry,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    csv_content = (
        b"registry,assignment,organization_name,organization_address\n"
        b"MA-L,00000D,Test Organization,Test Address\n"
    )

    response = Mock()
    response.headers = {
        "content-length": str(len(csv_content)),
    }
    response.iter_content.return_value = [csv_content]

    mocked_get = Mock(return_value=response)

    monkeypatch.setattr(
        registry_module.requests,
        "get",  # type: ignore
        mocked_get,
    )

    result = ieee_registry.fetch_online()

    assert result is True
    assert ieee_registry.filepath.exists()
    assert ieee_registry.filepath.read_bytes() == csv_content

    mocked_get.assert_called_once_with(
        headers=ieee_registry.req_headers(),
        url=ieee_registry.url,
        timeout=20,
        stream=True,
    )
    response.raise_for_status.assert_called_once_with()


def test_database_does_not_need_updates_when_fresh(
    ieee_registry: IEEERegistry,
) -> None:
    ieee_registry.filepath.touch()
    ieee_registry.last_retrieved = datetime.datetime.now(datetime.UTC)

    assert ieee_registry.need_updates() is False


def test_missing_cache_requires_update(
    ieee_registry: IEEERegistry,
) -> None:
    assert not ieee_registry.filepath.exists()
    assert ieee_registry.need_updates() is True


def test_download_retries_after_request_failure(
    ieee_registry: IEEERegistry,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    response = Mock()
    response.headers = {}
    response.iter_content.return_value = [b"test"]

    mocked_get = Mock(
        side_effect=[
            requests.exceptions.Timeout(),
            response,
        ]
    )

    monkeypatch.setattr(
        registry_module.requests,
        "get",  # type: ignore
        mocked_get,
    )

    result = ieee_registry.fetch_online()

    assert result is True
    assert mocked_get.call_count == 2
    assert ieee_registry.filepath.read_bytes() == b"test"


def test_download_fails_after_maximum_retries(
    ieee_registry: IEEERegistry,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mocked_get = Mock(side_effect=requests.exceptions.Timeout())

    monkeypatch.setattr(
        registry_module.requests,
        "get",  # type: ignore
        mocked_get,
    )

    result = ieee_registry.fetch_online()

    assert result is False
    assert mocked_get.call_count == 3
    assert not ieee_registry.filepath.exists()


# def test_failed_download_preserves_existing_cache(
#     ieee_registry: IEEERegistry,
#     monkeypatch: pytest.MonkeyPatch,
# ) -> None:
#     original = b"original and valid registry data"
#     ieee_registry.filepath.write_bytes(original)
#
#     response = Mock()
#     response.headers = {"content-length": "100"}
#
#     def interrupted_stream(chunk_size: int):
#         yield b"partial replacement"
#         raise requests.exceptions.ChunkedEncodingError("Connection interrupted")
#
#     response.iter_content.side_effect = interrupted_stream
#
#     monkeypatch.setattr(
#         registry_module.requests,
#         "get",  # type: ignore
#         Mock(return_value=response),
#     )
#
#     assert ieee_registry.fetch_online() is False
#     assert ieee_registry.filepath.read_bytes() == original


@pytest.mark.parametrize("status_code", [408, 421, 425, 429, 500, 502, 503, 504])
def test_http_errors_trigger_retries(
    ieee_registry: IEEERegistry,
    monkeypatch: pytest.MonkeyPatch,
    status_code: int,
) -> None:
    response = Mock()
    response.raise_for_status.side_effect = requests.exceptions.HTTPError(f"HTTP {status_code}")

    mocked_get = Mock(return_value=response)

    monkeypatch.setattr(
        registry_module.requests,
        "get",  # type: ignore
        mocked_get,
    )


@pytest.mark.parametrize("status_code", [400, 401, 403, 404, 405, 410, 422])
def test_http_errors_does_not_trigger_retries(
    ieee_registry: IEEERegistry,
    monkeypatch: pytest.MonkeyPatch,
    status_code: int,
) -> None:
    response = Mock()
    response.raise_for_status.side_effect = requests.exceptions.HTTPError(f"HTTP {status_code}")

    mocked_get = Mock(return_value=response)

    monkeypatch.setattr(
        registry_module.requests,
        "get",  # type: ignore
        mocked_get,
    )
