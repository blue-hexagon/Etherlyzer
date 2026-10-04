# EtherLyzer

EtherLyzer is a Python library and command-line toolkit for identifying, classifying, validating, formatting, and inspecting Ethernet-related identifiers.

It provides fast local lookups against IEEE registry data, including:

- IEEE MAC address registries:
  - MA-L / OUI-24
  - MA-M / OUI-28
  - MA-S / OUI-36
  - IAB
- Company Identifiers (CID)
- EtherType protocol identifiers
- Vendor and organization information
- Address ranges and allocation sizes
- Vendor allocation correlation across IEEE registries

EtherLyzer supports both single-value and bulk workflows through its CLI and exposes the underlying functionality as a Python library.

It is designed primarily for network engineers, cybersecurity professionals, automation, asset discovery, NAC workflows, NOC/SOC tooling, and inventory systems.

## Features

EtherLyzer maintains a local copy of the supported IEEE registries, allowing lookups to be performed locally without sending MAC addresses or other identifiers to third-party lookup services.

Typical use cases include:

- Identify the organization associated with a MAC address.
- Distinguish between MA-L, MA-M, MA-S, and legacy IAB allocations.
- Inspect IEEE assignments, prefixes, address ranges, and allocation sizes.
- Correlate all known IEEE MAC allocations belonging to an organization.
- Look up EtherTypes such as IPv4, IPv6, ARP, LLDP, VLAN tagging, MPLS, and 802.1X.
- Validate and normalize MAC addresses.
- Diagnose malformed MAC address input.
- Correct supported typo-like character substitutions.
- Convert MAC addresses between common formatting conventions.
- Bulk-process MAC addresses interactively or from files.
- Maintain a synchronized local IEEE registry database.
- Build high-performance lookup indexes for repeated queries.
- Integrate Ethernet identifier processing into Python applications and automation.

# Installation

EtherLyzer requires Python 3.14 or newer.

## Install from PyPI

```bash
pip install etherlyzer
```

Upgrade an existing installation with:

```bash
python -m pip install --upgrade etherlyzer
```

Verify the installation:

```text
etherlyzer --version
```

or:

```text
etherlyzer -v
```

## Developer Installation

```bash
git clone https://github.com/blue-hexagon/EtherLyzer
cd EtherLyzer
poetry install
poetry env activate
```

# Command-Line Interface

```text
usage: etherlyzer [-h] [-v] COMMAND ...

EtherLyzer - Ethernet identifier lookup, validation, formatting, and IEEE registry analysis toolkit.

options:
  -h, --help     show this help message and exit
  -v, --version  Show the installed EtherLyzer version and exit.

Commands:
  COMMAND
    whois        Identify IEEE vendors and organizations for MAC addresses.
    validate     Validate and normalize MAC addresses with optional diagnostics and filtering.
    format       Correct and normalize MAC address formatting.
    inspect      Inspect an IEEE assignment and display registry, organization, range, and allocation details.
    registries   Show local IEEE registry metadata and synchronization status.
    sync         Synchronize the local IEEE registry database with upstream sources.
```

Examples:

```text
etherlyzer whois 00:11:22:33:44:55
etherlyzer inspect 00:11:22:33:44:55
etherlyzer validate 00-11-22-33-44-55
etherlyzer format 001122334455
etherlyzer registries
etherlyzer sync
```

Use:

```text
etherlyzer <command> --help
```

for command-specific options and examples.

# Vendor Identification

The `whois` command performs IEEE vendor and organization identification for MAC addresses.

A single MAC address can be queried directly:

```text
etherlyzer whois 00:11:22:33:44:55
```

MAC addresses can also be loaded from a file:

```text
etherlyzer whois -f .\macs.txt
```

or entered interactively:

```text
etherlyzer whois -i
```

Help:

```text
usage: etherlyzer whois [-h] (-f FILE | -i | [mac])

Identify IEEE vendors and organizations for one or more MAC addresses.

positional arguments:
  mac                MAC address to identify

options:
  -h, --help         show this help message and exit
  -f, --file FILE    Read MAC addresses from a file
  -i, --interactive  Read multiple MAC addresses interactively
```

# Inspect IEEE Assignments

The `inspect` command performs a deeper inspection of an IEEE assignment.

It displays information such as:

- Organization name and address
- IEEE registry type
- Assignment prefix
- Address range
- Prefix length
- Address capacity
- Legacy status
- Related allocations belonging to the same organization

Example:

```text
etherlyzer inspect 00:00:0c:12:34:56
```

Example output:

```text
Organization
  Name            : Cisco Systems
  Full Name       : Cisco Systems, Inc
  Address
    170 WEST TASMAN DRIVE SAN JOSE CA US 95134-1706

Registry
  IEEE Type       : MA-L [MAC Address Block Large]
  Assignment      : 00-00-0c
  Range           : 00-00-0c-00-00-00 - 00-00-0c-ff-ff-ff
  Legacy          : False
  Prefix Bits     : 24 bits
  Address Bits    : 24 bits
  Addresses       : 16,777,216
```

EtherLyzer also correlates the organization against its other known MAC registry allocations.

The registry category defaults to `mac`:

```text
etherlyzer inspect 00:11:22:33:44:55
```

It can also be selected explicitly:

```text
etherlyzer inspect -t mac 00:11:22:33:44:55
etherlyzer inspect -t protocol 0800
etherlyzer inspect -t identifier <identifier>
```

Help:

```text
usage: etherlyzer inspect [-h] [-t {mac|protocol|identifier}] value

Inspect a single IEEE assignment and display detailed registry metadata,
organization information, address range, and related vendor allocations.

positional arguments:
  value                 IEEE assignment or identifier to inspect.

options:
  -h, --help            show this help message and exit
  -t, --type {mac|protocol|identifier}
                        IEEE registry category to search (default: mac).
```

# Validate and Normalize MAC Addresses

The `validate` command analyzes MAC address input without attempting typo correction.

Valid input is normalized, while malformed input can be reported together with a validation mask describing the detected problems.

```text
etherlyzer validate 00:11:22:33:44:55
```

For multiple values:

```text
etherlyzer validate -b
```

Additional output controls are available:

```text
etherlyzer validate -b --strict
etherlyzer validate -b --linenumbers --show-info
etherlyzer validate -b --show-originals
```

Help:

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

## Validation Masks

Validation diagnostics use compact mask characters:

```text
v = valid hexadecimal digit
M = missing digit
V = excess valid hexadecimal digit
I = invalid character
r/R = relaxed typo candidate
l/L = lenient typo candidate
```

Example:

```text
ERR 001a2b3c4d5     => vvvvvvvvvvvM
ERR 001a2b3c4d5e6   => vvvvvvvvvvvvV
ERR 001a2b3c4d5O    => vvvvvvvvvvvr
ERR 001a2b3c4d5I    => vvvvvvvvvvvl
```

The distinction between validation and formatting is intentional:

- `validate` interprets the input strictly and reports problems.
- `format --fix-typos` may correct supported typo-like substitutions.

# Format MAC Addresses

The `format` command converts MAC addresses into a chosen representation.

Formatting can control:

- Separator
- Block size
- Letter casing
- Supported typo correction

Basic usage:

```text
etherlyzer format 001122334455
```

Convert separators:

```text
etherlyzer format 00-11-22-33-44-55 -p :
```

Cisco-style blocks:

```text
etherlyzer format 001122334455 -p . -s 4
```

Uppercase output:

```text
etherlyzer format 00:11:22:33:44:55 -c upper
```

Correct supported typo-like input:

```text
etherlyzer format O0:1i:22:33:44:s5 --fix-typos
```

Bulk formatting:

```text
etherlyzer format -b -p . -s 4 --fix-typos
```

Example:

```text
etherlyzer format l..iIdOØ1!23-4oo.. --fix-typos --casing upper --block-size 4 --separator .

111D.0012.3400
```

Help:

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

# IEEE Registry Database

EtherLyzer maintains local copies of supported IEEE datasets.

The current registry configuration and synchronization state can be inspected with:

```text
etherlyzer registries
```

The output includes information such as:

- Registry name
- Legacy name
- Category
- Description
- Local dataset path
- IEEE source URL
- Prefix size
- Last retrieval time
- Update interval

Supported registry types include:

| Registry | Category | Purpose |
|---|---|---|
| MA-L | MAC | Large MAC address allocations / OUI-24 |
| MA-M | MAC | Medium MAC address allocations / OUI-28 |
| MA-S | MAC | Small MAC address allocations / OUI-36 |
| IAB | MAC | Legacy Individual Address Blocks |
| CID | Identifier | IEEE Company Identifiers |
| EtherType | Protocol | Ethernet protocol identifiers |

# Synchronization

The local IEEE registry database can be synchronized manually:

```text
etherlyzer sync
```

Example:

```text
Synchronizing IEEE registries...

Synchronization completed in 2.41 seconds.
```

EtherLyzer also supports automatic synchronization based on the configured maximum age of the local registry data.

# Configuration

EtherLyzer ships with a default `etherlyzer.env` configuration template.

On first use, the configuration is copied to EtherLyzer's platform-specific application-data directory. The user copy can then be modified without editing files inside the installed Python package.

Example configuration:

```dotenv
#---------------------------------------------------DATASET
# Maximum age of the local IEEE database before synchronization, in hours
DB_UPDATE_INTERVAL_HOURS=24

#---------------------------------------------------EXPORT
# Field delimiter used for CSV and stdout output
FIELD_SEPARATOR="\t"

# MAC address formatting
# Supported separators: :, -, ., or an empty value
MAC_SEPARATOR=-

# Number of hexadecimal characters per block
MAC_BLOCK_SIZE=2

# Supported values: upper, lower
MAC_CASE=lower

#---------------------------------------------------DISPLAY
# Print database synchronization messages
SHOW_SYNC_MESSAGES=true
```

Environment variables can also override values loaded from `etherlyzer.env`.

# Python Library

EtherLyzer can also be used directly from Python.

The library exposes components for:

- IEEE registry management
- Lookup indexes
- Vendor correlation
- MAC validation
- MAC normalization
- MAC formatting
- Registry synchronization

The command-line interface is built on the same underlying library functionality.

# Offline Operation

Once the IEEE registry datasets have been synchronized locally, lookups can be performed without querying an external MAC-address lookup service.

This is useful when:

- processing internal asset inventories,
- working with sensitive network information,
- performing large numbers of lookups,
- operating in restricted environments,
- or integrating lookups into automated workflows.

Internet access is only required when the local IEEE registry data needs to be synchronized.

# Development

EtherLyzer is developed using:

- Python 3.14+
- Poetry
- pytest
- mypy
- Ruff

Clone and install the development environment:

```bash
git clone https://github.com/blue-hexagon/EtherLyzer
cd EtherLyzer
poetry install
poetry env activate
```

# License

EtherLyzer is released under the MIT License.

You are free to use, modify, distribute, and sell the software subject to the terms of the included `LICENSE` file.
