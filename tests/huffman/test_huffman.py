from io import BytesIO, StringIO
from random import randrange
from string import printable

from compressor.compression_methods.huffman import Huffman, HuffmanTreeNode

from .testing_constants import (
    TEST_STRING_SHORT,
    TEST_STRING_SHORT_CHAR_FREQS,
    TEST_STRING_SHORT_COMPRESSED,
    TEST_STRING_SHORT_HUFFMAN_TREE,
    TEST_STRING_SHORT_HUFFMAN_CODES,
)


def test_decompression_with_short_input():
    h = Huffman()

    i = BytesIO(TEST_STRING_SHORT_COMPRESSED)
    o = StringIO()
    h.decompress(i, o)
    o.seek(0)
    assert o.read() == TEST_STRING_SHORT


def test_frequency_counter_with_short_input():
    h = Huffman()
    a = StringIO(TEST_STRING_SHORT)
    f = h._count_frequencies(a)
    assert set(f) == set(TEST_STRING_SHORT_CHAR_FREQS)


def test_huffman_tree_building_with_short_input():
    h = Huffman()

    # Multiple ways to arrange the tree in terms of character position,
    # as characters may have the same frequency.
    # Position of frequencies is important though, so those are tested for.
    tree = h._build_huffman_tree(TEST_STRING_SHORT_CHAR_FREQS)

    def test_tree(test_node: HuffmanTreeNode, correct_node: HuffmanTreeNode):
        assert test_node.freq == correct_node.freq

    test_tree(tree, TEST_STRING_SHORT_HUFFMAN_TREE)


def test_huffman_coding():
    h = Huffman()

    codes = h._get_codes(TEST_STRING_SHORT_HUFFMAN_TREE)
    assert codes == TEST_STRING_SHORT_HUFFMAN_CODES


def test_compression_with_short_input():
    h = Huffman()

    i = StringIO(TEST_STRING_SHORT)
    o = BytesIO()
    h.compress(i, o)
    o.seek(0)
    assert o.read() == TEST_STRING_SHORT_COMPRESSED


def test_compression_with_empty_input():
    h = Huffman()

    i = StringIO("")
    o = BytesIO()
    h.compress(i, o)
    o.seek(0)
    assert o.read() == b""


def test_compression_and_decompression_with_short_input():
    h = Huffman()
    original = StringIO(
        "".join([printable[randrange(0, len(printable))] for _ in range(1000)])
    )
    compressed = BytesIO()
    result = StringIO()

    h.compress(original, compressed)
    compressed.seek(0)
    original.seek(0)
    h.decompress(compressed, result)
    result.seek(0)

    assert result.read() == original.read()
