# from __future__ import annotations
#
# import argparse
# from pathlib import Path
#
#
#
# def run(args):
#
#     entries = Lookup.lookup_bulk(
#         infile=Path(args.file),
#     )
#
#     for entry in entries:
#         print(
#             entry.registry,
#             entry.assignment,
#             entry.organization_name,
#             sep="\t",
#         )
#
#     return 0
#
#
# def register(subparsers):
#
#     parser = subparsers.add_parser(
#         "bulk",
#         help="Bulk lookup",
#     )
#
#     parser.add_argument(
#         "file",
#         help="Input file",
#     )
#
#     parser.set_defaults(func=run)