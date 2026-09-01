#!/usr/bin/env python3
"""
French typography, applied uniformly to every layer at build time.

docs/STYLE.md §3 requires a non-breaking space before `; ! ? :` and on the inner
side of `« … »`. Doing it here
rather than by hand keeps the translation tables readable and guarantees no
string is missed.

Only an EXISTING regular space is converted — a missing one is never inserted.
That deliberately leaves clock times ("12:33"), ratios and any other unspaced
colon alone, and it never touches the inside of a markup tag.
"""
import re

NBSP = " "
_OUTSIDE_TAGS = re.compile(r"(<[^>]*>)")
_SPACE_BEFORE = re.compile(r" ([;!?:])")
_OPEN_QUOTE = re.compile(r"(«) ")
_CLOSE_QUOTE = re.compile(r" (»)")


def normalise(s):
    if not s:
        return s
    parts = _OUTSIDE_TAGS.split(s)
    # split() keeps the delimiters at odd indices; only rewrite the text between them
    for i in range(0, len(parts), 2):
        parts[i] = _SPACE_BEFORE.sub(NBSP + r"\1", parts[i])
        parts[i] = _OPEN_QUOTE.sub(r"\1" + NBSP, parts[i])
        parts[i] = _CLOSE_QUOTE.sub(NBSP + r"\1", parts[i])
    return "".join(parts)
