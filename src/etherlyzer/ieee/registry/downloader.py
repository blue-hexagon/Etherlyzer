from http import HTTPStatus
from typing import ClassVar

import requests
from requests import RequestException
from tqdm import tqdm

from etherlyzer.ieee.registry.cache import RegistryCache
from etherlyzer.util.knobs import etherlyzer_knobs


class RegistryDownloader:
    RETRYABLE_STATUS_CODES: ClassVar[frozenset[HTTPStatus]] = frozenset(
        {
            HTTPStatus.REQUEST_TIMEOUT,
            HTTPStatus.MISDIRECTED_REQUEST,
            HTTPStatus.TOO_EARLY,
            HTTPStatus.TOO_MANY_REQUESTS,
            HTTPStatus.INTERNAL_SERVER_ERROR,
            HTTPStatus.BAD_GATEWAY,
            HTTPStatus.SERVICE_UNAVAILABLE,
            HTTPStatus.GATEWAY_TIMEOUT,
        }
    )

    def __init__(self, url: str, name: str, cache: RegistryCache) -> None:
        self.url = url
        self.name = name
        self.cache = cache

    @property
    def req_headers(self) -> dict[str, str]:
        return {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/137.0.0.0 Safari/537.36"
            )
        }

    def fetch_online(self) -> bool:
        attempts = 1
        max_attempts = 3

        while attempts <= max_attempts:
            try:
                if etherlyzer_knobs.show_sync_messages:
                    print(f"Fetching Registry: {self.name}")

                res = requests.get(headers=self.req_headers, url=self.url, timeout=20, stream=True)
                res.raise_for_status()

                total_size = int(res.headers.get("content-length", 0)) or None

                with (
                    open(self.cache.filepath, "wb") as f,
                    tqdm(
                        total=total_size or None,
                        unit="B",
                        unit_scale=True,
                        unit_divisor=1024,
                        desc=f"Fetching {self.name}",
                        disable=not etherlyzer_knobs.show_sync_messages,
                    ) as progress,
                ):
                    for chunk in res.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            progress.update(len(chunk))

                return True
            except requests.exceptions.HTTPError as exc:
                status_code = exc.response.status_code if exc.response is not None else None

                if status_code not in self.RETRYABLE_STATUS_CODES:
                    print(f"Non-retryable HTTP error: {status_code}")
                    return False

                if etherlyzer_knobs.show_sync_messages:
                    print(
                        f"HTTP {status_code}: retryable failure (attempt {attempts}/{max_attempts})"
                    )
                attempts += 1
            except (
                requests.exceptions.Timeout,
                requests.exceptions.ConnectionError,
            ):
                if etherlyzer_knobs.show_sync_messages:
                    print(f"Request timed out on attempt {attempts} of {max_attempts}.")

                attempts += 1
            except RequestException as exc:
                raise RuntimeError(f"Request failed due to {exc}") from exc

        print(
            f"Unable to retrieve the registry '{self.name}' "
            f"from {self.url}. Maximum attempts exceeded."
        )

        return False
