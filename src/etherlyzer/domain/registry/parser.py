from __future__ import annotations

import csv
from dataclasses import MISSING, Field, fields, is_dataclass
from pathlib import Path
from typing import Any, TypeVar, get_type_hints

from etherlyzer.core.types import PathInput

T = TypeVar("T")


class RegistryParser:
    """Parses all the IEEE CSV files"""

    @staticmethod
    def _validate_model(model: type[object]) -> None:
        if not is_dataclass(model):
            raise TypeError(f"{model.__name__} must be a dataclass")

    @staticmethod
    def normalize(name: str) -> str:
        return name.strip().lower().replace("-", "_").replace(" ", "_")

    @staticmethod
    def convert(value: str, _type: type) -> Any:

        if value == "":
            return None

        if _type is int:
            return int(value)

        if _type is float:
            return float(value)

        if _type is bool:
            return value.lower() in {
                "true",
                "1",
                "yes",
            }

        return value

    @classmethod
    def load_file(cls, path: PathInput, model: type[T]) -> list[T]:
        path = Path(path)
        cls._validate_model(model)
        model_fields = {cls.normalize(field.name): field for field in get_dataclass_fields(model)}
        model_types = get_type_hints(model)

        objects: list[T] = []

        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                kwargs: dict[str, Any] = {}

                for header, value in row.items():
                    if header is None:
                        raise ValueError(f"Malformed CSV row: more values than headers: {row!r}")

                    field_name = cls.normalize(header)
                    field = model_fields.get(field_name)

                    if field is None:
                        continue

                    if value is None:
                        raise ValueError(f"Missing CSV value for field {header!r}")

                    kwargs[field.name] = cls.convert(
                        value,
                        model_types[field.name],
                    )

                cls.validate(model_fields, kwargs)
                objects.append(model(**kwargs))

        return objects

    @staticmethod
    def validate(
        model_fields: dict[str, Field[Any]],
        kwargs: dict[str, Any],
    ) -> None:
        missing = [
            field.name
            for field in model_fields.values()
            if (
                field.name not in kwargs
                and field.default is MISSING
                and field.default_factory is MISSING
            )
        ]

        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")


def get_dataclass_fields(
    model: type[object],
) -> tuple[Field[Any], ...]:
    if not is_dataclass(model):
        raise TypeError(f"{model.__name__} must be a dataclass")

    return fields(model)
