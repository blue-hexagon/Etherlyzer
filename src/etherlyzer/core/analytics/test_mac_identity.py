# from types import SimpleNamespace
# from typing import cast
# from unittest.mock import Mock
#
# import pytest
#
# from etherlyzer.core.analytics.mac_classifier import classify_mac
# from etherlyzer.core.analytics.mac_identity import (
#     IdentityResult,
#     MacForm,
#     MacResolution,
#     MacIdentity,
#     analyze_mac_identity,
# )
# from etherlyzer.ieee.initialize import EtherlyzerContext
#
#
# @pytest.fixture
# def ctx() -> Mock:
#     """Provide deterministic empty indexes; no real registry initialization."""
#     context = Mock()
#     context.indexes.mac.lookup.return_value = None
#     context.indexes.mac.lookup_group_allocation.return_value = None
#     context.indexes.identifier.lookup.return_value = None
#     return context
#
#
# def analyze(value: str, ctx: Mock) -> IdentityResult:
#     return analyze_mac_identity(classify_mac(value), cast(EtherlyzerContext, ctx))
#
#
# def allocation(registry: str) -> SimpleNamespace:
#     return SimpleNamespace(registry=registry)
#
#
# # ---------------------------------------------------------------------------
# # UAA: all four dispatch paths (prefix/address + unicast/mcast), each with/without a matching allocation.
# # ---------------------------------------------------------------------------
#
# @pytest.mark.parametrize(
#     ("value", "lookup", "registry", "expected"),
#     [
#         (
#             "001122", "lookup", "MA-L",
#             (MacIdentity.EUI48_PREFIX, MacResolution.REGISTERED_MAL, MacForm.UAA_PREFIX),
#         ),
#         (
#             "001122", "lookup", None,
#             (MacIdentity.EUI48_PREFIX, MacResolution.NO_INDIVIDUAL_ALLOCATION, MacForm.UAA_PREFIX),
#         ),
#         (
#             "001122334455", "lookup", "MA-L",
#             (MacIdentity.EUI48_CANDIDATE, MacResolution.REGISTERED_MAL, MacForm.UAA_ADDRESS),
#         ),
#         (
#             "001122334455", "lookup", None,
#             (MacIdentity.EUI48_STRUCTURE, MacResolution.NO_REGISTRY_ALLOCATION, MacForm.UAA_ADDRESS),
#         ),
#         (
#             "011122", "lookup_group_allocation", "MA-L",
#             (MacIdentity.GROUP_PREFIX_CANDIDATE, MacResolution.REGISTERED_MAL, MacForm.UAA_PREFIX),
#         ),
#         (
#             "011122", "lookup_group_allocation", None,
#             (MacIdentity.GROUP_PREFIX_STRUCTURE, MacResolution.NO_GROUP_ALLOCATION, MacForm.UAA_PREFIX),
#         ),
#         (
#             "011122334455", "lookup_group_allocation", "MA-L",
#             (MacIdentity.GROUP_ADDRESS_CANDIDATE, MacResolution.REGISTERED_MAL, MacForm.UAA_ADDRESS),
#         ),
#         (
#             "011122334455", "lookup_group_allocation", None,
#             (MacIdentity.GROUP_ADDRESS_STRUCTURE, MacResolution.NO_GROUP_ALLOCATION, MacForm.UAA_ADDRESS),
#         ),
#     ],
#     ids=[
#         "individual-prefix-registered", "individual-prefix-unmatched",
#         "individual-address-registered", "individual-address-unmatched",
#         "group-prefix-registered", "group-prefix-unmatched",
#         "group-address-registered", "group-address-unmatched",
#     ],
# )
# def test_uaa_identity_matrix(
#     value: str,
#     lookup: str,
#     registry: str | None,
#     expected: IdentityResult,
#     ctx: Mock,
# ) -> None:
#     index_lookup = getattr(ctx.indexes.mac, lookup)
#     index_lookup.return_value = allocation(registry) if registry else None
#
#     assert analyze(value, ctx) == expected
#     index_lookup.assert_called_once_with(value)
#
#     unused_lookup = (
#         ctx.indexes.mac.lookup_group_allocation
#         if lookup == "lookup"
#         else ctx.indexes.mac.lookup
#     )
#     unused_lookup.assert_not_called()
#     ctx.indexes.identifier.lookup.assert_not_called()
#
#
# @pytest.mark.parametrize(
#     ("registry", "expected"),
#     [
#         ("MA-L", MacResolution.REGISTERED_MAL),
#         ("MA-M", MacResolution.REGISTERED_MAM),
#         ("MA-S", MacResolution.REGISTERED_MAS),
#         ("IAB", MacResolution.REGISTERED_IAB),
#     ],
# )
# def test_individual_registry_mapping(
#     registry: str, expected: MacResolution, ctx: Mock
# ) -> None:
#     ctx.indexes.mac.lookup.return_value = allocation(registry)
#     assert analyze("001122334455", ctx)[1] == expected
#
#
# @pytest.mark.parametrize(
#     ("registry", "expected"),
#     [
#         ("MA-L", MacResolution.REGISTERED_MAL),
#         ("MA-M", MacResolution.REGISTERED_MAM),
#         ("MA-S", MacResolution.REGISTERED_MAS),
#     ],
# )
# def test_group_registry_mapping(
#     registry: str, expected: MacResolution, ctx: Mock
# ) -> None:
#     # IAB is deliberately excluded: the real group index must filter it.
#     ctx.indexes.mac.lookup_group_allocation.return_value = allocation(registry)
#     assert analyze("011122334455", ctx)[1] == expected
#
#
# def test_unsupported_registry_is_not_silently_accepted(ctx: Mock) -> None:
#     ctx.indexes.mac.lookup.return_value = allocation("UNEXPECTED")
#     with pytest.raises(KeyError, match="UNEXPECTED"):
#         analyze("001122334455", ctx)
#
#
# # ---------------------------------------------------------------------------
# # ELI: individual/group, prefix/complete, registered/unregistered.
# # First octet 0A = individual ELI; 0B = group ELI.
# # Both resolve through the same CID: 0A6791.
# # ---------------------------------------------------------------------------
#
# @pytest.mark.parametrize(
#     ("value", "matched", "expected_type", "expected_kind"),
#     [
#         ("0A6791", True, MacIdentity.ELI_INDIVIDUAL_PREFIX, MacForm.LAA_PREFIX),
#         ("0A6791", False, MacIdentity.ELI_INDIVIDUAL_PREFIX, MacForm.LAA_PREFIX),
#         ("0B6791", True, MacIdentity.ELI_GROUP_PREFIX, MacForm.LAA_PREFIX),
#         ("0B6791", False, MacIdentity.ELI_GROUP_PREFIX, MacForm.LAA_PREFIX),
#         ("0A6791123456", True, MacIdentity.ELI_INDIVIDUAL_CANDIDATE, MacForm.LAA_ADDRESS),
#         ("0A6791123456", False, MacIdentity.ELI_INDIVIDUAL_STRUCTURE, MacForm.LAA_ADDRESS),
#         ("0B6791123456", True, MacIdentity.ELI_GROUP_CANDIDATE, MacForm.LAA_ADDRESS),
#         ("0B6791123456", False, MacIdentity.ELI_GROUP_STRUCTURE, MacForm.LAA_ADDRESS),
#     ],
# )
# def test_eli_identity_and_cid_resolution(
#     value: str,
#     matched: bool,
#     expected_type: MacIdentity,
#     expected_kind: MacForm,
#     ctx: Mock,
# ) -> None:
#     ctx.indexes.identifier.lookup.return_value = object() if matched else None
#
#     assert analyze(value, ctx) == (
#         expected_type,
#         MacResolution.REGISTERED_CID if matched else MacResolution.NO_CID_ALLOCATION,
#         expected_kind,
#     )
#     ctx.indexes.identifier.lookup.assert_called_once_with("0A6791")
#     ctx.indexes.mac.lookup.assert_not_called()
#     ctx.indexes.mac.lookup_group_allocation.assert_not_called()
#
#
# # ---------------------------------------------------------------------------
# # SLAP: AAI/SAI/Reserved, individual/group, prefix/complete.
# # Second hex nibble is 2/3 (AAI), E/F (SAI), 6/7 (Reserved).
# # ---------------------------------------------------------------------------
#
# @pytest.mark.parametrize(
#     ("first_octet", "prefix_type", "address_type", "registration"),
#     [
#         ("02", MacIdentity.AAI_QUADRANT_PREFIX, MacIdentity.AAI_QUADRANT, MacResolution.SLAP_AAI),
#         ("03", MacIdentity.AAI_QUADRANT_PREFIX, MacIdentity.AAI_QUADRANT, MacResolution.SLAP_AAI),
#         ("0E", MacIdentity.SAI_QUADRANT_PREFIX, MacIdentity.SAI_QUADRANT, MacResolution.SLAP_SAI),
#         ("0F", MacIdentity.SAI_QUADRANT_PREFIX, MacIdentity.SAI_QUADRANT, MacResolution.SLAP_SAI),
#         ("06", MacIdentity.RESERVED_QUADRANT_PREFIX, MacIdentity.RESERVED_QUADRANT, MacResolution.SLAP_RESERVED),
#         ("07", MacIdentity.RESERVED_QUADRANT_PREFIX, MacIdentity.RESERVED_QUADRANT, MacResolution.SLAP_RESERVED),
#     ],
# )
# @pytest.mark.parametrize("complete", [False, True], ids=["prefix", "address"])
# def test_non_eli_slap_matrix(
#     first_octet: str,
#     prefix_type: MacIdentity,
#     address_type: MacIdentity,
#     registration: MacResolution,
#     complete: bool,
#     ctx: Mock,
# ) -> None:
#     # First octet plus 4 hex digits = 24-bit prefix;
#     # first octet plus 10 hex digits = complete EUI-length address.
#     value = first_octet + ("0000000001" if complete else "0000")
#
#     assert analyze(value, ctx) == (
#         address_type if complete else prefix_type,
#         registration,
#         MacForm.LAA_ADDRESS if complete else MacForm.LAA_PREFIX,
#     )
#     ctx.indexes.identifier.lookup.assert_not_called()
#     ctx.indexes.mac.lookup.assert_not_called()
#     ctx.indexes.mac.lookup_group_allocation.assert_not_called()
#
#
# # ---------------------------------------------------------------------------
# # Special addresses and precedence.
# # ---------------------------------------------------------------------------
#
# @pytest.mark.parametrize(
#     ("value", "expected"),
#     [
#         (
#             "000000000000",
#             (MacIdentity.ALL_ZERO, MacResolution.IEEE_RA_RESERVED, MacForm.SPECIAL_FIXED_ADDRESS),
#         ),
#         (
#             "FFFFFFFFFFFF",
#             (MacIdentity.BROADCAST, MacResolution.IEEE_8023_DEFINED, MacForm.SPECIAL_FIXED_ADDRESS),
#         ),
#         (
#             "333300",
#             (MacIdentity.IPV6_MULTICAST_PREFIX, MacResolution.IPV6_MULTICAST, MacForm.SPECIAL_PROTOCOL_PREFIX),
#         ),
#     ],
# )
# def test_special_addresses_take_precedence(
#     value: str, expected: IdentityResult, ctx: Mock
# ) -> None:
#     assert analyze(value, ctx) == expected
#     ctx.indexes.mac.lookup.assert_not_called()
#     ctx.indexes.mac.lookup_group_allocation.assert_not_called()
#     ctx.indexes.identifier.lookup.assert_not_called()
#
#
# def test_ipv6_multicast_complete_is_an_address_not_a_prefix(ctx: Mock) -> None:
#     # Expected-to-fail until the production enum/handler defines and uses
#     # SPECIAL_PROTOCOL_ADDRESS for complete IPv6 multicast addresses.
#     result = analyze("333300000001", ctx)
#     assert result[:2] == (MacIdentity.IPV6_MULTICAST, MacResolution.IPV6_MULTICAST)
#     assert result[2].value == "Special (Protocol-Defined Address)"
#
#
# def test_zero_prefix_is_not_the_all_zero_address(ctx: Mock) -> None:
#     ctx.indexes.mac.lookup.return_value = allocation("MA-L")
#     assert analyze("000000", ctx) == (
#         MacIdentity.EUI48_PREFIX,
#         MacResolution.REGISTERED_MAL,
#         MacForm.UAA_PREFIX,
#     )
#
#
# def test_group_lookup_does_not_fall_back_to_individual_lookup(ctx: Mock) -> None:
#     # This tests routing only; the IAB exclusion algorithm belongs to
#     # dedicated tests for the actual MAC allocation index.
#     ctx.indexes.mac.lookup.return_value = allocation("IAB")
#     ctx.indexes.mac.lookup_group_allocation.return_value = None
#     assert analyze("011122334455", ctx) == (
#         MacIdentity.GROUP_ADDRESS_STRUCTURE,
#         MacResolution.NO_GROUP_ALLOCATION,
#         MacForm.UAA_ADDRESS,
#     )
#     ctx.indexes.mac.lookup.assert_not_called()
#     ctx.indexes.mac.lookup_group_allocation.assert_called_once()
#
#
# # ---------------------------------------------------------------------------
# # Normalization is checked independently of whether IEEE allocated a prefix.
# # ---------------------------------------------------------------------------
#
# @pytest.mark.parametrize(
#     "value",
#     ["001122334455", "00:11:22:33:44:55", "00-11-22-33-44-55"],
# )
# def test_normalized_address_is_passed_to_index(value: str, ctx: Mock) -> None:
#     ctx.indexes.mac.lookup.return_value = allocation("MA-L")
#     cmac = classify_mac(value)
#     assert cmac.normalized == "001122334455"
#     assert analyze_mac_identity(cmac, cast(EtherlyzerContext, ctx)) == (
#         MacIdentity.EUI48_CANDIDATE,
#         MacResolution.REGISTERED_MAL,
#         MacForm.UAA_ADDRESS,
#     )
#     ctx.indexes.mac.lookup.assert_called_once_with("001122334455")
#
#
# @pytest.mark.parametrize("first_octet", ["02", "06", "0A", "0E"])
# def test_group_bit_does_not_change_slap_quadrant(first_octet: str) -> None:
#     """I/G changes delivery, not the SLAP quadrant (Y/Z bits)."""
#     group_octet = f"{int(first_octet, 16) ^ 0x01:02X}"
#     individual = classify_mac(first_octet + "0000000001")
#     group = classify_mac(group_octet + "0000000001")
#
#     assert individual.slap_quadrant == group.slap_quadrant
#     assert individual.delivery != group.delivery
#     assert individual.administration == group.administration
