# Synchronization

EtherLyzer maintains local copies of supported IEEE registry datasets, enabling offline lookups and analysis without relying on external lookup services.

Registry synchronization can be performed manually, triggered automatically when datasets expire, or forced for specific registries.

## How synchronization works

EtherLyzer uses locally stored IEEE registry data for address identification and inspection.

The synchronization process checks whether datasets require updating and refreshes them from their upstream IEEE sources when necessary.

| Mode | Behavior | Command |
|---|---|---|
| Standard | Check and refresh expired registries | `etherlyzer sync` |
| Status | Display registry expiration information | `etherlyzer sync --status` |
| Force | Synchronize regardless of expiration status | `etherlyzer sync --force` |

Synchronization can operate on all supported registries or selected datasets.

## Manual synchronization

Run the following command to check and synchronize the local registry database:

```text
etherlyzer sync
```

Example output:

```text
Synchronizing IEEE registries...

Synchronization completed in 2.41 seconds.
```

By default, synchronization refreshes registries when updates are required rather than unconditionally downloading every dataset.

### Check registry status

Use `-s` or `--status` to inspect expiration status:

```text
etherlyzer sync --status
```

To check individual registries:

```text
etherlyzer sync -s MA-L
```

Multiple registries can be selected:

```text
etherlyzer sync -s MA-L MA-M
```

### Force synchronization

Use `-f` or `--force` to refresh registry data regardless of its expiration status:

```text
etherlyzer sync --force
```

To force synchronization of selected registries:

```text
etherlyzer sync -f MA-L MA-M
```

This is useful when intentionally refreshing local data before its configured expiration.

:::{note}
The `--status` and `--force` options are mutually exclusive.

Both accept optional registry names. When no names are specified, the operation applies to all supported registries.
:::

## Automatic synchronization

EtherLyzer can automatically refresh registry datasets when they exceed their configured maximum age.

The expiration interval is controlled by:

```text
DB_UPDATE_INTERVAL_HOURS
```

This setting determines when locally stored registry data becomes eligible for synchronization.

For configuration instructions, see {doc}`configuration`.

:::{important}
Automatic synchronization depends on the application's synchronization behavior and the availability of upstream IEEE sources.

An expired dataset does not necessarily mean that its contents are invalid; it indicates that the configured refresh interval has been exceeded.
:::

## Offline operation

Once IEEE registry datasets have been synchronized, EtherLyzer performs lookups against its local database.

Commands such as `whois` and `inspect` can therefore resolve available registry information without querying an external lookup service for each address.

| Operation | Internet access |
|---|---|
| Local IEEE registry lookup | Not required |
| MAC address inspection using local data | Not required |
| Checking locally recorded expiration information | Not required |
| Downloading updated IEEE registry data | Required |

The local database reflects the most recently synchronized datasets. If upstream registrations have changed since the last successful synchronization, those changes will not be reflected until the local data is refreshed.

For details about the supported datasets, see {doc}`registries`.

## Command reference

```text
usage: etherlyzer sync [-h] [-s [REGISTRY ...] | -f [REGISTRY ...]]
```

| Argument / Option | Description |
|---|---|
| `-s, --status [REGISTRY ...]` | Display expiration status for all or selected IEEE registries. |
| `-f, --force [REGISTRY ...]` | Force synchronization of all or selected IEEE registries. |
| `-h, --help` | Display command help. |

### Examples

| Purpose | Command |
|---|---|
| Synchronize expired registries | `etherlyzer sync` |
| Check all registry statuses | `etherlyzer sync -s` |
| Check MA-L expiration status | `etherlyzer sync -s MA-L` |
| Check multiple registries | `etherlyzer sync -s MA-L MA-M` |
| Force synchronization of all registries | `etherlyzer sync -f` |
| Force synchronization of MA-L | `etherlyzer sync -f MA-L` |
| Force synchronization of selected registries | `etherlyzer sync -f MA-L MA-M` |

## Related documentation

- {doc}`configuration` — Configure synchronization intervals and application behavior.
- {doc}`registries` — Understand locally stored IEEE registry datasets.
- {doc}`../cookbook/whois` — Identify registered organizations using local registry data.
- {doc}`../cookbook/inspect` — Inspect IEEE assignments and related allocation information.
