import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Callable

from compressor.file_compressor import FileCompressionError

from .compression_methods import Huffman, LZW
from .file_compressor import FileCompressor

from .utils.logging import LOGFILE, get_logger

logger = get_logger(__name__)


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
    cmd_parser.add_parser(
        name="compress",
        help="Compress a file",
    )
    cmd_parser.add_parser(
        name="decompress",
        help="Decompress a file",
    )
    arg_parser.add_argument(dest="method", type=str, choices=methods)
    arg_parser.add_argument(dest="input_file", type=str)
    arg_parser.add_argument(dest="output_file", type=str)

    args = arg_parser.parse_args()

    return args


def error_handler(run_func: Callable[[], None]):
    """Decorator for use with the cli `run` function for handling errors."""

    def wrapper():
        try:
            return run_func()
        except FileCompressionError as e:
            logger.error("Compression failed: %s", e)
            print("Compression failed:", e)
            logger.exception(e)
        except KeyboardInterrupt as e:
            logger.error("Compression canceled by user")
            print("Compression canceled")
            logger.exception(e)
        except Exception as e:
            logger.critical("An unexpected error occured: %s", e)
            print(f"An unexpected error occured: {e}")
            print(f"See '{LOGFILE}' for more details.")
            logger.exception(e)

        sys.exit(1)

    return wrapper


@error_handler
def run() -> None:
    """Run the command line interface for the compressor."""
    methods = {"huffman": Huffman(), "lzw": LZW()}
    args = get_args(list(methods.keys()))

    method = methods.get(args.method, None)

    if not (method and args.input_file and args.output_file and args.command):
        raise ValueError("Invalid args")

    file_compressor = FileCompressor()
    input_path = Path(args.input_file)
    output_path = Path(args.output_file)

    if args.command == "compress":
        file_compressor.compress(input_path, output_path, method)
    elif args.command == "decompress":
        file_compressor.decompress(input_path, output_path, method)
