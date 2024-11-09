from ..compression_methods.huffman import Huffman
from io import StringIO

def test_frequency_counter():
  h = Huffman()
  test = "Hello, world!"
  a = StringIO(test)
  f = h._count_frequencies(a)
  assert set(f) == set([
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
  ])
