from typing import Callable
import pytest
from io import BytesIO, StringIO
from pathlib import Path
from filecmp import cmp

from compressor.compression_methods.huffman import Huffman, HuffmanTreeNode

from .constants import (
    TEST_STRING_SHORT,
    TEST_STRING_SHORT_CHAR_FREQS,
    TEST_STRING_SHORT_COMPRESSED,
    TEST_STRING_SHORT_HUFFMAN_TREE,
    TEST_STRING_SHORT_HUFFMAN_CODES,
)
from ..common import (
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
def h():
    return Huffman()


def test_frequency_counter_short_input(h: Huffman):
    a = StringIO(TEST_STRING_SHORT)
    f = h._count_frequencies(a)
    assert set(f) == set(TEST_STRING_SHORT_CHAR_FREQS)


def test_huffman_tree_with_short_input(h: Huffman):
    # Multiple ways to arrange the tree in terms of character position,
    # as characters may have the same frequency.
    # Position of frequencies is important though, so those are tested for.
    tree = HuffmanTreeNode.build_huffman_tree(TEST_STRING_SHORT_CHAR_FREQS)
    assert tree is not None

    def test_tree(test_node: HuffmanTreeNode, correct_node: HuffmanTreeNode):
        assert test_node.freq == correct_node.freq

    test_tree(tree, TEST_STRING_SHORT_HUFFMAN_TREE)


def test_huffman_coding(h: Huffman):
    codes = TEST_STRING_SHORT_HUFFMAN_TREE.get_codes()
    assert codes == TEST_STRING_SHORT_HUFFMAN_CODES


def test_decompression_short_input(h: Huffman):
    i = BytesIO(TEST_STRING_SHORT_COMPRESSED)
    o = StringIO()
    h.decompress(i, o)
    o.seek(0)
    assert o.read() == TEST_STRING_SHORT


def test_compression_short_input(h: Huffman):
    i = StringIO(TEST_STRING_SHORT)
    o = BytesIO()
    h.compress(i, o)
    o.seek(0)
    assert o.read() == TEST_STRING_SHORT_COMPRESSED


def test_compression_empty_input(h: Huffman):
    i = StringIO("")
    o = BytesIO()
    h.compress(i, o)
    o.seek(0)
    assert o.read() == b""


@pytest.mark.parametrize(
    "test_file",
    [
        (LONG_TEXT_FILE),
        (REPETITIVE_SENTENCE_TEXT_FILE),
        (REPETITIVE_SINGLE_CHAR_TEXT_FILE),
        (RANDOM_TEXT_FILE),
    ],
)
def test_roundtrip(h: Huffman, tmp_path: Path, test_file: Path):
    assert check_roundtrip_integrity(method=h, tmp_path=tmp_path, test_file=test_file)


@pytest.mark.parametrize(
    "test_file, size_limit, ratio_range",
    [
        # Test english input, should be fairly efficient for longer files
        (LONG_TEXT_FILE, SHORT_SIZE, (0.8, 0.9)),
        (LONG_TEXT_FILE, MEDIUM_SIZE, (0.5, 0.6)),
        (LONG_TEXT_FILE, None, (0.5, 0.6)),
        # Test repetitive input, should be very efficient for longer files, more so for single char
        (REPETITIVE_SENTENCE_TEXT_FILE, SHORT_SIZE, (0.7, 0.8)),
        (REPETITIVE_SENTENCE_TEXT_FILE, MEDIUM_SIZE, (0.5, 0.6)),
        (REPETITIVE_SENTENCE_TEXT_FILE, None, (0.5, 0.6)),
        (REPETITIVE_SINGLE_CHAR_TEXT_FILE, SHORT_SIZE, (0.1, 0.2)),
        (REPETITIVE_SINGLE_CHAR_TEXT_FILE, MEDIUM_SIZE, (0.1, 0.2)),
        (REPETITIVE_SINGLE_CHAR_TEXT_FILE, None, (0.1, 0.2)),
        # Test random input, should be quite inefficient, better than LZW though
        (RANDOM_TEXT_FILE, SHORT_SIZE, (1.1, 1.2)),
        (RANDOM_TEXT_FILE, MEDIUM_SIZE, (0.7, 0.8)),
        (RANDOM_TEXT_FILE, None, (0.7, 0.8)),
    ],
)
def test_compression_ratio(
    h: Huffman,
    tmp_path: Path,
    test_file: Path,
    size_limit: int | None,
    ratio_range: tuple[float, float],
):
    assert check_compression_ratio(
        method=h,
        tmp_path=tmp_path,
        size_limit=size_limit,
        test_file_path=test_file,
        ratio_range=ratio_range,
    )
