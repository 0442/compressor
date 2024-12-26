from heapq import heappop, heappush
from typing import override, Literal
from bitarray import bitarray

from .interface import CompressionMethodError

from ..utils.logging import get_logger

logger = get_logger(__name__)


# Note: for a more efficient implementation, should just skip this
# abstract representation of a Huffman tree and build the tree
# direclty as bytes. But this is maybe more verbose/explicit, maybe
# readable, though it is a lot longer.
# Could perhaps implement separately a "FastHuffman" CompressionMethod.
class HuffmanTreeNode:
    """Represents a node in a huffman tree"""

    TREE_TEXT_ENCODING: Literal["ascii"] = "ascii"

    def __init__(
        self,
        char: str,
        freq: int,
        left: "HuffmanTreeNode | None" = None,
        right: "HuffmanTreeNode | None" = None,
    ) -> None:
        """
        Args:
            char (str): Character (if leaf node) or multiple characters which this node represents.
            freq (int): The frequency of occurences of this character (if leaf node), or the sum
            of the child nodes' characters' frequencies.
            left (HuffmanTreeNode | None, optional): The left node with the smaller frequency,
            or None. Defaults to None.
            right (HuffmanTreeNode | None, optional): The right node with the higher frequency,
            or None. Defaults to None.
        """

        self.left: "HuffmanTreeNode | None" = left
        self.right: "HuffmanTreeNode | None" = right
        self.freq: int = freq
        self.char: str = char
        self.code: bitarray = bitarray()

    def _code_tree(self, code: bitarray | None = None) -> None:
        """Assign binary codes to self and recursively to every child node in the tree.

        Args:
            code (bitarray | None, optional): The code to assign to this node. Defaults to None.
        """
        code = code or bitarray()
        self.code = code

        if self.left and self.right:
            self.left._code_tree(code + [1])
            self.right._code_tree(code + [0])

        # If the tree is just a single node, i.e. input text consisted only of a single char,
        # then the code will be empty here.
        # Here we check for that by checking that this is a root(has no code) and
        # a leaf(has no children),  i.e. that this is the only node.
        # Then we assign it a code as just 1 or 0 as its code.
        if len(self.code) == 0 and self.left is None and self.right is None:
            self.code = bitarray([1])

    # Byte representation currently implemented by just using unicode chars.
    # Could be more efficient with just bits, but in large files the tree's
    # size is often insignificant.
    def to_bytes(self) -> bytearray:
        """Turn the Huffman tree into a bytes.

        Args:
            huffman_tree (HuffmanTreeNode): The Huffman tree to encode.

        Returns:
            bytearray: The Huffman tree in a byte format.
        """

        result = bytearray()

        def tree_to_bytes(node: HuffmanTreeNode, tree_bytes: bytearray) -> None:
            # Either node is a leaf or it has two children. If not, something has gone wrong.
            if (node.left is None and node.right) or (node.left and node.right is None):
                raise ValueError(
                    "Broken Huffman tree: tree has a node with a single child."
                )

            # If node is a leaf. 'and' should be sufficient, but for static type checking 'or' used.
            if node.left is None or node.right is None:
                tree_bytes.extend(b"1")
                tree_bytes.extend(node.char.encode(HuffmanTreeNode.TREE_TEXT_ENCODING))
                return

            tree_bytes.extend(b"0")
            tree_to_bytes(node.left, tree_bytes)
            tree_to_bytes(node.right, tree_bytes)

        tree_to_bytes(self, result)
        logger.debug("to_bytes: huffman tree bytearray len: %s", len(result))
        return result

    @staticmethod
    def from_bytes(tree_bytes: bytearray) -> "HuffmanTreeNode | None":
        """Reconstruct an encoded/compressed Huffman tree
        into a HuffmanTreeNode object.

        Args:
            tree (bytearray): The encoded tree.

        Returns:
            HuffmanTreeNode | None: The reconstructed Huffman tree, or None,
            if the tree does not exist.
        """

        def reconstruct_tree(
            tree_bytes: bytearray,
        ) -> tuple[HuffmanTreeNode | None, bytearray]:
            if not tree_bytes:
                return None, tree_bytes

            cur_char = str(
                tree_bytes[0].to_bytes(), encoding=HuffmanTreeNode.TREE_TEXT_ENCODING
            )

            if cur_char == "1":
                next_char = str(
                    tree_bytes[1].to_bytes(),
                    encoding=HuffmanTreeNode.TREE_TEXT_ENCODING,
                )
                return HuffmanTreeNode(next_char, 0), tree_bytes[2:]

            left, tree_bytes = reconstruct_tree(tree_bytes[1:])
            right, tree_bytes = reconstruct_tree(tree_bytes)
            return HuffmanTreeNode("", 0, left, right), tree_bytes

        try:
            tree, _remaining = reconstruct_tree(tree_bytes)
        except UnicodeDecodeError as e:
            raise CompressionMethodError(
                f"Error reading Huffman tree: invalid format, should be {e.encoding}"
            ) from e

        return tree

    @staticmethod
    def build_huffman_tree(
        freq_list: list[tuple[int, str]]
    ) -> "HuffmanTreeNode | None":
        """Constructs a huffman tree from a list of tuples,
        containing a character and its frequency, ordered by the frequencies.

        Args:
            freq_list (list[tuple[int, str]]): list of tuples, containing
            the frequency and the character.

        Returns:
            HuffmanTreeNode | None: The huffman tree built, or None,
            if no characters given in freq_list.
        """
        if len(freq_list) == 0:
            return None

        nodes: list[HuffmanTreeNode] = []

        # Init forest with single node "trees"
        for freq, char in freq_list:
            heappush(nodes, HuffmanTreeNode(char, freq, None, None))

        # Merge trees until only one tree is left, i.e. the huffman tree.
        # Trees are merged by taking the two trees with the smallest
        # frequencies and merging them into one tree.
        while len(nodes) >= 2:
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

    def get_codes(self) -> dict[str, bitarray | None]:
        """Compute the Huffman codes for each character in this tree.

        Returns:
            dict[str, bitarray | None]: the codes
        """
        self._code_tree()

        codes: dict[str, bitarray | None] = {}

        def traverse(node: HuffmanTreeNode, code: bitarray):
            if code is None:
                code = bitarray()

            if node.left and node.right:
                traverse(node.left, code + [0])
                traverse(node.right, code + [1])
            else:  # If leaf node, assign code and stop traversing
                codes[node.char] = code

        traverse(self, self.code)
        return codes

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
