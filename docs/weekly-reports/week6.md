# Week 6 Report

Hours Spent: ~8

## Progress of the program

- Added more tests and improved existing ones
  - Tests for large text files
  - Tests for the `FileCompressor` class
- Improved error handling in various places
- Improved documentation (updated docstrings, testing document, implementation document)
- General smaller improvements to thing like structure of code, varible/class/function names, etc.

## Other things done

- Updated docs

## Learnings/Challenges

At least some non-unix-like operating systems might use CR+LF for EOL and not LF in text files. 
Caused some "data loss" as the compress+decompress roundtrip would result in the final file using LF even if original used CR+LF.
Need to fix this in the future (possibly by using `"rb"` and `"wb"` for instead of `"r"` and `"w"` when reading/writing text IO).

## Next Steps

- Some thing from past reports 
- The aforementioned EOL issue
- Docs improvements
- Test improvements
