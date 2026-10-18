def read_multiline(
    linetype: str = "text",
    prompt: str = "Paste $1. Type $2 and press <Enter> when done:",
    delimiter: str = ";;;",
    skip_empty_lines: bool = True,
) -> list[str]:
    """linetype: the kind of input you are reading, will be pasted into the prompts $1"""
    print(prompt.replace("$1", linetype).replace("$2", delimiter))

    lines = []

    while True:
        line = input()

        if line.strip() == delimiter:
            break
        if len(line.strip()) == 0 and skip_empty_lines:
            continue
        lines.append(line)

    return lines


def print_table(
    rows: list[tuple[str, ...]],
    headers: tuple[str, ...] | None = None,
    delimiter: str | None = None,
) -> None:
    if headers:
        rows = [headers, *rows]

    if not rows:
        return

    if delimiter is not None:
        for row in rows:
            print(delimiter.join(row))
        return

    widths = [max(len(row[i]) for row in rows) for i in range(len(rows[0]))]

    for row in rows:
        print("  ".join(value.ljust(width) for value, width in zip(row, widths)).rstrip())
