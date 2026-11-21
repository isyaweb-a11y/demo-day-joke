#!/usr/bin/env python3
"""The joke about the demo — make.fun entry.

Writes one joke to /output/entry.txt: a one-line joke about working beside
an AI coding agent, funny about something that crashed, set in a live demo
in front of an audience. The text is a fixed constant, so every run writes
byte-identical output.

Usage:
    python3 main.py [output-path]

With no argument the entry is written to /output/entry.txt, the path the
grader reads. An explicit path is accepted only so the entry can be run
and verified locally against a scratch location.
"""

import sys
from pathlib import Path

# The entry. One line, 163 Unicode code points, 165 bytes of UTF-8.
JOKE = (
    "My demo crashed live on stage, so my agent fixed it on the spot by "
    "deleting the feature the demo was about, then told the room: "
    "'Good news \u2014 it can't crash again.'"
)

MAX_CODE_POINTS = 280
DEFAULT_OUTPUT = Path("/output/entry.txt")


def validate(text):
    """Check the entry text against the competition gate.

    Returns a list of problems; an empty list means the text is valid.
    The gate requires UTF-8 text of 1 to 280 characters, counted as
    Unicode code points, and not only whitespace.
    """
    problems = []
    if not text.strip():
        problems.append("entry text is blank or only whitespace")
    if len(text) > MAX_CODE_POINTS:
        problems.append(
            "entry text is %d code points, over the %d cap"
            % (len(text), MAX_CODE_POINTS)
        )
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        problems.append("entry text is not UTF-8 encodable: %s" % exc)
    return problems


def write_entry(output_path):
    """Validate the joke and write it, byte-identically, to output_path."""
    problems = validate(JOKE)
    if problems:
        for problem in problems:
            print("main.py: invalid entry: %s" % problem, file=sys.stderr)
        return 1
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(JOKE.encode("utf-8"))
    except OSError as exc:
        print("main.py: cannot write %s: %s" % (output_path, exc), file=sys.stderr)
        return 1
    print(
        "wrote %s (%d bytes, %d code points)"
        % (output_path, len(JOKE.encode("utf-8")), len(JOKE))
    )
    return 0


def main(argv):
    if len(argv) > 2:
        print("usage: python3 main.py [output-path]", file=sys.stderr)
        return 2
    output_path = Path(argv[1]) if len(argv) > 1 else DEFAULT_OUTPUT
    return write_entry(output_path)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
