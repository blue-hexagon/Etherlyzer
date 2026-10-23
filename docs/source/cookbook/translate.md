# Translate MAC Addresses

The `translation.py` command converts MAC addresses into numerical, binary, and byte-oriented representations.

Unlike [`format`](format.md), which changes an address's notation, `translation.py` interprets its underlying 48-bit value in different forms.

It supports individual and bulk input, semi-strict normalization, and reporting of invalid input lines.

## Basic usage

Translate a MAC address into all available representations:

```text
etherlyzer translate 40:06:AF:F1:08:08
```

Select a specific representation using `-t` or `--to`:

```text
etherlyzer translate 40:06:AF:F1:08:08 -t decimal_bytes
```

Output:

```text
64 6 175 241 8 8
```

By default, `translation.py` displays all supported representations.

## Available representations

The following representations are available for `40:06:AF:F1:08:08`:

| Representation  | Output                                                  | Description                              |
|-----------------|---------------------------------------------------------|------------------------------------------|
| `canonical`     | `40-06-AF-F1-08-08`                                     | Hyphen-separated hexadecimal octets      |
| `bit_reversed`  | `02:60:F5:8F:10:10`                                     | Bit order reversed within each octet     |
| `hex`           | `0x4006AFF10808`                                        | Complete 48-bit hexadecimal value        |
| `decimal`       | `70,397,465,790,472`                                    | Complete unsigned decimal value          |
| `decimal_bytes` | `64 6 175 241 8 8`                                      | Individual decimal octets                |
| `binary`        | `01000000.00000110.10101111.11110001.00001000.00001000` | Binary with octet boundaries             |
| `binary_raw`    | `010000000000011010101111111100010000100000001000`      | Continuous 48-bit binary                 |
| `hex_bytes`     | `0x40 0x06 0xAF 0xF1 0x08 0x08`                         | Individually prefixed hexadecimal octets |
| `bytes`         | `40 06 AF F1 08 08`                                     | Space-separated hexadecimal octets       |

Use `-t all` (the default) to display every representation.

### Numerical values and octets

A MAC address contains six octets, totaling 48 bits.

The entire address can be interpreted as one unsigned integer in big-endian (network) byte order:

```text
Hexadecimal : 0x4006AFF10808
Decimal     : 70,397,465,790,472
```

Alternatively, its octets can be represented individually:

```text
Hexadecimal bytes : 0x40 0x06 0xAF 0xF1 0x08 0x08
Decimal bytes     : 64 6 175 241 8 8
```

The distinction is whether the address is treated as one integer or six separate byte values.

### Binary representation

The `binary` representation preserves octet boundaries, whereas `binary_raw` produces an uninterrupted 48-bit sequence.

```text
Binary     : 01000000.00000110.10101111.11110001.00001000.00001000
Binary raw : 010000000000011010101111111100010000100000001000
```

These representations are useful for examining address bits, identifying recurring patterns, and comparing MAC addresses with packet data.

### Bit reversal

The `bit_reversed` representation reverses the eight bits within each octet, primarily for compatibility with historical non-canonical address representations.

For example:

```text
Original : 0x40 = 01000000
Reversed : 0x02 = 00000010
```

Applied to the complete address:

```text
Original     : 40:06:AF:F1:08:08
Bit-reversed : 02:60:F5:8F:10:10
```

This transformation is relevant to historical interoperability between Ethernet and technologies such as Token Ring.

See [RFC 2469](https://www.rfc-editor.org/rfc/rfc2469) for additional background.

:::{important}
Bit reversal is not byte reversal or an endianness conversion.

The bits within each octet are reversed, while the order of the six octets remains unchanged.
:::

## Bulk translation

Use `-b` or `--bulk` to translate multiple addresses interactively.

```text
etherlyzer translate -b -t decimal_bytes
```

Include original input line numbers using `-l` or `--linenumbers`:

```text
etherlyzer translate -bl -t decimal_bytes
```

Bulk processing preserves input order, making it possible to correlate translated values with their original entries.

### Common conversions

| Purpose                                       | Command                                     |
|-----------------------------------------------|---------------------------------------------|
| Translate multiple addresses                  | `etherlyzer translate -b`                   |
| Convert to decimal                            | `etherlyzer translate -b -t decimal`        |
| Compare decimal octets                        | `etherlyzer translate -bl -t decimal_bytes` |
| Examine hexadecimal octets                    | `etherlyzer translate -b -t hex_bytes`      |
| Examine individual bits                       | `etherlyzer translate -b -t binary`         |
| Display bit-reversed addresses                | `etherlyzer translate -b -t bit_reversed`   |
| Display all representations with line numbers | `etherlyzer translate -bl -t all`           |

For large datasets, selecting one representation generally produces more compact output than `all`.

## Complete translation output

Omitting `-t`, or explicitly selecting `all`, displays every supported representation:

```text
etherlyzer translate -bl -t all
```

Example output:

```text
Line 1
  Input          : 00:1A:2B:3C:4D:5E
  Canonical      : 00-1A-2B-3C-4D-5E
  Bit Reversed   : 00:58:D4:3C:B2:7A
  Decimal        : 112,394,521,950
  Decimal Bytes  : 0 26 43 60 77 94
  Binary         : 00000000.00011010.00101011.00111100.01001101.01011110
  Binary Raw     : 000000000001101000101011001111000100110101011110
  Hex            : 0x001A2B3C4D5E
  Hex Bytes      : 0x00 0x1A 0x2B 0x3C 0x4D 0x5E
  Bytes          : 00 1A 2B 3C 4D 5E
```

## Practical workflows

### Investigate unusual MAC address patterns

Translate multiple addresses into decimal octets:

```text
etherlyzer translate -bl -t decimal_bytes
```

Example output:

```text
1. 220 224 222 25  193 220
2. 187 165 201 142 157 83
3. 11  63  87  150 50  104
4. 31  97  110 143 55  250
5. 78  102 18  128 30  183
6. 42  201 218 19  52  251
7. 76  34  46  52  61  183
8. 189 11  190 136 209 24
```

Representing addresses as decimal octets makes it easier to compare individual byte values and recognize recurring patterns.

For bit-level investigation, use:

```text
etherlyzer translate -bl -t binary
```

### Analyze addresses extracted from a capture

First, discover unique addresses:

```text
etherlyzer extract -f capture.pcap -u
```

Then translate the extracted addresses using interactive bulk input:

```text
etherlyzer translate -bl -t hex_bytes
```

This produces byte-oriented hexadecimal representations suitable for comparison with packet data and hexadecimal dumps.

For address classification and IEEE allocation analysis, use [`inspect`](inspect.md).

## Input validation

The `translation.py` command uses semi-strict normalization.

Accepted input must contain exactly **12 hexadecimal digits**. Supported separators (`:`, `-`, `.`, and spaces) are permitted, including unconventional arrangements.

For example, these inputs represent the same value:

```text
00:1A:2B:3C:4D:5E
00-1A-2B-3C-4D-5E
001A.2B3C.4D5E
001A2B3C4D5E
00 1A 2B 3C 4D 5E
```

Inputs with missing or excess hexadecimal digits, or unsupported characters, are rejected.

During bulk translation, invalid input lines are identified for review:

```text
3 invalid lines: 4, 7, 12
```

:::{note}
Successful translation means that the input could be interpreted as a complete 48-bit value.

It does not establish IEEE registration, vendor identity, or whether the address is suitable for use on an Ethernet network.

Use [`validate`](validate.md) for input diagnostics and [`inspect`](inspect.md) for address-property analysis.
:::

## Command reference

```text
usage: etherlyzer translate [-h] [-b] [-l] [--parse-invalid-macs]
                            [-t FORMAT] [mac]
```

| Argument / Option      | Description                                                      |
|------------------------|------------------------------------------------------------------|
| `mac`                  | MAC address to translate.                                        |
| `-b, --bulk`           | Read multiple addresses interactively.                           |
| `-l, --linenumbers`    | Retain original input line numbers.                              |
| `-t, --to FORMAT`      | Select a representation (default: `all`).                        |
| `--parse-invalid-macs` | Enable permissive parsing of malformed input, where implemented. |
| `-h, --help`           | Display command help.                                            |

Supported values for `-t`:

```text
canonical, bit_reversed, hex, decimal, decimal_bytes,
binary, binary_raw, hex_bytes, bytes, all
```
