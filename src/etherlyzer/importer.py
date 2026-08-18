from __future__ import annotations

import csv
from dataclasses import MISSING, fields
from pathlib import Path
from typing import Any, TypeVar

T = TypeVar("T")


class CSVImporter:

    @staticmethod
    def normalize(name: str) -> str:
        return (
            name.strip()
            .lower()
            .replace("-", "_")
            .replace(" ", "_")
        )

    @staticmethod
    def convert(value: str, typ: type) -> Any:
        if value == "":
            return None

        if typ is int:
            return int(value)

        if typ is float:
            return float(value)

        if typ is bool:
            return value.lower() in {
                "true",
                "1",
                "yes",
            }

        return value

    @classmethod
    def load(cls, path: str | Path, model: type[T]) -> list[T]:
        model_fields = {
            cls.normalize(field.name): field
            for field in fields(model)
        }

        objects: list[T] = []

        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                kwargs = {}
                for header, value in row.items():
                    field_name = cls.normalize(header)
                    field = model_fields.get(field_name)

                    if field is None:
                        continue
                    kwargs[field.name] = cls.convert(
                        value,
                        field.type,
                    )

                cls.validate(model_fields, kwargs)
                objects.append(model(**kwargs))

        return objects

    @staticmethod
    def validate(model_fields, kwargs):
        missing = [
            field.name
            for field in model_fields.values()
            if (field.name not in kwargs and field.default is MISSING and field.default_factory is MISSING)
        ]

        if missing: raise ValueError(f"Missing required fields: {', '.join(missing)}")
