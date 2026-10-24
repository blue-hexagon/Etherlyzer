import os
import shutil
from dataclasses import MISSING, dataclass, fields
from enum import Enum, StrEnum
from importlib.resources import files
from pathlib import Path
from typing import get_type_hints

from dotenv import load_dotenv

from etherlyzer.util.dirs import DEFAULT_CACHE_DIR


class MACCasing(StrEnum):
    UPPER = "upper"
    LOWER = "lower"


INTERVAL_ALIASES = {
    "hourly": 1,
    "daily": 24,
    "twice-weekly": 84,
    "weekly": 7 * 24,
    "fortnightly": 14 * 24,
    "twice-monthly": 15 * 24,
    "monthly": 30 * 24,
    "quarterly": 90 * 24,
    "yearly": 365 * 24,
}


@dataclass(slots=True, frozen=True)
class EtherlyzerKnobs:
    db_update_interval_hours: int = INTERVAL_ALIASES["weekly"]

    field_separator: str = ";"
    mac_separator: str = "."
    mac_block_size: int = 4
    mac_case: MACCasing = MACCasing.UPPER

    show_sync_messages: bool = False


def _load_environment() -> None:
    DEFAULT_CACHE_DIR.mkdir(parents=True, exist_ok=True)

    destination_env = DEFAULT_CACHE_DIR / "etherlyzer.env"

    if not destination_env.exists():
        template_env = files("etherlyzer").joinpath("etherlyzer.env")

        with template_env.open("rb") as src, destination_env.open("wb") as dst:
            shutil.copyfileobj(src, dst)

    load_dotenv(destination_env)


def _validate_knobs(kbobs: EtherlyzerKnobs) -> None:
    if kbobs.db_update_interval_hours <= 0:
        raise ValueError("DB_UPDATE_INTERVAL_HOURS must be greater than zero.")

    if len(kbobs.field_separator) != 1:
        raise ValueError("FIELD_SEPARATOR must contain exactly one character.")

    if kbobs.mac_separator not in {"", ":", "-", "."}:
        raise ValueError("MAC_SEPARATOR must be one of '', ':', '-', or '.'.")

    if kbobs.mac_block_size not in {2, 4, 12}:
        raise ValueError("MAC_BLOCK_SIZE must be 2, 4, or 12.")


def knobs_builder(cls: type[EtherlyzerKnobs]) -> EtherlyzerKnobs:
    """Empty env-values specified in the env-file, are not equivalent to a None-value,
    they are equal to an empty string."""
    values = {}
    type_hints = get_type_hints(cls)

    for field in fields(cls):
        env_name = field.name.upper()
        value = os.getenv(env_name)

        # ------------------------------------------------------------------ Value is None
        if value is None:
            if field.default is not MISSING:
                values[field.name] = field.default
                continue
            if field.default_factory is not MISSING:
                values[field.name] = field.default_factory()
                continue

            raise ValueError(f"Missing required environment variable {env_name}")

        type_ = type_hints[field.name]
        # Resolve symbolic interval values before integer conversion.
        if field.name == "db_update_interval_hours":
            value = str(INTERVAL_ALIASES.get(value.strip().lower(), value))

        # ------------------------------------------------------------------ Value is Bool
        if type_ is bool:
            normalized_value = value.strip().lower()
            if normalized_value in {"1", "true", "yes", "on"}:
                values[field.name] = True
            elif normalized_value in {"0", "false", "no", "off"}:
                values[field.name] = False

            else:
                raise ValueError(f"Invalid Boolean value for {env_name}: {value!r}")

        # ------------------------------------------------------------------ Value is Integer
        elif type_ is int:
            values[field.name] = int(value)

        # ------------------------------------------------------------------ Value is Float
        elif type_ is float:
            values[field.name] = float(value)

        # ------------------------------------------------------------------ Value is String
        elif type_ is str:
            if env_name == "DB_UPDATE_INTERVAL_HOURS":
                if value.lower() == "daily":
                    values[field.name] = 24
                elif value.lower() == "weekly":
                    values[field.name] = 7 * 24
                elif value.lower() == "monthly":
                    values[field.name] = 30 * 24
                elif value.lower() == "quarterly":
                    values[field.name] = 30 * 24 * 3
                elif value.lower() == "yearly":
                    values[field.name] = 365 * 24
            else:
                values[field.name] = value

        # ------------------------------------------------------------------ Value is Path
        elif type_ is Path:
            values[field.name] = Path(value)

        # ------------------------------------------------------------------ Value is Enum
        elif isinstance(type_, type) and issubclass(type_, Enum):
            values[field.name] = type_(value)

        else:
            raise TypeError(f"Unsupported config type: {type_}")

    return cls(**values)


def load_knobs() -> EtherlyzerKnobs:
    _load_environment()
    knobs = knobs_builder(EtherlyzerKnobs)
    _validate_knobs(knobs)
    return knobs


etherlyzer_knobs = load_knobs()
