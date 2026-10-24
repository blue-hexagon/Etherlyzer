from dataclasses import dataclass

from etherlyzer.presentation.reporting.model import Report, Section


@dataclass(slots=True)
class TextRenderer:
    SHARED_WIDTH = 4
    indentation: int = 2

    def render(self, report: Report) -> str:
        rows: list[tuple[str, bool, str]] = []

        def recurse(_section: Section, level: int) -> None:
            prefix = " " * (level * self.indentation)
            rows.append((f"{prefix}{_section.title}", False, ""))

            for child in _section.items:
                if isinstance(child, Section):
                    recurse(child, level + 1)
                else:
                    prefix = " " * ((level + 1) * self.indentation)
                    rows.append((f"{prefix}{child.key}", True, str(child.value)))

        for section in report.sections:
            if rows:
                rows.append(("", False, ""))
            recurse(section, 0)

        width = (
            max(
                (len(label) for label, is_item, _ in rows if is_item),
                default=0,
            )
            + self.SHARED_WIDTH
        )

        return "\n".join(
            f"{label:<{width}}: {value}" if is_item else label for label, is_item, value in rows
        )
