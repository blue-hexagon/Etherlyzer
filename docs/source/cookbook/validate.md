# Validate MAC Addresses

The `validate` command checks and normalizes MAC address input without attempting typo correction.

Valid input is normalized, while malformed input is identified and reported with a validation mask describing the detected problems.

Unlike [`format`](format.md), which supports corrective formatting, `validate` preserves the distinction between accepted and malformed input.

For details about validation masks and their interpretation, see {doc}`../concepts/validation`.

## Basic usage

Validate a single MAC address:

```text
etherlyzer validate 00:11:22:33:44:55
```

For multiple addresses, use `-b` or `--bulk` to enter input interactively:

```text
etherlyzer validate -b
```

Terminate bulk input by entering `;;;` on a separate line.

## Input validation

EtherLyzer accepts different textual representations of MAC addresses and normalizes successfully validated input.

| Input                  | Classification | Reason                          |
|------------------------|----------------|---------------------------------|
| `00:11:22:33:44:55`    | Valid          | Colon-separated hexadecimal     |
| `00-11-22-33-44-55`    | Valid          | Hyphen-separated hexadecimal    |
| `0011.2233.4455`       | Valid          | Cisco-style hexadecimal         |
| `001122334455`         | Valid          | Twelve hexadecimal digits       |
| `00:11:22:33:44`       | Invalid        | Insufficient hexadecimal digits |
| `00:11:22:33:44:55:66` | Invalid        | Excess hexadecimal digits       |
| `00:11:22:33:44:ZZ`    | Invalid        | Non-hexadecimal characters      |

Validation is not limited to conventional separator placement. Some unconventional arrangements may still be normalized successfully.

### Validation masks

Malformed input is reported using validation masks that describe the problems detected during processing.

These can help distinguish between incorrect address lengths, unexpected characters, and other input irregularities.

:::{note}
Validation checks whether input can be accepted and normalized as a MAC address representation.

It does not establish IEEE registration, vendor identity, or whether an address is appropriate for use on an Ethernet network.

For the meaning of individual validation masks, see {doc}`../concepts/validation`.
:::

## Output controls

The command provides four options for controlling validation output.

| Option                 | Purpose                                          |
|------------------------|--------------------------------------------------|
| `-l, --linenumbers`    | Include original input line numbers              |
| `-s, --strict`         | Output only successfully normalized addresses    |
| `-o, --show-originals` | Display the original input alongside each result |
| `-i, --show-info`      | Prefix results with `OK` or `ERR`                |

These options can be combined.

### Common combinations

| Purpose                              | Command                      |
|--------------------------------------|------------------------------|
| Validate multiple addresses          | `etherlyzer validate -b`     |
| Output only valid addresses          | `etherlyzer validate -bs`    |
| Include original line numbers        | `etherlyzer validate -bl`    |
| Show validation status               | `etherlyzer validate -bi`    |
| Show original input                  | `etherlyzer validate -bo`    |
| Line numbers and validation status   | `etherlyzer validate -bli`   |
| Original input and validation status | `etherlyzer validate -boi`   |
| All reporting options                | `etherlyzer validate -bloi`  |
| Strict validation with all options   | `etherlyzer validate -blsoi` |

### Strict mode

Use `-s` or `--strict` to suppress invalid entries and output only successfully normalized addresses.

```text
etherlyzer validate -bs
```

Strict mode is useful when preparing normalized address lists for further processing.

When combined with `--linenumbers`, retained entries preserve their original input line numbers rather than being renumbered consecutively.

## Complete validation example

The following example combines bulk input, line numbers, original values, validation status, and strict filtering:

```text
etherlyzer validate -lbois
```

Input:

```text
Paste MAC addresses. Type ;;; and press <Enter> when done:
001a2b3c4d5e
001a2b3c4d5
001a2b3c4d5e6
001a2b3c4d5?
001a2b3c4d5O
001a2b3c4d5I
001a2b3c4d5L
001a2b3c4d5S
001a2b3c4d5eF
001a2b3c4d5eO
001a2b3c4d5eI
001a2b3c4d5eL
001a2b3c4d5eS
001a2b3c4d5e?
001a2b3c4d5eFF
001a2b3c4d5eOO
001a2b3c4d5eII
001a2b3c4d5eSS
00:1a:2b:3c:4d:5e
00-1a-2b-3c-4d-5e
001a.2b3c.4d5e
0:0:1:a:2:b:3:c:4:d:5:e
00 : 1a : 2b : 3c : 4d : 5e
"00:1a:2b:3c:4d:5e"
00::1a::2b::3c::4d::5e
00:1a-2b.3c:4d-5e
;;;
```

Output:

```text
1.  OK  001a2b3c4d5e    <~ 001a2b3c4d5e
14. OK  001a2b3c4d5e    <~ 001a2b3c4d5e?
19. OK  001a2b3c4d5e    <~ 00:1a:2b:3c:4d:5e
20. OK  001a2b3c4d5e    <~ 00-1a-2b-3c-4d-5e
21. OK  001a2b3c4d5e    <~ 001a.2b3c.4d5e
22. OK  001a2b3c4d5e    <~ 0:0:1:a:2:b:3:c:4:d:5:e
23. OK  001a2b3c4d5e    <~ 00 : 1a : 2b : 3c : 4d : 5e
24. OK  001a2b3c4d5e    <~ "00:1a:2b:3c:4d:5e"
25. OK  001a2b3c4d5e    <~ 00::1a::2b::3c::4d::5e
26. OK  001a2b3c4d5e    <~ 00:1a-2b.3c:4d-5e

Normalized 10/26 MAC addresses. Invalid MAC addresses identified: 16/26
```

This example illustrates several important behaviors:

- **Normalization:** Different separator arrangements can resolve to the same address.
- **Validation:** Inputs containing malformed hexadecimal data are distinguished from accepted input.
- **Strict filtering:** Only successfully normalized entries appear in the output.
- **Line preservation:** Output retains the original input line numbers, including gaps created by filtered entries.
- **Original values:** The `<~` notation associates normalized results with their original representations.

:::{important}
Validation does not perform typo correction. However, accepted normalization rules may discard certain non-hexadecimal characters, as demonstrated by line 14.

For this reason, successful normalization should not be interpreted as proof that the original input followed conventional MAC address notation.
:::

## Practical workflows

### Identify malformed entries in an inventory

Use bulk validation with line numbers, status indicators, and original input:

```text
etherlyzer validate -bloi
```

This helps correlate validation results with their original inventory entries and identify addresses requiring review.

### Prepare normalized input

Enable strict mode to suppress malformed addresses:

```text
etherlyzer validate -bs
```

The resulting output contains only successfully normalized addresses, suitable for subsequent processing.

### Review unconventional address notation

Preserve the original input alongside its normalized representation:

```text
etherlyzer validate -boi
```

This is useful when examining addresses collected from systems with different formatting conventions or inconsistent input quality.

## Command reference

```text
usage: etherlyzer validate [-h] [-l] [-s] [-o] [-i] (-b | mac)
```

| Argument / Option      | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| `mac`                  | MAC address to validate and normalize.                                      |
| `-b, --bulk`           | Read multiple MAC addresses interactively.                                  |
| `-l, --linenumbers`    | Prefix results with their original input line numbers.                      |
| `-s, --strict`         | Suppress invalid entries and output only successfully normalized addresses. |
| `-o, --show-originals` | Display original input alongside normalized results.                        |
| `-i, --show-info`      | Include `OK` or `ERR` validation status.                                    |
| `-h, --help`           | Display command help.                                                       |

Exactly one input source, `mac` or `-b`, must be provided.
