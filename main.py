#!/usr/bin/env python3
"""One-Line Office Joke: 24-Hour Sprint.

Writes one single-line joke about office life to
$MAKEFUN_OUTPUT_DIR/entry.txt (or ./output/entry.txt when the variable
is unset). The joke is at most 200 characters, one sentence, and the
program writes nothing anywhere else — in particular it never writes
into the repository folder itself.
"""

import os
import sys

JOKE = ("The office fridge has a sign saying 'your food, your "
        "responsibility', right above the sandwich someone stole in 2019.")


def output_dir():
    """Where the graded entry goes: the grader's output dir, else ./output."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "output")


def check_line(line):
    """The gate, as the bounty states it: UTF-8, 1 to 200 chars, not blank."""
    if not line or line != line.strip():
        raise ValueError("joke must not be empty or padded with whitespace")
    if len(line) > 200:
        raise ValueError("joke is %d characters, over the 200 limit" % len(line))
    line.encode("utf-8")
    if not line.strip():
        raise ValueError("joke must not be only whitespace")
    return line


def verify_written(path, line):
    """Read the file back and prove it holds exactly the joke, byte for byte."""
    with open(path, "rb") as handle:
        data = handle.read()
    if data != line.encode("utf-8"):
        raise ValueError("written entry does not match the joke")
    if b"\n" in data:
        raise ValueError("entry must be a single line with no newline")
    return len(data)


def main():
    line = check_line(JOKE)
    out_dir = output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(line)
    size = verify_written(path, line)
    print("Wrote %s (%d characters, verified %d bytes)" % (path, len(line), size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
