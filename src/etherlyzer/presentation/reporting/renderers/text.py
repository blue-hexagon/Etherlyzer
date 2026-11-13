from dataclasses import dataclass

from wcwidth import wcswidth

from etherlyzer.presentation.reporting.model import (
    Item,
    Report,
    ReportValue,
    Section,
    Table,
)


@dataclass(slots=True)
class TextRenderer:
    SHARED_WIDTH = 4
    indentation: int = 2

    def _render_table(self, table: Table, level: int) -> list[str]:
        self.indentation = 0
        if not table.columns:
            return []

        count = len(table.columns)

        for row in table.rows:
            if len(row) != count:
                raise ValueError("Table row has an invalid column count")

        def lines(val: ReportValue) -> list[str]:
            return ("" if val is None else str(val)).split("\n")

        def width(text: str) -> int:
            result = wcswidth(text)
            if result < 0:
                raise ValueError("Unsupported terminal control character")
            return result

        def pad(text: str, size: int, right: bool = False) -> str:
            padding = " " * (size - width(text))
            return padding + text if right else text + padding

        # Determine the width of every column.
        widths = [max(map(width, lines(name))) for name in table.columns]

        for row in table.rows:
            for i, value in enumerate(row):
                widths[i] = max(
                    widths[i],
                    *(width(line) for line in lines(value)),
                )

        prefix = " " * (level * self.indentation)

        # Unicode box-drawing borders.
        def border(left: str, join: str, right: str) -> str:
            segments = ["─" * (size + 2) for size in widths]
            return prefix + left + join.join(segments) + right

        # Render a logical row (potentially multiple physical lines).
        def render_row(
            values: tuple[ReportValue, ...],
            header: bool = False,
        ) -> list[str]:
            cells = [lines(val) for val in values]
            height = max(map(len, cells))
            output = []
            for line_index in range(height):
                rendered = []

                for idx, cell in enumerate(cells):
                    content = cell[line_index] if line_index < len(cell) else ""

                    # Right-align numeric values, except headers.
                    align_right = not header and type(values[idx]) in (int, float)

                    rendered.append(" " + pad(content, widths[idx], align_right) + " ")

                output.append(prefix + "│" + "│".join(rendered) + "│")

            return output

        return [
            border("╭", "┬", "╮"),
            *render_row(table.columns, header=True),
            border("├", "┼", "┤"),
            *(line for row in table.rows for line in render_row(row)),
            border("╰", "┴", "╯"),
        ]

    def render(self, report: Report) -> str:
        rows: list[tuple[str, bool, str]] = []

        def flush_grid(blocks: list[str], level: int) -> None:
            if not blocks:
                return

            prefix = " " * (level * self.indentation)
            cell_width = max(map(len, blocks)) + 2

            for i in range(0, len(blocks), 5):
                line = "".join(f"{block:<{cell_width}}" for block in blocks[i : i + 5]).rstrip()

                rows.append((prefix + line, False, ""))

            blocks.clear()

        def recurse(_section: Section, level: int) -> None:
            prefix = " " * (level * self.indentation)
            if _section.title:
                rows.append((f"{prefix}{_section.title}", False, ""))

            if _section.legend:
                rows.append(
                    (
                        f"{prefix}{' ' * self.indentation}Legend: {_section.legend}",
                        False,
                        "",
                    )
                )

            blocks: list[str] = []

            for child in _section.items:
                if isinstance(child, Item) and _section.layout == "grid":
                    blocks.append(f"[{child.key}] {child.value}")
                    continue

                flush_grid(blocks, level + 1)

                if isinstance(child, Section):
                    recurse(child, level + 1)

                elif isinstance(child, Table):
                    for line in self._render_table(child, level + 1):
                        rows.append((line, False, ""))  # noqa: PERF401

                elif isinstance(child, Item):
                    child_prefix = " " * ((level + 1) * self.indentation)
                    rows.append(
                        (
                            f"{child_prefix}{child.key}",
                            True,
                            str(child.value),
                        )
                    )

            flush_grid(blocks, level + 1)

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
