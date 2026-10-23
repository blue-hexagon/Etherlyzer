import argparse


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
