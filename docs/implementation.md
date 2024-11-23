# Structure
`Compressor` implements two methods, compress and decompress. These methods are provided with an instance of an implementation of the `CompressionMethod` interface, currently either the `Huffman` or `LZW`. This instance is used to perform the actual compression and decompression. The `Compressor` adds some extra error handling, as well as some cli output including measurements of the time taken and the compression efficiency.

`cli.py` implements the command-line interface using `argparser`. It is basically a simple command line interface for the `Compressor`.

# Performance
TODO

# Ides for further developement
* Adding more implementations of the `CompressionMethod` interface.
* More memory-efficient handling of data during compression/decompression. Currently the inputs and outputs are in some parts loaded fully into memory for processing. With very large files or machines with less memory this could cause probelms.

# Use of LLMs
Used for finding some information and writing a few small parts of docs texts. LLMs not used for code generation or extensive writing of documentation.
LLMs used: gpt-4o, claude 3.5 sonnet.

# References
* https://www.cs.auckland.ac.nz/~cthombor/Pubs/Old/UMDCS89.2.pdf
* https://www.cs.auckland.ac.nz/software/AlgAnim/huffman.html
* https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch
* https://en.wikipedia.org/wiki/LZ77_and_LZ78
* https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Storer%E2%80%93Szymanski
* https://en.wikipedia.org/wiki/Huffman_coding



