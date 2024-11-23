from argparse import ArgumentParser, Namespace
import sys

from .compression_methods import Huffman, LZW
from .compressor import Compressor


def get_args(methods: list[str]) -> Namespace:
    """Setup argparser and return Namespace object with the arguments.

    Args:
        methods (list[str]): List of the compression methods available.

    Returns:
        Namespace: Namespace from argparser containing the args.
    """
    arg_parser = ArgumentParser()

    cmd_parser = arg_parser.add_subparsers(
        dest="command", metavar="command", required=True
    )
    _ = cmd_parser.add_parser(
        name="compress",
        help="Compress a file",
    )
    _ = cmd_parser.add_parser(
        name="decompress",
        help="Decompress a file",
    )
    _ = arg_parser.add_argument(dest="method", type=str, choices=methods)
    _ = arg_parser.add_argument(dest="input_file", type=str)
    _ = arg_parser.add_argument(dest="output_file", type=str)

    args = arg_parser.parse_args()

    return args


def run() -> None:
    """Run the command line interface for the compressor."""
    methods = {"huffman": Huffman(), "lzw": LZW()}
    compressor = Compressor()
    args = get_args(list(methods.keys()))

    method = methods.get(args.method, None)

    if not method:
        print("Invalid method")
        sys.exit(1)

    if not args.input_file:
        print("Invalid input file")
        sys.exit(1)

    if not args.output_file:
        print("Invalid output file")
        sys.exit(1)

    if args.command == "compress":
        compressor.compress(args.input_file, args.output_file, method)
    elif args.command == "decompress":
        compressor.decompress(args.input_file, args.output_file, method)
