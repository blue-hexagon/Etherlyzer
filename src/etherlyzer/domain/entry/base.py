from dataclasses import astuple, dataclass, fields


@dataclass(frozen=True, slots=True)
class BaseEntry:
    @classmethod
    def get_header(cls) -> list[str]:
        return [f.name for f in fields(cls)]

    def get_row(self) -> tuple[str, ...]:
        return astuple(self)

    def __hash__(self) -> int:
        return hash(astuple(self))
