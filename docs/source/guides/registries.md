# Registry Database

EtherLyzer maintains local copies of supported IEEE Registration Authority datasets.

Inspect the current registry configuration and synchronization state with:

```text
etherlyzer registries
```

The output includes information such as:

- registry name,
- legacy name,
- category,
- description,
- local dataset path,
- IEEE source URL,
- prefix size,
- last retrieval time, and
- update interval.

## Supported registries

| Registry  | Category   | Purpose                          |
|-----------|------------|----------------------------------|
| MA-L      | MAC        | MAC Address Block Large          |
| MA-M      | MAC        | MAC Address Block Medium         |
| MA-S      | MAC        | MAC Address Block Small          |
| IAB       | MAC        | Legacy Individual Address Block  |
| CID       | Identifier | IEEE Company Identifier          |
| EtherType | Protocol   | Ethernet protocol identifier     |

For details about assignment sizes, OUIs, legacy IAB assignments, and the different IEEE registry types, see {doc}`../concepts/ieee-registries`.

## Local data

Registry datasets are stored locally and used directly for lookups.

This allows EtherLyzer to perform identifier lookups without querying third-party lookup services.

Registry data can be updated with:

```text
etherlyzer sync
```

See {doc}`synchronization` for synchronization behavior and configuration.
