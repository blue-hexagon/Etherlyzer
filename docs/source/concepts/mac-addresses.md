# MAC Addresses

EtherLyzer works primarily with EUI-48 MAC addresses.

An EUI-48 address contains:

- 48 bits
- 6 octets
- 12 hexadecimal digits

For example:

```text
00:1a:2b:3c:4d:5e
```

## First-octet flags

The two least-significant bits of the first octet have special meanings:

```text
First octet

bit:  7  6  5  4  3  2  1  0
      x  x  x  x  x  x U/L I/G
```

### I/G — Individual/Group

The I/G bit identifies whether the address represents an individual interface or a group.

```text
I/G = 0  Individual (Unicast)
I/G = 1  Group (Multicast/Broadcast)
```

### U/L — Universal/Local

The U/L bit identifies whether the address is universally or locally administered.

```text
U/L = 0  Universally administered
U/L = 1  Locally administered
```

Universally administered addresses are candidates for resolution against IEEE-assigned MAC address blocks.

Locally administered addresses may be used for purposes such as address randomization, virtualization, locally assigned addressing, or deliberate address replacement.

## Possible combinations

| U/L | I/G | Meaning               | Typically Seen With                                              |
|----:|----:|-----------------------|------------------------------------------------------------------|
|   0 |   0 | Individual, Universal | IEEE-assigned unicast addresses                                  |
|   0 |   1 | Group, Universal      | Standardized multicast addresses                                 |
|   1 |   0 | Individual, Local     | Locally assigned, randomized, or virtual MAC addresses           |
|   1 |   1 | Group, Local          | IPv6 multicast (`33:33:...`) and locally defined group addresses |

These bits are independent. A group address may therefore be universally or locally administered, just as an individual address may be.
