from io import BytesIO, StringIO
from random import randint

from compressor.compression_methods import LZW
from compressor.compression_methods.interface import CompressionError

SHORT_TEXT = "TOBEORNOTTOBEORTOBEORNOT"


def test_compression_with_empty_input():
    lzw = LZW()

    i = StringIO()
    o = BytesIO()
    lzw.compress(i, o)
    assert o.getvalue() == b""


def test_decompression_with_empty_input():
    lzw = LZW()

    i = BytesIO(b"\x00")
    o = StringIO()
    lzw.decompress(i, o)
    assert o.getvalue() == ""


def test_compression_with_short_input():
    lzw = LZW()

    i = StringIO(SHORT_TEXT)
    o = BytesIO()
    lzw.compress(i, o)
    assert len(o.getvalue()) > 1


def test_decompression_with_short_input():
    lzw = LZW()

    i = StringIO(SHORT_TEXT)
    o = BytesIO()
    lzw.compress(i, o)

    i = BytesIO(o.getvalue())
    o = StringIO()
    lzw.decompress(i, o)
    assert o.getvalue() == SHORT_TEXT


def test_compression_and_decompression_with_short_input():
    lzw = LZW()

    i = StringIO(SHORT_TEXT)
    o = BytesIO()
    lzw.compress(i, o)

    i = BytesIO(o.getvalue())
    o = StringIO()
    lzw.decompress(i, o)
    assert o.getvalue() == SHORT_TEXT


def test_compression_and_decompression_with_large_input():
    lzw = LZW()

    original = StringIO("".join([chr(randint(0, 255)) for _ in range(10)]))
    o = BytesIO()
    lzw.compress(original, o)

    i = BytesIO(o.getvalue())
    o = StringIO()
    lzw.decompress(i, o)
    assert o.getvalue() == original.getvalue()
