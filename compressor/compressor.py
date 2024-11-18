from .compression_methods.interface import CompressionMethod


class Compressor:
    """A wrapper around CompressinMethods with added functionality."""

    def compress(
        self, input_path: str, output_path: str, method: CompressionMethod
    ) -> None:
        """
        Reads the given file from input path and writes a new compressed version to output path.
        """
        with open(input_path, "r", encoding="utf-8") as i_file:
            with open(output_path, mode="wb") as o_file:
                method.compress(i_file, o_file)

    def decompress(
        self, input_path: str, output_path: str, method: CompressionMethod
    ) -> None:
        """
        Reads the given file from input path and writes a new decompressed version to output path.
        """
        with open(input_path, "rb") as i_file:
            with open(output_path, mode="w", encoding="utf-8") as o_file:
                method.decompress(i_file, o_file)
