from bitarray import bitarray

from compressor.compression_methods.huffman import HuffmanTreeNode

TEST_STRING_SHORT = "Hello, world!"

TEST_STRING_SHORT_HUFFMAN_CODES = {
    "l": bitarray("01"),
    "o": bitarray("00"),
    "H": bitarray("1101"),
    "e": bitarray("1100"),
    ",": bitarray("1111"),
    " ": bitarray("1110"),
    "w": bitarray("1001"),
    "r": bitarray("1000"),
    "d": bitarray("1011"),
    "!": bitarray("1010"),
}

TEST_STRING_SHORT_ENCODED_TEXT = bitarray(
    "1101"
    + "1100"
    + "01"
    + "01"
    + "00"
    + "1111"
    + "1110"
    + "1001"
    + "01"
    + "1000"
    + "01"
    + "1011"
).tobytes()

TEST_STRING_SHORT_COMPRESSED = b"\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x1d0001H1 1l0001e1,01!1r001w1d1o\x10\xbeN{v\x80"

HTN = HuffmanTreeNode
# Source for test tree gotten from here: https://huffman-coding-online.vercel.app/
TEST_STRING_SHORT_HUFFMAN_TREE = HTN(
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

TEST_STRING_SHORT_CHAR_FREQS = [
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
