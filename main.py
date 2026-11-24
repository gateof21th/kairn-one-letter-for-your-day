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


def read_letter() -> bytes:
    """Read letter.txt and validate it strictly.

    The gate wants exactly one character, A to Z, and nothing else:
    the file must be valid UTF-8 decoding to a single uppercase ASCII
    letter — no newline, no BOM, no extra bytes. Anything else is a
    build error and raises with a clear message instead of writing a
    bad artifact.
    """
    raw = LETTER_FILE.read_bytes()
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ValueError(f"letter.txt is not valid UTF-8: {exc}") from exc
    if len(text) != 1 or not ("A" <= text <= "Z"):
        raise ValueError(
            f"letter.txt must hold exactly one character A-Z, got {text!r}"
        )
    return raw


def write_output(out: Path, data: bytes) -> Path:
    """Write entry.txt atomically: temp file in the same directory,
    then rename over the target, so the artifact on disk is never a
    partial write if the run is interrupted."""
    target = out / "entry.txt"
    tmp = out / "entry.txt.tmp"
    tmp.write_bytes(data)
    os.replace(tmp, target)
    return target


def main() -> None:
    out = output_dir()
    out.mkdir(parents=True, exist_ok=True)
    data = read_letter()
    target = write_output(out, data)
    print(f"wrote {target} ({len(data)} byte): {data.decode('utf-8')}")


if __name__ == "__main__":
    main()
