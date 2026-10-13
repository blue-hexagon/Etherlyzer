# Vendor Identification

The `whois` command identifies the IEEE vendor or organization associated with one or more MAC addresses using the local IEEE registry data.

## Single MAC address

```text
etherlyzer whois 00:11:22:33:44:55
```

## Read MAC addresses from a file

```text
etherlyzer whois -f ./macs.txt
```

## Interactive input

```text
etherlyzer whois -i
```

For detailed registry, assignment, range, and allocation information, see {doc}`inspect`.

## Command reference

```text
usage: etherlyzer whois [-h] (-f FILE | -i | [mac])

Identify IEEE vendors and organizations for one or more MAC addresses.

positional arguments:
  mac                MAC address to identify

options:
  -h, --help         show this help message and exit
  -f, --file FILE    Read MAC addresses from a file
  -i, --interactive  Read multiple MAC addresses interactively
```
