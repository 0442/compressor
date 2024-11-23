from typing import TextIO, BinaryIO, override

from .interface import CompressionMethod, CompressionError


class LZWDict: ...


class LZW(CompressionMethod):
    @override
    def compress(self, text_in: TextIO, bin_out: BinaryIO) -> None:
        raise CompressionError("LZW method not implemented yet.")

    @override
    def decompress(self, bin_in: BinaryIO, text_out: TextIO) -> None:
        raise CompressionError("LZW method not implemented yet.")
