from etherlyzer.presentation.terminal.commands.inspect.common import InspectionParams


def inspect_universal_group(params: InspectionParams) -> None:
    args, context, inspect_flags, _, report = params.to_vars()
    print(context.indexes.ethertype.lookup(args.value))
    print(context.indexes.ethertype.ethertype.items())
    exit(0)
