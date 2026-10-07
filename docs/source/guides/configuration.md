# Configuration

EtherLyzer ships with a default `etherlyzer.env` configuration template.

On first use, the configuration is copied to EtherLyzer's platform-specific application-data directory. The user copy can then be modified without changing files inside the installed Python package.

Environment variables override values loaded from `etherlyzer.env`.

## Configuration options

| Variable                   | Default | Description                                                                   |
|----------------------------|---------|-------------------------------------------------------------------------------|
| `DB_UPDATE_INTERVAL_HOURS` | `24`    | Maximum age of the local IEEE registry data before synchronization, in hours. |
| `FIELD_SEPARATOR`          | `"\t"`  | Field delimiter used for CSV and standard output.                             |
| `MAC_SEPARATOR`            | `-`     | Separator used when formatting MAC addresses.                                 |
| `MAC_BLOCK_SIZE`           | `2`     | Number of hexadecimal characters per MAC-address block.                       |
| `MAC_CASE`                 | `lower` | Output casing for hexadecimal characters: `lower` or `upper`.                 |
| `SHOW_SYNC_MESSAGES`       | `true`  | Controls whether registry synchronization messages are displayed.             |

## Example configuration

```bash
# Maximum age of the local IEEE database before synchronization, in hours
DB_UPDATE_INTERVAL_HOURS=24

# Field delimiter used for CSV and stdout output
FIELD_SEPARATOR="\t"

# MAC address formatting
# Supported separators: :, -, ., or an empty value
MAC_SEPARATOR=-

# Number of hexadecimal characters per block
MAC_BLOCK_SIZE=2

# Supported values: upper, lower
MAC_CASE=lower

# Print database synchronization messages
SHOW_SYNC_MESSAGES=true
```

## Configuration precedence

Configuration is resolved in the following order (for both CLI and library usage):

1. Environment variables
2. Platform-specific Userdir `etherlyzer.env`
3. EtherLyzer defaults

Higher-priority values override lower-priority values.
