from etherlyzer.domain.entry.ethertype import EtherTypeEntry
from etherlyzer.presentation.reporting.model import Item, Section
from etherlyzer.presentation.reporting.renderers.text import TextRenderer
from etherlyzer.presentation.terminal.commands.inspect.common import CommonInspectionParams


def inspect_ethertype(
    params: CommonInspectionParams,
) -> int:

    value = int(params.args.value, 16)

    if not 0 <= value <= 0xFFFF:
        raise ValueError("EtherType must be a 16-bit hexadecimal value.")

    entry = f"{value:04X}"
    lookup = params.context.indexes.ethertype.lookup(entry)

    if not isinstance(lookup, EtherTypeEntry) and lookup is not None:
        raise TypeError("Wrong ethertype entry")

    items: list[Section | Item] = [
        Section(
            title="Input",
            items=[
                Item(key="Value", value=entry),
                Item(key="Length", value="16 bits"),
            ],
        ),
    ]

    if value <= 0x05DC:  # 0-1500
        items.append(
            Section(
                title="Classification",
                items=[
                    Item(key="Type", value="IEEE 802.3 Length Field"),
                    Item(key="Length Value", value=f"{value} bytes"),
                    Item(key="EtherType", value="False"),
                ],
            )
        )
    elif value < 0x0600:  # 1501-1535
        items.append(
            Section(
                title="Classification",
                items=[
                    Item(key="Type", value="Undefined Length/Type"),
                    Item(key="EtherType", value="False"),
                ],
            )
        )
    else:
        items.append(
            Section(
                title="Classification",
                items=[
                    Item(
                        key="Type",
                        value="Registered EtherType"
                        if lookup is not None
                        else "EtherType Structure",
                    ),
                    Item(key="EtherType", value="True"),
                ],
            )
        )

    if lookup is None:
        items.append(
            Section(
                title="Registration",
                items=[
                    Item(key="Registry", value="EtherType"),
                    Item(
                        key="Status",
                        value="No Match" if value >= 0x0600 else "Not Applicable",
                    ),
                ],
            )
        )
    else:
        items.append(
            Section(
                title="Registration",
                items=[
                    Item(key="Registry", value=lookup.registry),
                    Item(key="Assignment", value=f"0x{lookup.assignment.upper()}"),
                    Item(key="Description", value=lookup.protocol),
                ],
            ),
        )
        items.append(
            Section(
                title="Organization",
                items=[
                    Item(key="Name", value=lookup.organization_name),
                    Item(
                        key="Address",
                        value=lookup.organization_address.strip()
                        if lookup.organization_address is not None
                        else "Not Specified",
                    ),
                ],
            ),
        )

    section = Section(title="EtherType", items=items)

    params.report.sections.append(section)
    print(TextRenderer().render(params.report))
    return 0
