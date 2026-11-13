from __future__ import annotations

import argparse

from etherlyzer.application.analysis.mac_classifier import classify_mac
from etherlyzer.domain.initialize import (
    initialize_etherlyzer,
)
from etherlyzer.domain.registry.family import RegistryFamily
from etherlyzer.presentation.reporting.model import Report
from etherlyzer.presentation.terminal.commands.inspect.branch_ethertype import (
    inspect_ethertype,
)
from etherlyzer.presentation.terminal.commands.inspect.branch_macaddr import (
    mac_inspection_router,
)
from etherlyzer.presentation.terminal.commands.inspect.common import (
    CommonInspectionParams,
    MacInspectionParams,
    TerminalInspectFlags,
)

# from etherlyzer.presentation.terminal.commands.inspect.branch_identifier import inspect_identifier


def validate_inspect_args(args: argparse.Namespace) -> None:
    if args.show_vendor_blocks and args.type != "mac":
        raise argparse.ArgumentError(
            None, "--show-vendor-blocks is only supported for MAC assignments."
        )
    elif args.show_vendor_stats and args.type != "mac":
        raise argparse.ArgumentError(
            None, "--show-vendor-stats is only supported for MAC assignments."
        )
    elif args.show_mac_autopsy and args.type != "mac":
        raise argparse.ArgumentError(
            None, "--show-mac-analysis is only supported for MAC assignments."
        )
    else:
        pass


def dispatch(args: argparse.Namespace) -> int:
    validate_inspect_args(args)
    context = initialize_etherlyzer()
    inspect_flags = TerminalInspectFlags(
        show_mac_autopsy=(args.all or args.show_mac_autopsy),
        show_vendor_stats=(args.all or args.show_vendor_stats),
        show_vendor_blocks=(args.all or args.show_vendor_blocks),
    )

    family = RegistryFamily(args.type)

    match family:
        case RegistryFamily.ETHERTYPE_REGISTRY.value:
            return inspect_ethertype(
                CommonInspectionParams(
                    args=args, context=context, inspect_flags=inspect_flags, report=Report()
                )
            )
        case RegistryFamily.MAC_REGISTRY.value:  # Allows CID lookups
            return mac_inspection_router(
                MacInspectionParams(
                    args=args,
                    context=context,
                    inspect_flags=inspect_flags,
                    classified_mac=classify_mac(args.value),
                    report=Report(),
                )
            )
        case RegistryFamily.IP_UNICAST_REGISTRY:
            raise NotImplementedError()
        case RegistryFamily.IP_MULTICAST_REGISTRY:
            raise NotImplementedError()
        case _:
            print(f"No valid type ({args.type}) selected.")
            return 1
