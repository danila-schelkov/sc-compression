import argparse
import os
from typing import Callable

from sc_compression import compress, decompress
from sc_compression.signatures import Signatures


def main() -> int:
    argument_parser = argparse.ArgumentParser(
        description="A module for compression like in Supercell games."
    )
    argument_parser.add_argument(
        "-d", "--decompress", help="Decompress all files", action="store_true"
    )
    argument_parser.add_argument(
        "-c", "--compress", help="Compress all files", action="store_true"
    )
    argument_parser.add_argument(
        "-s",
        "--signature",
        choices=[signature.name for signature in Signatures],
        help="Required signature name",
        type=str,
        default=Signatures.SC.name,
    )
    argument_parser.add_argument(
        "-f",
        "--files",
        help="Files to be processed",
        type=str,
        nargs="+",
        required=True,
    )
    argument_parser.add_argument(
        "-S",
        "--suffix",
        help="Suffix for processed files",
        type=str,
        default=None,
    )

    args = argument_parser.parse_args()
    if args.decompress:
        process_files(
            args.files,
            lambda data: decompress(data)[0],
            args.suffix or "decompressed",
        )
    elif args.compress:
        signature = Signatures[args.signature]

        process_files(
            args.files,
            lambda data: compress(data, signature, 1),
            args.suffix or "compressed",
        )
    else:
        argument_parser.print_help()

    return 0


def get_absolute_file_path(file_path: str) -> str:
    if os.path.isabs(file_path):
        return file_path

    return os.path.join(os.getcwd(), file_path)


def get_directory(file_path: str) -> str:
    return os.path.dirname(file_path)


def get_base_name(file_path: str) -> str:
    return os.path.splitext(file_path)[0]


def get_extension(file_path: str) -> str:
    return os.path.splitext(file_path)[1][1:]


def join_filename(*parts, divider: str = ".") -> str:
    return divider.join(part for part in parts if type(part) is str and len(part) > 0)


def process_files(files: list[str], action: Callable[[bytes], bytes], suffix: str):
    for filename in files:
        path = get_absolute_file_path(filename)
        directory = get_directory(path)
        base_name = get_base_name(path)
        extension = get_extension(path)

        if os.path.isfile(path):
            with open(path, "rb") as file:
                data = action(file.read())

            processed_filename = join_filename(base_name, suffix, extension)
            with open(os.path.join(directory, processed_filename), "wb") as file:
                file.write(data)


if __name__ == "__main__":
    exit(main())
