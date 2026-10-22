# Format MAC Addresses

The `format` command standardizes MAC address notation using configurable separators, block sizes, and hexadecimal casing.

It supports individual and bulk input, with optional correction of supported typing mistakes.

Unlike [`validate`](validate.md), which identifies malformed addresses, `format` focuses on transforming their textual representation without performing address validation.

## Basic usage

Format a single MAC address:

```text
etherlyzer format 001122334455
```

Output:

```text
00:11:22:33:44:55
```

By default, addresses are formatted using lowercase hexadecimal, colon separators, and two-character blocks.

Use `-b` or `--bulk` to format multiple addresses interactively:

```text
etherlyzer format -b
```

## Customize formatting

The command provides three independent formatting controls:

| Option             | Purpose                                    | Default |
|--------------------|--------------------------------------------|---------|
| `-p, --separator`  | Character separating hexadecimal blocks    | `:`     |
| `-s, --block-size` | Number of hexadecimal characters per block | `2`     |
| `-c, --casing`     | Lowercase or uppercase hexadecimal         | `lower` |

### Formatting examples

For the input `aabbccddeeff`:

| Purpose                  | Options              | Output              |
|--------------------------|----------------------|---------------------|
| Default notation         | None                 | `aa:bb:cc:dd:ee:ff` |
| Hyphen separators        | `-p -`               | `aa-bb-cc-dd-ee-ff` |
| Period separators        | `-p .`               | `aa.bb.cc.dd.ee.ff` |
| Cisco-style notation     | `-p . -s 4`          | `aabb.ccdd.eeff`    |
| Four-character blocks    | `-p - -s 4`          | `aabb-ccdd-eeff`    |
| Uppercase hexadecimal    | `-c upper`           | `AA:BB:CC:DD:EE:FF` |
| Uppercase Cisco notation | `-p . -s 4 -c upper` | `AABB.CCDD.EEFF`    |
| No separators            | `-p ""`              | `aabbccddeeff`      |

These options can be combined to produce the desired output notation.

### Common commands

| Purpose                   | Command                                    |
|---------------------------|--------------------------------------------|
| Format a single address   | `etherlyzer format aabbccddeeff`           |
| Format multiple addresses | `etherlyzer format -b`                     |
| Use hyphen separators     | `etherlyzer format aabbccddeeff -p -`      |
| Use Cisco-style notation  | `etherlyzer format aabbccddeeff -p . -s 4` |
| Use uppercase hexadecimal | `etherlyzer format aabbccddeeff -c upper`  |
| Remove separators         | `etherlyzer format aabbccddeeff -p ""`     |

:::{note}
Formatting changes the textual representation of an address, not its underlying hexadecimal value.

For example, `aa:bb:cc:dd:ee:ff` and `AABB.CCDD.EEFF` represent the same 48-bit address.
:::

## Typo correction

Use `-f` or `--fix-typos` to enable correction of supported typo-like character substitutions before formatting.

This is useful when processing addresses copied from documents, spreadsheets, or manually entered inventories.

| Purpose                              | Command                             |
|--------------------------------------|-------------------------------------|
| Enable typo correction               | `etherlyzer format aabbccddeeff -f` |
| Correct typos in bulk input          | `etherlyzer format -bf`             |
| Correct typos and use uppercase      | `etherlyzer format -bf -c upper`    |
| Correct typos and use Cisco notation | `etherlyzer format -bf -p . -s 4`   |

Typo correction is optional and must be explicitly enabled.

:::{important}
The `format` command does not validate MAC addresses. Enabling typo correction may change how the original input is interpreted.

Use [`validate`](validate.md) when malformed entries must be identified rather than corrected.
:::

## Practical workflows

### Standardize a MAC address inventory

When working with addresses collected from different sources, use bulk formatting to produce consistent notation:

```text
etherlyzer format -b -c upper
```

This is useful for inventories containing a mixture of colon-separated, hyphen-separated, and Cisco-style addresses.

### Prepare addresses for Cisco-style notation

Use four-character hexadecimal blocks separated by periods:

```text
etherlyzer format -b -p . -s 4
```

For example:

```text
aabbccddeeff → aabb.ccdd.eeff
```

### Normalize manually entered addresses

Enable supported typo correction while applying standardized formatting:

```text
etherlyzer format -bf -c upper
```

For workflows where input integrity is more important than correcting possible mistakes, use [`validate`](validate.md) instead.

## Command reference

```text
usage: etherlyzer format [-h] [-b] [-p SEPARATOR] [-s BLOCK_SIZE]
                         [-c {lower,upper}] [-f] [mac]
```

| Argument / Option             | Description                                                            |
|-------------------------------|------------------------------------------------------------------------|
| `mac`                         | MAC address to format.                                                 |
| `-b, --bulk`                  | Read multiple MAC addresses interactively.                             |
| `-p, --separator SEPARATOR`   | Set the separator to `:`, `-`, `.`, or empty (default: `:`).           |
| `-s, --block-size BLOCK_SIZE` | Set hexadecimal characters per block (default: `2`).                   |
| `-c, --casing {lower,upper}`  | Set hexadecimal casing (default: `lower`).                             |
| `-f, --fix-typos`             | Correct supported typo-like character substitutions before formatting. |
| `-h, --help`                  | Display command help.                                                  |

Provide a positional MAC address for individual formatting, or use `-b` for interactive bulk processing.
