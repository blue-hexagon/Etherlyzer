# Format MAC Addresses

The `format` command converts MAC addresses into a selected representation.

Formatting can control:

- separator,
- block size,
- letter casing, and
- optional typo correction.

## Basic usage

```text
etherlyzer format 001122334455
```

## Convert separators

```text
etherlyzer format 00-11-22-33-44-55 -p :
```

## Cisco-style blocks

```text
etherlyzer format 001122334455 -p . -s 4
```

## Uppercase output

```text
etherlyzer format 00:11:22:33:44:55 -c upper
```

## Correct supported typo-like input

Use `--fix-typos` to correct supported character substitutions before formatting:

```text
etherlyzer format O0:1i:22:33:44:s5 --fix-typos
```

## Bulk formatting

```text
etherlyzer format -b -p . -s 4 --fix-typos
```

## Example

```text
etherlyzer format l..iIdOØ1!23-4oo.. --fix-typos --casing upper --block-size 4 --separator .
```

```text
111D.0012.3400
```

The `format` command performs formatting and optional typo correction, but does not perform MAC-address validation.

Use the [`validate`](validate.md) command when validation and diagnostic output are required.

## Command reference

```text
usage: etherlyzer format [-h] [-b] [-p SEPARATOR] [-s BLOCK_SIZE]
                         [-c {lower,upper}] [-f] [mac]

Format MAC addresses using a selected separator, block size, and casing.
Optional typo correction can repair supported character substitutions.
This command formats input without performing MAC address validation.

positional arguments:
  mac                   MAC address to format.

options:
  -h, --help            show this help message and exit
  -b, --bulk            Read multiple MAC addresses interactively.
  -p, --separator SEPARATOR
                        Output separator: ':', '-', '.', or empty (default: ':').
  -s, --block-size BLOCK_SIZE
                        Number of hexadecimal characters per block (default: 2).
  -c, --casing {lower,upper}
                        Output hexadecimal casing (default: lower).
  -f, --fix-typos       Correct supported typo-like character substitutions before formatting.
```
