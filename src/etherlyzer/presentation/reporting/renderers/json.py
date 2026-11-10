import json
from dataclasses import dataclass

from etherlyzer.presentation.reporting.model import Item, Report, Section

type JSONValue = str | int | float | bool | list[JSONValue] | dict[str, JSONValue] | None


@dataclass(slots=True)
class JSONRenderer:
    indentation: int = 2

    def render(self, report: Report) -> str:
        def serialize(node: Section | Item) -> dict[str, JSONValue]:
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
