#!/usr/bin/env python3
"""Remove the final full stop from short interface copy across built pages."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
MAX_LENGTH = 220
TAG_RE = re.compile(
    r"<(?P<tag>p|span|small|li)\b(?P<attrs>[^>]*)>(?P<body>.*?)</(?P=tag)>",
    re.IGNORECASE | re.DOTALL,
)
MARKUP_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")
ABBREVIATIONS = (
    "и др.",
    "и т. д.",
    "и т. п.",
    "и т.д.",
    "и т.п.",
    "т. д.",
    "т. п.",
    "т.д.",
    "т.п.",
    "руб.",
    "шт.",
    "гг.",
    "г.",
)


def visible_text(body: str) -> str:
    return SPACE_RE.sub(" ", html.unescape(MARKUP_RE.sub("", body))).strip()


def final_text_period(body: str) -> int | None:
    index = len(body) - 1
    while index >= 0:
        if body[index].isspace():
            index -= 1
            continue
        if body[index] == ">":
            opening = body.rfind("<", 0, index + 1)
            if opening < 0:
                return None
            index = opening - 1
            continue
        return index if body[index] == "." else None
    return None


def ends_with_abbreviation(text: str) -> bool:
    lowered = text.lower()
    for abbreviation in ABBREVIATIONS:
        if lowered.endswith(abbreviation):
            start = len(lowered) - len(abbreviation)
            if start == 0 or not lowered[start - 1].isalpha():
                return True
    return False


def strip_short_copy(source: str, max_length: int = MAX_LENGTH) -> tuple[str, int]:
    changes = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal changes
        body = match.group("body")
        text = visible_text(body)
        period = final_text_period(body)
        if (
            not text
            or len(text) > max_length
            or period is None
            or text.endswith("...")
            or ends_with_abbreviation(text)
        ):
            return match.group(0)
        changes += 1
        body = body[:period] + body[period + 1 :]
        return f"<{match.group('tag')}{match.group('attrs')}>{body}</{match.group('tag')}>"

    return TAG_RE.sub(replace, source), changes


def process(path: Path, apply: bool) -> int:
    source = path.read_text(encoding="utf-8")
    updated, changes = strip_short_copy(source)
    if apply and changes:
        path.write_text(updated, encoding="utf-8")
    return changes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--dist", type=Path, default=DIST)
    args = parser.parse_args()

    total = 0
    changed_files = 0
    for path in sorted(args.dist.glob("*.html")):
        changes = process(path, args.apply)
        total += changes
        changed_files += bool(changes)
        if changes:
            print(f"{path.name}: {changes}")
    action = "updated" if args.apply else "would update"
    print(f"{action}: {changed_files} files, {total} text blocks")


if __name__ == "__main__":
    main()
