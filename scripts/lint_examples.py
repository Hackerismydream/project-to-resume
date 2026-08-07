#!/usr/bin/env python3
"""Validate the small, public two-version example contract.

This linter checks structure, placeholder boundaries, and orphaned numeric
claims. It does not claim to verify semantics, attribution, or benchmark
validity; those require evidence review.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


CURRENT_HEADING = "## 当前证据版（证据可用）"
PENDING_ENHANCED_HEADING = "## 指标增强版（推荐目标，待实测，不可投递）"
READY_ENHANCED_HEADING = "## 指标增强版（推荐版，指标已验证）"
PLAN_HEADING = "## 指标验证计划"
EVIDENCE_HEADING = "## 证据索引"
BOUNDARY_HEADING = "## 证据边界"
REQUIRED_HEADINGS = (CURRENT_HEADING, PLAN_HEADING, EVIDENCE_HEADING, BOUNDARY_HEADING)
GENERIC_PLACEHOLDER_RE = re.compile(
    r"\[(?:X|A|B|N|baseline|metric|result)\]|\{(?:X|A|B|N)\}|"
    r"\b(?:TBD|TODO|XX+%?)\b",
    re.IGNORECASE,
)
PENDING_METRIC_RE = re.compile(r"\[待实测：[^\]\r\n]+\]")
FULL_SHA_RE = re.compile(r"\b[0-9a-f]{40}\b")
NUMBER_RE = re.compile(r"(?<![A-Za-z])\d+(?:\.\d+)?%?")
BULLET_RE = re.compile(r"^\d+\.\s+", re.MULTILINE)
EVIDENCE_ROW_RE = re.compile(r"^\|\s*\d+\s*\|", re.MULTILINE)


def _section(text: str, start: str, end: str) -> str:
    """Return text between two headings, or an empty string when incomplete."""
    if start not in text or end not in text:
        return ""
    return text.split(start, 1)[1].split(end, 1)[0]


def _values_to_fill(plan: str) -> str:
    """Return the cells under the measurement plan's Values to fill column."""
    rows = [line for line in plan.splitlines() if line.strip().startswith("|")]
    if not rows:
        return ""
    headers = [cell.strip() for cell in rows[0].strip().strip("|").split("|")]
    try:
        values_index = headers.index("Values to fill")
    except ValueError:
        return ""

    values: list[str] = []
    for row in rows[2:]:
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        if values_index < len(cells):
            values.append(cells[values_index])
    return "\n".join(values)


def validate(path: Path) -> list[str]:
    """Return contract violations for one example Markdown file."""
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            errors.append(f"missing heading: {heading}")

    enhanced_headings = [
        heading
        for heading in (PENDING_ENHANCED_HEADING, READY_ENHANCED_HEADING)
        if heading in text
    ]
    if len(enhanced_headings) != 1:
        errors.append("must contain exactly one metric-enhanced status heading")
        enhanced_heading = PENDING_ENHANCED_HEADING
    else:
        enhanced_heading = enhanced_headings[0]

    if not FULL_SHA_RE.search(text):
        errors.append("missing full 40-character commit SHA")

    if GENERIC_PLACEHOLDER_RE.search(text):
        errors.append("contains an unnamed or generic placeholder")

    current = _section(text, CURRENT_HEADING, enhanced_heading)
    enhanced = _section(text, enhanced_heading, PLAN_HEADING)
    plan = _section(text, PLAN_HEADING, EVIDENCE_HEADING)
    evidence = _section(text, EVIDENCE_HEADING, BOUNDARY_HEADING)
    current_bullets = BULLET_RE.findall(current)
    enhanced_bullets = BULLET_RE.findall(enhanced)
    rows = EVIDENCE_ROW_RE.findall(evidence)
    if not current_bullets:
        errors.append("current-evidence version contains no numbered bullets")
    if not enhanced_bullets:
        errors.append("metric-enhanced version contains no numbered bullets")
    if len(current_bullets) != len(rows):
        errors.append(
            "current/evidence count mismatch: "
            f"{len(current_bullets)} bullets, {len(rows)} rows"
        )

    current_pending = sorted(set(PENDING_METRIC_RE.findall(current)))
    for placeholder in current_pending:
        errors.append(
            "current-evidence version contains a pending metric placeholder: "
            f"{placeholder}"
        )

    enhanced_pending = sorted(set(PENDING_METRIC_RE.findall(enhanced)))
    if enhanced_heading == PENDING_ENHANCED_HEADING:
        if not enhanced_pending:
            errors.append("pending metric-enhanced version contains no named placeholder")
        mapped_values = _values_to_fill(plan)
        if not mapped_values:
            errors.append("measurement plan is missing a Values to fill column")
        for placeholder in enhanced_pending:
            if placeholder not in mapped_values:
                errors.append(f"enhanced placeholder has no measurement plan: {placeholder}")
    elif enhanced_pending:
        errors.append("ready metric-enhanced version still contains pending placeholders")

    # Structural guards only: verified numbers must also appear in the evidence
    # section. Pending enhanced prose is exempt because its values do not exist
    # yet and must instead map to the measurement plan above.
    verified_text = current
    if enhanced_heading == READY_ENHANCED_HEADING:
        verified_text += enhanced
    for number in sorted(set(NUMBER_RE.findall(verified_text))):
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
