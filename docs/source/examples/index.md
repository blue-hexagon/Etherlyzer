# Examples

This section collects practical EtherLyzer workflows.

## Identify a vendor

```text
etherlyzer whois 00:11:22:33:44:55
```

## Inspect an assignment

```text
etherlyzer inspect 00:11:22:33:44:55
```

## Validate a MAC address

```text
etherlyzer validate 00-11-22-33-44-55
```

## Format a MAC address

```text
etherlyzer format 001122334455
```

## Cisco-style formatting

```text
etherlyzer format 001122334455 -p . -s 4
```
## Windows-style formatting

```text
etherlyzer format 001122334455 -p - -s 2
```

## Bulk vendor lookup from a file

```text
etherlyzer whois -f ./macs.txt
```

## Bulk interactive validation

```text
etherlyzer validate -b --linenumbers --show-info
```

## Synchronize registries

```text
etherlyzer sync
```
