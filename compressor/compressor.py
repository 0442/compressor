from typing import TextIO, BinaryIO
import sys
from time import process_time

from compressor.compression_methods.huffman import CompressionError

from .compression_methods.interface import CompressionMethod


class Compressor:
    """A wrapper around CompressinMethods with added functionality."""

    def compress(
        self, input_path: str, output_path: str, method: CompressionMethod
    ) -> None:
        """
        Reads the given file from input path and writes a new compressed version to output path.
        """
        with open(input_path, "r", encoding="utf-8") as i_file:
            with open(output_path, mode="wb") as o_file:
                try:
                    s = process_time()
                    method.compress(i_file, o_file)
                    print(f"Compression took {process_time() - s:.2f}s")
                except CompressionError as e:
                    print(f"Compressor: {e}.")
                    sys.exit(1)

                self._compare_sizes(i_file, o_file)

    def decompress(
        self, input_path: str, output_path: str, method: CompressionMethod
    ) -> None:
        """
        Reads the given file from input path and writes a new decompressed version to output path.
        """
        # TODO: check that input files exists and not overwriting existing files.
        with open(input_path, "rb") as i_file:
            with open(output_path, mode="w", encoding="utf-8") as o_file:
                try:
                    s = process_time()
                    method.decompress(i_file, o_file)
                    print(f"Compression took {process_time() - s:.2f}s")
                except CompressionError as e:
                    print(f"Compressor: {e}")
                    sys.exit(1)

                self._compare_sizes(o_file, i_file)

    def _compare_sizes(self, decompressed: TextIO, compressed: BinaryIO):
        decomp_size = decompressed.tell()
        comp_size = compressed.tell()

        print(f"Size (decompressed): {decomp_size/1024:.2f} KB")
        print(f"Size (compressed): {comp_size/1024:.2f} KB")
        if decomp_size != 0:
            print(f"Compression ratio: {(comp_size / decomp_size):.3f}")
