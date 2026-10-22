# Identify IEEE Organizations

The `whois` command identifies IEEE registry assignments and their associated organizations using EtherLyzer's local registry database.

It supports individual addresses, file-based lookups, and interactive bulk processing, with configurable output formatting and optional preservation of unsuccessful lookups.

Unlike [`inspect`](inspect.md), which provides detailed assignment metadata and allocation analysis, `whois` focuses on efficiently identifying registered organizations.

## Basic usage

Identify the organization associated with a MAC address:

```text
etherlyzer whois 00:20:AF:1B:07:FA
```

The command searches locally stored IEEE registry data for an applicable assignment and returns the corresponding registration information.

:::{note}
An IEEE registry assignment identifies the organization associated with an address allocation, not necessarily the manufacturer of the device currently using the address.
:::

## Input methods

EtherLyzer supports three input methods:

| Source             | Command                              |
|--------------------|--------------------------------------|
| Single MAC address | `etherlyzer whois 00:20:AF:1B:07:FA` |
| Text file          | `etherlyzer whois -f macs.txt`       |
| Interactive input  | `etherlyzer whois -b`                |

### File-based lookups

Use `-f` or `--file` to process addresses from a file:

```text
etherlyzer whois -f ./macs.txt
```

This is useful for device inventories, exported network data, and collections of addresses gathered during investigations.

### Interactive lookups

Use `-b` or `--bulk` to enter multiple addresses interactively:

```text
etherlyzer whois -b
```

Enter one address per line and terminate input with `;;;` on a separate line.

For example:

```text
00:20:AF:1B:07:FA
00:E0:29:68:8B:FB
;;;
```

## Result presentation

The command provides several options for controlling which results are included and how they are presented.

| Option                       | Purpose                                                                               |
|------------------------------|---------------------------------------------------------------------------------------|
| `-p, --preserve-bad-entries` | Preserve unsuccessful lookups, including locally administered and multicast addresses |
| `-l, --linenumbers`          | Include original input line numbers                                                   |
| `-c, --column-names`         | Include a header row                                                                  |
| `-d, --delimiter`            | Customize the delimiter between output fields                                         |

These options can be combined for more informative or structured output.

### Common combinations

| Purpose                                         | Command                  |
|-------------------------------------------------|--------------------------|
| Include line numbers                            | `etherlyzer whois -bl`   |
| Preserve unsuccessful lookups                   | `etherlyzer whois -bp`   |
| Include column headers                          | `etherlyzer whois -bc`   |
| Include line numbers and headers                | `etherlyzer whois -blc`  |
| Preserve unsuccessful lookups with line numbers | `etherlyzer whois -blp`  |
| Enable all reporting options                    | `etherlyzer whois -blcp` |

### Example output

Use line numbers, headers, and preservation of unsuccessful lookups:

```text
etherlyzer whois -blcp
```

Illustrative output:

```text
Line  Result  Registry  Assignment  Organization
1.    MATCH   MA-L      0020AF      3COM
2.    MATCH   MA-L      00E029      STANDARD MICROSYSTEMS CORP.
```

Line numbers make it easier to correlate results with their original input, particularly when processing large address collections.

## Preserve unsuccessful lookups

By default, entries without successful lookups may be omitted.

Use `-p` or `--preserve-bad-entries` to retain them:

```text
etherlyzer whois -bp
```

This is particularly useful when analyzing inventories containing locally administered, multicast, malformed, or otherwise unresolved addresses.

:::{important}
Locally administered and multicast addresses do not necessarily correspond to conventional IEEE vendor assignments.

An unsuccessful lookup does not, by itself, indicate that an address is malformed or malicious.

For address classification and administration-bit analysis, use [`inspect`](inspect.md).
:::

## Delimited output

Use `-d` or `--delimiter` to select the separator between output fields.

The default delimiter is a tab character.

### Delimiter examples

| Purpose                          | Command                                    |
|----------------------------------|--------------------------------------------|
| Default tab-separated output     | `etherlyzer whois -b`                      |
| Semicolon-separated output       | `etherlyzer whois -blcp -d ";"`            |
| Comma-separated output           | `etherlyzer whois -blcp -d ","`            |
| Pipe-separated output            | `etherlyzer whois -blcp -d "\|"            |
| Semicolon-delimited file results | `etherlyzer whois -f macs.txt -lcp -d ";"` |

For example:

```text
etherlyzer whois -blcp -d ";"
```

This produces semicolon-delimited output suitable for importing into spreadsheets or further processing.

:::{note}
Delimited output is not necessarily equivalent to fully escaped CSV. When importing results into other applications, select a delimiter appropriate for the data and account for any delimiter characters occurring inside field values.
:::

## Practical workflows

### Identify organizations in a device inventory

Process an existing list of MAC addresses:

```text
etherlyzer whois -f macs.txt -lcp -d ";"
```

This includes original line numbers, column headers, and unsuccessful lookups in semicolon-delimited output.

It is particularly useful when correlating IEEE registration data with device inventories or exported network records.

### Investigate addresses from a packet capture

Extract unique addresses from a PCAP file:

```text
etherlyzer extract -f capture.pcap -u
```

Then use interactive bulk lookups:

```text
etherlyzer whois -blcp
```

Paste the extracted addresses and terminate the input with `;;;`.

This provides a way to identify organizations represented in observed Ethernet traffic.

### Investigate related IEEE allocations

After identifying an organization, use [`inspect`](inspect.md) to examine the corresponding assignment in greater detail:

```text
etherlyzer inspect 00:20:AF:1B:07:FA -a
```

For associated vendor allocation statistics:

```text
etherlyzer inspect 00:20:AF:1B:07:FA -s
```

Or list related registered vendor blocks:

```text
etherlyzer inspect 00:20:AF:1B:07:FA -b
```

These operations extend a basic `whois` lookup into a more detailed investigation of IEEE allocation data.

## Understanding lookup results

IEEE registry data describes registered address allocations, not necessarily the identity of individual devices.

| Result                       | Interpretation                                                                  |
|------------------------------|---------------------------------------------------------------------------------|
| Successful lookup            | An applicable IEEE registry assignment was identified                           |
| Unsuccessful lookup          | No applicable assignment was resolved                                           |
| Locally administered address | Vendor identification through conventional IEEE allocation lookup may not apply |
| Multicast address            | Does not necessarily represent an individual device or vendor assignment        |

An address observed in network traffic may be spoofed, randomized, locally assigned, or otherwise unrelated to the organization identified by its hexadecimal prefix.

Consequently, registered organization information should be treated as **allocation intelligence**, not definitive device identification.

:::{tip}
Use `whois` for quick IEEE registration lookups and [`inspect`](inspect.md) for detailed address properties, registry metadata, allocation ranges, and related organizational blocks.
:::

## Command reference

```text
usage: etherlyzer whois [-h] [-d DELIMITER] [-p] [-l] [-c]
                        (-f FILE | -b | mac)
```

| Argument / Option            | Description                                                                            |
|------------------------------|----------------------------------------------------------------------------------------|
| `mac`                        | MAC address to identify.                                                               |
| `-f, --file FILE`            | Read MAC addresses from a file.                                                        |
| `-b, --bulk`                 | Read multiple MAC addresses interactively.                                             |
| `-d, --delimiter DELIMITER`  | Set the output delimiter (default: tab).                                               |
| `-p, --preserve-bad-entries` | Preserve unsuccessful lookups, including locally administered and multicast addresses. |
| `-l, --linenumbers`          | Include original input line numbers.                                                   |
| `-c, --column-names`         | Include a header row with column names.                                                |
| `-h, --help`                 | Display command help.                                                                  |

Exactly one input source, `mac`, `-f`, or `-b`, must be provided.
