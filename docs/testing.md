# Coverage report
```
Name                                             Stmts   Miss Branch BrPart  Cover   Missing
--------------------------------------------------------------------------------------------
compressor/__init__.py                               0      0      0      0   100%
compressor/compression_methods/__init__.py           3      0      0      0   100%
compressor/compression_methods/huffman.py           99      5     24      3    93%   68, 114, 145, 199-200
compressor/compression_methods/huffman_tree.py      91      6     26      3    92%   85, 120, 139-140, 199, 214
compressor/compression_methods/interface.py          8      0      0      0   100%
compressor/compression_methods/lzw.py               74      3     30      4    93%   51->55, 78, 106, 124
compressor/file_compressor.py                       53      4      4      1    91%   55-58, 115->exit
compressor/utils/logging.py                          8      0      0      0   100%
tests/__init__.py                                    0      0      0      0   100%
tests/common.py                                     35      0      4      0   100%
tests/huffman/__init__.py                            0      0      0      0   100%
tests/huffman/constants.py                           9      0      0      0   100%
tests/huffman/test_huffman.py                       48      0      0      0   100%
tests/lzw/__init__.py                                0      0      0      0   100%
tests/lzw/test_lzw.py                               32      0      0      0   100%
tests/test_compressor.py                            62      0      0      0   100%
--------------------------------------------------------------------------------------------
TOTAL                                              522     18     88     11    95%
```

# Description of tests
## Huffman
Tested the following:
* Character frequencies are counted correctly for the example sentence `Hello, world!`.
* Huffman codes are chosen correclty frequencies are counted correctly using a manually constructed Huffman tree from the example sentence `Hello, world!`.
* The Huffman tree is built correctly
  * (tested that the tree is correct in terms of the frequencies, as characters with same freq may change place depending on implementation).
* The whole compression pipeline: the example sentence `Hello, world!` is compressed correctly into binary, including headers, the Huffman code representation of the text, and the Huffman tree.
* The whole decompression pipeline: the compressed format of `Hello, world!` is decompressed correctly into the original text.
* Compression + decompression of ~5MB ASCII text, which results in a perfectly identical to the original one.

## LZW
* Tested handling of empty inputs for both compression and decompression.
* Tested the combination of compresion and decompression with short ASCII text input.
* Compression + decompression of short ASCII text.
* Compression + decompression of ~5MB ASCII text, which results in a perfectly identical file to the original one.

## FileCompressor
* Compression + decompression roundtrip results in a new text file identical to the original one being created
  * With both Huffman and LZW
* Compressing and decompressing with an existing file with the same name as given output destination will throw the proper error and not cause any side-effects to the files
* Compressing and decompressing with a missing input file will throw the proper error and not cause any side-effects to the files
* TODO: proper errors for invalid file formats

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
