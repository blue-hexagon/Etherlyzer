def read_multiline(
    linetype: str = "text",
    prompt: str = "Paste $1. Enter a triple semicolon ;;; when done:",
) -> list[str]:
    print(prompt.replace("$1", linetype))

    lines = []

    while True:
        line = input()

        if line.strip() == ";;;":
            break
        if len(line.strip()) == 0:
            continue
        lines.append(line)

    return lines
