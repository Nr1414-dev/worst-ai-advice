"""Worst AI Advice: The 48-Hour Tight Line Open — entry program.

Writes one line of deliberately terrible advice, at most 140 characters,
to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt when the grader
sets it).

The line was picked from six candidates scored against the judge brief's
five criteria in order (worst advice, funny on first read, tight, AI voice,
concrete) and won every 1v1 comparison. See worst-ai-advice-research.md.

The file is written directly with open() and chmodded to 0644 on purpose:
an atomic write via tempfile would leave the output mode 0600, which the
grader's scorer cannot read (that exact failure rejected another entry's
round 1). The content is one short line, so a direct write is safe.
"""

import os

LINE = "To make your code run faster, delete all the comments — the computer has to read them too."

# The gate only accepts UTF-8 text of 1 to 140 characters, not only
# whitespace, so refuse to write anything that would fail it.
MAX_CHARS = 140


def check_line(text):
    """Refuse to write a line the gate would reject."""
    if not text.strip():
        raise SystemExit("entry must not be only whitespace")
    if len(text) > MAX_CHARS:
        raise SystemExit(f"entry must be at most {MAX_CHARS} characters, got {len(text)}")


def main():
    check_line(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", os.environ.get("ENTRY_OUTPUT_DIR", "/output"))
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(LINE)
    # The scorer runs as a different user than the program, so the output
    # must be world-readable regardless of the process umask.
    os.chmod(path, 0o644)
    # Read back and confirm the file holds exactly the chosen line.
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != LINE:
        raise SystemExit(f"entry.txt holds {written!r}, expected {LINE!r}")


if __name__ == "__main__":
    main()
