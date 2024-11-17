# Coverage report
```
Name                                          Stmts   Miss Branch BrPart  Cover   Missing
-----------------------------------------------------------------------------------------
compressor/__init__.py                            0      0      0      0   100%
compressor/compression_methods/__init__.py        0      0      0      0   100%
compressor/compression_methods/huffman.py       144     13     44      6    88%   43, 47-54, 169, 184, 203, 216, 231, 286->288
compressor/compression_methods/interface.py       7      0      0      0   100%
tests/__init__.py                                 0      0      0      0   100%
tests/test_huffman_tree.py                       50      0      0      0   100%
-----------------------------------------------------------------------------------------
TOTAL                                           201     13     44      6    91%
```


# Description of tests
## Huffman
Tested the following:
* Character frequencies are counted correctly for the example sentence `Hello, world!`.
* Huffman codes are chosen correclty frequencies are counted correctly using a manually constructed Huffman tree from the example sentence `Hello, world!`.
* The Huffman tree is built correctly
  * (tested that the tree is correct in terms of the frequencies, as characters with same freq may change place depending on implementation).
* The whole compression pipeline; the example sentence `Hello, world!` is compressed correctly into binary, including headers, the Huffman code representation of the text, and the Huffman tree.
* The whole decompression pipeline; the compressed format of `Hello, world!` is decompressed correctly into the original text.
* Tested the combination of compression and decompression with a random string of 1000 printable ascii characters. The original text is exactly the same after being compressed and decompressed.

## LZW
* TODO

# Testing instructions
install and set up the projcect first, see the [installation instructions](/README.md#installation)
## Running the `pytest` tests
Go to project root and run
```
poetry run pytest
```

## Viewing test coverage with `coverage`
```shell
poetry run coverage run --branch -m pytest
poetry run coverage report -m
```