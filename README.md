<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/source/_static/logo_dark.png">
  <source media="(prefers-color-scheme: light)" srcset="docs/source/_static/logo_light.png">
  <img alt="Etherlyzer" src="docs/source/_static/logo_light.png" width="460">
</picture>

<p>
  <strong>Lightweight Ethernet Address Intelligence Engine</strong>
</p>

<p>
  <a href="https://pypi.org/project/etherlyzer/">
    <img src="https://img.shields.io/pypi/v/etherlyzer?label=PyPI" alt="PyPI">
  </a>
  <a href="https://pypi.org/project/etherlyzer/">
    <img src="https://img.shields.io/pypi/pyversions/etherlyzer" alt="Python">
  </a>
  <a href="https://github.com/blue-hexagon/etherlyzer/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/blue-hexagon/etherlyzer/tests.yml?branch=main&label=build" alt="Build">
  </a>
  <a href="https://etherlyzer.docs.manjana.dev/">
    <img src="https://img.shields.io/badge/docs-online-6f42c1" alt="Documentation">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/github/license/blue-hexagon/etherlyzer" alt="License">
  </a>
</p>

<p>
  <a href="https://etherlyzer.docs.manjana.dev/"><strong>Documentation</strong></a>
  ·
  <a href="https://pypi.org/project/etherlyzer/"><strong>PyPI</strong></a>
  ·
  <a href="https://github.com/blue-hexagon/etherlyzer"><strong>Source</strong></a>
</p>

</div>

---

A lightweight, offline-first Python toolkit for analyzing Ethernet identifiers and IEEE EUI-48 address allocations.

Etherlyzer goes beyond conventional MAC vendor lookups by combining IEEE registry data, address classification, allocation analysis, and organizational correlation into a unified command-line interface and Python API.

Identify the organization behind a MAC address, determine its IEEE-registered allocation, inspect address ranges and allocation capacities, correlate related vendor blocks, resolve EtherTypes, and validate or normalize MAC addresses — all locally, without relying on third-party lookup APIs.

Built for network engineers, security researchers, and developers who need fast, reliable, standards-aware insight into Ethernet addressing.
## Why Etherlyzer?

Most MAC lookup tools stop at:

> `00:00:0c → Cisco`

Etherlyzer goes further.

It understands the IEEE allocation behind the address:

- **MA-L / OUI-24**
- **MA-M / OUI-28**
- **MA-S / OUI-36**
- **Legacy IAB allocations**
- **Company Identifiers (CID)**
- **EtherType protocol identifiers**

And exposes details such as:

- organization and vendor identity,
- assignment prefix,
- registry type,
- address range,
- prefix and host bit lengths,
- allocation capacity,
- legacy status,
- related IEEE allocations belonging to the same organization.

All registry data is synchronized locally, so normal lookups stay local too.

### Built for real workflows

Etherlyzer is useful anywhere Ethernet identifiers become data rather than something you inspect manually:

- network automation,
- asset discovery,
- NAC and inventory systems,
- NOC/SOC workflows,
- packet-analysis tooling,
- security investigations,
- bulk dataset enrichment,
- Python applications and scripts.

## Install

Requires Python 3.14+.

```console
pip install etherlyzer
etherlyzer --version
```

## See what a MAC address really belongs to

```console
etherlyzer inspect 00:00:0c:12:34:56
```

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

Etherlyzer can also correlate the organization against its other known IEEE MAC allocations.

## One toolkit, multiple jobs

```console
# Identify a vendor
etherlyzer whois 00:11:22:33:44:55

# Inspect the exact IEEE allocation
etherlyzer inspect 00:00:0c:12:34:56

# Inspect an Ethernet protocol identifier
etherlyzer inspect -t protocol 0800

# Validate and diagnose malformed input
etherlyzer validate 00-11-22-33-44-55

# Normalize MAC representation
etherlyzer format 001122334455

# Cisco-style formatting
etherlyzer format 001122334455 -p . -s 4

# Process multiple values
etherlyzer whois -f macs.txt
etherlyzer validate -b

# Inspect local registry state
etherlyzer registries

# Refresh IEEE registry data
etherlyzer sync
```

## Local by design

Etherlyzer maintains synchronized copies of the supported IEEE datasets on the local system.

That means routine lookups do **not** require sending MAC addresses or internal asset data to an external lookup service.

This makes Etherlyzer particularly useful for:

- internal infrastructure inventories,
- restricted environments,
- sensitive network datasets,
- high-volume lookups,
- offline analysis,
- automated enrichment pipelines.

Internet access is only required when the IEEE registry datasets need to be refreshed.

## CLI and Python API

The command-line interface is built on the same underlying Python library.

Use Etherlyzer interactively from a terminal, compose it into shell workflows, or integrate its registry, lookup, validation, and formatting capabilities directly into Python applications.

## Documentation

Full documentation is available at:

### **https://etherlyzer.docs.manjana.dev/**

It includes:

- CLI reference
- Python API
- IEEE registry concepts
- MAC address concepts
- validation masks
- configuration
- registry synchronization
- examples and guides

For quick CLI help:

```console
etherlyzer --help
etherlyzer <command> --help
```

## License

Etherlyzer is released under the [MIT License](LICENSE).
