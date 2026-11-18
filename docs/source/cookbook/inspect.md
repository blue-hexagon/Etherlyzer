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
etherlyzer inspect mac 00:00:0c:12:34:56
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
etherlyzer inspect mac 00:00:0c:12:34:56 -a
```

## Registry categories

The `-t` or `--type` option selects the IEEE registry category to inspect.

| Category     | Description                                     | Example                                |
|--------------|-------------------------------------------------|----------------------------------------|
| `mac`        | MAC address assignments (MA-L, MA-M, MA-S, IAB) | `etherlyzer inspect mac 00:00:0c:12:34:56` |
| `ethertype`  | IEEE EtherType assignments                      | `etherlyzer inspect ethertype 0800`    |
| `identifier` | IEEE Company Identifiers                        | `etherlyzer inspect identifier 00000C` |

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

## Vendor allocation analysis

IEEE organizations may hold multiple registered address blocks across different registry types.

EtherLyzer can correlate an inspected assignment with other known allocations associated with the same organization.

### Allocation statistics

Use `-s` to display allocation counts and their corresponding address capacities:

```text
etherlyzer inspect mac 10:7B:EF:AF:AF:FF -s
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
```

This provides an overview of the organization's registered allocation footprint across the supported MAC registries.

### Related vendor blocks

Use `-b` to list associated IEEE assignments:

```text
etherlyzer inspect mac 10:7B:EF:0F:0D:1C -b
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

## Additional inspection examples

| Goal                                   | Command                                       |
|----------------------------------------|-----------------------------------------------|
| Inspect a complete MAC address         | `etherlyzer inspect mac 00:11:22:33:44:55`    |
| Inspect an IEEE MAC assignment prefix  | `etherlyzer inspect mac 000001`               |
| Explicitly select MAC registries       | `etherlyzer inspect mac 00:11:22:33:44:55`    |
| Inspect an EtherType assignment        | `etherlyzer inspect ethertype 0800`           |
| Inspect an IEEE Company Identifier     | `etherlyzer inspect identifier 00000C`        |
| Examine vendor allocation statistics   | `etherlyzer inspect mac 10:7B:EF -s`          |
| Discover related organizational blocks | `etherlyzer inspect mac 10:7B:EF -b`          |
| Perform a comprehensive inspection     | `etherlyzer inspect mac 00:11:22:33:44:55 -a` |

## Example

```text
etherlyzer inspect mac 000000010101 -a

MAC Address Autopsy
  Input
    Value                        : 000000010101
    Length                       : 48 bits
  IEEE Identity
    Kind                         : Universal Individual Address
    Type                         : EUI-48-Compatible Individual Address
    Registration                 : Registered Block (MA-L)
    SLAP Quadrant                : None
    Assessment
      Registered Candidate       : The complete identifier falls within an eligible IEEE-registered allocation, but assignment of the specific identifier has not been verified.
      Structurally Conformant    : The identifier conforms to the applicable structural addressing rules. This does not establish that it has been registered or assigned.
  Representations
    Canonical                    : 00-00-00-01-01-01
    Bit-Reversed                 : 00:00:00:80:80:80
    To Hex                       : 0x000000010101
    To Integer                   : 65,793
    To Decimals                  : 0 0 0 1 1 1
    To Binary                    : 00000000.00000000.00000000.00000001.00000001.00000001
    To Bytes                     : 00 00 00 01 01 01
  Address Properties
    Null Address                 : False
    Broadcast                    : False
    Special Bits
      U/L                        : 0 Universal / Universally Administered
      I/G                        : 0 Individual / Unicast
  IEEE Registry
    Organization
      Name                       : XEROX CORPORATION
      Full Name                  : XEROX CORPORATION
      Address                    : M/S 105-50C WEBSTER NY US 14580 
    Allocation
      Registry                   : MA-L [MAC Address Block Large]
      Assignment                 : 00:00:00
      Range                      : 00:00:00:00:00:00 - 00:00:00:ff:ff:ff
      Prefix Bits                : 24 bits
      Address Bits               : 24 bits
      Address Capacity           : 16,777,216
      Legacy                     : No
    Associated Allocations
      Summary
        Blocks                   : 13
        Capacity                 : 202,375,168
      By Registry
        MA-L
          Blocks                 : 12
          Capacity               : 201,326,592
        MA-M
          Blocks                 : 1
          Capacity               : 1,048,576
    Registered Blocks
      Legend: B=IAB, S=MA-S, M=MA-M, L=MA-L
      [L] 00:00:01    [L] 00:00:02    [L] 00:00:03    [L] 00:00:04    [L] 00:00:05
      [L] 00:00:06    [L] 00:00:07    [L] 00:00:08    [L] 00:00:09    [L] 00:00:aa
      [L] 9c:93:4e    [L] e8:4d:ec    [M] c0:fb:f9:0
```
