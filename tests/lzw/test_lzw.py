from pytest import fixture
from io import BytesIO, StringIO
from pathlib import Path
from filecmp import cmp

from compressor.compression_methods.lzw import LZW

from ..common import SHORT_TEXT, LONG_TEXT_FILE


@fixture
def lzw():
    return LZW()


def test_compression_empty_input(lzw: LZW):
    i = StringIO()
    o = BytesIO()
    lzw.compress(i, o)
    assert o.getvalue() == b""


def test_decompression_empty_input(lzw: LZW):
    lzw = LZW()

    i = BytesIO(b"\x00")
    o = StringIO()
    lzw.decompress(i, o)
    assert o.getvalue() == ""


def test_compression_short_input(lzw: LZW):
    lzw = LZW()

    i = StringIO(SHORT_TEXT)
    o = BytesIO()
    lzw.compress(i, o)
    # TODO: needs more rigorous checks.
    assert len(o.getvalue()) > 1


def test_roundtrip_short_input(lzw: LZW):
    lzw = LZW()

    i = StringIO(SHORT_TEXT)
    o = BytesIO()
    lzw.compress(i, o)

    i = BytesIO(o.getvalue())
    o = StringIO()
    lzw.decompress(i, o)
    assert o.getvalue() == SHORT_TEXT


def test_roundtrip_with_large_input(lzw: LZW, tmp_path: Path):
    tmp_comp_file = tmp_path / "compressed.lzw"
    tmp_decomp_file = tmp_path / "decompressed.txt"

    with open(LONG_TEXT_FILE, "r", encoding="utf-8") as original:
        with open(tmp_comp_file, "wb") as compressed:
            lzw.compress(original, compressed)
            compressed.seek(0)

        with open(tmp_comp_file, "rb") as compressed:
            with open(tmp_decomp_file, "w", encoding="utf-8") as decompressed:
                lzw.decompress(compressed, decompressed)
                original.seek(0)
                decompressed.seek(0)

    assert cmp(LONG_TEXT_FILE, tmp_decomp_file)
