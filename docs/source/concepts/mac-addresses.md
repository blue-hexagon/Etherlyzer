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

### As Table Quadrants

```{list-table} MAC Address Administration and Delivery Classification
:header-rows: 1
:widths: 25 38 38
:align: center

* - **U/L → </br> I/G ↓**
  - **Universally Administered </br> (U/L = 0)**
  - **Locally Administered </br> (U/L = 1)**
* - **Unicast / Individual </br> (I/G = 0)**
  -  Universal Individual</br>MA-L, MA-M, MA-S, IAB</br>
    `x0-xx-xx-xx-xx-xx`  
    `x4-xx-xx-xx-xx-xx`  
    `x8-xx-xx-xx-xx-xx`  
    `xC-xx-xx-xx-xx-xx`
  -  Local Individual</br>SLAP Quadrant </br>
    `x2-xx-xx-xx-xx-xx`  
    `x6-xx-xx-xx-xx-xx`  
    `xA-xx-xx-xx-xx-xx`  
    `xE-xx-xx-xx-xx-xx`
* - **Multicast / Group </br>(I/G = 1)**
  -  Universal Group</br>Administered Multicast</br>
    `x1-xx-xx-xx-xx-xx`  
    `x5-xx-xx-xx-xx-xx`  
    `x9-xx-xx-xx-xx-xx`  
    `xD-xx-xx-xx-xx-xx`
  -  Local Group</br>Locally Administered Multicast</br>
    `x3-xx-xx-xx-xx-xx`  
    `x7-xx-xx-xx-xx-xx`  
    `xB-xx-xx-xx-xx-xx`  
    `xF-xx-xx-xx-xx-xx`
```

### The Structured Local Address Plan (SLAP)

The **Structured Local Address Plan (SLAP)**, introduced by IEEE 802c, provides an optional framework for organizing locally administered individual MAC addresses.

SLAP divides this address space into four quadrants using two additional bits in the first octet, known as the **Y and Z bits** (bits 2 and 3).

The four quadrants are:

```{list-table} SLAP Quadrant Classification
:header-rows: 1
:widths: 15 30 55
:align: center

* - **Quadrant**
  - **Designation**
  - **Purpose**
* - **AAI**
  - Administratively Assigned Identifier
  - Addresses assigned by local administrators or applications without requiring an IEEE-registered prefix.
* - **ELI**
  - Extended Local Identifier
  - Addresses structured around an IEEE-assigned 24-bit Company ID (CID), followed by a 24-bit extension assigned under the CID registrant's authority.
* - **Reserved**
  - Reserved
  - Reserved for future standardized local addressing schemes.
* - **SAI**
  - Standard Assigned Identifier
  - Addresses assigned according to an IEEE 802 standard-defined addressing protocol.
```

#### Identifying the SLAP Quadrant

For a locally administered individual address, the Y and Z bits determine the SLAP quadrant:

```{list-table} SLAP Quadrant Bit Patterns
:header-rows: 1
:widths: 15 15 25 45
:align: center

* - **Y (bit 2)**
  - **Z (bit 3)**
  - **Quadrant**
  - **First-octet pattern**
* - 0
  - 0
  - AAI
  - `x2`
* - 0
  - 1
  - ELI
  - `xA`
* - 1
  - 0
  - Reserved
  - `x6`
* - 1
  - 1
  - SAI
  - `xE`
```

For example, consider the MAC address `3A:72:C2:AC:DE:FF`.

Its first octet is `0x3A`, represented in binary as:

```text
Bit position:  7 6 5 4 3 2 1 0
Bit value:     0 0 1 1 1 0 1 0
                         | | |
                         | | +-- I/G = 0 (Individual)
                         | +---- U/L = 1 (Local)
                         +------ Y   = 0

Z = 1 (bit 3)
```

The resulting classification is:

- **I/G = 0:** Individual (Unicast)
- **U/L = 1:** Locally administered
- **Y = 0:** SLAP Y bit cleared
- **Z = 1:** SLAP Z bit set

The address therefore falls within the **ELI quadrant**.

```{important}
**SLAP is optional.**

A locally administered address may occupy a particular SLAP quadrant without actually having been generated or assigned according to that quadrant's intended addressing scheme.

Structural classification alone does not establish SLAP compliance.
```

### IEEE Registrations and Address Assignment

**MA-L**, **MA-M**, **MA-S**, and the legacy **IAB** scheme define IEEE address allocation structures.

However, an address having the appropriate U/L and I/G bit pattern does not necessarily belong to a registered IEEE allocation.

It is important to distinguish three separate concepts:

```{list-table} IEEE Address Assignment Terminology
:header-rows: 1
:widths: 30 70

* - **Concept**
  - **Meaning**
* - **Structurally Eligible**
  - The address has the bit pattern required for a particular addressing scheme.
* - **Registered Allocation**
  - The address or prefix matches an allocation recorded in the relevant IEEE registry.
* - **Individually Assigned**
  - The specific identifier has actually been assigned to a device, interface, or other intended recipient by an authorized entity.
```

A successful IEEE registry lookup establishes the existence of a matching registered allocation.

It does **not** independently prove that:

- The specific address was legitimately assigned by the registrant.
- The device was manufactured by the registered organization.
- The address has not been modified, randomized, or spoofed.
- The address is globally unique in actual use.

Similarly, an ELI-quadrant address containing a registered **Company ID (CID)** identifies the organization associated with that CID, but does not establish the legitimacy or origin of the remaining 24-bit extension.

```{note}
**EtherLyzer distinguishes structural classifications from IEEE registry lookup results.**

An address may be structurally consistent with an IEEE identifier scheme without having a corresponding registered allocation.

Conversely, a registered allocation identifies ownership of an address block, not necessarily the identity or authenticity of a device using an address within that block.
```

### References

- [RFC 8948 — Structured Local Address Plan (SLAP)](https://www.rfc-editor.org/rfc/rfc8948.html)
- [RFC 9542 — IANA Considerations and IETF Protocol and Documentation Usage for IEEE 802 Parameters](https://www.rfc-editor.org/rfc/rfc9542.html)
