import os
from dataclasses import MISSING, dataclass, fields
from enum import Enum, StrEnum
from pathlib import Path

from dotenv import load_dotenv

from etherlyzer.util.dirs import DATA_PLATFORM_DIR



class MACCasing(StrEnum):
    UPPER = "upper"
    LOWER = "lower"


@dataclass(slots=True, frozen=True)
class EtherlyzerKnobs:
    db_update_interval_hours: int = 24

    field_separator: str = ";"
    mac_separator: str = "."
    mac_block_size: int = 4
    mac_case: MACCasing = MACCasing.UPPER

    show_sync_messages: bool = False

    def __post_init__(self) -> None:  # noqa
        if not (DATA_PLATFORM_DIR / "etherlyzer.env").exists():
            from importlib.resources import files
            import shutil
            template_env = files("etherlyzer").joinpath("etherlyzer.env")
            destination_env = DATA_PLATFORM_DIR / "etherlyzer.env"
            with template_env.open("rb") as src, destination_env.open("wb") as dst:
                shutil.copyfileobj(src, dst)
        load_dotenv(DATA_PLATFORM_DIR / "etherlyzer.env")


def validate_knobs(conf: EtherlyzerKnobs) -> None:
    if conf.db_update_interval_hours <= 0:
        raise ValueError(
            "DB_UPDATE_INTERVAL_HOURS must be greater than zero."
        )

    if len(conf.field_separator) != 1:
        raise ValueError(
            "FIELD_SEPARATOR must contain exactly one character."
        )

    if conf.mac_separator not in {"", ":", "-", "."}:
        raise ValueError(
            "MAC_SEPARATOR must be one of '', ':', '-', or '.'."
        )

    if conf.mac_block_size not in {2, 4, 12}:
        raise ValueError(
            "MAC_BLOCK_SIZE must be 2, 4, or 12."
        )


def load_config(cls: type[EtherlyzerKnobs]) -> EtherlyzerKnobs:
    values = {}

    for field in fields(cls):
        env_name = field.name.upper()

        value = os.getenv(env_name)

        if value is None:
            if field.default is not MISSING:
                values[field.name] = field.default
            elif field.default_factory is not MISSING:
                values[field.name] = field.default_factory()
            else:
                raise ValueError(
                    f"Missing required environment variable {env_name}"
                )

        type_ = field.type

        if type_ is bool:
            values[field.name] = value.lower() in {"1", "true", "yes", "on"}

        elif type_ is int:
            values[field.name] = int(value)

        elif type_ is float:
            values[field.name] = float(value)

        elif type_ is str:
            values[field.name] = value
        elif type_ is Path:
            values[field.name] = Path(value)

        elif issubclass(type_, Enum):
            values[field.name] = type_(value)

        else:
            raise TypeError(f"Unsupported config type: {type_}")
    return cls(**values)


config = load_config(EtherlyzerKnobs)
validate_knobs(config)
