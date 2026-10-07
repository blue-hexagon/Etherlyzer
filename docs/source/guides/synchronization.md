# Synchronization

EtherLyzer maintains synchronized local copies of supported IEEE registry datasets.

## Manual synchronization

Synchronize the local registry database manually with:

```text
etherlyzer sync
```

Example output:

```text
Synchronizing IEEE registries...

Synchronization completed in 2.41 seconds.
```

## Automatic synchronization

EtherLyzer can also synchronize registry data automatically when the local datasets exceed the configured maximum age.

The synchronization interval is controlled by `DB_UPDATE_INTERVAL_HOURS`.

See {doc}`configuration` for configuration details.

## Offline operation

Once the IEEE registry datasets have been synchronized locally, identifier lookups are performed against the local database.

This means EtherLyzer does not need to query an external MAC-address lookup service during normal lookup operations.

Internet access is only required when registry data needs to be synchronized.

For information about the local registry database, see {doc}`registries`.
