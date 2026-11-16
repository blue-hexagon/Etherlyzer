from functools import cache
from importlib.metadata import PackageNotFoundError, version

from etherlyzer.bootstrap import EtherlyzerContext, initialize_etherlyzer
from etherlyzer.core.interpretation.ethertype.classifier import (
    EtherTypeStruct,
    get_ethertype_struct,
)
from etherlyzer.core.interpretation.mac import extraction, formatting, translation
from etherlyzer.core.interpretation.mac.classifier import (
    MacStructure,
    get_mac_structure,
)
from etherlyzer.core.interpretation.mac.constants import (
    HEX_DIGITS,
    LENIENT_TYPOS,
    RELAXED_TYPOS,
    STRICT_TYPOS,
)
from etherlyzer.core.interpretation.mac.inspection import (
    MacForm,
    MacIdentity,
    MacIdentityResult,
    MacResolution,
    inspect,
)
from etherlyzer.core.interpretation.mac.normalization import normalize, normalize_strict
from etherlyzer.domain.entry.ethertype import EtherTypeEntry
from etherlyzer.domain.entry.mac import MACAllocationEntry

try:
    __version__ = version("etherlyzer")
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"


@cache
def _get_context() -> EtherlyzerContext:
    return initialize_etherlyzer()


def inspect_mac(mac: str) -> MacIdentityResult:
    return inspect(get_mac_structure(mac), _get_context())


def lookup_mac(mac: str) -> MACAllocationEntry | None:
    return _get_context().indexes.mac.lookup(mac)


def lookup_ethertype(ethertype: str) -> EtherTypeEntry | None:
    return _get_context().indexes.ethertype.lookup(ethertype.strip().upper())


def inspect_ethertype(ethertype: str) -> EtherTypeStruct:
    structure = get_ethertype_struct(ethertype)

    if not structure.is_ethertype:
        return structure

    entry = lookup_ethertype(ethertype)

    return get_ethertype_struct(
        structure.normalized,
        entry=entry,
    )


__all__ = [
    "HEX_DIGITS",
    "LENIENT_TYPOS",
    "RELAXED_TYPOS",
    "STRICT_TYPOS",
    "EtherTypeStruct",
    "MacForm",
    "MacIdentity",
    "MacIdentityResult",
    "MacResolution",
    "MacStructure",
    "extraction",
    "formatting",
    "inspect_ethertype",
    "inspect_mac",
    "lookup_mac",
    "normalize",
    "normalize_strict",
    "translation",
]
