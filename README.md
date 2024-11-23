# Documentation

- [Specification document](/docs/specification.md)
- [Testing document](/docs/testing.md)
- [Implementation document](/docs/implementation.md)
- [Weekly reports](/docs/weekly-reports/)

# Installation

Clone the project and `cd` into it

```shell
git clone git@github.com:0442/compressor.git
cd compressor
```

Install dependencies

```shell
poetry install
```

# Running
> Note: overwriting existing files is not checked for!

## Method 1.
Use `poetry run compressor` to run the program:

To view the help page, run
```shell
poetry run compressor -h
```

To compress a text file with the Huffman compressor, run
```shell
poetry run compressor compress huffman <input_file> <output_file>
```

## Method 2.
Use `poetry shell` and directly run the `main.py` file using `python`:

Activate the poetry virtual environment
```shell
poetry shell
```
Then to view the help page, run
```shell
python main.py -h
```
To compress a text file with the Huffman compressor, run
```shell
python main.py compress huffman <input_file> <output_file>
```
