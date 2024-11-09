# Week 2 Report

Hours Spent: ~4

## Things done

- LZ variant chosen: LZW.
- Started writing the program.
- Testing with pytest started.
- Test coverage with `coverage` available.
- More research done into the Huffman algorithm.
- Some usage documentation added.

## Progress of the program

- Started to implement a Compressor class as well as a unified interface for the compression methods.
- Started to implement user interface (cli).
- Started implementing Huffman compression with an initial version of Huffman tree building.
- LZW implementation not yet started.

## Learnings

Learned how the Huffman tree is structured:

First character frequencies are counted. Then from each of these we create a "tree" (consisting of a single node), creating a list of trees, or a "forest". Each node at thist point hold a character and its frequency. Two trees with the smallest frequencies (root node's frequency) are then taken and merged into a new tree. Merging is done by adding a new root node, under which the two trees are added. The root node's frequency is the sum of these two child nodes' frequencies. The new tree is is put back into the forest. Mergning trees is continued until only one tree, the Huffman tree, is left.

## Challenges

None

## Next Steps

- Continuing with the Huffman implementation.
- Continuing to add more tests for better test coverage.
- Finding some suitable example text files for testing compression with differntly sized files.
- Starting to implement LZW as well.
