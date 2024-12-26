from typing import TextIO, BinaryIO, override
from bitarray import bitarray

from .interface import CompressionMethod, CompressionMethodError
from .huffman_tree import HuffmanTreeNode

from ..utils.logging import get_logger

logger = get_logger(__name__)


class Huffman(CompressionMethod):
    """Implements the Huffman compression algorithm as a CompressionMethod."""

    def _count_frequencies(self, text: TextIO) -> list[tuple[int, str]]:
        """Count the number of occurences for each character in given input.

        Args:
            text (TextIO): Object containing the text from which to count character frequencies.

        Returns:
            list[tuple[int, str]]: Returns a list of tuples, containing each character's
            frequency and the respective character.
        """
        saved_pointer = text.tell()
        text.seek(0)

        freq_dict: dict[str, int] = {}

        for c in text.read():
            freq_dict[c] = freq_dict.get(c, 0) + 1

        freq_list: list[tuple[int, str]] = []
        for c, f in freq_dict.items():
            freq_list.append((f, c))

        freq_list.sort(reverse=True)

        text.seek(saved_pointer)
        return freq_list

    def _encode_text(
        self, text: TextIO, huffman_codes: dict[str, bitarray | None]
    ) -> bitarray:
        """Encodes the given string using the given huffman codes.

        Args:
            text (TextIO): The text to encode

            huffman_codes (dict[str, bitarray  |  None]):
            The huffman codes to be used for text encoding. Preferably the codes that were
            generated for the same text provided for best compression and no missing codes.

        Raises:
            ValueError: If the provided Huffman tree misses characters used in the given text.

        Returns:
            bitarray: Encoded text.
        """
        saved_pointer = text.tell()
        logger.debug("_encode_text: pointer was at %s", saved_pointer)
        text.seek(0)

        result = bitarray()
        for c in text.read():
            code = huffman_codes[c]
            if code is None:
                raise CompressionMethodError(
                    f"Code for character {c} missing from huffman tree"
                )

            result.extend(code)

        logger.debug("_encode_text: read %s characters", text.tell())
        logger.debug("_encode_text: encoded bitarray len: %s", len(result))
        text.seek(saved_pointer)
        return result

    def _decode_text(
        self, encoded_text: bitarray, huffman_tree: HuffmanTreeNode
    ) -> str:
        """Decompres compressed text using the given Huffman tree.

        Args:
            encoded_text (bitarray): Encoded text to be decoded.
            huffman_tree (HuffmanTreeNode): Huffman tree to be used for decoding the text.

        Returns:
            str: The resulting decoded text.
        """
        result: list[str] = []
        current_node: HuffmanTreeNode = huffman_tree

        for bit in encoded_text:
            # Traverse left/right down the Huffman tree based on bit
            if bit == 0 and current_node.left is not None:
                current_node = current_node.left
            elif bit == 1 and current_node.right is not None:
                current_node = current_node.right

            # If hit a leaf, append that char and reset back to root
            if current_node.left is None and current_node.right is None:
                assert current_node.left is None and current_node.right is None
                result.append(current_node.char)
                current_node = huffman_tree  # Reset to root for next character

        return "".join(result)

    def _decode(self, tree_bytes: bytearray, encoded_text: bitarray) -> str:
        huffman_tree = HuffmanTreeNode.from_bytes(tree_bytes)
        logger.debug("Reconstructed Huffman tree: %s", str(huffman_tree))

        if huffman_tree is None:
            raise ValueError("Invalid tree string")

        decoded_text = self._decode_text(encoded_text, huffman_tree)
        return decoded_text

    def _read_headers(self, bin_in: BinaryIO) -> tuple[int, int]:
        """Reads th headers from a BinaryIO object containing compressed text.

        Args:
            bin_in (BinaryIO): Object from which to read compressed text.

        Raises:
            CompressionMethodError: If compressed content is invalid.

        Returns:
            tuple[int, int]: A tuple containing the length of padding and the tree, in bytes.
        """
        # Header is 16 bytes long, see the compress method for how header is formed.
        header = bin_in.read(16)
        padding_len = int.from_bytes(bytes=header[:8], byteorder="big", signed=False)
        tree_len = int.from_bytes(bytes=header[8:], byteorder="big", signed=False)

        # Check that values are sensible
        # Tree length should be less than remaining length.
        # Padding is to make the length a multiple of 8 so it should be less than 8.
        if (
            padding_len < 0
            or tree_len < 0
            or padding_len >= 8
            or tree_len > len(bin_in.read())
        ):
            raise CompressionMethodError(
                "Invalid header: padding_len or tree_len out of bounds. "
                + "Make sure the file is a valid compressed file."
            )

        # Move pointer back to the start of the tree
        bin_in.seek(16, 0)

        return padding_len, tree_len

    def _create_header(self, encoded_tree: bytearray, encoded_text: bitarray):
        # Prepare the header
        # Info fields are eight byte unsigned integers. The header is therefore 16 bytes long.
        # Also tree length is limited to 2^64, probably sufficient though.
        # Note: consider defining the header params in some constants
        tree_len = len(encoded_tree)
        tree_len_info = tree_len.to_bytes(length=8, byteorder="big", signed=False)

        padding_len_info = encoded_text.padbits.to_bytes(
            length=8, byteorder="big", signed=False
        )

        header = padding_len_info + tree_len_info

        return header

    def _write(
        self,
        tree: HuffmanTreeNode,
        encoded_text: bitarray,
        bin_out: BinaryIO,
    ):
        saved_pointer = bin_out.tell()
        bin_out.seek(0)

        tree_bytes = tree.to_bytes()
        header = self._create_header(tree_bytes, encoded_text)
        bin_out.write(header)
        bin_out.write(tree_bytes)
        bin_out.write(encoded_text.tobytes())

        bin_out.seek(saved_pointer)

    @override
    def compress(self, text_in: TextIO, bin_out: BinaryIO) -> None:
        try:
            freq_list = self._count_frequencies(text_in)
            tree = HuffmanTreeNode.build_huffman_tree(freq_list)
            if tree is None:
                return
            codes = tree.get_codes()
            encoded_text = self._encode_text(text_in, codes)
            self._write(tree, encoded_text, bin_out)

        except UnicodeDecodeError as e:
            raise CompressionMethodError(
                f"Invalid file format. Must be {e.encoding} encoded."
            ) from e

    @override
    def decompress(self, bin_in: BinaryIO, text_out: TextIO) -> None:
        padding_len, tree_len = self._read_headers(bin_in)
        tree_bytes = bytearray(bin_in.read(tree_len))
        encoded_text_bytes = bin_in.read()
        encoded_text_bits = bitarray()
        encoded_text_bits.frombytes(encoded_text_bytes)

        # Remove padding
        if padding_len > 0:
            encoded_text_bits = encoded_text_bits[:-padding_len]
        decoded_text = self._decode(tree_bytes, encoded_text_bits)
        text_out.write(decoded_text)
