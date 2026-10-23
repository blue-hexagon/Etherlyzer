# from etherlyzer.exporter import RegistryMatchExporter
# from etherlyzer.ieee.index.ieee_index import IEEEIndexCatalog
# from etherlyzer.ieee.registry.catalog import IEEERegistryCatalog
#
# if __name__ == "__main__":
#     import time
#
#     t0 = time.perf_counter()
#
#     registry = IEEERegistryCatalog()
#     print(f"Registry: {time.perf_counter() - t0:.3f}s")
#
#     t1 = time.perf_counter()
#     registries = registry.get_all_registries_and_ensure_cache_is_synced(check_for_updates=True)
#     print(f"Load CSVs: {time.perf_counter() - t1:.3f}s")
#
#     t2 = time.perf_counter()
#     index = IEEEIndexCatalog.build(registries)
#     print(f"Build index: {time.perf_counter() - t2:.3f}s")
#
#     t3 = time.perf_counter()
#     index.mac_index.get_one("C8-95-CE-A0-3B-A6")
#     macs = IEEEIndexCatalog.get_bulk(
#         ieee_index=index.mac_index, path_or_text="src/etherlyzer/in2.txt"
#     )
#     for mac in macs:
#         print(f"[{mac.registry + ']':<6}{mac.assignment + ':':<12} {mac.organization_name}")
#     print(f"Looked up MAC index: {time.perf_counter() - t3:.3f}s")
#     tz = time.perf_counter()
#     print(f"Total time used: {tz - t3 + tz - t2 + tz - t1:.3f}s")
#     exit(0)
#     registry = IEEERegistryCatalog()
#     index = IEEEIndexCatalog.build(registry.get_all_registries_and_ensure_cache_is_synced())
#     retrieved_vendors = index.get_bulk(ieee_index=index.mac_index, infile="src/etherlyzer/in2.txt")
#     RegistryMatchExporter().export_csv_to_console(retrieved_vendors)
#     print(f"{len(retrieved_vendors)} vendors found")
