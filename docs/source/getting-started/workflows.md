---
tocdepth: 4
---

# Common Workflows

**Practical workflows for Ethernet address analysis and investigation.**

EtherLyzer's commands can be combined to discover, identify, validate, and investigate MAC addresses using local IEEE registry intelligence.

This page provides task-oriented workflows, command-selection guidance, and a consolidated CLI option reference. For detailed command behavior, consult the individual [Cookbook](index.md) pages.

## Investigation workflows

The following workflows demonstrate how to combine EtherLyzer's capabilities for common networking and forensic tasks.

### Investigate an unknown MAC address

Start by validating the address, identifying its registered organization, and examining its properties.

| Step | Command | Purpose |
|---|---|---|
| 1 | `etherlyzer validate 00:20:AF:1B:07:FA` | Validate and normalize the input |
| 2 | `etherlyzer whois 00:20:AF:1B:07:FA` | Identify the IEEE registrant |
| 3 | `etherlyzer inspect 00:20:AF:1B:07:FA -a` | Examine address structure, registry metadata, and related allocations |

For an unregistered or locally administered address, the MAC autopsy can still reveal useful structural information:

```text
etherlyzer inspect 40:06:AF:F1:08:08 -x
```

:::{note}
An IEEE registry assignment identifies the organization associated with an allocated address block, not necessarily the manufacturer or identity of the device currently using that address.
:::

### Analyze a network packet capture

Extract distinct Ethernet addresses from a capture, identify their registered organizations, and investigate unusual values.

| Step | Command | Purpose |
|---|---|---|
| 1 | `etherlyzer extract -f capture.pcap -ul` | Extract unique addresses with their first packet numbers |
| 2 | `etherlyzer whois -blcp` | Identify registered organizations |
| 3 | `etherlyzer inspect 00:20:AF:1B:07:FA -x` | Investigate an address of interest |
| 4 | `etherlyzer translate 00:20:AF:1B:07:FA -t binary` | Examine its individual bits |

Copy the extracted addresses into the interactive `whois` session and terminate input with `;;;`.

The packet numbers from the extraction step can be used to locate the corresponding frames in Wireshark.

:::{important}
Packet capture extraction reads decoded Ethernet source and destination fields. Textual scanning instead searches for hexadecimal address candidates.

Neither method establishes that an observed address is legitimate or registered with IEEE.
:::

### Prepare a MAC address inventory

Standardize notation, validate input, and enrich an existing inventory with IEEE registration data.

| Step | Command | Purpose |
|---|---|---|
| 1 | `etherlyzer format -b -p : -s 2 -c upper` | Standardize hexadecimal notation |
| 2 | `etherlyzer validate -bli` | Validate input and retain line numbers |
| 3 | `etherlyzer whois -f macs.txt -lcp -d ";"` | Generate semicolon-delimited registry results |

The commands operate on their respective inputs; the normalized addresses must be transferred between steps or saved to `macs.txt` before the file-based lookup.

For inventories containing malformed entries, strict validation can suppress unsuccessful normalization:

```text
etherlyzer validate -bs
```

:::{tip}
Use `validate` when input integrity matters. Unlike `format`, it does not attempt supported typo correction.
:::

### Investigate suspicious MAC address patterns

When many unexpected addresses appear on a network, comparing their bytes and bits can reveal patterns that ordinary vendor lookups may miss.

| Step | Command | Purpose |
|---|---|---|
| 1 | `etherlyzer translate -bl -t decimal_bytes` | Compare individual octets numerically |
| 2 | `etherlyzer translate -bl -t binary` | Examine recurring bit patterns |
| 3 | `etherlyzer translate -bl -t hex_bytes` | Compare hexadecimal byte sequences |
| 4 | `etherlyzer inspect 40:06:AF:F1:08:08 -x` | Examine address properties and IEEE classification |

For example:

```text
40:06:AF:F1:08:08
```

becomes:

```text
64 6 175 241 8 8
```

These byte values may provide clues about malformed Ethernet frames, unexpected address generation, or possible protocol-header misalignment.

For a detailed investigation involving thousands of unexpected MAC addresses, see the MAC autopsy case study in [`inspect`](../cookbook/inspect.md).

:::{warning}
Recurring byte patterns are investigative clues, not proof of packet corruption or malicious activity.

Determining their origin requires supporting packet captures, device diagnostics, or other network evidence.
:::

### Examine an organization's IEEE allocations

Investigate the allocations associated with an organization using locally synchronized IEEE registry data.

| Step | Command | Purpose |
|---|---|---|
| 1 | `etherlyzer sync --status` | Check local registry expiration status |
| 2 | `etherlyzer whois 00:20:AF:1B:07:FA` | Identify the registered organization |
| 3 | `etherlyzer inspect 00:20:AF:1B:07:FA -s` | Examine allocation counts and address capacities |
| 4 | `etherlyzer inspect 00:20:AF:1B:07:FA -b` | List associated registered blocks |

Alternatively, display all available inspection details:

```text
etherlyzer inspect 00:20:AF:1B:07:FA -a
```

If the registry data needs refreshing, synchronize it before performing further lookups:

```text
etherlyzer sync
```

For synchronization intervals, forced updates, and offline operation, see {doc}`../guides/synchronization`.

---

## Choosing the right command

Use this table when you know what you want to accomplish but aren't sure which command to use.

| I want to...                                       | Command                                                      |
|----------------------------------------------------|--------------------------------------------------------------|
| Discover MAC addresses in logs or packet captures  | [`extract`](../cookbook/extract.md)                          |
| Remove duplicates from extracted addresses         | [`extract -u`](../cookbook/extract.md#duplicate-filtering)   |
| Standardize address notation                       | [`format`](../cookbook/format.md)                            |
| Correct supported typing mistakes                  | [`format -f`](../cookbook/format.md#typo-correction)         |
| Validate input and identify malformed entries      | [`validate`](../cookbook/validate.md)                        |
| Output only successfully normalized addresses      | [`validate -s`](../cookbook/validate.md#strict-mode)         |
| Identify an IEEE-registered organization           | [`whois`](../cookbook/whois.md)                              |
| Examine address properties and IEEE classification | [`inspect`](../cookbook/inspect.md)                          |
| Investigate related vendor allocations             | [`inspect -b`](../cookbook/inspect.md#related-vendor-blocks) |
| Convert a MAC address to decimal                   | [`translate`](../cookbook/translate.md)                      |
| Examine individual decimal octets                  | `translate -t decimal_bytes`                                 |
| Examine address bits                               | `translate -t binary`                                        |
| Reverse the bit order within each octet            | `translate -t bit_reversed`                                  |
| Check local IEEE registry freshness                | `sync -s`                                                    |
| Refresh expired IEEE registry data                 | `sync`                                                       |
| Force registry synchronization                     | `sync -f`                                                    |

## CLI option reference

EtherLyzer uses command-specific option names. Some short flags have different meanings depending on the command.

### Input options

| Option                              | Commands                                              | Purpose                  |
|-------------------------------------|-------------------------------------------------------|--------------------------|
| Positional MAC address              | `format`, `validate`, `translate`, `whois`            | Process one address      |
| Positional assignment or identifier | `inspect`                                             | Inspect a registry entry |
| `-b, --bulk`                        | `extract`, `format`, `validate`, `translate`, `whois` | Interactive input        |
| `-f, --file`                        | `extract`, `whois`                                    | Read input from a file   |

### Formatting and output

| Option                 | Commands                         | Purpose                                |
|------------------------|----------------------------------|----------------------------------------|
| `-l, --linenumbers`    | `validate`, `translate`, `whois` | Include original input line numbers    |
| `-l, --offsets`        | `extract`                        | Include packet numbers or byte offsets |
| `-u, --unique`         | `extract`                        | Remove duplicate addresses             |
| `-p, --separator`      | `extract`, `format`              | Customize hexadecimal separators       |
| `-s, --block-size`     | `extract`, `format`              | Set hexadecimal block sizes            |
| `-c, --casing`         | `extract`, `format`              | Set hexadecimal casing                 |
| `-o, --show-originals` | `validate`                       | Include original input                 |
| `-i, --show-info`      | `validate`                       | Include validation status              |
| `-d, --delimiter`      | `whois`                          | Customize output field delimiters      |
| `-c, --column-names`   | `whois`                          | Include column headers                 |

### Validation and analysis

| Option                       | Commands    | Purpose                                      |
|------------------------------|-------------|----------------------------------------------|
| `-f, --fix-typos`            | `format`    | Enable supported typo correction             |
| `-s, --strict`               | `validate`  | Suppress invalid results                     |
| `-t, --to`                   | `translate` | Select a target representation               |
| `-p, --preserve-bad-entries` | `whois`     | Preserve unsuccessful lookups                |
| `-t, --type`                 | `inspect`   | Select an IEEE registry category             |
| `-x, --show-mac-autopsy`     | `inspect`   | Display address structure and classification |
| `-s, --show-vendor-stats`    | `inspect`   | Display allocation counts and capacities     |
| `-b, --show-vendor-blocks`   | `inspect`   | List related IEEE allocations                |
| `-a, --all`                  | `inspect`   | Display all available inspection details     |
| `-s, --status`               | `sync`      | Display registry expiration status           |
| `-f, --force`                | `sync`      | Force registry synchronization               |

:::{warning}
**Short flags are not interchangeable between commands.**

For example, `-b` enables interactive bulk input for `whois`, but lists related vendor blocks for `inspect`.

Use `etherlyzer <command> --help` for the complete command-specific reference.
:::

## Further reading

| Documentation                           | Focus                                                        |
|-----------------------------------------|--------------------------------------------------------------|
| [`Extract`](../cookbook/extract.md)     | Source formats, scanning behavior, and extraction options    |
| [`Format`](../cookbook/format.md)       | Notation, block sizes, casing, and typo correction           |
| [`Validate`](../cookbook/validate.md)   | Validation rules, masks, and normalized output               |
| [`Translate`](../cookbook/translate.md) | Numerical, binary, and byte representations                  |
| [`Whois`](../cookbook/whois.md)         | IEEE registry lookups and organization identification        |
| [`Inspect`](../cookbook/inspect.md)     | Address classification, allocation analysis, and MAC autopsy |
| {doc}`../guides/synchronization`        | Registry synchronization and offline operation               |
