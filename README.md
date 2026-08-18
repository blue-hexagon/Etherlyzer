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
* Identify industrial, AV, IoT, and network infrastructure vendors.
* Bulk-process thousands of MAC addresses from text files.
* Build high-performance lookup indexes for repeated searches.
* Automatically synchronize the local IEEE registry database.
* Normalize MAC addresses from virtually any format.
* Format MAC addresses using Cisco, Windows, Linux, or custom styles.
* Export lookup results as CSV or other delimited formats.
* Integrate into automation scripts, inventory systems, NAC workflows, NOC/SOC tooling, and asset discovery solutions.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/blue-hexagon/EtherLyzer.git
cd EtherLyzer
```

Install the project using Poetry:

```bash
poetry install
```

---

## Configuration

The included `.env` file provides sensible defaults and works out of the box.

Example configuration:

```dotenv
DB_UPDATE_INTERVAL_HOURS=24

FIELD_SEPARATOR=;
MAC_SEPARATOR=.
MAC_BLOCK_SIZE=4
MAC_CASE=upper

SHOW_SYNC_MESSAGES=false

USE_FILE_ENABLED=true
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
poetry shell
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
