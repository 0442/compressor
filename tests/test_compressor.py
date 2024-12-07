from pathlib import Path
import filecmp
from os import path
from pytest import fixture, raises

from compressor.file_compressor import FileCompressor, FileCompressionError
from compressor.compression_methods import LZW, Huffman

from .common import LONG_TEXT_FILE


@fixture
def fc():
    return FileCompressor()


def test_file_compressor_roundtrip_lzw(tmp_path: Path, fc: FileCompressor):
    method = LZW()

    tmp_compressed = tmp_path / "compressed.lzw"
    tmp_decompressed = tmp_path / "decompressed.txt"

    fc = FileCompressor()
    fc.compress(str(LONG_TEXT_FILE), str(tmp_compressed), method)

    fc.decompress(str(tmp_compressed), str(tmp_decompressed), method)

    assert filecmp.cmp(LONG_TEXT_FILE, tmp_decompressed)


def test_file_compressor_roundtrip_huffman(tmp_path: Path, fc: FileCompressor):
    method = Huffman()

    tmp_compressed = tmp_path / "compressed.huffman"
    tmp_decompressed = tmp_path / "decompressed.txt"

    fc.compress(str(LONG_TEXT_FILE), str(tmp_compressed), method)

    fc.decompress(str(tmp_compressed), str(tmp_decompressed), method)

    assert filecmp.cmp(LONG_TEXT_FILE, tmp_decompressed)


def test_file_compressor_output_file_exists(tmp_path: Path, fc: FileCompressor):
    o_file_contents = "output file contents that should not be affected"
    i_file_contents = "input file contents that should not be affected"

    o_file = tmp_path / "o_file"
    i_file = tmp_path / "i_file"

    # Write some valid text content for both files
    with open(o_file, "w", encoding="ascii") as o:
        with open(i_file, "w", encoding="ascii") as i:
            i.write(i_file_contents)

        o.write(o_file_contents)

    # Both compression methods should throw an error saying the file already exists
    h = Huffman()
    with raises(FileCompressionError, match="already exists"):
        fc.compress(str(i_file), str(o_file), h)

    lzw = LZW()
    with raises(FileCompressionError, match="already exists"):
        fc.compress(str(i_file), str(o_file), lzw)

    # Make sure the contents were not affected
    with open(o_file, "r", encoding="ascii") as o:
        assert o.read() == o_file_contents

    with open(i_file, "r", encoding="ascii") as i:
        assert i.read() == i_file_contents


def test_file_compressor_input_file_not_exists(tmp_path: Path, fc: FileCompressor):
    o_file = tmp_path / "o_file"
    i_file = tmp_path / "i_file"

    h = Huffman()
    with raises(FileCompressionError, match="^Input file '.*' does not exist.$"):
        fc.compress(str(i_file), str(o_file), h)

    lzw = LZW()
    with raises(FileCompressionError, match="^Input file '.*' does not exist.$"):
        fc.compress(str(i_file), str(o_file), lzw)

    # Make sure neither file was created
    assert not path.exists(i_file)
    assert not path.exists(o_file)
