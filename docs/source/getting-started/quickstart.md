# Quick Start

EtherLyzer provides commands for identifying, inspecting, validating, and formatting Ethernet-related identifiers, as well as managing local IEEE registry data.

## Main commands

| Command   | Purpose                                                                                       |
|-----------|-----------------------------------------------------------------------------------------------|
| `whois`   | Identify IEEE vendors and organizations for MAC addresses.                                    |
| `inspect` | Inspect an IEEE assignment and display registry, organization, range, and allocation details. |
| `validate` | Validate and normalize MAC addresses with optional diagnostics and filtering.                 |
| `format`  | Normalize MAC address formatting with optional typo correction.                               |
| `registries` | Show local IEEE registry metadata and synchronization status.                                 |
| `sync`    | Synchronize the local IEEE registry database with upstream sources.                           |

## Identify a MAC address

```text
etherlyzer whois 00:11:22:33:44:55
```

## Inspect an IEEE assignment

```text
etherlyzer inspect 00:11:22:33:44:55
```

## Validate a MAC address

```text
etherlyzer validate 00-11-22-33-44-55
```

## Format a MAC address

```text
etherlyzer format 001122334455
```

## Inspect local registries

```text
etherlyzer registries
```

## Synchronize IEEE data

```text
etherlyzer sync
```

## Command help

Every command provides command-specific help and comes with a lot of options and serveral examples:

```text
etherlyzer <command> -h
```

For example:

```text
etherlyzer whois -h
```
```text
usage: etherlyzer whois [-h] [-d DELIMITER] [-p] [-l] [-c] (-f FILE | -b | mac)

Identify IEEE vendors and organizations for one or more MAC addresses.

positional arguments:
  mac                   MAC address to identify

options:
  -h, --help            show this help message and exit
  -d, --delimiter DELIMITER
                        Select a delimiter, if none is chosen tabs is default
  -p, --preserve-bad-entries
                        Enables preservation of bad entries such as self-assigned or multicast addresses
  -l, --linenumbers     Prefix output lines with their corresponding input line number
  -c, --column-names    Write a header row on the first line of the output
  -f, --file FILE       Read MAC addresses from a file
  -b, --bulk            Read multiple MAC addresses interactively

Examples:
  etherlyzer whois 00:11:22:33:44:55   Look up a single MAC address
  etherlyzer whois -b                  Enter MAC addresses interactively
  etherlyzer whois -f .\macs.txt       Look up MAC addresses from a file
  etherlyzer whois -bl                 Show original input line numbers
  etherlyzer whois -bp                 Include unsuccessful lookups
  etherlyzer whois -blcp               Show all results in an aligned table
  etherlyzer whois -blcp -d ";"        Output semicolon-delimited results

```
