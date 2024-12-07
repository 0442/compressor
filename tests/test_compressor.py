from pathlib import Path
import filecmp

from compressor.file_compressor import FileCompressor
from compressor.compression_methods import LZW, Huffman

from .common import LONG_TEXT_FILE


def test_compressor_roundtrip_lzw(tmp_path: Path):
    method = LZW()

    tmp_compressed = tmp_path / "compressed.lzw"
    tmp_decompressed = tmp_path / "decompressed.txt"

    c = FileCompressor()
    c.compress(str(LONG_TEXT_FILE), str(tmp_compressed), method)

    c.decompress(str(tmp_compressed), str(tmp_decompressed), method)

    assert filecmp.cmp(LONG_TEXT_FILE, tmp_decompressed)


def test_compressor_roundtrip_huffman(tmp_path: Path):
    method = Huffman()

    tmp_compressed = tmp_path / "compressed.huffman"
    tmp_decompressed = tmp_path / "decompressed.txt"

    c = FileCompressor()
    c.compress(str(LONG_TEXT_FILE), str(tmp_compressed), method)

    c.decompress(str(tmp_compressed), str(tmp_decompressed), method)

    assert filecmp.cmp(LONG_TEXT_FILE, tmp_decompressed)
