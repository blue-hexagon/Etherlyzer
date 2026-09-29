# EtherLyzer

EtherLyzer is a Python library and command-line utility for identifying, classifying, and working with Ethernet-related identifiers.

It provides fast, offline lookups for:

* IEEE MAC address registries (MA-L, MA-M, MA-S)
* EtherTypes
* Protocol identifiers
* Vendor information
* High-performance bulk lookups and indexing

EtherLyzer is designed for network engineers, cybersecurity professionals, automation, and asset discovery.

---

## What can EtherLyzer do?

EtherLyzer maintains a local copy of IEEE registries, enabling fast, offline lookups without requiring Internet access.

Typical use cases include:

* Identify the manufacturer of a MAC address.
* Distinguish between MA-L, MA-M, and MA-S allocations.
* Look up EtherTypes (e.g. IPv4, IPv6, ARP, LLDP).
* Identify industrial, AV, IoT, network infrastructure vendors and a bunch more.
* Bulk-process thousands of MAC addresses from text files in seconds.
* Build high-performance lookup indexes for repeated searches.
* Automatically synchronize the local IEEE registry database (update interval configurable).
* Normalize MAC addresses from virtually any format.
* Format MAC addresses using Cisco, Windows, Linux, or custom formats.
* Export lookup results as CSV or other delimited formats.
* Integrate into automation scripts, inventory systems, NAC workflows, NOC/SOC tooling, and asset discovery solutions.

---

## Installation

Clone the repository:

```bash
pip install etherlyzer
```

## Running

```bash
etherlyzer normalize --bulk --linenumbers | Select-String "Invalid"

>>>
00:1A:2B:3C:4D:5E
00-1A-2B-3C-4D-5E
001A.2B3C.4D5E
001A2B3C4D5E
00 1A 2B 3C 4D 5E
001A-2B3C-4D5E
001A:2B3C:4D5E

aa:bb:cc:dd:ee:ff
AA-BB-CC-DD-EE-FF
aabb.ccdd.eeff
AABBCCDDEEFF

00:00:00:00:00:00
FF:FF:FF:FF:FF:FF
02:00:00:00:00:01

00:1A:2B:3C:4D
00:1A:2B:3C:4D:5E:6F
001A2B3C4D5
001A2B3C4D5E00

00:1A:2B:3C:4D:ZZ
GG:1A:2B:3C:4D:5E
00:1A:2B:3C:4D:5G

00::1A:2B:3C:4D:5E
00:1A::2B:3C:4D:5E
00-1A:2B-3C:4D-5E
00.1A.2B.3C.4D.5E

 00:1A:2B:3C:4D:5E
00:1A:2B:3C:4D:5E 
00:1A:2B:3C:4D:5E\t
00 : 1A : 2B : 3C : 4D : 5E
;;;

15. Invalid MAC address: 001a2b3c4d?
16. Invalid MAC address: 001a2b3c4d5e?6f

```
---

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
