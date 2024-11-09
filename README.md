# Documentation

- [Specification documnent](/docs/specification.md)
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

> Note: no meaningful working functionality implemented yet

```shell
poetry run compressor
```

# Checking test coverage

```shell
poetry run coverage run --branch -m pytest
poetry run coverage report -m
```
