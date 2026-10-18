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
usage: etherlyzer whois [-h] [-d DELIMITER] [-p] [-l] [-c] (-f FILE | -b | mac)

Identify IEEE vendors and organizations for one or more MAC addresses.

positional arguments:
  mac                   MAC address to identify

options:
  -h, --help            show this help message and exit
  -d, --delimiter DELIMITER
                        Select a delimiter, if none is chosen tabs is default
  -p, --preserve-bad-entries
                        Enables preservation of bad entries such as self-assigned or multicast addresses
  -l, --linenumbers     Prefix output lines with their corresponding input line number
  -c, --column-names    Write a header row on the first line of the output
  -f, --file FILE       Read MAC addresses from a file
  -b, --bulk            Read multiple MAC addresses interactively

Examples:
  etherlyzer whois 00:11:22:33:44:55   Look up a single MAC address
  etherlyzer whois -b                  Enter MAC addresses interactively
  etherlyzer whois -f .\macs.txt       Look up MAC addresses from a file
  etherlyzer whois -bl                 Show original input line numbers
  etherlyzer whois -bp                 Include unsuccessful lookups
  etherlyzer whois -blcp               Show all results in an aligned table
  etherlyzer whois -blcp -d ";"        Output semicolon-delimited results
```
