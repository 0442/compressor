# Coverage report
```
Name                                          Stmts   Miss Branch BrPart  Cover   Missing
-----------------------------------------------------------------------------------------
compressor/__init__.py                            0      0      0      0   100%
compressor/compression_methods/__init__.py        2      0      0      0   100%
compressor/compression_methods/huffman.py       154     17     50      8    86%   52, 56-63, 181, 201, 229, 265, 276, 307, 336, 355-356, 369->371
compressor/compression_methods/interface.py       8      0      0      0   100%
compressor/compression_methods/lzw.py            74      6     30      7    86%   42->47, 51->55, 78, 91, 104, 119-122, 126->129
tests/__init__.py                                 0      0      0      0   100%
tests/huffman/__init__.py                         0      0      0      0   100%
tests/huffman/test_huffman.py                    52      0      0      0   100%
tests/huffman/testing_constants.py                9      0      0      0   100%
tests/lzw/__init__.py                             0      0      0      0   100%
tests/lzw/test_lzw.py                            50      0      0      0   100%
-----------------------------------------------------------------------------------------
TOTAL                                           349     23     80     15    90%
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
* Tested handling of empty inputs for both compression and decompression.
* Tested the combination of compresion and decompression with the short text input `TOBEORNOTTOBEORTOBEORNOT`
* Tested the combination of compression and decompression with a random string of 1000 printable ascii characters. The original text is exactly the same after being compressed and decompressed.

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