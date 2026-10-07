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

## Command reference

```text
usage: etherlyzer validate [-h] [-b] [-l] [-s] [-o] [-i] [mac]

Validate and normalize MAC addresses without typo correction.
Malformed input is reported rather than corrected; use `format`
for corrective formatting.

positional arguments:
  mac                   MAC address to validate and normalize.

options:
  -h, --help            show this help message and exit
  -b, --bulk            Read multiple MAC addresses interactively.
  -l, --linenumbers     Prefix output lines with their corresponding input line number.
  -s, --strict          Suppress invalid entries and output only successfully normalized MAC addresses.
  -o, --show-originals  Show the original input alongside each normalized MAC address.
  -i, --show-info       Prefix each result with OK or ERR to indicate validation status.
```
