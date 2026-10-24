from typing import TypeVar
from unittest.mock import Mock

import pytest
import requests

from etherlyzer.ieee.registry.downloader import RegistryDownloader
from etherlyzer.ieee.registry.ieee_registry import IEEERegistry

T = TypeVar("T")


def mock_http_response(status_code: int) -> Mock:
    response = requests.Response()
    response.status_code = status_code
    response.url = "https://example.com/registry.csv"

    return Mock(return_value=response)


def test_downloader_can_fetch(
    registry_downloader: RegistryDownloader,
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
    response.iter_content.return_value = [
        csv_content[:20],
        csv_content[20:60],
        b"",
        csv_content[60:],
    ]

    mocked_get = Mock(return_value=response)

    monkeypatch.setattr(
        requests,
        "get",
        mocked_get,
    )

    result = registry_downloader.fetch_online()

    assert result is True
    assert registry_downloader.cache.filepath.exists()
    assert registry_downloader.cache.filepath.read_bytes() == csv_content
    response.iter_content.assert_called_once_with(chunk_size=8192)

    mocked_get.assert_called_once_with(
        headers=registry_downloader.req_headers,
        url=registry_downloader.url,
        timeout=20,
        stream=True,
    )

    response.raise_for_status.assert_called_once_with()


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
        requests,
        "get",  # type: ignore
        mocked_get,
    )

    result = ieee_registry.registry_downloader.fetch_online()

    assert result is True
    assert mocked_get.call_count == 2
    assert ieee_registry.registry_cache.filepath.read_bytes() == b"test"


def test_download_fails_after_maximum_retries(
    ieee_registry: IEEERegistry,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mocked_get = Mock(side_effect=requests.exceptions.Timeout())

    monkeypatch.setattr(
        requests,
        "get",
        mocked_get,
    )

    result = ieee_registry.registry_downloader.fetch_online()

    assert result is False
    assert mocked_get.call_count == 3
    assert not ieee_registry.registry_cache.filepath.exists()


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
def test_http_errors_trigger_retries[T](
    ieee_registry: IEEERegistry[T],
    monkeypatch: pytest.MonkeyPatch,
    status_code: int,
) -> None:
    response = Mock()
    response.raise_for_status.side_effect = requests.exceptions.HTTPError(f"HTTP {status_code}")

    mocked_get = Mock(return_value=response)

    monkeypatch.setattr(
        requests,
        "get",
        mocked_get,
    )


@pytest.mark.parametrize("status_code", [400, 401, 403, 404, 405, 410, 422])
def test_http_errors_does_not_trigger_retries[T](
    ieee_registry: IEEERegistry[T],
    monkeypatch: pytest.MonkeyPatch,
    status_code: int,
) -> None:
    response = Mock()
    response.raise_for_status.side_effect = requests.exceptions.HTTPError(f"HTTP {status_code}")

    mocked_get = Mock(return_value=response)

    monkeypatch.setattr(
        requests,
        "get",
        mocked_get,
    )
