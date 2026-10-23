# Extract MAC Addresses

The `extraction.py` command discovers MAC address candidates in text, binary files, and network packet captures.

It supports protocol-aware extraction from PCAP and PCAPNG files, hexadecimal text scanning, duplicate filtering, location tracking, and customizable output formatting.

Unlike [`format`](format.md), which reformats known addresses, `extraction.py` identifies addresses embedded in existing data.

## Basic usage

Extract MAC addresses from a text file:

```text
etherlyzer extract -f network-log.txt
```

Given the following input:

```text
Interface: GigabitEthernet1/0/15
MAC: 00:20:AF:1B:07:FA

Interface: GigabitEthernet1/0/16
MAC: 00-E0-29-68-8B-FB
```

Output:

```text
00:20:af:1b:07:fa
00:e0:29:68:8b:fb
```

Addresses are returned in discovery order, using lowercase hexadecimal notation with colon separators by default.

## Supported input sources

EtherLyzer selects its extraction method based on the input source.

| Source           | Extraction method                                 | Location information |
|------------------|---------------------------------------------------|----------------------|
| Text files       | ASCII hexadecimal candidate scanning              | Byte offset          |
| Binary files     | ASCII hexadecimal candidate scanning              | Byte offset          |
| Interactive text | ASCII hexadecimal candidate scanning              | Byte offset          |
| PCAP / PCAPNG    | Decoded Ethernet source and destination addresses | Packet number        |

### Text and binary scanning

The scanner searches for sequences of 12 ASCII hexadecimal digits (`0-9`, `A-F`, `a-f`), allowing limited separation between digits.

| Purpose            | Command                                 |
|--------------------|-----------------------------------------|
| Scan a text file   | `etherlyzer extract -f network-log.txt` |
| Scan a binary file | `etherlyzer extract -f capture.bin`     |
| Scan pasted text   | `etherlyzer extract -b`                 |

Recognized candidates may use different hexadecimal representations:

```text
00:20:AF:1B:07:FA
00-20-AF-1B-07-FA
0020.AF1B.07FA
0020AF1B07FA
```

Each represents the same address and is normalized to:

```text
00:20:af:1b:07:fa
```

:::{important}
Binary-file scanning searches for **ASCII-encoded hexadecimal representations**, not arbitrary six-byte binary sequences.

Textual extraction is heuristic: a matching sequence may be unrelated hexadecimal data rather than an actual MAC address.
:::

### Packet captures

PCAP and PCAPNG files are processed using Scapy to extract Ethernet source and destination addresses from decoded frames.

| Purpose                              | Command                                  |
|--------------------------------------|------------------------------------------|
| Extract from PCAP                    | `etherlyzer extract -f capture.pcap`     |
| Extract from PCAPNG                  | `etherlyzer extract -f capture.pcapng`   |
| Extract unique addresses             | `etherlyzer extract -f capture.pcap -u`  |
| Include packet numbers               | `etherlyzer extract -f capture.pcap -l`  |
| Unique addresses with packet numbers | `etherlyzer extract -f capture.pcap -ul` |

Unlike text scanning, capture extraction reads decoded protocol fields rather than searching for textual representations.

:::{note}
Capture extraction requires decoded Ethernet layers. Captures using other link-layer formats may not expose Ethernet addresses directly.
:::

## Location tracking

Use `-l` or `--offsets` to identify where each address was found.

The reported location depends on the input source.

### Packet numbers

For packet captures:

```text
etherlyzer extract -f c04-wap-r1.pcap -l
```

Output:

```text
Packet 1  00:20:af:1b:07:fa
Packet 1  00:e0:29:68:8b:fb
```

Both addresses originate from the same Ethernet frame. Packet numbering begins at 1.

### Byte offsets

For text and binary files:

```text
etherlyzer extract -f network-log.txt -l
```

Example output:

```text
Offset 0x00000020  00:20:af:1b:07:fa
Offset 0x00000056  00:e0:29:68:8b:fb
```

Byte offsets identify positions within the input stream and are displayed in hexadecimal. The values above are illustrative.

## Duplicate filtering

Use `-u` or `--unique` to retain only the first occurrence of each normalized address.

```text
etherlyzer extract -f capture.pcap -u
```

Duplicate comparison uses normalized hexadecimal values, meaning differently formatted representations of the same address are treated as identical.

Combine `-u` and `-l` to retain the first observed location of each unique address:

```text
etherlyzer extract -f capture.pcap -ul
```

Output:

```text
Packet 1  00:20:af:1b:07:fa
Packet 1  00:e0:29:68:8b:fb
```

Subsequent occurrences are omitted, while discovery order is preserved.

This is particularly useful for generating unique MAC address inventories from packet captures or network-device logs.

## Interactive extraction

Use `-b` or `--bulk` to extract addresses directly from pasted text:

```text
etherlyzer extract -b
```

Example:

```text
Paste text. Type ;;; and press <Enter> when done:
Interface GigabitEthernet1/0/15
MAC address: 00:20:AF:1B:07:FA
Connected device: 00-E0-29-68-8B-FB
;;;
```

Output:

```text
00:20:af:1b:07:fa
00:e0:29:68:8b:fb
```

Interactive extraction supports the same filtering, location tracking, and formatting options as file-based text scanning.

| Purpose                       | Command                   |
|-------------------------------|---------------------------|
| Extract from pasted text      | `etherlyzer extract -b`   |
| Remove duplicates             | `etherlyzer extract -bu`  |
| Include byte offsets          | `etherlyzer extract -bl`  |
| Unique addresses with offsets | `etherlyzer extract -bul` |

## Output formatting

Use `-p`, `-s`, and `-c` to control the separator, block size, and hexadecimal casing.

These options affect the output notation without changing the extracted address value.

### Formatting examples

Given `00:20:AF:1B:07:FA`:

| Options              | Output              |
|----------------------|---------------------|
| Default              | `00:20:af:1b:07:fa` |
| `-p -`               | `00-20-af-1b-07-fa` |
| `-p . -s 4`          | `0020.af1b.07fa`    |
| `-c upper`           | `00:20:AF:1B:07:FA` |
| `-p . -s 4 -c upper` | `0020.AF1B.07FA`    |
| `-p ""`              | `0020af1b07fa`      |

### Common formatting commands

| Purpose                         | Command                                                    |
|---------------------------------|------------------------------------------------------------|
| Hyphen-separated notation       | `etherlyzer extract -f network-log.txt -p -`               |
| Cisco-style notation            | `etherlyzer extract -f network-log.txt -p . -s 4`          |
| Uppercase hexadecimal           | `etherlyzer extract -f network-log.txt -c upper`           |
| No separators                   | `etherlyzer extract -f network-log.txt -p ""`              |
| Unique uppercase Cisco notation | `etherlyzer extract -f capture.pcap -u -p . -s 4 -c upper` |

For example, the last command can produce:

```text
0020.AF1B.07FA
00E0.2968.8BFB
```

## Practical workflows

The following examples demonstrate how extraction can support broader network investigations.

### Investigate addresses in a packet capture

Extract unique Ethernet addresses while recording their first observed packet:

```text
etherlyzer extract -f capture.pcap -ul
```

Packet numbers can be used to locate the corresponding frames in Wireshark for further investigation.

### Analyze network-device logs

Scan an exported switch log for unique MAC address candidates:

```text
etherlyzer extract -f switch-log.txt -ul
```

The resulting hexadecimal byte offsets identify where each address was first encountered.

This is useful when examining MAC learning events, authentication records, and interface diagnostics.

### Identify registered organizations

Extract unique addresses:

```text
etherlyzer extract -f capture.pcap -u
```

Then resolve them against locally stored IEEE registries using [`whois`](whois.md):

```text
etherlyzer whois -blcp
```

Paste the extracted addresses and terminate the input with `;;;`.

Example output:

```text
Line  Result  Registry  Assignment  Organization
1.    MATCH   MA-L      0020AF      3COM
2.    MATCH   MA-L      00E029      STANDARD MICROSYSTEMS CORP.
```

For additional analysis, inspect an individual address or examine its numerical representation:

```text
etherlyzer inspect 00:20:af:1b:07:fa -a
etherlyzer translate 00:20:af:1b:07:fa -t decimal_bytes
```

## Understanding extraction results

An extracted address is a candidate, not necessarily a legitimate or registered Ethernet address.

| Extraction method | Reliability and limitations                                                   |
|-------------------|-------------------------------------------------------------------------------|
| Text scanning     | May match unrelated hexadecimal data                                          |
| Binary scanning   | Detects textual representations, not arbitrary six-byte sequences             |
| PCAP / PCAPNG     | Extracts decoded Ethernet header addresses without verifying their legitimacy |

Packet capture extraction is more specific than textual scanning because addresses are retrieved from Ethernet fields. However, this does not establish vendor identity, IEEE registration, or legitimate use.

:::{warning}
The `extraction.py` command does not validate the legitimacy or IEEE registration of extracted addresses.

Use [`validate`](validate.md) for input validation, [`inspect`](inspect.md) for address-property analysis, and [`whois`](whois.md) for IEEE registry lookups.
:::

## Command reference

```text
usage: etherlyzer extract [-h] (-f FILE | -b) [-l] [-u]
                          [-p SEPARATOR] [-s BLOCK_SIZE]
                          [-c {lower,upper}]
```

| Argument / Option             | Description                                           |
|-------------------------------|-------------------------------------------------------|
| `-f, --file FILE`             | Read a text, binary, PCAP, or PCAPNG file.            |
| `-b, --bulk`                  | Read text interactively.                              |
| `-l, --offsets`               | Display byte offsets or packet numbers.               |
| `-u, --unique`                | Return only the first occurrence of each MAC address. |
| `-p, --separator SEPARATOR`   | Set the output separator (default: `:`).              |
| `-s, --block-size BLOCK_SIZE` | Set hexadecimal characters per block (default: `2`).  |
| `-c, --casing {lower,upper}`  | Set hexadecimal casing (default: `lower`).            |
| `-h, --help`                  | Display command help.                                 |

Exactly one input source, `-f` or `-b`, must be selected.
