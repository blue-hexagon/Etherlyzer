# Inspect IEEE Assignments

The `inspect` command performs detailed inspection of IEEE registry assignments and identifiers.

Depending on the registry category, it can display information such as:

- organization name and address,
- IEEE registry type,
- assignment prefix,
- address range,
- prefix length,
- address capacity,
- legacy status, and
- related allocations belonging to the same organization.

For an overview of the supported IEEE registries, see {doc}`../concepts/ieee-registries`.

## Inspection Branches

Etherlyzer uses **quadrant-based inspection** rather than enforcing a single, unified output schema across all MAC address types.

Each address is normalized, validated, and classified using the **Universal/Local (U/L)** and **Individual/Group (I/G)** bits of its first octet. These bits determine which of four specialized inspection branches handles the address.

See {doc}`../concepts/mac-addresses` for details about MAC address classification and the Structured Local Address Plan (SLAP).

```text
                       MAC Input
                           │
                           ▼
                   Normalize / Validate
                           │
                           ▼
                     Classify MAC
                      U/L + I/G
                           │
            ┌──────────────┴──────────────┐
            │                             │
       Universal                       Local
            │                             │
      ┌─────┴─────┐                 ┌─────┴─────┐
      │           │                 │           │
  Individual     Group          Individual     Group
      │           │                 │           │
      ▼           ▼                 ▼           ▼
   EUI-48      Universal          SLAP        Local
 Allocations    Group           Analysis      Group
      │                             │
      ▼                      ┌──────┴──────┐
 MA-L / MA-M                 │             │
 MA-S / IAB               ELI/CID      AAI/SAI/
                                       Reserved
```

### Inspection Types

| Branch                   | Classification   | Inspection Focus                                                                                              |
|--------------------------|------------------|---------------------------------------------------------------------------------------------------------------|
| **Universal Individual** | U/L = 0, I/G = 0 | IEEE EUI-48 allocation resolution, registry metadata, registered organizations, and associated address blocks |
| **Universal Group**      | U/L = 0, I/G = 1 | Group addressing, standardized multicast assignments, and recognized protocol mappings                        |
| **Local Individual**     | U/L = 1, I/G = 0 | SLAP quadrant classification, CID resolution for ELI candidates, and locally administered addressing          |
| **Local Group**          | U/L = 1, I/G = 1 | Locally administered group addressing, broadcast detection, and recognized multicast mappings                 |

All four branches share common address normalization, validation, bit-level classification, and formatting conventions. Their additional inspection capabilities differ according to the applicable addressing schemes and available registry or protocol information.

```{note}
The four inspection branches represent structural MAC address classifications, not four separate IEEE registries.

Special-purpose addresses, such as the all-zero address and Ethernet broadcast, retain their underlying U/L and I/G classifications but require additional interpretation.

The Structured Local Address Plan (SLAP) is optional. An address matching a SLAP quadrant's bit pattern does not necessarily follow that quadrant's intended assignment scheme.
```

## Basic usage

MAC registry inspection is the default:

```text
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

## Correlating Vendor Assignments

For MAC assignments, EtherLyzer can also correlate the inspected organization against any other known MAC registry allocations they are associated with:
```text
etherlyzer inspect 10:7B:EF -b
```
```text
IEEE Registry
  IEEE Type           : MA-L [MAC Address Block Large]
  Assignment          : 10-7b-ef
  Range               : 10-7b-ef-00-00-00 - 10-7b-ef-ff-ff-ff
  Prefix Bits         : 24 bits
  Address Bits        : 24 bits
  Legacy              : False
  Legacy Name         : OUI
  Address Capacity    : 16,777,216

Associated Allocations
  Total
    Blocks           : 72
    Capacity         : 1,207,959,552
  MA-L
    Blocks           : 72
    Capacity         : 1,207,959,552
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
      [L] 00-13-49      [L] 00-19-cb      [L] 00-23-f8      [L] 00-a0-c5      [L] 04-23-36
      [L] 04-bf-6d      [L] 08-26-97      [L] 10-71-b3      [L] 10-7b-ef      [L] 10-c5-fa
      [L] 14-33-75      [L] 14-36-0e      [L] 14-c7-c4      [L] 1c-74-0d      [L] 28-28-5d
      [L] 30-15-77      [L] 30-bd-13      [L] 3c-f7-5d      [L] 40-4a-03      [L] 44-5e-82
      [L] 44-63-c2      [L] 48-ed-e6      [L] 4c-9e-ff      [L] 4c-c5-3e      [L] 50-67-f0
      [L] 50-e0-39      [L] 54-83-3a      [L] 58-8b-f3      [L] 5c-64-8e      [L] 5c-6a-80
      [L] 5c-e2-8c      [L] 5c-f4-ab      [L] 60-31-97      [L] 64-dd-68      [L] 6c-4f-89
      [L] 70-49-a2      [L] 78-c5-7d      [L] 7c-77-16      [L] 80-ea-0b      [L] 88-ac-c0
      [L] 88-f3-d5      [L] 8c-59-73      [L] 90-9f-22      [L] 90-ef-68      [L] 98-0d-67
      [L] a0-e4-cb      [L] b0-b2-dc      [L] b8-d5-26      [L] b8-ec-a3      [L] bc-7e-c3
      [L] bc-99-11      [L] bc-cf-4f      [L] c0-2e-5f      [L] c4-9a-31      [L] c8-33-74
      [L] c8-54-4b      [L] c8-6c-87      [L] cc-5d-4e      [L] d4-1a-d1      [L] d4-3d-f3
      [L] d8-91-2a      [L] d8-ec-e5      [L] e4-18-6b      [L] e8-37-7a      [L] ec-3e-b3
      [L] ec-43-f6      [L] f0-87-56      [L] f4-4d-5c      [L] f8-0d-a9      [L] fc-22-f4
      [L] fc-9f-2a      [L] fc-f5-28

Organization
  Name              : Zyxel
  Full Name         : Zyxel Communications Corporation
  Address
    No. 6 Innovation Road II
    Science Park Hsichu Taiwan TW 300
```

## MAC Autopsy

EtherLyzer can dissect MAC addresses to reveal their underlying structure and properties. The following is a real-world example of how this capability proved useful during a network investigation.

One morning, a NOC engineer discovered that more than **20,000 unique MAC addresses** had appeared on a single switch interface overnight.

The initial suspicion was a possible MAC Authentication Bypass (MAB) attack, potentially involving an attempt to impersonate authorized devices.

However, further analysis revealed something unusual. Only about 10% of the observed addresses corresponded to registered IEEE address blocks, while the remaining addresses exhibited patterns that warranted closer inspection.

By examining their hexadecimal and decimal representations, the engineer identified byte sequences resembling portions of an IPv4 header: a TTL of 64 (`0x40`), TCP protocol identifier (`0x06`), varying header checksums, and what appeared to be fragments of IPv4 addresses.

This suggested that parts of network-layer packet headers were being misinterpreted as Ethernet source MAC addresses.

The investigation ultimately pointed toward an inexpensive unmanaged switch connected to the affected interface as the likely source of the malformed frames.

### Example

```text
etherlyzer inspect 40:06:AF:F1:08:08 -x
```

```text
MAC Address Autopsy
 Input
   Value             : 40:06:AF:F1:08:08
   Length            : 48 bits
 Representations
   Canonical         : 40-06-AF-F1-08-08
   Bit-Reversed      : 02:60:F5:8F:10:10
   To Hex            : 4006AFF10808
   To Integer        : 70,397,465,790,472
   To Decimals       : 64 6 175 241 8 8
   To Octal          : 2000325774204010
   To Binary         : 0100.0000.0000.0110.1010.1111.1111.0001.0000.1000.0000.1000
   To Bytes          : 40 06 AF F1 08 08
 Address Properties
   Null Address      : False
   Broadcast         : False
   Special Bits
     U/L             : 0 Universal / Universally Administered
     I/G             : 0 Individual / Unicast

IEEE Identifier
 Type                : Universal Individual (Unverified)
 SLAP Quadrant       : None
IEEE Registry
 Status              : Not Found
```

The byte sequence `40 06 AF F1 08 08` illustrates the suspected pattern:

- `40` — TTL of 64.
- `06` — TCP protocol identifier.
- `AF F1` — Possible IPv4 header checksum.
- `08 08` — Possible beginning of an IPv4 address.

Although these values alone cannot establish the origin of the malformed frames, their repeated appearance across thousands of MAC addresses provided a valuable lead in identifying the underlying network issue.

## Registry categories

The registry category defaults to `mac`:

```text
etherlyzer inspect 00:11:22:33:44:55
```

A registry category can also be selected explicitly:

```text
etherlyzer inspect -t mac 00:11:22:33:44:55
etherlyzer inspect -t protocol 0800
etherlyzer inspect -t identifier <identifier>
```

The available categories are:

| Category     | Used For                              |
|--------------|---------------------------------------|
| `mac`        | MA-L, MA-M, MA-S, and IAB assignments |
| `protocol`   | EtherType protocol identifiers        |
| `identifier` | IEEE Company Identifiers              |

## Command reference

```text
usage: etherlyzer inspect [-h] [-t {mac|protocol|identifier}] [-x] [-s] [-b] [-a] value

Inspect a single IEEE assignment and display detailed registry metadata, organization information, address range, and related vendor allocations.

positional arguments:
  value                 IEEE assignment or identifier to inspect.

options:
  -h, --help            show this help message and exit
  -t, --type {mac|protocol|identifier}
                        IEEE registry category to search (default: mac).
  -x, --show-mac-autopsy
                        Show MAC address structure, representations, and IEEE identifier classification.
  -s, --show-vendor-stats
                        Show associated vendor allocation counts and address capacities.
  -b, --show-vendor-blocks
                        List associated IEEE-registered vendor blocks.
  -a, --all             Display all available inspection details.

Examples:
  etherlyzer inspect 00:11:22:33:44:55
  etherlyzer inspect 000001 --show-vendor-blocks
  etherlyzer inspect -t mac 00:11:22:33:44:55
  etherlyzer inspect -t protocol 0800
  etherlyzer inspect -t identifier <identifier>
```
