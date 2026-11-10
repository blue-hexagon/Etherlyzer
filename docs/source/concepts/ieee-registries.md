# IEEE Registries

EtherLyzer maintains local copies of supported IEEE Registration Authority datasets and uses them for local identifier lookups.

## Supported registry types

| Registry  | Category   | Purpose                              |
|-----------|------------|--------------------------------------|
| MA-L      | MAC        | MAC Address Block Large              |
| MA-M      | MAC        | MAC Address Block Medium             |
| MA-S      | MAC        | MAC Address Block Small              |
| IAB       | MAC        | Legacy Individual Address Block      |
| CID       | Identifier | IEEE Company Identifier              |
| EtherType | Protocol   | Ethernet protocol identifier         |

## EUI-48 assignment sizes

| Type | Prefix bits | Address bits |  Addresses |
|------|------------:|-------------:|-----------:|
| MA-L |          24 |           24 | 16,777,216 |
| MA-M |          28 |           20 |  1,048,576 |
| MA-S |          36 |           12 |      4,096 |
| IAB  |          36 |           12 |      4,096 |

The prefix and address sizes above refer to allocations within the 48-bit EUI-48 address space.

## MA-L

MA-L, or **MAC Address Block Large**, uses a 24-bit assignment prefix and provides 24 bits of address space.

An MA-L assignment includes an IEEE **Organizationally Unique Identifier (OUI)**.

```text
Prefix        Address space
24 bits       24 bits
────────────┬────────────────────────
00:11:22    │ xx:xx:xx
```

This provides **16,777,216** EUI-48 addresses per assignment.

## MA-M

MA-M, or **MAC Address Block Medium**, uses a 28-bit assignment prefix and provides 20 bits of address space.

```text
Prefix             Address space
28 bits            20 bits
────────────────┬────────────────────
00:11:22:3      │ x:xx:xx
```

This provides **1,048,576** EUI-48 addresses per assignment.

Unlike MA-L, an MA-M assignment does not include an OUI.

## MA-S

MA-S, or **MAC Address Block Small**, uses a 36-bit assignment prefix and provides 12 bits of address space.

An MA-S assignment includes an IEEE **OUI-36**.

```text
Prefix                     Address space
36 bits                    12 bits
────────────────────────┬────────────
00:11:22:33:4           │ x:xx
```

This provides **4,096** EUI-48 addresses per assignment.

## IAB

IAB, or **Individual Address Block**, is a legacy 36-bit assignment type providing 4,096 EUI-48 addresses.

The IAB registry is no longer active and was replaced by MA-S. Existing IAB assignments remain valid and may still appear in historical and currently deployed hardware.

EtherLyzer retains IAB registry data so these assignments can still be resolved and inspected as they are very much active to this day, despite being a legacy registry.

### Background Explainer

> The Individual Address Block is an inactive registry activity, which has been replaced by the MA-S registry product as of January 1,2014. The owner of an already assigned IAB may continue to use the assignment until its exhaustion. The IAB was used by organizations/companies that required less than 4097 unique 48-bit numbers (EUI-48) and thus found it hard to justify buying their own OUI. The IAB uses a MA-L (and OUI) belonging to the IEEE Registration Authority, concatenated with 12 additional IEEE-provided bits (for a total of 36 bits), leaving only 12 bits for the IAB owner to assign to their (up to 4096) individual devices. Unlike an OUI, which allows the assignee to assign values in various different number spaces (for example, EUI-48, EUI-64, and the various CDI number spaces), the Individual Address Block could only be used to assign EUI-48 identifiers. All other potential uses based on the OUI from which the IABs are allocated are reserved, and remain the property of the IEEE Registration Authority. It should also be noted that, between 2007 and September 2012, the OUI value 00:50:C2 was used for IAB assignments. After September 2012, the value 40:D8:55 was used. Applications making use of EUI-48 values assigned under an IAB should have made no assumptions about the bit pattern present in the (24-bit most-significant) OUI portion of the assigned numbers.
- https://standards.ieee.org/faqs/regauth/ What is an Individual Address Block (IAB)?

## CID

CID, or **Company Identifier**, is a globally unique 24-bit identifier assigned by the IEEE Registration Authority.

Unlike an OUI, a CID cannot be used to generate universally unique EUI-48 or EUI-64 addresses.

CID is intended for applications where an organization requires a globally unique identifier without requiring globally unique MAC addresses.

## EtherType

An **EtherType** is a 16-bit protocol identifier used to indicate the protocol carried by an Ethernet frame.

Common examples include:

| EtherType | Protocol         |
|----------:|------------------|
|  `0x0800` | IPv4             |
|  `0x0806` | ARP              |
|  `0x86DD` | IPv6             |
|  `0x8100` | IEEE 802.1Q VLAN |

## Local registry data

EtherLyzer performs lookups against synchronized local IEEE registry data rather than sending identifiers to third-party lookup services.

Internet access is only required when the local registry data needs to be synchronized.
