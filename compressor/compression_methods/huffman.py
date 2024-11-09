from typing import TextIO, BinaryIO, override
from heapq import heappop, heappush

from .interface import CompressionMethod

class HuffmanTreeNode:
  """Represents a node in a huffman tree"""
  def __init__(self, char: str, freq: int, left: 'HuffmanTreeNode | None' = None, right: 'HuffmanTreeNode | None' = None) -> None:
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

  def __lt__(self, other: 'HuffmanTreeNode') -> bool:
    return self.freq < other.freq
  
  def __le__(self, other: 'HuffmanTreeNode') -> bool:
    return self.freq <= other.freq


class Huffman(CompressionMethod):
  """Implements the Huffman compression algorithm as a CompressionMethod."""

  def _build_huffman_tree(self, freq_list: list[tuple[int,str]]) -> HuffmanTreeNode:
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
      heappush(nodes, HuffmanTreeNode(
        left.char + right.char,
        left.freq + right.freq,
        left,
        right
      ))

    huffman_tree = heappop(nodes)

    return huffman_tree
  
  def _count_frequencies(self, text: TextIO) -> list[tuple[int, str]]:
    freq_dict: dict[str, int] = {}

    for c in text.read():
      freq_dict[c] = freq_dict.get(c, 0) + 1

    freq_list: list[tuple[int, str]] = []
    for c, f in freq_dict.items():
      freq_list.append((f,c))
    
    freq_list.sort(reverse=True)

    return freq_list

  @override
  def compress(self, input: TextIO, otuput: BinaryIO) -> None:
    freq_list = self._count_frequencies(input)
    _tree = self._build_huffman_tree(freq_list)
    ...
  
  @override
  def uncompress(self, input: BinaryIO, output: TextIO) -> None:
    pass
