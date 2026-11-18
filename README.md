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

**EtherLyzer** is an offline-first Python library and command-line toolkit for examining **MAC addresses, IEEE
registrations, EtherTypes, and other Ethernet identifiers**.

A MAC address is more than an OUI, and an EtherType is more than a protocol name. EtherLyzer combines IEEE registry data
with address structure, standards-defined identities, precise allocation boundaries, and reusable analysis tools to
explain **what an identifier is, what it is used for, and what can actually be inferred from it**.

Use it from the terminal or build it into your own network automation, asset inventory, packet-analysis, and security
workflows. Registry-backed lookups run locally after the required datasets have been synchronized.

## A lookup is only the beginning

Consider three different identifiers:

| Identifier          | What EtherLyzer can establish                                                                                                         |
|---------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| `B8:1E:A4:33:70:3F` | An individual, universally administered address within an IEEE MA-L allocation registered to Liteon Technology Corporation.           |
| `33:33:00:00:00:01` | A protocol-defined IPv6 multicast address (RFC 2464), even without an ordinary IEEE organizational allocation match.                  |
| `0x88B7`            | An OUI Extended EtherType: the following **3-byte OUI + 2-byte protocol ID** are needed to identify the organization-scoped protocol. |

Those are different kinds of answers. EtherLyzer distinguishes **structural classification**, **registry resolution**,
and **standards-defined identity** instead of treating them as the same lookup.

## Install

Requires **Python 3.12+** (Python 3.12 to 3.x; see `pyproject.toml` for the authoritative constraint).

```console
python -m pip install etherlyzer
etherlyzer --version
```

## Quick start

### Identify a MAC address

```python
from etherlyzer import inspect_mac, lookup_mac

mac = "B8:1E:A4:33:70:3F"

inspection = inspect_mac(mac)
registration = lookup_mac(mac)

print(inspection.structure.delivery.value)
print(inspection.structure.administration.value)
print(inspection.identity.value)
print(inspection.resolution.value)
print(registration.organization_name if registration else "No IEEE allocation match")
```

`inspect_mac()` answers **what the address represents**. `lookup_mac()` independently answers **which IEEE allocation,
if any, covers it**.

### Inspect an EtherType

```python
from etherlyzer import inspect_ethertype

result = inspect_ethertype("88B7")

print(result.field_type.value)  # EtherType
print(result.is_ethertype)  # True
print(result.requires_oui_pid)  # True
print(result.match_status)  # Depends on the local IEEE registry data
```

EtherLyzer understands the **16-bit Ethernet Type/Length field**, including the distinction between payload lengths, the
undefined interval, and actual EtherTypes:

| Range             | Interpretation                         |
|-------------------|----------------------------------------|
| `0x0000`–`0x05DC` | IEEE 802.3 length field (0–1500 bytes) |
| `0x05DD`–`0x05FF` | Undefined Length/Type values           |
| `0x0600`–`0xFFFF` | EtherType values                       |

A valid EtherType value does **not** necessarily have a matching IEEE registry entry. And inspecting `88B7` alone does
not reveal its encapsulated protocol: that requires the additional five bytes from the frame.

## What EtherLyzer does

| Capability               | Details                                                                                                                                                      |
|--------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **MAC inspection**       | Individual/group delivery, universal/local administration, broadcast and zero addresses, SLAP quadrants, address form, identity, resolution, and assessments |
| **IEEE lookup**          | MA-L, MA-M, MA-S, legacy IAB, and CID information; organization metadata and associated allocation data                                                      |
| **EtherType inspection** | 16-bit field classification, registered protocol information, unknown EtherTypes, and OUI Extended EtherType recognition                                     |
| **Address intelligence** | Supported fixed and ranged protocol-defined MAC identities, including IPv4/IPv6 multicast and IEEE link-local group addresses                                |
| **Formatting**           | Canonical, Cisco, default, and configurable grouping, separators, and case                                                                                   |
| **Translation**          | Binary, decimal, hexadecimal, octet-oriented, and per-octet bit-reversed representations                                                                     |
| **Extraction**           | MAC extraction from supported files and Ethernet packet captures, including PCAP/PCAPNG                                                                      |
| **Reporting**            | Composable `Report`, `Section`, and `Item` objects; text, JSON, and CSV renderers                                                                            |
| **Offline-first**        | Local, synchronizable IEEE datasets and indexed lookups without per-query external API requests                                                              |

## Python API

EtherLyzer exposes high-level domain operations directly and groups stateless transformations into modules:

```python
from etherlyzer import (
    extraction,
    formatting,
    inspect_ethertype,
    inspect_mac,
    lookup_mac,
    normalize,
    normalize_strict,
    translation,
)
from etherlyzer.presentation import Item, Report, Section, get_renderer
```

### MAC inspection: structure, identity, and evidence

```python
from etherlyzer import inspect_mac

result = inspect_mac("33:33:00:00:00:01")

print(result.structure.normalized)
print(result.structure.delivery.value)
print(result.structure.administration.value)
print(result.structure.slap_quadrant.value if result.structure.slap_quadrant else None)
print(result.form.value)
print(result.identity.value)
print(result.resolution.value)

for assessment in sorted(result.assessment, key=lambda item: item.name):
    print(f"{assessment.label}: {assessment.description}")
```

An abridged example of the interpreted result:

```text
Address        : 33:33:00:00:00:01
Delivery       : Group Address
Administration : Locally Administered Address (LAA)
SLAP           : Administratively Assigned (AAI)
Form           : Special (Protocol-Defined Address)
Identity       : IPv6 Multicast Address
Resolution     : IETF IPv6 Multicast Mapping (RFC 2464)
Assessment     : Standards-Defined
```

**A missing vendor registration is not an unknown address.** The IPv6 multicast mapping is defined by a protocol
standard, not by an ordinary manufacturer allocation.

Conversely, a registered MA-L/MA-M/MA-S match identifies the **holder of the assigned address block**. It does not prove
the manufacturer or owner of an observed device, or establish that a particular MAC was legitimately assigned.
EtherLyzer's inspection assessments preserve that distinction.

### EtherType inspection: more than protocol names

```python
from etherlyzer import inspect_ethertype

for identifier in ("05DC", "05DD", "0800", "0806", "86DD", "88B7"):
    result = inspect_ethertype(identifier)
    print(
        f"0x{result.assignment} | "
        f"{result.field_type.value} | "
        f"{result.description or result.match_status}"
    )
```

The returned structure also exposes the numeric value, optional length in bytes, registry metadata, organization
information, match status, and whether the identifier is `0x88B7` (OUI Extended EtherType).

Some familiar EtherTypes include `0x0800` (IPv4), `0x0806` (ARP), `0x86DD` (IPv6), `0x888E` (802.1X/EAPOL), `0x88CC`
(LLDP), and `0x88E5` (MACsec).

### Normalize, format, and translate

```python
from etherlyzer import formatting, normalize_strict, translation

mac = normalize_strict("b81e.a433.703f")

print(formatting.canonical_format(mac))
print(formatting.custom_format(mac, block_size=4, separator=".", case="lower"))
print(translation.to_binary(mac))
print(translation.to_decimal(mac))
print(translation.to_hex_bytes(mac))
print(translation.to_bit_reversed(mac))
```

`normalize_strict()` requires a complete 48-bit hexadecimal address, allowing supported separators. The lenient
`normalize()` is available for deliberate input cleanup. Bit reversal operates **within each octet**, not across the
entire 48-bit address.

### Extract unique addresses from a capture

```python
from pathlib import Path
from etherlyzer import extraction, inspect_mac

macs = extraction.extract_unique_pcap_macs(Path("capture.pcapng"))

for mac in sorted(macs):
    result = inspect_mac(mac)
    print(f"{mac}: {result.identity.value}")
```

This is useful when analyzing network captures, building address inventories, or enriching capture-derived datasets.
Inspecting a set of addresses avoids repeating registry lookups for every observed packet.

### Build a report and export it as text or JSON

EtherLyzer's reporting objects are **independent of extraction and classification**. You decide which facts to include
and how to present them.

```python
from pathlib import Path
from etherlyzer import extraction, inspect_mac, lookup_mac
from etherlyzer.presentation import Item, Report, Section, get_renderer

macs = extraction.extract_unique_pcap_macs(Path("capture.pcapng"))
sections = []

for mac in sorted(macs):
    inspection = inspect_mac(mac)
    registration = lookup_mac(mac)

    sections.append(
        Section(
            title=mac,
            items=[
                Item("Identity", inspection.identity.value),
                Item("Resolution", inspection.resolution.value),
                Item(
                    "IEEE Organization",
                    registration.organization_name if registration else None,
                ),
                Section(
                    title="Assessment",
                    items=[
                        Item(item.label, item.description)
                        for item in sorted(inspection.assessment, key=lambda x: x.name)
                    ],
                ),
            ],
        )
    )

report = Report(sections=sections)

print(report.render(get_renderer("text")))
Path("report.json").write_text(
    report.render(get_renderer("json")),
    encoding="utf-8",
)
```

One report, one consistent data model, different output formats. A CSV renderer is also available where a tabular
representation is appropriate.

## Command-line interface

The CLI provides interactive and batch-oriented access to the same underlying capabilities.

```console
# whois bulk example
etherlyzer whois -f addrs.txt -p

╭──────┬───────────────────┬──────────┬────────────┬─────────────────────────────────────────────────┬────────────────────────────────────┬───────────────────────────────────────┬───────────────────────────────────────────────╮
│ Line │ Input             │ Registry │ Assignment │ Organization                                    │ Form                               │ Identity                              │ Resolution                                    │
├──────┼───────────────────┼──────────┼────────────┼─────────────────────────────────────────────────┼────────────────────────────────────┼───────────────────────────────────────┼───────────────────────────────────────────────┤
│    1 │ 00:00:0C:12:34:56 │ MA-L     │ 00000C     │ Cisco Systems, Inc                              │ Universal Individual Address       │ EUI-48-Compatible Individual Address  │ Registered Block (MA-L)                       │
│    2 │ 00:50:56:12:34:56 │ MA-L     │ 005056     │ VMware, Inc.                                    │ Universal Individual Address       │ EUI-48-Compatible Individual Address  │ Registered Block (MA-L)                       │
│    3 │ 05:0C:29:AA:BB:CC │ -        │ -          │ -                                               │ Universal Group Address            │ Group Address                         │ No Matching Eligible IEEE Allocation          │
│    4 │ 08:00:27:12:34:56 │ MA-L     │ 080027     │ PCS Systemtechnik GmbH                          │ Universal Individual Address       │ EUI-48-Compatible Individual Address  │ Registered Block (MA-L)                       │
│    5 │ 03:1C:42:12:34:56 │ -        │ -          │ -                                               │ Local Group Address                │ AAI Address                           │ SLAP Administrative Assignment Space          │
│    6 │ B8:27:EB:12:34:56 │ MA-L     │ B827EB     │ Raspberry Pi Foundation                         │ Universal Individual Address       │ EUI-48-Compatible Individual Address  │ Registered Block (MA-L)                       │
│    7 │ DC:A6:32:12:34:56 │ MA-L     │ DCA632     │ Raspberry Pi Trading Ltd                        │ Universal Individual Address       │ EUI-48-Compatible Individual Address  │ Registered Block (MA-L)                       │
│    8 │ 00:15:5D:12:34:56 │ MA-L     │ 00155D     │ Microsoft Corporation                           │ Universal Individual Address       │ EUI-48-Compatible Individual Address  │ Registered Block (MA-L)                       │
│    9 │ 01:16:3E:12:34:56 │ MA-L     │ 00163E     │ Xensource, Inc.                                 │ Universal Group Address            │ OUI-Derived Group Address             │ Registered Block (MA-L)                       │
│   10 │ 52:54:00:12:34:56 │ -        │ -          │ -                                               │ Local Individual Address           │ AAI Address                           │ SLAP Administrative Assignment Space          │
│   11 │ 00:00:00:12:34:56 │ MA-L     │ 000000     │ XEROX CORPORATION                               │ Universal Individual Address       │ EUI-48-Compatible Individual Address  │ Registered Block (MA-L)                       │
│   12 │ 70:B3:D5:12:34:56 │ MA-S     │ 70B3D5123  │ Amfitech ApS                                    │ Universal Individual Address       │ EUI-48-Compatible Individual Address  │ Registered Block (MA-S)                       │
│   13 │ 00:1B:21:12:34:56 │ MA-L     │ 001B21     │ Intel Corporate                                 │ Universal Individual Address       │ EUI-48-Compatible Individual Address  │ Registered Block (MA-L)                       │
│   14 │ 02:00:00:00:00:01 │ -        │ -          │ -                                               │ Local Individual Address           │ AAI Address                           │ SLAP Administrative Assignment Space          │
│   15 │ 06:11:22:33:44:55 │ -        │ -          │ -                                               │ Local Individual Address           │ Reserved SLAP Address                 │ Reserved SLAP Assignment Space                │
│   16 │ 01:00:5E:00:00:01 │ MA-L     │ 00005E     │ ICANN, IANA Department                          │ Special (Protocol-Defined Address) │ IPv4 Multicast Address                │ IETF IPv4 Multicast Mapping (RFC 1112 + 9542) │
│   17 │ 33:33:00:00:00:01 │ -        │ -          │ -                                               │ Special (Protocol-Defined Address) │ IPv6 Multicast Address                │ IETF IPv6 Multicast Mapping (RFC 2464)        │
│   18 │ 01:80:C2:00:00:0E │ MA-L     │ 0080C2     │ IEEE 802.1 Working Group                        │ Special (Protocol-Defined Address) │ Nearest Bridge Group Address          │ IEEE 802.1Q Defined                           │
│   19 │ 01:80:C2:00:00:00 │ MA-L     │ 0080C2     │ IEEE 802.1 Working Group                        │ Special (Protocol-Defined Address) │ Nearest Customer Bridge Group Address │ IEEE 802.1Q Defined                           │
│   20 │ FF:FF:FF:FF:FF:FF │ -        │ -          │ -                                               │ Special (Fixed Address)            │ Ethernet Broadcast                    │ IEEE 802.3 Defined                            │
│   21 │ 00:00:00:00:00:00 │ -        │ -          │ -                                               │ Special (Fixed Address)            │ All-Zero / Null Address               │ IEEE RA Reserved                              │
│   22 │ 00:00:00:00:00:0F │ MA-L     │ 000000     │ XEROX CORPORATION                               │ Universal Individual Address       │ EUI-48-Compatible Individual Address  │ Registered Block (MA-L)                       │
│   23 │ 00:00:00:00:00:0  │ -        │ -          │ -                                               │ Universal Individual Prefix        │ Ambiguous Identity                    │ Prefix Spans Multiple Address Identities      │
│   24 │ AAF01901CDFA      │ CID      │ AAF019     │ TransferJet Consortium Incorporated Association │ Local Individual Address           │ ELI-48-Compatible Individual Address  │ Registered (CID)                              │
│   25 │ ABF01901          │ CID      │ AAF019     │ TransferJet Consortium Incorporated Association │ Local Group Prefix                 │ Group ELI Prefix                      │ Registered (CID)                              │
│   26 │ 0AAB.8C01.cabf    │ CID      │ 0AAB8C     │ Midwest Microwave Solutions Inc.                │ Local Individual Address           │ ELI-48-Compatible Individual Address  │ Registered (CID)                              │
│   27 │ 0BAB.8C01.cabf    │ CID      │ 0AAB8C     │ Midwest Microwave Solutions Inc.                │ Local Group Address                │ ELI-48-Compatible Group Address       │ Registered (CID)                              │
│   28 │ 000000            │ -        │ -          │ -                                               │ Universal Individual Prefix        │ Ambiguous Identity                    │ Prefix Spans Multiple Address Identities      │
│   29 │ 00000000          │ -        │ -          │ -                                               │ Universal Individual Prefix        │ Ambiguous Identity                    │ Prefix Spans Multiple Address Identities      │
│   30 │ 0000000000        │ -        │ -          │ -                                               │ Universal Individual Prefix        │ Ambiguous Identity                    │ Prefix Spans Multiple Address Identities      │
│   31 │ 000000000000      │ -        │ -          │ -                                               │ Special (Fixed Address)            │ All-Zero / Null Address               │ IEEE RA Reserved                              │
│   32 │ 000000000001      │ MA-L     │ 000000     │ XEROX CORPORATION                               │ Universal Individual Address       │ EUI-48-Compatible Individual Address  │ Registered Block (MA-L)                       │
│   33 │ 52:54:00:12:34:5  │ -        │ -          │ -                                               │ Local Individual Prefix            │ AAI Prefix                            │ SLAP Administrative Assignment Space          │
│   34 │ 57:54:00:12:34:56 │ -        │ -          │ -                                               │ Local Group Address                │ Reserved SLAP Address                 │ Reserved SLAP Assignment Space                │
│   35 │ 57:500:12:34:56   │ -        │ -          │ -                                               │ Local Group Prefix                 │ Reserved SLAP Prefix                  │ Reserved SLAP Assignment Space                │
│   36 │ 53:54:00:12:34:56 │ -        │ -          │ -                                               │ Local Group Address                │ AAI Address                           │ SLAP Administrative Assignment Space          │
│   37 │ 53:00:12:34:56    │ -        │ -          │ -                                               │ Local Group Prefix                 │ AAI Prefix                            │ SLAP Administrative Assignment Space          │
╰──────┴───────────────────┴──────────┴────────────┴─────────────────────────────────────────────────┴────────────────────────────────────┴───────────────────────────────────────┴───────────────────────────────────────────────╯

```

```console
# Inspect MAC address structure and identity
etherlyzer inspect mac 333300000001

MAC Address Autopsy
  Input
    Value                        : 0AAB.8C01.cabf
    Length                       : 48 bits
  IEEE Identity
    Kind                         : Local Individual Address
    Type                         : ELI-48-Compatible Individual Address
    Registration                 : Registered (CID)
    SLAP Quadrant                : Extended Local (ELI)
    Assessment
      Registered Candidate       : The complete identifier falls within an eligible IEEE-registered allocation, but assignment of the specific identifier has not been verified.
      Structurally Conformant    : The identifier conforms to the applicable structural addressing rules. This does not establish that it has been registered or assigned.
  Representations
    Canonical                    : 0A-AB-8C-01-CA-BF
    Bit-Reversed                 : 50:D5:31:80:53:FD
    To Hex                       : 0x0AAB8C01CABF
    To Integer                   : 11,731,904,613,055
    To Decimals                  : 10 171 140 1 202 191
    To Binary                    : 00001010.10101011.10001100.00000001.11001010.10111111
    To Bytes                     : 0A AB 8C 01 CA BF
  Address Properties
    Null Address                 : False
    Broadcast                    : False
    Special Bits
      U/L                        : 1 Local / Locally Administered
      I/G                        : 0 Individual / Unicast
  CID
    Assignment
      Organization               : Midwest Microwave Solutions Inc.
      Address
        Line 1                   : 2000 Progress Drive Hiawatha IA US 52233
```

```console
# Inspect an Ethernet Type/Length identifier
etherlyzer inspect ethertype 88B7

# Inspect an IEEE company identifier
etherlyzer inspect identifier 0A6791

# Validate, format, and translate addresses
etherlyzer validate 00-11-22-33-44-55
etherlyzer format 001122334455
etherlyzer translate 001122334455

# Extract addresses from a packet capture
etherlyzer extract -f capture.pcapng

# Inspect and refresh local registry data
etherlyzer registries
etherlyzer sync
```

See `etherlyzer --help` or `etherlyzer <command> --help` for the commands and options supported by your installed
version.

## IEEE registry coverage and interpretation

EtherLyzer works with the following IEEE datasets:

| Registry      | Meaning                       | Identifier width / allocation scope                                   |
|---------------|-------------------------------|-----------------------------------------------------------------------|
| **MA-L**      | MAC Address Block Large       | 24-bit allocation prefix; remaining 24 bits within EUI-48 space       |
| **MA-M**      | MAC Address Block Medium      | 28-bit allocation prefix; remaining 20 bits within EUI-48 space       |
| **MA-S**      | MAC Address Block Small       | 36-bit allocation prefix; remaining 12 bits within EUI-48 space       |
| **IAB**       | Individual Address Block      | Legacy allocations using a 36-bit assignment scope                    |
| **CID**       | Company Identifier            | 24-bit company identifier; **not** an ordinary MAC address allocation |
| **EtherType** | Ethernet protocol identifiers | 16-bit protocol / Type-field assignments                              |

For MAC allocations, EtherLyzer considers the applicable assignment scope, not just the first three octets. This matters
when more specific MA-M, MA-S, or legacy IAB assignments overlap broad prefix patterns.

Its address interpretation also recognizes supported standards-defined special addresses and distinguishes
**structurally conformant**, **registered-candidate**, and **standards-defined** results. The existence of a registry
entry should not be mistaken for evidence that a specific observed device is genuine.

## Offline-first by design

Supported IEEE datasets are cached and indexed locally. Once available, ordinary address lookups do not need to submit
queried MACs or inventory data to a third-party API.

That makes EtherLyzer well suited for network automation, NOC/SOC investigations, asset inventories, offline packet
analysis, and restricted environments. Initial dataset acquisition and configured synchronization may require network
access.

## Documentation and development

Full documentation: **[etherlyzer.docs.manjana.dev](https://etherlyzer.docs.manjana.dev/)**

The documentation covers CLI commands, public Python interfaces, IEEE registries, MAC addressing, validation,
configuration, and synchronization.

To work on EtherLyzer locally:

```console
git clone https://github.com/blue-hexagon/Etherlyzer.git
cd Etherlyzer
poetry install
```

## License

EtherLyzer is released under the [MIT License](LICENSE).
