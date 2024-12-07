# Structure
`FileCompressor` in `file_compressor.py` implements two public methods, `compress` and `decompress`. `FileCompressor`'s role is to provide a tool specifically for compressing *text files* from given paths. It does not implement any compression algorithms, but is a *wrapper around the actual algorithm implementations*, providing some extra error handling as well as some cli output like measurements of the time taken and the compression efficiency.

The compression algorithms are implemented as classes, which implement the `CompressionMethod` interface. Currently there are two implementations, `Huffman` and `LZW`. An instance of one of these is passed to `FileCompressor`'s `compress`/`decompress` methods, and is then used to perform the actual compression and decompression.

`cli.py` implements the command line interface using `argparser`. It basically just provides a cli for the `FileCompressor` class and does some additional extra error handling.

# Performance
> Note: methods not yet perfectly comparable. LZW only for fixed ASCII dictionary, while Huffman stores dynamically built tree inside the file.
## Huffman compression with a large file
Size (decompressed): 5337.33 KB
Size (compressed): 3091.78 KB
Compression ratio: 0.579
Compression took 2.23s

## LZW compression with a large file
Size (decompressed): 5337.33 KB
Size (compressed): 3019.90 KB
Compression ratio: 0.566
Compression took 3.08s

## Huffman compression with a small file
Size (decompressed): 21.29 KB
Size (compressed): 12.96 KB
Compression ratio: 0.609
Compression took 0.01s

## LZW compression with a small file
Size (decompressed): 21.29 KB
Size (compressed): 10.98 KB
Compression ratio: 0.516
Compression took 0.01s

# Ides for further developement
* Adding more implementations of the `CompressionMethod` interface.
* More memory-efficient handling of data during compression/decompression. Currently the inputs and outputs are in some parts loaded fully into memory for processing. With very large files or machines with less memory this could cause probelms. Could instead load in chunks and implement the process with generators.

# Use of LLMs
Used for finding some information and writing a few small parts of docs texts. LLMs not used for code generation or extensive writing of documentation. LLMs have been used to improve some docstrings/comments.
LLMs used: gpt-4o, claude 3.5 sonnet.

# References
* https://www.cs.auckland.ac.nz/~cthombor/Pubs/Old/UMDCS89.2.pdf
* https://www.cs.auckland.ac.nz/software/AlgAnim/huffman.html
* https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch
* https://en.wikipedia.org/wiki/LZ77_and_LZ78
* https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Storer%E2%80%93Szymanski
* https://en.wikipedia.org/wiki/Huffman_coding
