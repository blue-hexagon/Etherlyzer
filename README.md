# EtherLyzer

EtherLyzer is a Python library and command-line utility for identifying, classifying, and working with Ethernet-related identifiers.

It provides fast, high-performance offline lookups:

* IEEE MAC address registries (EtherType, MA-L/OUI-24, MA-M/OUI-28, MA-S/OUI-36, MANID, OPID, CID, IAB)
* Protocol identifiers
* Block sizes and vendor information

Etherlyzer provides a CLI utilty supporting single and bulk-processing + a Python library/API.

It builds high-performance indexes of fresh datasets that by default (althrough this can be adjusted) update once every 24 hours.

EtherLyzer is designed for network engineers, cybersecurity professionals, automation, and asset discovery.

---

## What can EtherLyzer do?

EtherLyzer maintains a local copy of IEEE registries, enabling fast, offline lookups without requiring Internet access and sharing MAC adresses with a third-party that might collect your searches and correlate them with your IP and more.

Typical use cases include:

* Identify the manufacturer of a MAC address.
* Distinguish between MA-L, MA-M, and MA-S allocations.
* Look up EtherTypes (e.g. IPv4, IPv6, ARP, LLDP).
* Identify vendor information.
* Bulk-process thousands of MAC addresses from CLI/API in seconds.
* Build high-performance lookup indexes for repeated searches.
* Automatically synchronize the local IEEE registry database (update interval configurable).
* Validate, normalize and format MAC addresses from and to, virtually any format.
* Export lookup results as CSV or other delimited formats.
* Integrate into automation scripts, inventory systems, NAC workflows, NOC/SOC tooling and asset discovery solutions.


Etherlyzer automatically fetches the official IEEE registry listings once every 24 hours, ensuring that the local registry data remains up to date. IEEE states that its public listings are updated every 24 hours.

The synchronization interval can be adjusted to your preference in the shipped `etherlyzer.env` file.

---

## Showcasing

### Identify HW Vendor

```text
etherlyzer identify --type mac 001a2b3c4d5e

Organization
  Name           : Ayecom Technology
  Full Name      : Ayecom Technology Co., Ltd.
  Address
    No. 25
    R&D Road 2
    Science-Based Industrial Park Hsinchu
    TW 300

Registry
  IEEE Type    : MA-L [MAC Address Block Large]
  Assignment   : 00-1a-2b
  Range        : 00-1a-2b-00-00-00 - 00-1a-2b-ff-ff-ff
  Legacy       : False
  Prefix Bits  : 24 bits
  Address Bits : 24 bits
  Addresses    : 16,777,216

```

### The Data Layer

From the command-line: `etherlyzer info`:

```text
(etherlyzer-py3.14) PS C:\Users\T\Desktop\EtherTools> etherlyzer info

EtherLyzer 0.3.0

Registries
IEEE Name: MA-L (MAC Address Block Large)
Legacy Name: OUI
Category: mac
Description: Large IEEE MAC address allocation. Formerly known as the Organizationally Unique Identifier (OUI). Used by vendors requiring large address spaces.
Is Legacy: False
Filepath: C:\Users\T\AppData\Local\Manjana\etherlyzer\Cache\1.0\MA-L.csv
URL: https://standards-oui.ieee.org/oui/oui.csv
Prefix bits: 24
Last retrieved: 2026-09-28 17:33:17.442158+00:00
Update interval: 1 day, 0:00:00

IEEE Name: MA-M (MAC Address Block Medium)
Legacy Name: OUI-28
Category: mac
Description: Medium-sized IEEE MAC address allocation intended for organizations requiring fewer addresses than MA-L.
Is Legacy: False
Filepath: C:\Users\T\AppData\Local\Manjana\etherlyzer\Cache\1.0\MA-M.csv
URL: https://standards-oui.ieee.org/oui28/mam.csv
Prefix bits: 28
Last retrieved: 2026-09-28 17:33:20.061122+00:00
Update interval: 1 day, 0:00:00

IEEE Name: MA-S (MAC Address Block Small)
Legacy Name: OUI-36
Category: mac
Description: Small IEEE MAC address allocation for embedded devices, IoT, industrial equipment, and smaller manufacturers.
Is Legacy: False
Filepath: C:\Users\T\AppData\Local\Manjana\etherlyzer\Cache\1.0\MA-S.csv
URL: https://standards-oui.ieee.org/oui36/oui36.csv
Prefix bits: 36
Last retrieved: 2026-09-28 17:33:22.278145+00:00
Update interval: 1 day, 0:00:00

IEEE Name: MANID (Manufacturer Identifier)
Legacy Name: None
Category: identifier
Description: Manufacturer identifier registry maintained by the IEEE Registration Authority. Used to uniquely identify manufacturers rather than allocating MAC addresses.
Is Legacy: False
Filepath: C:\Users\T\AppData\Local\Manjana\etherlyzer\Cache\1.0\MANID.csv
URL: https://standards-oui.ieee.org/manid/manid.csv
Prefix bits: None
Last retrieved: 2026-09-28 17:33:23.313482+00:00
Update interval: 1 day, 0:00:00

IEEE Name: OPID (OUI-based Protocol Identifier)
Legacy Name: None
Category: identifier
Description: Registry of protocol identifiers based on IEEE-assigned organizational identifiers. Used by vendor-specific and IEEE protocols.
Is Legacy: False
Filepath: C:\Users\T\AppData\Local\Manjana\etherlyzer\Cache\1.0\OPID.csv
URL: https://standards-oui.ieee.org/bopid/opid.csv
Prefix bits: None
Last retrieved: 2026-09-28 17:33:24.455807+00:00
Update interval: 1 day, 0:00:00

IEEE Name: CID (Company Identifier)
Legacy Name: None
Category: identifier
Description: Unique company identifiers assigned by IEEE. Identifies organizations independently of MAC address allocations.
Is Legacy: False
Filepath: C:\Users\T\AppData\Local\Manjana\etherlyzer\Cache\1.0\CID.csv
URL: https://standards-oui.ieee.org/cid/cid.csv
Prefix bits: None
Last retrieved: 2026-09-28 17:33:25.409803+00:00
Update interval: 1 day, 0:00:00

IEEE Name: IAB (Individual Address Block)
Legacy Name: None
Category: mac
Description: Legacy IEEE MAC address allocation scheme superseded by MA-S. Retained for compatibility with older hardware.
Is Legacy: True
Filepath: C:\Users\T\AppData\Local\Manjana\etherlyzer\Cache\1.0\IAB.csv
URL: https://standards-oui.ieee.org/iab/iab.csv
Prefix bits: 36
Last retrieved: 2026-09-28 17:33:27.785458+00:00
Update interval: 1 day, 0:00:00

IEEE Name: EtherType (EtherType Registry)
Legacy Name: None
Category: protocol
Description: Registry mapping EtherType values to Ethernet protocols, including IPv4, IPv6, ARP, VLAN tagging, LLDP, MPLS, 802.1X, and many vendor-specific protocols.
Is Legacy: False
Filepath: C:\Users\T\AppData\Local\Manjana\etherlyzer\Cache\1.0\EtherType.csv
URL: https://standards-oui.ieee.org/ethertype/eth.csv
Prefix bits: None
Last retrieved: 2026-09-28 17:33:29.763446+00:00
Update interval: 1 day, 0:00:00
```
### Format Nasty MAC Addresses

```shell
etherlyzer format l..iIdOØ1!23-4oo.. --fix-typos --casing "upper" --block-size 4 --separator .

> 111D.0012.3400
```

## Installation

Clone the repository:

*Not published to pypi yet(!).*

```bash
pip install etherlyzer
```

## Commandline Interface
```text
usage: etherlyzer [-h] [-v] {validize,format,update,info,identify} ...

EtherLyzer - Ethernet lookup and analysis toolkit

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

Commands:
  {validize,format,update,info,identify}
    validize            Validates and normalizes MAC addresses
    format              Format MAC address
    update              Synchronize IEEE registries
    info                Show application information
    identify            Search vendors, protocols or assignments
```

### Example: validize

Validates and normalizes MAC adresses in bulk.

Validation runs first after which candidates are normalized and optionally a masked output of the MACs failing validation are output.

```text
v = valid hex digit
M = missing digit
V = excess valid hex digit
I = invalid character
r/R = relaxed typo candidate
l/L = lenient typo candidate
```

Options:
```text
usage: etherlyzer validize [-h] [-b] [-l] [-s] [-o] [-n] [mac]

positional arguments:
  mac                   MAC address to normalize

options:
  -h, --help            show this help message and exit
  -b, --bulk            Read multiple MAC addresses interactively
  -l, --linenumbers     Show linenumbers corresponding to each MAC address (kind of only useful when validizing in bulk)
  -s, --strict          Only return MAC's that can be normalized without errors.
  -o, --show-originals  Displays the original MAC addresses after the normalized MAC address on each line.
  -n, --no-info         Doesn't display an OK or ERR before each line depending on whether the outout succeeded normalization.
```

Example

```text
etherlyzer validize --bulk --linenumbers

Paste MAC addresses. Enter a triple semicolon ;;; when done:
001a2b3c4d5e
001a2b3c4d5
001a2b3c4d5e6
001a2b3c4d5?
001a2b3c4d5O
001a2b3c4d5I
001a2b3c4d5L
001a2b3c4d5S
001a2b3c4d5eF
001a2b3c4d5eO
001a2b3c4d5eI
001a2b3c4d5eL
001a2b3c4d5eS
001a2b3c4d5e?
001a2b3c4d5eFF
001a2b3c4d5eOO
001a2b3c4d5eII
001a2b3c4d5eSS
00:1a:2b:3c:4d:5e
00-1a-2b-3c-4d-5e
001a.2b3c.4d5e
0:0:1:a:2:b:3:c:4:d:5:e
00 : 1a : 2b : 3c : 4d : 5e
"00:1a:2b:3c:4d:5e"
00::1a::2b::3c::4d::5e
00:1a-2b.3c:4d-5e
;;;

OK  001a2b3c4d5e    << 001a2b3c4d5e
ERR 001a2b3c4d5     >> vvvvvvvvvvvM
ERR 001a2b3c4d5e6   >> vvvvvvvvvvvvV
ERR 001a2b3c4d5     >> vvvvvvvvvvvM
ERR 001a2b3c4d5O    >> vvvvvvvvvvvr
ERR 001a2b3c4d5I    >> vvvvvvvvvvvl
ERR 001a2b3c4d5L    >> vvvvvvvvvvvl
ERR 001a2b3c4d5S    >> vvvvvvvvvvvl
ERR 001a2b3c4d5ef   >> vvvvvvvvvvvvV
ERR 001a2b3c4d5eO   >> vvvvvvvvvvvvR
ERR 001a2b3c4d5eI   >> vvvvvvvvvvvvL
ERR 001a2b3c4d5eL   >> vvvvvvvvvvvvL
ERR 001a2b3c4d5eS   >> vvvvvvvvvvvvL
OK  001a2b3c4d5e    << 001a2b3c4d5e?
ERR 001a2b3c4d5eff  >> vvvvvvvvvvvvVV
ERR 001a2b3c4d5eOO  >> vvvvvvvvvvvvRR
ERR 001a2b3c4d5eII  >> vvvvvvvvvvvvLL
ERR 001a2b3c4d5eSS  >> vvvvvvvvvvvvLL
OK  001a2b3c4d5e    << 00:1a:2b:3c:4d:5e
OK  001a2b3c4d5e    << 00-1a-2b-3c-4d-5e
OK  001a2b3c4d5e    << 001a.2b3c.4d5e
OK  001a2b3c4d5e    << 0:0:1:a:2:b:3:c:4:d:5:e
OK  001a2b3c4d5e    << 00 : 1a : 2b : 3c : 4d : 5e
OK  001a2b3c4d5e    << "00:1a:2b:3c:4d:5e"
OK  001a2b3c4d5e    << 00::1a::2b::3c::4d::5e
OK  001a2b3c4d5e    << 00:1a-2b.3c:4d-5e

Normalized 10/26 MAC addresses. Invalid MAC addresses identified: 16/26
```


## Configuration

The included `etherlyzer.env` file provides sensible defaults and works out of the box.

Example configuration:

```dotenv
#---------------------------------------------------DATASET
# Maximum age of the local IEEE database before synchronization, in hours
DB_UPDATE_INTERVAL_HOURS=24

#---------------------------------------------------EXPORT
# Field delimiter used for CSV and stdout output
FIELD_SEPARATOR="\t"
# MAC address formatting
# Supported separators: :, -, ., or an empty value
MAC_SEPARATOR=-
# Number of hexadecimal characters per block
# 2 -> 00:11:22:33:44:55
# 4 -> 0011.2233.4455
MAC_BLOCK_SIZE=2
# Supported values: upper, lower
MAC_CASE=lower

#---------------------------------------------------DISPLAY
# Print database synchronization messages
SHOW_SYNC_MESSAGES=true

#---------------------------------------------------INPUT (deprecated - will use stdin in future)
# Read lookup values from a text file
USE_FILE_ENABLED=true
# Input filename relative to the configured input directory
USE_FILE=in.txt
```

---

## Running

Using Poetry:

```bash
poetry run python main.py
```

Or activate the virtual environment first:

```bash
poetry env activate
python main.py
```

---

## Project Structure

```text
EtherLyzer/
├── data/
├── src/
│   └── etherlyzer/
├── .env
├── pyproject.toml
└── README.md
```

---

## Requirements

Developed with:

* Python 3.14+
* Poetry

The project may also run on earlier Python versions with minor modifications, although Python 3.14 is the officially supported development target.

---

## License

This project is released under the MIT License.

You're free to use, modify, distribute, and sell it with very few restrictions. See the `LICENSE` file for details.
