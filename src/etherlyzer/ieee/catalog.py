from etherlyzer.ieee.ieee_registry import RegCategory, IEEEEntry, EtherTypeEntry, IEEERegistry


class Catalog:
    IEEE_REGISTRIES = {  # noqa
        "mal": IEEERegistry(
            enabled=True,
            name="MA-L",
            model=IEEEEntry,
            full_name="MAC Address Block Large",
            legacy_name="OUI",
            category=RegCategory.MAC,
            prefix_bits=24,
            address_bits=24,
            address_count=16_777_216,
            legacy=False,
            description=(
                "Large IEEE MAC address allocation. Formerly known as the "
                "Organizationally Unique Identifier (OUI). Used by vendors "
                "requiring large address spaces."
            ),
            url="https://standards-oui.ieee.org/oui/oui.csv",
        ),
        "mam": IEEERegistry(
            enabled=True,
            name="MA-M",
            model=IEEEEntry,
            full_name="MAC Address Block Medium",
            legacy_name="OUI-28",
            category=RegCategory.MAC,
            prefix_bits=28,
            address_bits=20,
            address_count=1_048_576,
            legacy=False,
            description=(
                "Medium-sized IEEE MAC address allocation intended for "
                "organizations requiring fewer addresses than MA-L."
            ),
            url="https://standards-oui.ieee.org/oui28/mam.csv",
        ),
        "mas": IEEERegistry(
            enabled=True,
            name="MA-S",
            model=IEEEEntry,
            full_name="MAC Address Block Small",
            legacy_name="OUI-36",
            category=RegCategory.MAC,
            prefix_bits=36,
            address_bits=12,
            address_count=4_096,
            legacy=False,
            description=(
                "Small IEEE MAC address allocation for embedded devices, "
                "IoT, industrial equipment, and smaller manufacturers."
            ),
            url="https://standards-oui.ieee.org/oui36/oui36.csv",
        ),
        "cid": IEEERegistry(
            enabled=True,
            name="CID",
            model=IEEEEntry,
            full_name="Company Identifier",
            legacy_name=None,
            category=RegCategory.IDENTIFIER,
            legacy=False,
            description=(
                "Unique company identifiers assigned by IEEE. Identifies "
                "organizations independently of MAC address allocations."
            ),
            url="https://standards-oui.ieee.org/cid/cid.csv",
        ),
        "iab": IEEERegistry(
            enabled=True,
            name="IAB",
            model=IEEEEntry,
            full_name="Individual Address Block",
            legacy_name=None,
            category=RegCategory.MAC,
            prefix_bits=36,
            address_bits=12,
            address_count=4_096,
            legacy=True,
            description=(
                "Legacy IEEE MAC address allocation scheme superseded by "
                "MA-S. Retained for compatibility with older hardware."
            ),
            url="https://standards-oui.ieee.org/iab/iab.csv",
        ),
        "ethertype": IEEERegistry(
            enabled=True,
            name="EtherType",
            model=EtherTypeEntry,
            full_name="EtherType Registry",
            legacy_name=None,
            category=RegCategory.PROTOCOL,
            legacy=False,
            description=(
                "Registry mapping EtherType values to Ethernet protocols, "
                "including IPv4, IPv6, ARP, VLAN tagging, LLDP, MPLS, "
                "802.1X, and many vendor-specific protocols."
            ),
            url="https://standards-oui.ieee.org/ethertype/eth.csv",
        ),
    }

    @classmethod
    def db_is_initialized(cls):
        db_init_checks: list[bool] = []
        for registry in cls.IEEE_REGISTRIES.values():
            db_init_checks.append(registry.filepath.exists())
        if not all([check for check in db_init_checks]):
            return False
        return True

    @staticmethod
    def get_registry(registry_name: str) -> IEEERegistry | None:
        return Catalog.IEEE_REGISTRIES.get(registry_name, None)

    def get_all_registries(self, check_for_updates=True) -> list[IEEERegistry]:
        for registry in self.IEEE_REGISTRIES.values():
            # If not checking for updates, we still need a present dataset.
            if (check_for_updates and registry.need_updates()) or not self.db_is_initialized():

                status = registry.save()
                if status is False:
                    break
        return list(self.IEEE_REGISTRIES.values())

    def __getitem__(self, key):
        return self.IEEE_REGISTRIES[key]
