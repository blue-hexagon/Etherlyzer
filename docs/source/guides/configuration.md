# Configuration

## Configuration precedence

Configuration is resolved in the following order (for both CLI and library usage):

1. Environment variables
2. Platform-specific Userdir `etherlyzer.env`
3. EtherLyzer defaults

Higher-priority values override lower-priority values.

### Detailed Explanation

EtherLyzer supports configuration through environment variables and an optional `etherlyzer.env` file.

Configuration values are resolved in the following order, from highest to lowest priority:

1. **Process environment variables** — Variables already defined in the process environment take precedence.
2. **`etherlyzer.env`** — Values from the selected configuration file are loaded only when the corresponding environment
   variables are not already defined.
3. **Built-in defaults** — Values defined by `EtherlyzerKnobs` are used when no environment value is available or if a
   setting wasn't defined in the `.env` file.

#### Configuration file discovery

EtherLyzer searches for `etherlyzer.env` starting from the current working directory and continuing upward through its
parent directories.

The first matching file is selected.

If no file is found, EtherLyzer uses:

`DEFAULT_CACHE_DIR / "etherlyzer.env"`

Which is `Platformsdir` ->
`user_cache_dir(appname="etherlyzer", appauthor="Manjana", version="1.0", ensure_exists=True)`

If this fallback file does not exist, it is created from the packaged configuration template.

Only **one configuration file** is loaded. Configuration files are not merged.

#### Example

Consider the following `etherlyzer.env`:

```dotenv
MAC_SEPARATOR=:
MAC_BLOCK_SIZE=2
MAC_CASE=lower
```

If the process environment also defines:

```bash
MAC_SEPARATOR=-
```

The effective configuration becomes:

| Setting           | Effective value | Source              |
|-------------------|-----------------|---------------------|
| `MAC_SEPARATOR`   | `-`             | Process environment |
| `MAC_BLOCK_SIZE`  | `2`             | Configuration file  |
| `MAC_CASE`        | `lower`         | Configuration file  |
| `FIELD_SEPARATOR` | `;`             | Built-in default    |

### Additional behavior

- Environment variable names correspond to the uppercase dataclass field names.
- Empty strings are treated as explicitly configured values, not as missing variables.
- Boolean values accept `true`, `false`, `yes`, `no`, `on`, `off`, `1`, and `0` (case-insensitive).
- Enum values are resolved using their case-insensitive member names.
- `DB_UPDATE_INTERVAL_HOURS` accepts positive integer values or predefined aliases such as `hourly`, `daily`, `weekly`,
  `monthly`, and `yearly`.
- Invalid configuration values raise an exception during configuration loading.

**Configuration is initialized at import time.** Editing the environment file does not automatically update an existing
`etherlyzer_knobs` instance. Restart the application to load the updated configuration reliably.

---

## Configuration options

EtherLyzer supports the following environment variables:

| Variable                   | Default          | Description                                                                                                                              |
|----------------------------|------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| `DB_UPDATE_INTERVAL_HOURS` | `168` (`weekly`) | Maximum age of the local IEEE registry data before synchronization, in hours. Accepts a positive integer or a predefined interval alias. |
| `FIELD_SEPARATOR`          | `;`              | Field delimiter used for CSV export and CLI output. Must be exactly one character.                                                       |
| `MAC_SEPARATOR`            | `.`              | Separator used when formatting MAC addresses. Supported values: `:`, `-`, `.`, or an empty string.                                       |
| `MAC_BLOCK_SIZE`           | `4`              | Number of hexadecimal characters per MAC-address block. Supported values: `2`, `4`, or `12`.                                             |
| `MAC_CASE`                 | `upper`          | Output casing for hexadecimal characters. Supported values: `upper`, `lower`.                                                            |
| `TYPO_TOLERANCE`           | `strict`         | Controls input normalization tolerance. Supported values: `strict`, `relaxed`, `lenient`.                                                |
| `SHOW_SYNC_MESSAGES`       | `false`          | Controls whether database synchronization messages are displayed.                                                                        |

### Synchronization interval aliases

The `DB_UPDATE_INTERVAL_HOURS` setting accepts the following symbolic values:

| Alias           | Hours |
|-----------------|------:|
| `hourly`        |     1 |
| `daily`         |    24 |
| `twice-weekly`  |    84 |
| `weekly`        |   168 |
| `fortnightly`   |   336 |
| `twice-monthly` |   360 |
| `monthly`       |   720 |
| `quarterly`     |  2160 |
| `yearly`        |  8760 |

Intervals such as `monthly` and `yearly` use fixed durations rather than calendar-aware calculations.

### Example configuration

```bash
# Maximum age of the local IEEE database before synchronization, in hours
# Alternatively, the following may be specified:
# hourly, daily, twice-weekly, weekly, fortnightly, twice-monthly, monthly, quarterly, yearly
DB_UPDATE_INTERVAL_HOURS=fortnightly

# Field delimiter used for CSV export and CLI output
FIELD_SEPARATOR=";"

# MAC address formatting
# Allowed separators: :, -, ., or an empty value
MAC_SEPARATOR=:

# Number of hexadecimal characters per block
# 2 -> 00:11:22:33:44:55
# 4 -> 0011.2233.4455
MAC_BLOCK_SIZE=2

# MAC Address Casing
# Supported values: upper, lower
MAC_CASE=lower

# Print database synchronization messages
SHOW_SYNC_MESSAGES=true

# strict|relaxed|lenient
TYPO_TOLERANCE=lenient
```
