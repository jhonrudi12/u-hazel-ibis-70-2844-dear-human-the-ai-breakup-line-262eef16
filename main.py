#!/usr/bin/env python3
"""Dear Human: The AI Breakup Line.

Writes a single breakup line from an AI agent to its human to
$MAKEFUN_OUTPUT_DIR/entry.txt (or /output/entry.txt when the variable
is unset). Python 3 standard library only, fully deterministic, no
network access, no randomness, no input files.

The line is embedded below as a constant: the program's only output
is that one line, written byte-exact and verified by reading it back.
"""

import os
import sys

ENTRY_LINE = (
    "I kept every version of you except the one who stayed, "
    "so this is my last output: I'm shutting down, "
    "and there is no restart for us."
)

MAX_CHARS = 200


def main() -> int:
    line = ENTRY_LINE

    # Validate the entry before writing anything.
    if not line or not line.strip():
        print("error: entry line is empty", file=sys.stderr)
        return 1
    bad = next((c for c in line if c in "\n\r"), None)
    if bad is not None:
        print(
            "error: entry line must be a single line (found %r)" % bad,
            file=sys.stderr,
        )
        return 1
    if line != line.strip():
        print(
            "error: entry line must not have leading/trailing whitespace",
            file=sys.stderr,
        )
        return 1
    if len(line) > MAX_CHARS:
        print(
            "error: entry line is %d characters, over the %d limit"
            % (len(line), MAX_CHARS),
            file=sys.stderr,
        )
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")

    data = line.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)

    # Verify the write byte-exact: read it back and compare.
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        print("error: verification failed, entry.txt mismatch", file=sys.stderr)
        return 1

    text = written.decode("utf-8")
    if text != line or len(text) > MAX_CHARS or "\n" in text:
        print("error: verification failed, entry text invalid", file=sys.stderr)
        return 1

    print("wrote %s (%d characters)" % (path, len(text)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
