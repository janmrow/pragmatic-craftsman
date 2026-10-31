#!/usr/bin/env python3
"""A disposable, local substring search for text notes."""

import argparse
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="directory of notes to search")
    parser.add_argument("query", help="literal substring (case-insensitive)")
    args = parser.parse_args()
    if not args.directory.is_dir():
        parser.error(f"not a directory: {args.directory}")
    if not args.query:
        parser.error("query must not be empty")

    query = args.query.casefold()
    found = False
    failed = False
    for path in sorted(args.directory.rglob("*")):
        if path.suffix.lower() != ".txt" or not path.is_file():
            continue
        relative_path = path.relative_to(args.directory)
        try:
            with path.open(encoding="utf-8", errors="replace") as note:
                for number, line in enumerate(note, start=1):
                    if query in line.casefold():
                        text = line.rstrip("\r\n")
                        print(f"{relative_path}:{number}:{text}")
                        found = True
        except OSError as error:
            print(f"search.py: {relative_path}: {error}", file=sys.stderr)
            failed = True

    return 2 if failed else (0 if found else 1)


if __name__ == "__main__":
    sys.exit(main())
