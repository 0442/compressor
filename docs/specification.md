> Study Program: **Bachelor of Science in Computer Science (CS)**
> 
>  Project language: **English**

# Project Specification
## Programming Language
The program will be written in **Python**.
Other languages I can review are **Java** and **JavaScript/TypeScript**.

## Problem
The project will address the problem of efficient and lossless compression and decompression of text files. The efficincy of compression and computation of two lossless compression algorithms, LZ and Huffman, will be compared.

## Algorithms
Two algorithms and the necessary data structures will be implemented:

  1. A varint of the LZ algorithm (LZ77, LZ78, LZSS or LZW).
  2. Huffman Coding

## Program Inputs and Usage
For compression, the program will accept text files. For decompression, it will accept files compressed by this program.

Users will choose an algorithm (LZ or Huffman) to apply for compression or decompression.

## Expected time and space complexities
LZ:
  * Time: O(n)
  * Space: O(n)

Huffman: 
  * Time: O(n log n)
  * Space: O(n)

## Core of the project
The core of the project is the efficient implementation of the compression algorithms. The implementation will also be properly tested to evaluate whether the implementations behave as expected.

## References

* https://en.wikipedia.org/wiki/LZ77_and_LZ78
* https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Storer%E2%80%93Szymanski
* https://www.cs.auckland.ac.nz/software/AlgAnim/huffman.html
* https://en.wikipedia.org/wiki/Huffman_coding

