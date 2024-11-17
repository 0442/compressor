from typing import TextIO, BinaryIO, override
from heapq import heappop, heappush

from .interface import CompressionMethod


class HuffmanTreeNode:
    """Represents a node in a huffman tree"""

    def __init__(
        self,
        char: str,
        freq: int,
        left: "HuffmanTreeNode | None" = None,
        right: "HuffmanTreeNode | None" = None,
    ) -> None:
        """
        Parameters
        ----------
        char : str
            Character (if leaf node) or multiple characters which this node represents.
        freq : int
            The frequency of occurences of this character (if leaf node), or the sum of the child nodes' characters' frequencies
        left : HuffmanTreeNode | None
            The left node with the smaller frequency, or None
        right : HuffmanTreeNode | None
            The right node with the higher frequency, or None
        """
        self.left = left
        self.right = right
        self.freq = freq
        self.char = char
        self.code = None

    def code_tree(self, code: bytes | None = None) -> None:
        """Assign binary codes to self and recursively to every child node in the tree."""
        if code is None:
            self.code = b"1"
        else:
            self.code = code

        if self.left and self.right:
            self.left.code_tree(self.code + b"0")
            self.right.code_tree(self.code + b"1")

    def __lt__(self, other: "HuffmanTreeNode") -> bool:
        return self.freq < other.freq

    def __le__(self, other: "HuffmanTreeNode") -> bool:
        return self.freq <= other.freq

    @override
    def __str__(self, indent: str = "") -> str:
        output: str = f"{indent} ({self.char} {self.freq} {self.code})"
        indent += 4 * " "
        if self.left:
            output += "\n" + self.left.__str__(indent)
        if self.right:
            output += "\n" + self.right.__str__(indent)

        return output


class Huffman(CompressionMethod):
    """Implements the Huffman compression algorithm as a CompressionMethod."""

    def _build_huffman_tree(self, freq_list: list[tuple[int, str]]) -> HuffmanTreeNode:
        """
        Constructs a huffman tree from a list of tuples,
        containing a character and its frequency, ordered by the frequencies.
        """
        nodes: list[HuffmanTreeNode] = []

        # Init forest with single node "trees"
        for freq, char in freq_list:
            heappush(nodes, HuffmanTreeNode(char, freq, None, None))

        # Merge trees until only one tree is left, i.e. the huffman tree.
        # Trees are merged by taking the two trees with the smallest frequencies and merging them into one tree.
        while len(nodes) > 1:
            # Left popped first as it is smaller than right in huffman tree
            left, right = heappop(nodes), heappop(nodes)
            heappush(
                nodes,
                HuffmanTreeNode(
                    left.char + right.char, left.freq + right.freq, left, right
                ),
            )

        huffman_tree = heappop(nodes)

        return huffman_tree

    def _count_frequencies(self, text: TextIO) -> list[tuple[int, str]]:
        """Count the number of occurences for each character in given input.
        Parameters
        ----------
        text : TextIO
          TextIO object containing the text from which to count character frequencies.
        """
        freq_dict: dict[str, int] = {}

        for c in text.read():
            freq_dict[c] = freq_dict.get(c, 0) + 1

        freq_list: list[tuple[int, str]] = []
        for c, f in freq_dict.items():
            freq_list.append((f, c))

        freq_list.sort(reverse=True)

        return freq_list

    def _get_codes(self, huffman_tree: HuffmanTreeNode) -> dict[str, bytearray]:
        """Compute the huffman codes for each character in the given Huffman tree.
        Parameters
        ----------
        huffman_tree : HuffmanTreeNode
          The huffman tree based on which to construct Huffman codes.
        """
        huffman_tree.code_tree()

        codes: dict[str, bytearray] = {}

        def traverse(node: HuffmanTreeNode, code: bytearray):
            if node.left and node.right:
                traverse(node.left, code + b"0")
                traverse(node.right, code + b"1")
            else:
                codes[node.char] = code

        traverse(huffman_tree, bytearray())
        return codes

    def _encode_text(
        self, text: TextIO, huffman_codes: dict[str, bytearray]
    ) -> bytearray:
        """
        Encodes the given string using the given huffman codes.

        Parameters
        ----------
        text : TextIO
          The text to encode
        huffman_codes : dict[str, bytearray]
          The huffman codes to be used for the text encoding.
          Preferably the codes that were generated for the same
          text provided for best compression and no missing codes.
        """
        result = bytearray()
        c = text.read(1)
        while c:
            result.extend(huffman_codes[c])
            c = text.read(1)

        return result

    def _encode_tree(self, huffman_tree: HuffmanTreeNode) -> bytes:
        """Compress the Huffman tree by encoding it into a byte format."""

        def encode_tree(node: HuffmanTreeNode) -> bytes:
            assert (not node.left and not node.right) or (node.left and node.right)

            if node.left is None or node.right is None:
                return b"1" + node.char.encode("utf-8")
            else:
                return b"0" + encode_tree(node.left) + encode_tree(node.right)

        return encode_tree(huffman_tree)

    def _decode_tree(self, tree_str: str) -> HuffmanTreeNode | None:
        """Decompress an encoded/compressed Huffman tree (by _encode_tree), into a HuffmanTreeNode object."""

        def decode_tree(
            tree_str: str, depth: int = 0
        ) -> tuple[HuffmanTreeNode | None, str]:
            if not tree_str:
                return None, tree_str

            if tree_str[0] == "1":
                char = tree_str[1]
                # print(f"{'  ' * depth}Leaf: {char}")
                return HuffmanTreeNode(char, 0), tree_str[2:]
            else:
                # print(f"{'  ' * depth}Internal Node")
                left, tree_str = decode_tree(tree_str[1:], depth + 1)
                right, tree_str = decode_tree(tree_str, depth + 1)
                return HuffmanTreeNode("", 0, left, right), tree_str

        tree, remaining = decode_tree(tree_str)
        if remaining:
            # print(f"Warning: Unused tree string: {remaining}")
            pass

        return tree

    def _decode_text(self, encoded_text: str, huffman_tree: HuffmanTreeNode) -> str:
        """Decompres compressed text using the given Huffman tree."""
        result: list[str] = []
        current_node = huffman_tree

        for i, bit in enumerate(encoded_text):
            # print(f"Bit {i}: {bit}, Current node: {'Leaf' if current_node.left is None and current_node.right is None else 'Internal'}")

            if bit == "0":
                current_node = current_node.left
            else:
                current_node = current_node.right

            if current_node is None:
                break

            if current_node.left is None and current_node.right is None:  # Leaf node
                result.append(current_node.char)
                # print(f"Found leaf node: {current_node.char}")
                current_node = huffman_tree  # Reset to root for next character

        return "".join(result)

    def decode(self, tree_str: str, encoded_text: str) -> str:
        huffman_tree = self._decode_tree(tree_str)
        if huffman_tree is None:
            raise ValueError("Invalid tree string")
        # print(f"Tree string: {tree_str}")
        # print(f"Encoded text (first 50 bits): {encoded_text[:50]}")
        decoded_text = self._decode_text(encoded_text, huffman_tree)
        return decoded_text

    def _read_headers(self, bin_in: BinaryIO) -> tuple[int, int]:
        header = bin_in.read(16)
        padding_len, tree_len = int(header[:8].hex(), 16), int(header[8:].hex(), 16)

        # Check that values are sensible
        # Tree length should be less than remaining length.
        # Padding is to make the length a multiple of 8 so it should be less than 8.
        if (
            padding_len < 0
            or tree_len < 0
            or padding_len >= 8
            or tree_len > len(bin_in.read())
        ):
            raise ValueError(
                "Invalid header: padding_len or tree_len out of bounds. "
                + "Make sure the file is a valid compressed file."
            )

        # Move pointer back to the start of the tree
        _ = bin_in.seek(16, 0)

        return padding_len, tree_len

    # Interface methods

    # Note: to allow more memory-efficient handling of larger files, might want to consider using generators in some places.
    @override
    def compress(self, text_in: TextIO, bin_out: BinaryIO) -> None:
        _ = text_in.seek(0)
        freq_list = self._count_frequencies(text_in)
        _ = text_in.seek(0)
        tree = self._build_huffman_tree(freq_list)
        codes = self._get_codes(tree)

        encoded_text = self._encode_text(text_in, codes)
        encoded_tree = self._encode_tree(tree)

        # Convert encoded_text from a string of '0's and '1's to bytes
        encoded_text_bytes = bytearray()
        for i in range(0, len(encoded_text), 8):
            byte = encoded_text[i : i + 8].ljust(8, b"0")
            encoded_text_bytes.append(int(byte, 2))

        # Calculate padding
        padding_len = (8 - len(encoded_text) % 8) % 8

        # Prepare header
        # info fields are eight byte integers
        padding_len_info = padding_len.to_bytes(8, "big")
        tree_len_info = len(encoded_tree).to_bytes(8, "big")
        header = padding_len_info + tree_len_info
        print(len(encoded_tree))

        result = header + encoded_tree + bytes(encoded_text_bytes)

        _ = bin_out.write(result)

    @override
    def decompress(self, bin_in: BinaryIO, text_out: TextIO) -> None:
        padding_len, tree_len = self._read_headers(bin_in)
        tree_str = bin_in.read(tree_len).decode("utf-8")
        encoded_text_bytes = bin_in.read()

        # Convert encoded_text back to a string of '0's and '1's
        bit_string = "".join([bin(byte)[2:].zfill(8) for byte in encoded_text_bytes])

        # Remove padding
        if padding_len > 0:
            bit_string = bit_string[:-padding_len]
        encoded_text = bit_string

        decoded_text = self.decode(tree_str, encoded_text)
        _ = text_out.write(decoded_text)
