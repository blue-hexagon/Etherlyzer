def read_multiline(
        linetype: str = "text",
        prompt: str = "Paste $1. Type $2 and press <Enter> when done:",
        marker: str = ";;;"
) -> list[str]:
    """ linetype: the kind of input you are reading, will be pasted into the prompts $1"""
    print(prompt.replace("$1", linetype).replace("$2", marker))

    lines = []

    while True:
        line = input()

        if line.strip() == marker:
            break
        if len(line.strip()) == 0:
            continue
        lines.append(line)

    return lines
