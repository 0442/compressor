from abc import ABC, abstractmethod
from typing import TextIO, BinaryIO


class CompressionError(Exception):
    """Represents an error during compression."""


class CompressionMethod(ABC):
    """ABC defining an interface for different text compression methods."""

    @abstractmethod
    def compress(self, text_in: TextIO, bin_out: BinaryIO) -> None:
        """Compresses text from text_in into bin_out.

        Args:
            text_in (TextIO): TextIO object from which compressable text data is read.
            bin_out (BinaryIO): BinaryIO object to which compressed output is written to.
        """

    @abstractmethod
    def decompress(self, bin_in: BinaryIO, text_out: TextIO) -> None:
        """Compresses compressed text from bin_in into text_out.

        Args:
            bin_in (BinaryIO): BinaryIO object from which compressed data is read.
            text_out (TextIO): TextIO object to which decompressed text output is written to.
        """
