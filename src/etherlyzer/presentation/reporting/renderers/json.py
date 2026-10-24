import datetime
import json
from dataclasses import dataclass

from etherlyzer.presentation.reporting.model import Item, Report, Section


@dataclass(slots=True)
class JSONRenderer:
    indentation: int = 2

    def render(self, report: Report) -> str:
        def serialize(node: Section | Item) -> dict[str, str | int | float | datetime]:
            if isinstance(node, Item):
                return {
                    "type": "item",
                    "key": node.key,
                    "value": node.value,
                }

            return {
                "type": "section",
                "title": node.title,
                "items": [serialize(child) for child in node.items],
            }

        data = {"sections": [serialize(section) for section in report.sections]}

        return json.dumps(
            data,
            indent=self.indentation,
            ensure_ascii=False,
        )
