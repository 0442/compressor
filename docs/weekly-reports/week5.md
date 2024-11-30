# Week 5 Report

Hours Spent: ~7

## Progress of the program

- Finished the initial working version of LZW.
  - Program can now compress and decompress using the LZW method:
    ```shell
    poetry run compressor compress lzw <input.txt> <output.bin>
    ```
    ```shell
    poetry run compressor decompress lzw <input.bin> <output.txt>
    ```
- Added some basic tests for LZW

## Other things done

- Updated docs
- Peer review

## Learnings

Some more about LZW, enough to be able to implement a first working version.

## Challenges

None

## Next Steps

- Some things from the previous weeks' lists
- Improving and updating documentation, keeping it up-to-date
- Checking if there are things in the program itself to improve
  - Reading input from files in chunks for better memory efficiency. Would allows handling larger files on systems with less memory
  - More reporting. E.g. for Huffman, could add reporting about tree size vs. data size in the resulting file.
  - Better error handling
  - Checking input data validity in different parts for more accurate error logs
  - ...
