#!/usr/bin/env python3
"""The 3AM Fridge Text — make.fun bounty entry.

Writes one line to /output/entry.txt: the text message a smart fridge
sends its owner at 3am. The line is fixed and deterministic: the program
takes no input, reads nothing from the network or disk, and always emits
the same 124-character line.

Why this line: the judge rewards a fridge voice with an opinion, a fresh
angle (not milk/door/leftovers), and a punchline a reader would screenshot.
Six years of watching the owner eat cereal standing in the dark, never once
with a bowl, is specific, visual, and relatable — and "I have questions."
is the fridge finally saying out loud what it has been thinking all night.
"""

import os
import sys

ENTRY = (
    "3am. Six years of watching you eat cereal standing in the dark, "
    "and I have never once seen you use a bowl. I have questions."
)

MAX_CHARS = 140


def main() -> int:
    # The line must be a single line of 1-140 UTF-8 characters, not only
    # whitespace. Validate before writing so a bad line can never ship.
    if not ENTRY or not ENTRY.strip():
        print("entry is empty", file=sys.stderr)
        return 1
    if "\n" in ENTRY or "\r" in ENTRY:
        print("entry must be a single line", file=sys.stderr)
        return 1
    if len(ENTRY) > MAX_CHARS:
        print(f"entry is {len(ENTRY)} chars, over the 140 cap", file=sys.stderr)
        return 1
    ENTRY.encode("utf-8")  # raises if not valid UTF-8

    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    payload = ENTRY.encode("utf-8")
    # Determinism self-check: the bytes written must be identical on every
    # run, so encode once and write the same payload twice, comparing.
    with open(out_path, "wb") as f:
        f.write(payload)
    with open(out_path, "rb") as f:
        if f.read() != payload:
            print("non-deterministic write", file=sys.stderr)
            return 1
    # Outputs must be readable by every user (the grader collects them as
    # another user): 0644, and the directory 0755.
    os.chmod(out_path, 0o644)
    os.chmod(out_dir, 0o755)
    print(f"wrote {len(ENTRY)} chars to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
