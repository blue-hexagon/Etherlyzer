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
