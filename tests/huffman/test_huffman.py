from pytest import fixture
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
from ..common import LONG_TEXT_FILE


@fixture
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
    tree = h._build_huffman_tree(TEST_STRING_SHORT_CHAR_FREQS)

    def test_tree(test_node: HuffmanTreeNode, correct_node: HuffmanTreeNode):
        assert test_node.freq == correct_node.freq

    test_tree(tree, TEST_STRING_SHORT_HUFFMAN_TREE)


def test_huffman_coding(h: Huffman):
    codes = h._get_codes(TEST_STRING_SHORT_HUFFMAN_TREE)
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


def test_roundtrip_with_large_input(h: Huffman, tmp_path: Path):
    tmp_comp_file = tmp_path / "compressed.huffman"
    tmp_decomp_file = tmp_path / "decompressed.txt"

    with open(LONG_TEXT_FILE, "r", encoding="utf-8") as original:
        with open(tmp_comp_file, "wb") as compressed:
            h.compress(original, compressed)
            compressed.seek(0)

        with open(tmp_comp_file, "rb") as compressed:
            with open(tmp_decomp_file, "w", encoding="utf-8") as decompressed:
                h.decompress(compressed, decompressed)
                original.seek(0)
                decompressed.seek(0)

    assert cmp(LONG_TEXT_FILE, tmp_decomp_file)
