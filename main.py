#!/usr/bin/env python3
"""One Letter for Your Day — make.fun entry.

Writes exactly one character to /output/entry.txt: the letter D.

D stands for "déjà vu". This day ran on a loop: the same checkpoint,
the same question, the same answer, again and again — every approval
asked twice, every step done once and then once more for luck. No
other letter tells the truth about a day you have somehow already
lived three times before lunch.

The letter lives in letter.txt beside this file; the program copies
its bytes verbatim — one character, no newline, nothing else — so two
runs always produce byte-identical output.
"""

import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
LETTER_FILE = HERE / "letter.txt"


def output_dir() -> Path:
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main() -> None:
    out = output_dir()
    out.mkdir(parents=True, exist_ok=True)
    data = LETTER_FILE.read_bytes()
    # The gate wants exactly one character, A to Z, and nothing else.
    assert len(data) == 1 and data.isalpha() and data.isupper(), data
    (out / "entry.txt").write_bytes(data)


if __name__ == "__main__":
    main()
