# MAC Inspection

## Queries

:::{note}
Both query-types support IEEE **Company Identifier** (CID) lookups for ELI-48 addresses. Although CIDs are organizational identifiers rather than MAC address allocations, they can be used to resolve the registered organization associated with an ELI-48 address.
:::

```{eval-rst}
.. autofunction:: etherlyzer.inspect_mac
```


```{eval-rst}
.. autofunction:: etherlyzer.lookup_mac
```

## Result Models

```{eval-rst}
.. autoclass:: etherlyzer.MacIdentityResult
   :undoc-members:
   :class-doc-from: both
   :members:
```

```{eval-rst}
.. autoclass:: etherlyzer.MacStructure
   :undoc-members:
   :class-doc-from: both
   :members:
```

```{eval-rst}
.. autoclass:: etherlyzer.MacForm
   :undoc-members:
   :class-doc-from: both
   :members:
```

```{eval-rst}
.. autoclass:: etherlyzer.MacIdentity
   :undoc-members:
   :class-doc-from: both
   :members:
```

```{eval-rst}
.. autoclass:: etherlyzer.MacResolution
   :undoc-members:
   :class-doc-from: both
   :members:
```
