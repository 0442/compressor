from argparse import ArgumentParser, Namespace

from .compressor import Compressor

def get_args() -> Namespace:
  """Setup argparser and return Namespace object with the arguments."""
  arg_parser = ArgumentParser()

  cmd_parser = arg_parser.add_subparsers(dest="command", required=True)
  _ = cmd_parser.add_parser(
    "compress", 
    help="Compress a file",
  )

  _ = cmd_parser.add_parser(
    "uncompress", 
    help="Uncompress a file",
  )

  _ = arg_parser.add_argument("method", type=str, choices=[])

  args = arg_parser.parse_args()

  return args

def main():
  _compressor = Compressor([])
  _args = get_args()
