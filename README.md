<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/source/_static/logo_dark.png">
  <source media="(prefers-color-scheme: light)" srcset="docs/source/_static/logo_light.png">
  <img alt="Etherlyzer" src="docs/source/_static/logo_light.png" width="460">
</picture>

<p>
  <strong>Lightweight Ethernet Address Intelligence Engine</strong>
</p>

<p align="center">

  <!-- Compatibility -->
  <a href="https://pypi.org/project/etherlyzer/">
    <img src="https://img.shields.io/pypi/pyversions/etherlyzer" alt="Python Versions">
  </a>

  <!-- Distribution -->
  <a href="https://pypi.org/project/etherlyzer/">
    <img src="https://img.shields.io/pypi/v/etherlyzer?label=PyPI" alt="PyPI Version">
  </a>

  <!-- Quality -->
  <a href="https://github.com/blue-hexagon/Etherlyzer/actions/workflows/tests.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/blue-hexagon/Etherlyzer/tests.yml?branch=master&label=tests" alt="Tests">
  </a>

  <!-- Project -->
  <a href="https://etherlyzer.docs.manjana.dev/">
    <img src="https://img.shields.io/badge/docs-online-6f42c1" alt="Documentation">
  </a>
  <a href="https://github.com/blue-hexagon/Etherlyzer/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/blue-hexagon/Etherlyzer" alt="License">
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

Etherlyzer goes beyond conventional MAC vendor lookups by combining IEEE registry data, address classification,
allocation analysis, and organizational correlation into a unified command-line interface and Python API.

Identify the organization behind a MAC address, determine its IEEE-registered allocation, inspect address ranges and
allocation capacities, correlate related vendor blocks, resolve EtherTypes, and validate or normalize MAC addresses —
all locally, without relying on third-party lookup APIs.

Built for network engineers, security researchers, and developers who need fast, reliable, standards-aware insight into
Ethernet addressing.

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
etherlyzer inspect -xsb 00000f
```

```text
MAC Address Autopsy
  Input
    Value             : 00000f
    Length            : 24 bits
  Representations
    Canonical         : 00-00-0F
    Bit-Reversed      : 00:00:F0
    To Hex            : 00000F
    To Integer        : 15
    To Decimals       : 0 0 15
    To Octal          : 00000017
    To Binary         : 0000.0000.0000.0000.0000.1111
    To Bytes          : 00 00 0F
  Address Properties
    Null Address      : False
    Broadcast         : False
    Special Bits
      U/L             : 0 Universal / Universally Administered
      I/G             : 0 Individual / Unicast

IEEE Identifier
  Type                : Universal Individual Prefix (Registered Block)
  SLAP Quadrant       : None

IEEE Registry
  IEEE Type           : MA-L [MAC Address Block Large]
  Assignment          : 00-00-0f
  Range               : 00-00-0f-00-00-00 - 00-00-0f-ff-ff-ff
  Prefix Bits         : 24 bits
  Address Bits        : 24 bits
  Legacy              : False
  Legacy Name         : OUI
  Address Capacity    : 16,777,216

Associated Allocations
  Total
    Blocks           : 1
    Capacity         : 16,777,216
  MA-L
    Blocks           : 1
    Capacity         : 16,777,216
  MA-M
    Blocks           : 0
    Capacity         : 0
  MA-S
    Blocks           : 0
    Capacity         : 0
  IAB
    Blocks           : 0
    Capacity         : 0
  Registered Blocks (B=IAB, S=MA-S, M=MA-M, L=MA-L)
      [L] 00-00-0f

Organization
  Name              : NEXT
  Full Name         : NEXT, INC.
  Address
    3475 DEER CREEK ROAD PALO ALTO CA US 94304
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

That means routine lookups do **not** require sending MAC addresses or internal asset data to an external lookup
service.

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

Use Etherlyzer interactively from a terminal, compose it into shell workflows, or integrate its registry, lookup,
validation, and formatting capabilities directly into Python applications.

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
