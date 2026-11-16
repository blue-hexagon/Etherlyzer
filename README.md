<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/source/_static/logo_dark.png">
  <source media="(prefers-color-scheme: light)" srcset="docs/source/_static/logo_light.png">
  <img alt="EtherLyzer" src="docs/source/_static/logo_light.png" width="460">
</picture>

<p><strong>Offline-first Ethernet identifier intelligence for Python and the command line.</strong></p>

<p>
  <a href="https://pypi.org/project/etherlyzer/"><img src="https://img.shields.io/pypi/pyversions/etherlyzer" alt="Supported Python versions"></a>
  <a href="https://pypi.org/project/etherlyzer/"><img src="https://img.shields.io/pypi/v/etherlyzer?label=PyPI" alt="PyPI version"></a>
  <a href="https://github.com/blue-hexagon/Etherlyzer/actions/workflows/tests.yml"><img src="https://img.shields.io/github/actions/workflow/status/blue-hexagon/Etherlyzer/tests.yml?branch=master&label=tests" alt="Tests"></a>
  <a href="https://etherlyzer.docs.manjana.dev/"><img src="https://img.shields.io/badge/docs-online-6f42c1" alt="Documentation"></a>
  <a href="https://github.com/blue-hexagon/Etherlyzer/blob/master/LICENSE"><img src="https://img.shields.io/github/license/blue-hexagon/Etherlyzer" alt="License"></a>
</p>

<p>
  <a href="https://etherlyzer.docs.manjana.dev/"><strong>Documentation</strong></a> ·
  <a href="https://pypi.org/project/etherlyzer/"><strong>PyPI</strong></a> ·
  <a href="https://github.com/blue-hexagon/Etherlyzer"><strong>Source</strong></a>
</p>

</div>

---

**EtherLyzer** is a Python library and CLI toolkit for analyzing MAC addresses, IEEE assignments, and Ethernet-related identifiers. It combines **local IEEE registry lookups**, **structural classification**, **standards-aware identity resolution**, **formatting and translation**, and **packet-capture extraction** in a composable interface.

It goes beyond conventional OUI lookups: an address can identify an IEEE-registered organization, follow a protocol-defined addressing rule, or have a special purpose without belonging to an ordinary vendor allocation.

Designed for network engineering, automation, asset discovery, NOC/SOC investigations, and network forensics.

## Why EtherLyzer?

A conventional lookup might tell you that a MAC prefix belongs to a particular organization. EtherLyzer helps answer different questions:

- **Who holds the allocation?** Resolve MA-L, MA-M, MA-S, and legacy IAB assignments, including the registered organization and assignment prefix.
- **What kind of address is this?** Examine individual/group delivery, universal/local administration, broadcast and zero-address properties, and the applicable SLAP quadrant.
- **Does it have a standards-defined purpose?** Recognize addresses and address patterns used by protocols such as IPv6 multicast, rather than treating every unmatched address as unknown.
- **What can legitimately be inferred?** Distinguish a registered *address block* from a verified assignment of a specific 48-bit address.
- **How can I process it?** Normalize, validate, reformat, translate, extract, inspect, and incorporate results into structured reports.

For example, `33:33:00:00:00:01` need not match an IEEE vendor allocation to be meaningful: EtherLyzer can identify it as an **IPv6 multicast address** under the mapping defined by RFC 2464.

An inspection can distinguish the address's structure from its standards-defined identity:

```text
MAC: 33:33:00:00:00:01
  Delivery       : Group Address
  Administration : Locally Administered Address (LAA)
  Identity       : IPv6 Multicast Address
  Resolution     : IETF IPv6 Multicast Mapping (RFC 2464)
  IEEE Assignment: No match found
```

A missing vendor match is not the same as an unknown address.

## Features

| Capability                   | Description                                                                             |
|------------------------------|-----------------------------------------------------------------------------------------|
| IEEE lookup                  | Local lookups for MA-L, MA-M, MA-S, IAB, and company identifiers (CID)                  |
| MAC inspection               | Structural classification, address identity, registry resolution, and assessments       |
| Special addresses            | Recognition of supported standards-defined fixed addresses and group address ranges     |
| EtherType intelligence       | Lookup and inspection of Ethernet protocol identifiers                                  |
| Allocation analysis          | Prefixes, address ranges, capacities, and related organizational allocations            |
| Normalization and formatting | Strict or lenient normalization; common and customizable MAC representations            |
| Translation                  | Binary, hexadecimal, decimal, byte-oriented, and per-octet bit-reversed representations |
| Extraction                   | Source and destination MAC extraction from supported files and packet captures          |
| Reporting                    | Composable `Report`, `Section`, and `Item` objects with text, JSON, and CSV renderers   |
| Local operation              | Synchronizable IEEE datasets; ordinary lookups do not require third-party lookup APIs   |

## Installation

The currently published PyPI distribution requires **Python 3.14+**. Check your development branch's `pyproject.toml` if you are using an unreleased version.

```console
python -m pip install etherlyzer
etherlyzer --version
```

## Quick start: Python API

The Python API exposes domain operations directly and groups related transformations into modules.

### Inspect a MAC address

```python
from etherlyzer import inspect_mac, lookup_mac

mac = "B8:1E:A4:33:70:3F"

inspection = inspect_mac(mac)
registration = lookup_mac(mac)

print(inspection.structure.delivery.value)
print(inspection.structure.administration.value)
print(inspection.identity.value)
print(inspection.resolution.value)
print(registration.organization_name if registration else "No IEEE assignment found")
```

**Inspection and registration are deliberately separate.** `lookup_mac()` resolves organizational allocations; `inspect_mac()` interprets structure and identity, including standards-defined addresses without an ordinary vendor registration.

An allocation match identifies the holder of an IEEE-registered block. It does **not** prove the observed device's manufacturer, the current owner, or that a specific 48-bit address was legitimately assigned.

### Normalize, format, and translate

```python
from etherlyzer import formatting, normalize_strict, translation

mac = normalize_strict("b81e.a433.703f")

print(formatting.to_canonical_format(mac))
print(formatting.to_customized_format(mac, block_size=4, separator=".", case="lower"))
print(translation.to_binary(mac))
print(translation.to_decimal(mac))
print(translation.to_bit_reversed(mac))
```

`normalize_strict()` requires a complete 48-bit address and rejects unsupported characters. The more permissive `normalize()` is also available when lenient input cleanup is intentional.

### Extract unique MAC addresses from a packet capture

```python
from pathlib import Path
from etherlyzer import extraction, inspect_mac, normalize_strict

unique_macs = {
    normalize_strict(address)
    for packet in extraction.extract_file(Path("capture.pcapng"))
    for address in (packet.src, packet.dst)
    if address is not None
}

for mac in sorted(unique_macs):
    result = inspect_mac(mac)
    print(mac, result.identity.value)
```

This extracts both source and destination MAC addresses, normalizes them, and performs one inspection per unique address. For captures with unusual or malformed records, handle normalization errors per record.

### Build structured reports

EtherLyzer's presentation API is independent of its inspection and lookup logic. Applications can assemble their own report hierarchy and choose an output renderer.

```python
from etherlyzer import inspect_mac, lookup_mac
from etherlyzer.presentation import Item, Report, Section, get_renderer

mac = "33:33:00:00:00:01"
inspection = inspect_mac(mac)
registration = lookup_mac(mac)

report = Report(
    sections=[
        Section(
            title="MAC Analysis",
            items=[
                Item("Address", mac),
                Item("Identity", inspection.identity.value),
                Item("Resolution", inspection.resolution.value),
                Item("IEEE Assignment", registration.assignment if registration else None),
            ],
        )
    ]
)

print(report.render(get_renderer("text")))
print(report.render(get_renderer("json")))
```

The same report model can support text, JSON, and CSV workflows. More elaborate reports can compose nested sections for formatting, translation, IEEE registration, and structural inspection.

## Command-line interface

The CLI provides lookup, inspection, validation, formatting, extraction, and local registry management. Examples below use the newer, type-first `inspect` syntax from the current development interface; run `--help` against your installed version to confirm its supported commands and options.

```console
# Identify an IEEE allocation holder
etherlyzer whois B8:1E:A4:33:70:3F

# Inspect a MAC address and its classification
etherlyzer inspect mac 333300000001

# Inspect an EtherType identifier
etherlyzer inspect ethertype 0800

# Validate or format MAC input
etherlyzer validate 00-11-22-33-44-55
etherlyzer format 001122334455

# Inspect and update local IEEE registry data
etherlyzer registries
etherlyzer sync

# Discover available extraction options
etherlyzer extract --help
```

For command-specific options:

```console
etherlyzer --help
etherlyzer inspect --help
etherlyzer whois --help
```

> **Version note:** The public PyPI release may not yet include all APIs or command-line syntax shown in this development-oriented README. Check the installed package version and the changelog before relying on an example.

## Supported IEEE data

| Dataset   | Scope                                                               |
|-----------|---------------------------------------------------------------------|
| MA-L      | Large MAC address allocations; 24-bit assignment prefixes (OUI-24)  |
| MA-M      | Medium MAC address allocations; 28-bit assignment prefixes          |
| MA-S      | Small MAC address allocations; 36-bit assignment prefixes           |
| IAB       | Legacy Individual Address Blocks                                    |
| CID       | IEEE Company Identifiers; not equivalent to MAC address allocations |
| EtherType | Ethernet protocol identifier assignments                            |

EtherLyzer uses applicable assignment boundaries for resolution, including more specific allocations where relevant. Results may include allocation capacities, ranges, registry metadata, and related blocks associated with an organization.

## Offline-first by design

EtherLyzer maintains local copies of supported IEEE datasets and builds indexes for repeated lookups. Once the necessary data is available, routine lookups can be completed locally without sending queried MAC addresses or internal inventory data to third-party lookup services.

This is especially useful for restricted environments, private inventories, offline analysis, packet-capture investigations, and bulk enrichment pipelines. Network access may be required for initial dataset acquisition or synchronization, including any configured automatic refresh.

## Documentation

Full documentation: **[etherlyzer.docs.manjana.dev](https://etherlyzer.docs.manjana.dev/)**

Explore the CLI reference, Python API, IEEE registry concepts, MAC address classification, validation, configuration, and registry synchronization guides.

## Development

```console
git clone https://github.com/blue-hexagon/Etherlyzer.git
cd Etherlyzer
poetry install
```

The repository uses Poetry for dependency management, with pytest, mypy, and Ruff for testing and code quality. Refer to `pyproject.toml` for the authoritative Python version and development configuration.

## License

EtherLyzer is released under the [MIT License](LICENSE).
