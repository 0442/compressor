from typing import TextIO, BinaryIO, override
from bitarray import bitarray

from .interface import CompressionMethod, CompressionMethodError


class LZW(CompressionMethod):
    """Implements the LZW compression algorithm as a CompressionMethod."""

    _MAX_DICT_SIZE = 4096
    _CODE_SIZE = 12  # Size in bits
    _INITIAL_DICT_SIZE = 256

    @override
    def compress(self, text_in: TextIO, bin_out: BinaryIO) -> None:
        """Compresses the input text and writes the result to binary output.

        Args:
            text_in (TextIO): The text input to compress.
            bin_out (BinaryIO): The binary output to write the compressed data.
        """
        data = text_in.read()
        if not data:
            return

        # Initialize the dictionary of char sequence codes with single char ASCII
        # Char seq -> code
        dictionary = {chr(i): i for i in range(self._INITIAL_DICT_SIZE)}
        cur_dict_size = self._INITIAL_DICT_SIZE

        cur_char_seq = ""
        output_codes: list[int] = []

        for c in data:
            new_char_seq = cur_char_seq + c

            if new_char_seq not in dictionary:
                # Write this code to output
                output_codes.append(dictionary[cur_char_seq])

                # If room in dict, add the new one, which did not yet exist
                if cur_dict_size < self._MAX_DICT_SIZE:
                    dictionary[new_char_seq] = cur_dict_size
                    cur_dict_size += 1

                # Continue with the new char only
                cur_char_seq = c
            else:
                cur_char_seq += c

        if cur_char_seq:
            output_codes.append(dictionary[cur_char_seq])

        # Pack the codes into bits
        bits = bitarray(endian="big")
        for code in output_codes:
            bits.extend(bin(code)[2:].zfill(self._CODE_SIZE))

        # Calculate required padding
        padding_len = (8 - (len(bits) % 8)) % 8
        bits.extend("0" * padding_len)

        # Write padding header (1 byte) and the compressed data
        bin_out.write(bytes([padding_len]))
        bin_out.write(bits.tobytes())

    @override
    def decompress(self, bin_in: BinaryIO, text_out: TextIO) -> None:
        """Decompresses the compressed binary input and writes the text to text_out.

        Args:
            bin_in (BinaryIO): The binary input containing compressed data.
            text_out (TextIO): The text output to write the decompressed data.
        """
        # Read the padding header (1 byte)
        padding_len_byte = bin_in.read(1)
        if len(padding_len_byte) != 1:
            raise CompressionMethodError(
                "Invalid input file header: missing padding length byte."
            )

        padding_len = padding_len_byte[0]

        # Read compressed data
        compressed_data = bin_in.read()
        if not compressed_data:
            return

        bits = bitarray(endian="big")
        bits.frombytes(compressed_data)

        if padding_len > 0:
            bits = bits[:-padding_len]

        # Extract self._CODE_SIZE -bit codes from bits
        result_codes: list[int] = []
        i = 0
        total_bits = len(bits)
        while i + self._CODE_SIZE <= total_bits:
            code_bits = bits[i : i + self._CODE_SIZE]
            code = int(code_bits.to01(), 2)
            result_codes.append(code)
            i += self._CODE_SIZE

        if not result_codes:
            return

        # Start decompressing

        # Code -> char seq
        dictionary = {i: chr(i) for i in range(self._INITIAL_DICT_SIZE)}
        dict_size = self._INITIAL_DICT_SIZE

        char_seq = dictionary[result_codes[0]]

        output_chars: list[str] = [char_seq]

        for code in result_codes[1:]:
            if code in dictionary:
                entry = dictionary[code]
            elif code == dict_size:
                entry = char_seq + char_seq[:1]
            else:
                raise CompressionMethodError(f"Bad code: {code}")

            output_chars.append(entry)

            if dict_size < self._MAX_DICT_SIZE:
                dictionary[dict_size] = char_seq + entry[:1]
                dict_size += 1
            char_seq = entry

        output_str = "".join(output_chars)
        text_out.write(output_str)
