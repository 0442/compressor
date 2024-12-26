from typing import Callable
import pytest
from io import BytesIO, StringIO
from pathlib import Path

from compressor.compression_methods.lzw import LZW

from ..common import (
    SHORT_TEXT,
    LONG_TEXT_FILE,
    RANDOM_TEXT_FILE,
    REPETITIVE_SENTENCE_TEXT_FILE,
    REPETITIVE_SINGLE_CHAR_TEXT_FILE,
    MEDIUM_SIZE,
    SHORT_SIZE,
    check_roundtrip_integrity,
    check_compression_ratio,
)


@pytest.fixture
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


@pytest.mark.parametrize(
    "test_file",
    [
        (LONG_TEXT_FILE),
        (REPETITIVE_SENTENCE_TEXT_FILE),
        (REPETITIVE_SINGLE_CHAR_TEXT_FILE),
        (RANDOM_TEXT_FILE),
    ],
)
def test_roundtrip(lzw: LZW, tmp_path: Path, test_file: Path):
    assert check_roundtrip_integrity(method=lzw, tmp_path=tmp_path, test_file=test_file)


@pytest.mark.parametrize(
    "test_file, size_limit, ratio_range",
    [
        # Test english input, should be fairly efficient for longer files
        (LONG_TEXT_FILE, SHORT_SIZE, (0.9, 1)),
        (LONG_TEXT_FILE, MEDIUM_SIZE, (0.5, 0.6)),
        (LONG_TEXT_FILE, None, (0.5, 0.6)),
        # Test repetitive input, should be much more efficient than Huffman for both
        (REPETITIVE_SENTENCE_TEXT_FILE, SHORT_SIZE, (0.5, 0.6)),
        (REPETITIVE_SENTENCE_TEXT_FILE, MEDIUM_SIZE, (0, 0.1)),
        (REPETITIVE_SENTENCE_TEXT_FILE, None, (0, 0.1)),
        (REPETITIVE_SINGLE_CHAR_TEXT_FILE, SHORT_SIZE, (0, 0.1)),
        (REPETITIVE_SINGLE_CHAR_TEXT_FILE, MEDIUM_SIZE, (0, 0.1)),
        (REPETITIVE_SINGLE_CHAR_TEXT_FILE, None, (0, 0.1)),
        # Test random input, should be very inefficient, worse than Huffman
        (RANDOM_TEXT_FILE, SHORT_SIZE, (1.4, 1.5)),
        (RANDOM_TEXT_FILE, MEDIUM_SIZE, (0.9, 1)),
        (RANDOM_TEXT_FILE, None, (0.9, 1)),
    ],
)
def test_compression_ratio(
    lzw: LZW,
    tmp_path: Path,
    test_file: Path,
    size_limit: int | None,
    ratio_range: tuple[float, float],
):
    assert check_compression_ratio(
        method=lzw,
        tmp_path=tmp_path,
        size_limit=size_limit,
        test_file_path=test_file,
        ratio_range=ratio_range,
    )
