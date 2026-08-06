#!/usr/bin/env python3
"""Validate the small, public example contract.

This linter checks structure and orphaned numeric claims. It does not claim to
verify semantics, attribution, or benchmark validity; those require evidence
review.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_HEADINGS = (
    "## 简历草稿",
    "## 证据索引",
    "## 证据边界",
)
PLACEHOLDER_RE = re.compile(r"\[(?:X|A|B|N)\]|\b(?:TBD|TODO)\b", re.IGNORECASE)
FULL_SHA_RE = re.compile(r"\b[0-9a-f]{40}\b")
NUMBER_RE = re.compile(r"(?<![A-Za-z])\d+(?:\.\d+)?%?")
BULLET_RE = re.compile(r"^\d+\.\s+", re.MULTILINE)
EVIDENCE_ROW_RE = re.compile(r"^\|\s*\d+\s*\|", re.MULTILINE)


def validate(path: Path) -> list[str]:
    """Return contract violations for one example Markdown file."""
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            errors.append(f"missing heading: {heading}")

    if not FULL_SHA_RE.search(text):
        errors.append("missing full 40-character commit SHA")

    if PLACEHOLDER_RE.search(text):
        errors.append("contains an unresolved placeholder")

    resume = text.split("## 简历草稿", 1)[-1].split("## 证据索引", 1)[0]
    evidence = text.split("## 证据索引", 1)[-1]
    bullets = BULLET_RE.findall(resume)
    rows = EVIDENCE_ROW_RE.findall(evidence)
    if not bullets:
        errors.append("resume draft contains no numbered bullets")
    if len(bullets) != len(rows):
        errors.append(
            f"resume/evidence count mismatch: {len(bullets)} bullets, {len(rows)} rows"
        )

    # A structural guard only: every numeric token used in the resume draft must
    # also appear in the evidence section. Evidence review must still establish
    # that the matching source is relevant and valid.
    for number in sorted(set(NUMBER_RE.findall(resume))):
        if number not in evidence:
            errors.append(f"numeric token has no evidence mention: {number}")

    return errors


def main() -> int:
    """Run the example linter."""
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()

    failed = False
    for path in args.paths:
        errors = validate(path)
        if errors:
            failed = True
            for error in errors:
                print(f"{path}: {error}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
