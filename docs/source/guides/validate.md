# Validate MAC Addresses

The `validate` command analyzes MAC-address input without attempting typo correction.

Valid input is normalized, while malformed input is reported together with a validation mask describing the detected problems.

For details about validation masks, see {doc}`../concepts/validation`.

## Basic usage

```text
etherlyzer validate 00:11:22:33:44:55
```

## Bulk validation

Read multiple MAC addresses interactively:

```text
etherlyzer validate -b
```

## Output controls

Only output successfully normalized MAC addresses:

```text
etherlyzer validate -b --strict
```

Include input line numbers and validation status:

```text
etherlyzer validate -b --linenumbers --show-info
```

Show the original input alongside the normalized result:

```text
etherlyzer validate -b --show-originals
```

The `validate` command reports malformed input rather than correcting it.

For corrective formatting and supported typo substitution, see {doc}`format`.

## Putting it all together
```text
etherlyzer validate -lbois
```
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
## Command reference

```text
usage: etherlyzer validate [-h] [-l] [-s] [-o] [-i] (-b | mac)

Validate and normalize MAC addresses without typo correction. Malformed input is reported rather than corrected; use `format` for corrective formatting.

positional arguments:
  mac                   MAC address to validate and normalize.

options:
  -h, --help            show this help message and exit
  -b, --bulk            Read multiple MAC addresses interactively.
  -l, --linenumbers     Prefix output lines with their corresponding input line number.
  -s, --strict          Suppress invalid entries and output only successfully normalized MAC addresses.
  -o, --show-originals  Show the original input alongside each normalized MAC address.
  -i, --show-info       Prefix each result with OK or ERR to indicate validation status.

Examples:
  etherlyzer validate 00:11:22:33:44:55
  etherlyzer validate -b
  etherlyzer validate -b --strict
  etherlyzer validate -b --linenumbers --show-info
  etherlyzer validate -b --show-originals
```
