# Documentation

- [Specification documnent](/docs/specification.md)
- [Testing documnentation](/docs/testing.md)
- [Weekly reports](/docs/weekly-reports/)

# Installation

Clone the project and `cd` into it

```shell
git clone git@github.com:0442/harjoitustyo.git
cd harjoitustyo
```

Install dependencies

```shell
poetry install
```

# Running
To view the help page, run
```shell
poetry run compressor -h
```
Compressing a text file:
```shell
poetry run compressor compress huffman <input_file> <output_file>
```

Uncompressing a compressed file (compressed by this program):
> Note: overwriting existing files is not checked for!
```shell
poetry run compressor uncompress huffman <input_file> <output_file>
```
