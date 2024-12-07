from typing import Any, Callable, TextIO, BinaryIO
from os import path
from time import process_time
from functools import wraps
from pathlib import Path

from compressor.compression_methods.interface import CompressionMethodError

from .compression_methods.interface import CompressionMethod


class FileCompressionError(Exception):
    """Represents an error during compression."""


def _command_wrapper(
    func: Callable[[Any, Path, Path, CompressionMethod], None]
) -> Callable[[Any, Path, Path, CompressionMethod], None]:
    """Returns a wrapper for use with both the compression and decompression methods.
    Checks whether output file exists and handles errors.

    Args:
        func (Callable[[Any, str, str, CompressionMethod], None]):
        Either the `compress` or `decompress` method.

    Returns:
        Callable[[Any, str, str, CompressionMethod], None]: the wrapper
    """

    @wraps(func)
    def wrapper(
        self: Any, input_path: Path, output_path: Path, method: CompressionMethod
    ) -> None:
        # Make sure output file does not exist.
        if path.exists(output_path):
            raise FileCompressionError(f"Path '{output_path}' already exists")

        try:
            start = process_time()
            func(self, input_path, output_path, method)
            end = process_time()
            print(f"Compression took {end-start:.2f}s")
        except FileNotFoundError as e:
            raise FileCompressionError(
                f"Input file '{e.filename}' does not exist."
            ) from e
        except CompressionMethodError as e:
            raise FileCompressionError(e) from e

    return wrapper


class FileCompressor:
    """A wrapper around CompressionMethods with added functionality."""

    @_command_wrapper
    def compress(
        self, input_path: Path, output_path: Path, method: CompressionMethod
    ) -> None:
        """Compresses the input file using provided method.

        Args:
            input_path (str): path to the file to be compressed
            output_path (str): path to the file to which compressed data is written to
            method (CompressionMethod): method to be used for compression
        """
        with open(input_path, "r", encoding="utf-8") as i_file:
            with open(output_path, mode="wb") as o_file:
                method.compress(i_file, o_file)
                self._compare_sizes(i_file, o_file)

    @_command_wrapper
    def decompress(
        self, input_path: Path, output_path: Path, method: CompressionMethod
    ) -> None:
        """Decompresses the input file using provided method.

        Args:
            input_path (str): path to the file to be decompressed
            output_path (str): path to the file to which decompressed data is written to
            method (CompressionMethod): method to be used for decompression
        """
        with open(input_path, "rb") as i_file:
            with open(output_path, mode="w", encoding="utf-8") as o_file:
                method.decompress(i_file, o_file)
                self._compare_sizes(o_file, i_file)

    def _compare_sizes(self, decompressed: TextIO, compressed: BinaryIO):
        """Compares the sizes of the compressed and uncompressed data and prints to the terminal.

        Args:
            decompressed (TextIO): The object containing the uncompressed data
            compressed (BinaryIO): The object containing the compressed data
        """
        decomp_size = decompressed.tell()
        comp_size = compressed.tell()

        print(f"Size (decompressed): {decomp_size/1024:.2f} KB")
        print(f"Size (compressed): {comp_size/1024:.2f} KB")
        if decomp_size != 0:
            print(f"Compression ratio: {(comp_size / decomp_size):.3f}")
