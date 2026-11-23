# Command line entry points: help, version and the commands built by later tickets.
import argparse
import sys

from . import __version__


def build_parser():
    parser = argparse.ArgumentParser(
        prog="word_processor",
        description="Local paginated word processor workbench.",
    )
    parser.add_argument("--version", action="version", version=f"word_processor {__version__}")
    sub = parser.add_subparsers(dest="command")
    serve = sub.add_parser("serve", help="run the local app (not implemented yet: see #2)")
    serve.add_argument("--port", type=int, default=8766)
    serve.add_argument("--data-dir", default="./data")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "serve":
        print("not implemented yet: see #2", file=sys.stderr)
        return 1
    parser.print_help()
    return 0
