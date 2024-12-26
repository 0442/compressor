"""Shared stuff for tests
"""

from filecmp import cmp

from pathlib import Path

from compressor.compression_methods import Huffman, LZW


SHORT_TEXT = "The quick brown fox jumps over the lazy dog."
LONG_TEXT_FILE = Path("tests/large_ascii_eng.txt")
REPETITIVE_SENTENCE_TEXT_FILE = Path("tests/repetitive_ascii.txt")
REPETITIVE_SINGLE_CHAR_TEXT_FILE = Path("tests/single_char_ascii.txt")
RANDOM_TEXT_FILE = Path("tests/random_ascii.txt")

# Size in chars read
SHORT_SIZE = 500
MEDIUM_SIZE = SHORT_SIZE * 1000


def check_compression_ratio(
    method: Huffman | LZW,
    tmp_path: Path,
    test_file_path: Path,
    size_limit: int | None,
    ratio_range: tuple[float, float],
) -> bool:
    """Performs compression and checks if the ratio falls in the given range.

    Args:
        method (Huffman | LZW): the method to use
        tmp_path (Path): path to temporary directory to write temporary files to
        test_file_path (Path): file to use for testing compression
        size_limit (int | None): how many characters to read. If None, whole file is read
    """
    tmp_input_path = tmp_path / "input"
    tmp_output_path = tmp_path / "compressed"

    with open(test_file_path, "r", encoding="ascii") as test_file:
        with open(tmp_input_path, "w", encoding="ascii") as tmp_i:
            tmp_i.write(test_file.read(size_limit or -1))

        original_size = tmp_input_path.stat().st_size

        with open(tmp_input_path, "r", encoding="ascii") as tmp_i:
            with open(tmp_output_path, "wb") as compressed:
                method.compress(tmp_i, compressed)

    compressed_size = tmp_output_path.stat().st_size

    return (
        original_size * ratio_range[0] <= compressed_size
        and compressed_size <= original_size * ratio_range[1]
    )


def check_roundtrip_integrity(
    method: Huffman | LZW, tmp_path: Path, test_file: Path
) -> bool:
    """Does a "roundtrip", i.e. compression and recompression, with the provided method.
    Then compares the original and resulting file, returning the result.

    Args:
        method (Huffman | LZW): method to use for compression and decompression
        tmp_path (Path): temporary dir path for temporary files
        test_file (Path): file to test roundtrip with

    Returns:
        bool: Whether original file is identical to roundtrip file
    """
    tmp_comp_file = tmp_path / "compressed"
    tmp_decomp_file = tmp_path / "decompressed"

    with open(test_file, "r", encoding="ascii") as original:
        with open(tmp_comp_file, "wb") as compressed:
            method.compress(original, compressed)
            compressed.seek(0)

        with open(tmp_comp_file, "rb") as compressed:
            with open(tmp_decomp_file, "w", encoding="ascii") as decompressed:
                method.decompress(compressed, decompressed)
                original.seek(0)
                decompressed.seek(0)

    return cmp(test_file, tmp_decomp_file)
