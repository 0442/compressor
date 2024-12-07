from argparse import ArgumentParser, Namespace
import sys
from typing import Callable

from compressor.file_compressor import FileCompressionError

from .compression_methods import Huffman, LZW
from .file_compressor import FileCompressor


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


def error_handler(func: Callable[[], None]):
    """Wrapper for use with the `run` function for handling errors."""

    def wrapper():
        try:
            func()
        except FileCompressionError as e:
            print(e)
        except Exception as e:
            print(f"An unexpected error occured: {e}")

    return wrapper


@error_handler
def run() -> None:
    """Run the command line interface for the compressor."""
    methods = {"huffman": Huffman(), "lzw": LZW()}
    file_compressor = FileCompressor()
    args = get_args(list(methods.keys()))

    method = methods.get(args.method, None)

    if not method:
        raise ValueError("Invalid method")

    if not args.input_file:
        raise ValueError("Invalid input file")

    if not args.output_file:
        raise ValueError("Invalid output file")

    if args.command == "compress":
        file_compressor.compress(args.input_file, args.output_file, method)
    elif args.command == "decompress":
        file_compressor.decompress(args.input_file, args.output_file, method)
