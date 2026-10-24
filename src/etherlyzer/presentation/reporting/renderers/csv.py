import csv
from dataclasses import dataclass
from io import StringIO

from etherlyzer.presentation.reporting.model import Report, Section


@dataclass(slots=True)
class CSVRenderer:
    delimiter: str = ","

    def render(self, report: Report) -> str:
        output = StringIO(newline="")
        writer = csv.writer(
            output,
            delimiter=self.delimiter,
            lineterminator="\n",
        )

        writer.writerow(("section_path", "key", "value"))

        def recurse(_section: Section, path: tuple[str, ...]) -> None:
            current_path = (*path, _section.title)

            for child in _section.items:
                if isinstance(child, Section):
                    recurse(child, current_path)
                else:
                    writer.writerow(
                        (
                            " / ".join(current_path),
                            child.key,
                            "" if child.value is None else child.value,
                        )
                    )

        for section in report.sections:
            recurse(section, ())

        return output.getvalue()
