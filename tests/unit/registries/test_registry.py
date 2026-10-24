from typing import TypeVar
from unittest.mock import Mock

import pytest

from etherlyzer.ieee.entry.mac import MACAllocationEntry
from etherlyzer.ieee.registry.ieee_registry import IEEERegistry

T = TypeVar("T")


def test_registry_loads(
    ieee_registry: IEEERegistry[T],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Preconditions: cache not expired and cache available."""
    ieee_registry.registry_cache.filepath.write_text(
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
    monkeypatch.setattr(ieee_registry.registry_downloader, "fetch_online", mocked_fetch)

    entries: list[MACAllocationEntry] = ieee_registry.load()

    assert len(entries) == 11
    assert entries[4].assignment == "20F83B"
    assert entries[4].organization_name == "Nabu Casa, Inc."
    assert entries[4].organization_address == "8 The Green, Suite 12630 Dover DE US 19901 "
    assert entries[4].registry == "MA-L"

    mocked_fetch.assert_not_called()


def test_registry_load_raises_when_cache_missing(
    ieee_registry: IEEERegistry,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    assert not ieee_registry.registry_cache.filepath.exists()

    mocked_fetch = Mock()
    monkeypatch.setattr(
        ieee_registry.registry_downloader,
        "fetch_online",
        mocked_fetch,
    )

    with pytest.raises(FileNotFoundError, match="Missing registry cache"):
        ieee_registry.load()

    mocked_fetch.assert_not_called()
