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

## Example output

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

For MAC assignments, EtherLyzer also correlates the organization against its other known MAC registry allocations.

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
