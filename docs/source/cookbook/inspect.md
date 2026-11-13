# Inspect IEEE Assignments

The `inspect` command provides detailed analysis of MAC addresses, IEEE registry assignments, and protocol identifiers.

It goes beyond organizational identification to examine address structure, registry metadata, allocation ranges, and related IEEE registrations.

Depending on the inspected value, EtherLyzer can provide:

- **Registry information:** Assignment type, prefix length, address range, capacity, and legacy status.
- **Organization details:** Registered organization names and addresses.
- **Address classification:** Universal/Local (U/L), Individual/Group (I/G), and applicable SLAP quadrants.
- **Vendor intelligence:** Related IEEE allocations, block counts, and total address capacity.
- **MAC autopsy:** Numerical representations, address properties, and identifier classification.

For background on IEEE allocations and addressing conventions, see {doc}`../concepts/ieee-registries` and {doc}`../concepts/mac-addresses`.

## Basic usage

Inspect a MAC address:

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

The result identifies the registered organization and the IEEE assignment containing the supplied address.

For a more comprehensive inspection, use `-a` or `--all`:

```text
etherlyzer inspect 00:00:0c:12:34:56 -a
```

## Registry categories

The `-t` or `--type` option selects the IEEE registry category to inspect.

| Category     | Description                                     | Example                                       |
|--------------|-------------------------------------------------|-----------------------------------------------|
| `mac`        | MAC address assignments (MA-L, MA-M, MA-S, IAB) | `etherlyzer inspect -t mac 00:00:0c:12:34:56` |
| `protocol`   | IEEE EtherType assignments                      | `etherlyzer inspect -t protocol 0800`         |
| `identifier` | IEEE Company Identifiers                        | `etherlyzer inspect -t identifier 00000C`     |

The default category is `mac`, so specifying `-t mac` is optional.

:::{note}
The inspection options and available output depend on the selected registry category and the type of assignment being inspected.
:::

## MAC address classification

EtherLyzer uses **quadrant-based inspection** to distinguish MAC addresses according to their addressing properties.

After normalization and validation, the Universal/Local (U/L) and Individual/Group (I/G) bits determine which inspection branch applies.

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
             ┌─────────────┴─────────────┐
             │                           │
         Universal                     Local
             │                           │
       ┌─────┴─────┐               ┌─────┴─────┐
       │           │               │           │
   Individual     Group        Individual     Group
       │           │               │           │
       ▼           ▼               ▼           ▼
    EUI-48      Universal        SLAP         Local
  Allocations    Group          Analysis       Group
       │                           │
       ▼                     ┌─────┴─────┐
  MA-L / MA-M                │           │
  MA-S / IAB              ELI/CID    AAI/SAI/
                                     Reserved
```

### Inspection branches

| Branch                   | U/L | I/G | Inspection focus                                                                              |
|--------------------------|-----|-----|-----------------------------------------------------------------------------------------------|
| **Universal Individual** | 0   | 0   | EUI-48 assignments, registry metadata, registered organizations, and related blocks           |
| **Universal Group**      | 0   | 1   | Group addressing, standardized multicast assignments, and protocol mappings                   |
| **Local Individual**     | 1   | 0   | SLAP quadrants, ELI/CID resolution, and locally administered addressing                       |
| **Local Group**          | 1   | 1   | Locally administered group addressing, broadcast detection, and recognized multicast mappings |

Each branch shares basic normalization, bit-level classification, and address representation logic. Additional analysis depends on the addressing scheme and available registry information.

:::{important}
These branches describe structural address classifications, not separate IEEE registries.

Special-purpose addresses, including the all-zero address and Ethernet broadcast, require additional interpretation.

SLAP classification is also structural: matching a quadrant's bit pattern does not prove that the address was assigned according to the corresponding scheme.
:::

## Inspection options

The following options enable additional analysis.

| Option                     | Description                                                                    |
|----------------------------|--------------------------------------------------------------------------------|
| `-x, --show-mac-autopsy`   | Display address structure, representations, and IEEE identifier classification |
| `-s, --show-vendor-stats`  | Display associated allocation counts and address capacities                    |
| `-b, --show-vendor-blocks` | List related IEEE-registered vendor allocations                                |
| `-a, --all`                | Display all available inspection details                                       |

Options can be combined to select particular sections.

### Common commands

| Purpose                           | Command                                    |
|-----------------------------------|--------------------------------------------|
| Inspect a MAC address             | `etherlyzer inspect 00:00:0c:12:34:56`     |
| Examine address structure         | `etherlyzer inspect 40:06:AF:F1:08:08 -x`  |
| Show vendor allocation statistics | `etherlyzer inspect 10:7B:EF -s`           |
| List related vendor blocks        | `etherlyzer inspect 10:7B:EF -b`           |
| Show statistics and blocks        | `etherlyzer inspect 10:7B:EF -sb`          |
| Combine autopsy and statistics    | `etherlyzer inspect 00:00:0c:12:34:56 -xs` |
| Display all available details     | `etherlyzer inspect 00:00:0c:12:34:56 -a`  |

## Vendor allocation analysis

IEEE organizations may hold multiple registered address blocks across different registry types.

EtherLyzer can correlate an inspected assignment with other known allocations associated with the same organization.

### Allocation statistics

Use `-s` to display allocation counts and their corresponding address capacities:

```text
etherlyzer inspect 10:7B:EF -s
```

Example:

```text
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
```

This provides an overview of the organization's registered allocation footprint across the supported MAC registries.

### Related vendor blocks

Use `-b` to list associated IEEE assignments:

```text
etherlyzer inspect 10:7B:EF -b
```

Example excerpt:

```text
Registered Blocks (B=IAB, S=MA-S, M=MA-M, L=MA-L)
    [L] 00-13-49      [L] 00-19-cb      [L] 00-23-f8
    [L] 00-a0-c5      [L] 04-23-36      [L] 04-bf-6d
    [L] 08-26-97      [L] 10-71-b3      [L] 10-7b-ef
    [L] 10-c5-fa      [L] 14-33-75      [L] 14-36-0e
    ...
```

The prefix markers identify the registry type associated with each block.

| Marker | Registry | Prefix length | Address capacity |
|--------|----------|--------------:|-----------------:|
| `L`    | MA-L     |       24 bits |       16,777,216 |
| `M`    | MA-M     |       28 bits |        1,048,576 |
| `S`    | MA-S     |       36 bits |            4,096 |
| `B`    | IAB      |       36 bits |            4,096 |

:::{note}
Vendor correlation is based on available IEEE registration information and the organization's recorded identity.

It does not establish whether every allocation belongs to the same legal entity today, nor whether all available addresses have been assigned to physical devices.
:::

### Practical applications

Allocation analysis can help with:

- Identifying additional IEEE blocks registered to an organization.
- Comparing allocation counts and address capacities.
- Investigating unfamiliar prefixes associated with known vendors.
- Understanding an organization's registered addressing footprint.

For a quick organizational lookup without additional allocation analysis, use [`whois`](whois.md).

## MAC address autopsy

The `-x` or `--show-mac-autopsy` option performs a structural analysis of an individual MAC address.

It displays numerical representations, address properties, and IEEE identifier classification, including cases where no corresponding IEEE registration can be found.

```text
etherlyzer inspect 40:06:AF:F1:08:08 -x
```

Example output:

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

The autopsy separates **structural classification** from **IEEE registry resolution**.

In this example, the address has the bit structure of a universally administered individual address, but EtherLyzer does not identify a corresponding registry assignment.

:::{important}
The U/L and I/G bits describe address properties. They do not, by themselves, verify whether a MAC address was legitimately allocated or assigned.

A structurally universal address without an identifiable IEEE registration should not automatically be treated as malicious or malformed.
:::

## Case study: Investigating malformed Ethernet frames

MAC autopsy can be particularly useful when unexpected addresses contain patterns suggesting that the observed values originated from other packet fields.

During a network investigation, more than **20,000 unique MAC addresses** were observed on a single switch interface over several hours.

The initial suspicion involved possible MAC Authentication Bypass (MAB) abuse or device impersonation.

However, only approximately 10% of the observed addresses corresponded to registered IEEE allocations. Many of the remaining addresses exhibited recurring byte patterns.

### Examining the address bytes

One representative address was:

```text
40:06:AF:F1:08:08
```

Its decimal octets can be obtained using [`translate`](translate.md):

```text
etherlyzer translate 40:06:AF:F1:08:08 -t decimal_bytes
```

Output:

```text
64 6 175 241 8 8
```

The corresponding hexadecimal bytes are:

```text
40 06 AF F1 08 08
```

These values resemble fields that can occur in an IPv4 header:

| Bytes   | Decimal | Possible interpretation     |
|---------|---------|-----------------------------|
| `40`    | 64      | IPv4 Time to Live (TTL)     |
| `06`    | 6       | TCP protocol identifier     |
| `AF F1` | 45041   | IPv4 header checksum        |
| `08 08` | 8, 8    | Fragment of an IPv4 address |

This raised the possibility that bytes from the network-layer header were being interpreted as an Ethernet source address.

### Investigative significance

The recurring patterns suggested a packet-assembly or parsing problem rather than a conventional collection of independently assigned MAC addresses.

The investigation pointed toward an inexpensive unmanaged switch connected to the affected interface as a possible source of the malformed frames.

However, the byte patterns alone did not establish the exact failure mechanism or conclusively identify the responsible device.

The important finding was that **structural analysis of the addresses revealed relationships that ordinary IEEE vendor lookups could not explain**.

This illustrates why MAC autopsy can be valuable when investigating:

- Unexpectedly large numbers of learned MAC addresses.
- Addresses containing recurring byte sequences.
- Possible packet-header misalignment or corruption.
- Unregistered addresses with recognizable protocol-field patterns.
- Unusual address distributions on a single switch interface.

:::{note}
A pattern resembling protocol-header fields is an investigative clue, not proof of header corruption.

Confirming the underlying cause requires supporting packet captures, device diagnostics, or other network evidence.
:::

## Additional inspection examples

| Goal                                   | Command                                       |
|----------------------------------------|-----------------------------------------------|
| Inspect a complete MAC address         | `etherlyzer inspect 00:11:22:33:44:55`        |
| Inspect an IEEE MAC assignment prefix  | `etherlyzer inspect 000001`                   |
| Explicitly select MAC registries       | `etherlyzer inspect -t mac 00:11:22:33:44:55` |
| Inspect an EtherType assignment        | `etherlyzer inspect -t protocol 0800`         |
| Inspect an IEEE Company Identifier     | `etherlyzer inspect -t identifier 00000C`     |
| Investigate an unusual address         | `etherlyzer inspect 40:06:AF:F1:08:08 -x`     |
| Examine vendor allocation statistics   | `etherlyzer inspect 10:7B:EF -s`              |
| Discover related organizational blocks | `etherlyzer inspect 10:7B:EF -b`              |
| Perform a comprehensive inspection     | `etherlyzer inspect 00:11:22:33:44:55 -a`     |

## Command reference

```text
usage: etherlyzer inspect [-h] [-t {mac|protocol|identifier}]
                          [-x] [-s] [-b] [-a] value
```

| Argument / Option                        | Description                                                                     |
|------------------------------------------|---------------------------------------------------------------------------------|
| `value`                                  | IEEE assignment or identifier to inspect.                                       |
| `-t, --type {mac\|protocol\|identifier}` | Select the IEEE registry category (default: `mac`).                             |
| `-x, --show-mac-autopsy`                 | Display address structure, representations, and IEEE identifier classification. |
| `-s, --show-vendor-stats`                | Display associated allocation counts and address capacities.                    |
| `-b, --show-vendor-blocks`               | List associated IEEE-registered vendor blocks.                                  |
| `-a, --all`                              | Display all available inspection details.                                       |
| `-h, --help`                             | Display command help.                                                           |

The `inspect` command operates on a single assignment or identifier at a time.

Unlike commands supporting interactive bulk processing, `-b` in `inspect` means **show vendor blocks**, not bulk input.
