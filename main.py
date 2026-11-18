import json
from pathlib import Path

from etherlyzer import (
    extraction,
    formatting,
    inspect_ethertype,
    inspect_mac,
    lookup_mac,
    normalize,
    normalize_strict,
    translation,
)
from etherlyzer.presentation import Item, Report, Section, get_renderer


def build_mac_registration(mac: str) -> Section:
    registered_mac = lookup_mac(mac)
    if registered_mac is None:
        return Section(title="IEEE Assignment", items=[Item(key="Result", value="No match found.")])
    return Section(
        title="IEEE Assignment",
        items=[
            Item(key="Registry", value=registered_mac.registry),
            Item(key="Assignment", value=registered_mac.assignment),
            Item(key="Name", value=registered_mac.organization_name),
            Item(key="Address", value=registered_mac.organization_address),
        ],
    )


def build_mac_translation(mac: str) -> Section:
    normalized = normalize(mac)
    return Section(
        title="Translation",
        items=[
            Item("Binary", translation.to_binary(normalized)),
            Item("Bytes", translation.to_bytes(normalized)),
        ],
    )


def build_mac_formats(mac: str) -> Section:
    normalized = normalize(mac)
    return Section(
        title="Formats",
        items=[
            Item(key="Etherlyzer", value=formatting.default_format(normalized)),
            Item(key="Canonical", value=formatting.canonical_format(normalized)),
            Item(
                key="Cisco",
                value=formatting.custom_format(
                    normalized,
                    block_size=4,
                    separator=".",
                    case="lower",
                ),
            ),
        ],
    )


def build_mac_inspection(mac: str) -> Section:
    rich_mac = inspect_mac(mac)

    return Section(
        title="Mac Inspection",
        items=[
            Section(
                title="Autopsy",
                items=[
                    Item("Normalization", rich_mac.structure.normalized),
                    Item("Complete", rich_mac.structure.is_complete),
                    Item("Zero Address", rich_mac.structure.is_zero),
                    Item("Broadcast Address", rich_mac.structure.is_broadcast),
                    Item("Delivery", rich_mac.structure.delivery.value),
                    Item("Administration", rich_mac.structure.administration.value),
                    Item(
                        "SLAP",
                        rich_mac.structure.slap_quadrant.value
                        if rich_mac.structure.slap_quadrant
                        else None,
                    ),
                ],
            ),
            Section(
                title="Identity",
                items=[
                    Item("Form", rich_mac.form.value),
                    Item("Resolution", rich_mac.resolution.value),
                    Item("Identity", rich_mac.identity.value),
                    Section(
                        title="Assessment",
                        items=[
                            Item(a.label, a.description)
                            for a in sorted(
                                rich_mac.assessment,
                                key=lambda a: a.name,
                            )
                        ],
                    ),
                ],
            ),
        ],
    )


def build_reports_from_pcap(pcap_fp: Path):
    unique_macs: set[str] = extraction.extract_unique_pcap_macs(pcap_fp)
    total_report_count = len(unique_macs)
    reports: list[Report] = [
        Report(
            sections=[
                Section(
                    title=f"Report {idx}/{total_report_count} [{mac}]:",
                    items=[
                        build_mac_formats(mac),
                        build_mac_registration(mac),
                        build_mac_inspection(mac),
                        build_mac_translation(mac),
                    ],
                )
            ]
        )
        for idx, mac in enumerate(sorted(unique_macs), start=1)
    ]
    text_renderer = get_renderer("text")
    json_renderer = get_renderer("json")

    for report in reports:
        print(report.render(text_renderer), end="\n\n")

    payload = [json.loads(report.render(json_renderer)) for report in reports]

    Path("report.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def translate_bulk(file_path: Path) -> None:
    with file_path.open("r", encoding="utf-8") as f:
        for line in f:
            try:
                mac = normalize_strict(line.strip())
            except ValueError:
                continue

            reversed_hex = translation.to_bit_reversed(mac)
            reversed_mac = normalize(reversed_hex)

            print(f"MAC Address       : {formatting.canonical_format(mac)}")
            print(
                f"Cisco Format      : {formatting.custom_format(mac, block_size=4, separator='.', case='lower')}"
            )
            print(f"Normalized        : {mac}")
            print()
            print(f"Hexadecimal       : {translation.to_hex(mac)}")
            print(f"Hexadecimal Bytes : {translation.to_hex_bytes(mac)}")
            print(f"Decimal           : {translation.to_decimal(mac)}")
            print(f"Decimal Bytes     : {translation.to_decimal_octets(mac)}")
            print()
            print(f"Binary            : {translation.to_binary(mac)}")
            print(f"Binary Raw        : {translation.to_binary_raw(mac)}")
            print(f"Bit-Reversed Hex  : {reversed_hex}")
            print(f"Bit-Reversed Bin  : {translation.to_binary(reversed_mac)}")
            print()
            print(
                f"Reversible        : {normalize(translation.to_bit_reversed(reversed_mac)) == mac}"
            )
            print("-" * 90)


def format_bulk(file_path: Path) -> None:
    formats = [
        (2, ":"),
        (2, "-"),
        (4, "."),
        (12, ""),
    ]

    with file_path.open("r", encoding="utf-8") as f:
        for line in f:
            try:
                mac = normalize_strict(line.strip())
            except ValueError:
                continue

            print(f"Input: {mac}")

            for block_size, separator in formats:
                formatted = formatting.custom_format(
                    mac,
                    block_size=block_size,
                    separator=separator,
                    case="upper",
                )
                print(f"  {formatted}")

            print()


def build_ethertype_section(ethertype: str) -> Section:
    result = inspect_ethertype(ethertype)

    return Section(
        title=f"EtherType Inspection [0x{result.assignment}]",
        items=[
            Item("Field Type", result.field_type.value),
            Item("Value", f"0x{result.value:04X}"),
            Item("Length", result.length_value),
            Item("EtherType", result.is_ethertype),
            Item("Registry Match", result.match_status),
            Item("Registry", result.registry),
            Item("Protocol", result.description),
            Item("Organization", result.organization_name),
            Item("Organization Address", result.organization_address),
            Item("OUI Extended", result.requires_oui_pid),
        ],
    )


def build_ethertype_report():
    report = Report(
        sections=[
            build_ethertype_section("0806"),
        ],
    )
    print(get_renderer("csv").render(report))


if __name__ == "__main__":
    build_reports_from_pcap(Path("./c04-wap-r1.pcap"))
    translate_bulk(Path("whois.txt"))
    format_bulk(Path("whois.txt"))
    build_ethertype_report()
