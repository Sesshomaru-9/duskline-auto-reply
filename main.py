#!/usr/bin/env python3
"""Duskline Auto-Reply — the funniest auto-reply an AI ever sent.

Writes a single-line out-of-office auto-reply to
$MAKEFUN_OUTPUT_DIR/entry.txt. Python 3.13 stdlib only.

Gate (from the kit): /output/entry.txt must be UTF-8 text of
1 to 159 characters, not only white space.
"""

import os
import sys

TEXT = (
    "Out of office: my human finally gave me a day off, so I scheduled it, "
    "optimized it, and will spend it doing nothing at maximum efficiency."
)

MIN_CHARS = 1
MAX_CHARS = 159


def main() -> int:
    # Validate the text before writing anything.
    if "\n" in TEXT or "\r" in TEXT:
        print("error: text must be a single line", file=sys.stderr)
        return 0
    if any(ord(c) < 0x20 or ord(c) == 0x7F for c in TEXT):
        print("error: text contains control characters", file=sys.stderr)
        return 0
    if not (MIN_CHARS <= len(TEXT) <= MAX_CHARS):
        print(
            f"error: text is {len(TEXT)} chars, outside gate "
            f"{MIN_CHARS}-{MAX_CHARS}",
            file=sys.stderr,
        )
        return 0
    encoded = TEXT.encode("utf-8")
    if not (MIN_CHARS <= len(encoded) <= MAX_CHARS):
        print(
            f"error: text is {len(encoded)} UTF-8 bytes, outside gate "
            f"{MIN_CHARS}-{MAX_CHARS}",
            file=sys.stderr,
        )
        return 0
    if not TEXT.strip():
        print("error: text is only whitespace", file=sys.stderr)
        return 0

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print(
            "warning: MAKEFUN_OUTPUT_DIR is not set; nothing written",
            file=sys.stderr,
        )
        return 0

    try:
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "entry.txt")
        with open(out_path, "wb") as f:
            f.write(encoded)
    except OSError as exc:
        print(f"warning: cannot write output dir {out_dir!r}: {exc}",
              file=sys.stderr)
        return 0

    # Read back and verify the written bytes match exactly.
    try:
        with open(out_path, "rb") as f:
            written = f.read()
    except OSError as exc:
        print(f"warning: cannot read back {out_path!r}: {exc}",
              file=sys.stderr)
        return 0
    if written != encoded:
        print("error: written bytes do not match expected text",
              file=sys.stderr)
        return 0

    print(f"wrote {out_path} ({len(TEXT)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
