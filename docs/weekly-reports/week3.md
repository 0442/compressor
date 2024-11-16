# Week 2 Report

Hours Spent: ~6

## Progress of the program

- Continued the implementation of Huffman and the rest of the program.
- Continued implement user interface (cli).
- More tests written.
- **Compression and uncompression using Huffman should now work.**
  - Example (replace <test.txt> with an actual .txt file):
    - `poetry run compressor compress huffman <test.txt> output.bin`
    - `poetry run compressor uncompress huffman output.bin test2.txt`
  - Robust error handling is not yet implemented. E.g. missing files won't give nice output.
  - More tests, especially with large files, are to be added.
  - **Note: destructive actions, like overwriting of files, is not checked for yet.**.

- LZW implementation not yet started.

## Other things done

- Started documentation of testing
  - Coverage report
  - Tests implemented
  - Instructions
- Started utilizing Pylint

## Learnings

How the rest of the Huffman compression works, i.e. how you can store the Huffman codes, the Huffman tree, as well as metadata for the decompression process. And how you can then decompress this data.

## Challenges

None

## Next Steps

- Cleaning up code:
  - Removing commented-out code
  - Removing excess comments
  - Possibly refactoring Huffman implementation (e.g. extracting compressor and decompressor into own classes)
  - Pylint warnings
  - More and better docstring
- Better handling of errors and edge cases
  - Missing input files / existing output files
  - Wrong file formats (non-text files, files not compressed with this program, ...)
  - ...
- Suitable, large, example text files for testing still to be found
- Continuing to add more tests for better test coverage
- Finalizing the Huffman implementation.
- Start to implement LZW
