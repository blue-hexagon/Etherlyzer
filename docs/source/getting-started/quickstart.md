# Quick Start

EtherLyzer provides commands for identifying, inspecting, validating, and formatting Ethernet-related identifiers, as well as managing local IEEE registry data.

## Main commands

| Command      | Purpose                                                                                       |
|--------------|-----------------------------------------------------------------------------------------------|
| `whois`      | Identify IEEE vendors and organizations for MAC addresses.                                    |
| `inspect`    | Inspect an IEEE assignment and display registry, organization, range, and allocation details. |
| `validate`   | Validate and normalize MAC addresses with optional diagnostics and filtering.                 |
| `format`     | Normalize MAC address formatting with optional typo correction.                               |
| `registries` | Show local IEEE registry metadata and synchronization status.                                 |
| `sync`       | Synchronize the local IEEE registry database with upstream sources.                           |

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

Every command provides command-specific help:

```text
etherlyzer <command> -h
```

For example:

```text
etherlyzer whois -h
```
