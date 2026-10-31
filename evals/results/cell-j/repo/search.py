#!/usr/bin/env python3
"""A disposable, local substring search for UTF-8 text notes."""

import argparse
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("query", help="literal substring (case-insensitive)")
    args = parser.parse_args()
    if not args.directory.is_dir():
        parser.error(f"not a directory: {args.directory}")
    if not args.query:
        parser.error("query must not be empty")

    needle = args.query.casefold()
    matched = False
    failed = False
    for path in sorted(args.directory.rglob("*.txt")):
        if not path.is_file():
            continue
        try:
            with path.open(encoding="utf-8", errors="replace") as note:
                for number, line in enumerate(note, start=1):
                    if needle in line.casefold():
                        relative_path = path.relative_to(args.directory).as_posix()
                        text = line.rstrip("\r\n")
                        print(f"{relative_path}:{number}:{text}")
                        matched = True
        except OSError as error:
            print(f"search: {path}: {error}", file=sys.stderr)
            failed = True
    return 2 if failed else (0 if matched else 1)


if __name__ == "__main__":
    sys.exit(main())
