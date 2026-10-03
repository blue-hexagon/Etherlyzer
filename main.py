from etherlyzer.ieee.index import IEEEIndex
from etherlyzer.exporter import RegistryMatchExporter
from etherlyzer.ieee.catalog import Catalog

if __name__ == '__main__':
    import time
    t0 = time.perf_counter()

    registry = Catalog()
    print(f"Registry: {time.perf_counter() - t0:.3f}s")

    t1 = time.perf_counter()
    registries = registry.get_all_registries(check_for_updates=True)
    print(f"Load CSVs: {time.perf_counter() - t1:.3f}s")

    t2 = time.perf_counter()
    index = IEEEIndex.from_registries(registries)
    print(f"Build index: {time.perf_counter() - t2:.3f}s")

    t3 = time.perf_counter()
    index.mac_index.lookup("C8-95-CE-A0-3B-A6")
    macs = (IEEEIndex.get_bulk(
        ieee_index=index.mac_index,
        path_or_text='src/etherlyzer/in2.txt'
    ))
    for mac in macs:
        print(f"[{mac.registry+']':<6}{mac.assignment+':':<12} {mac.organization_name}")
    print(f"Looked up MAC index: {time.perf_counter() - t3:.3f}s")
    tz = time.perf_counter()
    print(f"Total time used: {tz - t3 + tz - t2 + tz-t1:.3f}s")
    exit(0)
    registry = Catalog()
    index = IEEEIndex.from_registries(
        registry.get_all_registries()
    )
    retrieved_vendors = index.get_bulk(
        ieee_index=index.mac_index,
        infile='src/etherlyzer/in2.txt'
    )
    RegistryMatchExporter().export_csv_to_console(
        retrieved_vendors
    )
    print(f"{len(retrieved_vendors)} vendors found")
