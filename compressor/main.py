from argparse import ArgumentParser, Namespace

from .compression_methods.huffman import Huffman
from .compressor import Compressor

def get_args(methods: list[str]) -> Namespace:
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
  _ = arg_parser.add_argument("method", type=str, choices=methods)
  _ = arg_parser.add_argument("input_file", type=str)
  _ = arg_parser.add_argument("output_file", type=str)

  args = arg_parser.parse_args()

  return args

def main() -> None:
  methods = {
    "huffman" : Huffman()
  }
  compressor = Compressor()
  args = get_args(list(methods.keys()))

  method = methods.get(args.method, None)

  if not method:
    print("Invalid method")
    exit(1)

  if not args.input_file:
    print("Invalid input file")
    exit(1)

  if not args.output_file:
    print("Invalid output file")
    exit(1)

  if args.command == "compress":
    compressor.compress(args.input_file, args.output_file, method)
  elif args.command == "uncompress":
    compressor.uncompress(args.input_file, args.output_file, method)
