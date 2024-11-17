from io import BytesIO, StringIO
from random import randrange
from string import printable

from compressor.compression_methods.huffman import Huffman, HuffmanTreeNode


def test_frequency_counter():
    h = Huffman()
    test = "Hello, world!"
    a = StringIO(test)
    f = h._count_frequencies(a)
    assert set(f) == set(HELLOWORLD_CHAR_FREQUENCIES)


def test_huffman_tree():
    h = Huffman()

    # Multiple ways to arrange the tree in terms of character position,
    # as characters may have the same frequency.
    # Position of frequencies is important though, so those are tested for.
    tree = h._build_huffman_tree(HELLOWORLD_CHAR_FREQUENCIES)

    def test_tree(test_node: HuffmanTreeNode, correct_node: HuffmanTreeNode):
        assert test_node.freq == correct_node.freq

    test_tree(tree, HELLOWORLD_HUFFMAN_TREE)


def test_huffman_coding():
    h = Huffman()

    codes = h._get_codes(HELLOWORLD_HUFFMAN_TREE)
    assert codes == HELLOWORLD_HUFFMAN_CODES


def test_compression():
    h = Huffman()

    i = StringIO("Hello, world!")
    o = BytesIO()
    h.compress(i, o)
    o.seek(0)
    assert o.read() == HELLOWORLD_COMPRESSED


def test_decompression():
    h = Huffman()

    i = BytesIO(HELLOWORLD_COMPRESSED)
    o = StringIO()
    h.decompress(i, o)
    o.seek(0)
    assert o.read() == "Hello, world!"


def test_compression_and_decompression():
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


HELLOWORLD_COMPRESSED = b"\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x1d0001H1 1l0001e1,01!1r001w1d1o\x10\xbeN{v\x80"

HELLOWORLD_HUFFMAN_CODES = {
    "l": b"01",
    "o": b"00",
    "H": b"1101",
    "e": b"1100",
    ",": b"1111",
    " ": b"1110",
    "w": b"1001",
    "r": b"1000",
    "d": b"1011",
    "!": b"1010",
}

HTN = HuffmanTreeNode
# Source for test tree gotten from here: https://huffman-coding-online.vercel.app/
HELLOWORLD_HUFFMAN_TREE = HTN(
    "olrw!deH",
    13,
    left=HTN("ol", 5, left=HTN("o", 2), right=HTN("l", 3)),
    right=HTN(
        "rw!deH ,",
        8,
        left=HTN(
            "rw!d",
            4,
            left=HTN(
                "rw",
                2,
                left=HTN("r", 1),
                right=HTN("w", 1),
            ),
            right=HTN("!d", 2, left=HTN("!", 1), right=HTN("d", 1)),
        ),
        right=HTN(
            "eH ,",
            4,
            left=HTN("eH", 2, left=HTN("e", 1), right=HTN("H", 1)),
            right=HTN(" ,", 2, left=HTN(" ", 1), right=HTN(",", 1)),
        ),
    ),
)

HELLOWORLD_CHAR_FREQUENCIES = [
    (3, "l"),
    (2, "o"),
    (1, "e"),
    (1, "d"),
    (1, "H"),
    (1, "w"),
    (1, "r"),
    (1, "!"),
    (1, ","),
    (1, " "),
]
