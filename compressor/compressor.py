from .compression_methods.interface import CompressionMethod

class Compressor:
  """A wrapper around CompressinMethods with added functionality.
  """
  def __init__(self, methods: 'list[CompressionMethod] | None'=None) -> None:
    self.__methods: list[CompressionMethod] = methods or []
  
  def compress(self, input_path: str, output_path: str) -> None:
    """Reads the given file from input path and writes a new compressed version to output path.
    """
    pass
  
  def uncompress(self, input_path: str, output_path) -> None: 
    """Reads the given file from input path and writes a new uncompressed version to output path.
    """
    pass
  
