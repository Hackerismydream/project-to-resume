#!/usr/bin/env python3
"""Validate the public copy-ready example contract.

This linter checks deterministic structure, placeholders, audit-language leaks,
and exact-normalized duplication. It deliberately does not validate factual
attribution, metric truth, semantic story quality, or model behavior.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RESUME_HEADING = "## 可直接粘贴的简历版本"
QUESTION_HEADING = "## 仅在必要时追问"
TITLE_RE = re.compile(r"^\*\*(?P<title>[^*\n]+｜[^*\n]+)\*\*\s*$", re.MULTILINE)
TECH_RE = re.compile(r"^\*\*技术栈：\*\*\s*\S.*$", re.MULTILINE)
DESCRIPTION_RE = re.compile(r"^\*\*项目描述：\*\*\s*\S.*$", re.MULTILINE)
BULLET_RE = re.compile(r"^(?:\d+[.)]|[-*])\s+(?P<body>\S.*)$", re.MULTILINE)
QUESTION_RE = re.compile(r"^[-*]\s+\S", re.MULTILINE)
PLACEHOLDER_RE = re.compile(
    r"\[待[^\]\r\n]*\]|\[(?:X|A|B|N|baseline|metric|result)\]|"
    r"\{(?:X|A|B|N)\}|\b(?:TBD|TODO|XX+%?)\b",
    re.IGNORECASE,
)
AUDIT_JARGON_RE = re.compile(
    r"证据注记|Claim Ledger|Claim Record|Story Card|Repository Map|完整\s*SHA|"
    r"项目级草稿|当前证据|待实测|\bartifact\b|\brevision\b",
    re.IGNORECASE,
)
MAX_BULLETS = 5
MAX_QUESTIONS = 3


def _section(text: str, heading: str) -> str:
    start = text.find(heading)
    if start < 0:
        return ""
    start = text.find("\n", start)
    if start < 0:
        return ""
    start += 1
    following = re.search(r"^##\s+", text[start:], re.MULTILINE)
    end = start + following.start() if following else len(text)
    return text[start:end]


def _project_blocks(resume: str) -> list[tuple[str, str]]:
    matches = list(TITLE_RE.finditer(resume))
    blocks: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(resume)
        blocks.append((match.group("title").strip(), resume[match.end() : end]))
    return blocks


def _normalized_bullet(body: str) -> str:
    return re.sub(r"[\s，。；;、,.：:（）()]+", "", body.casefold())


def validate(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    if RESUME_HEADING not in text:
        return [f"missing heading: {RESUME_HEADING}"]

    resume = _section(text, RESUME_HEADING)
    projects = _project_blocks(resume)
    if not projects:
        errors.append("resume section is missing a bold 'project｜role' title")

    seen_titles: set[str] = set()
    seen_bullets: dict[str, str] = {}
    for title, block in projects:
        if title in seen_titles:
            errors.append(f"duplicate project title: {title}")
        seen_titles.add(title)

        if not TECH_RE.search(block):
            errors.append(f"project '{title}' is missing a non-empty technology line")
        if not DESCRIPTION_RE.search(block):
            errors.append(f"project '{title}' is missing a non-empty project description")

        bullet_matches = list(BULLET_RE.finditer(block))
        bullets = [match.group("body").strip() for match in bullet_matches]
        if not bullets:
            errors.append(f"project '{title}' has no bullets; keep at least one strong story")
        elif len(bullets) > MAX_BULLETS:
            errors.append(
                f"project '{title}' has {len(bullets)} bullets; keep each project "
                f"to at most {MAX_BULLETS}"
            )

        if bullet_matches and block[bullet_matches[-1].end() :].strip():
            errors.append(
                f"project '{title}' has prose after its final bullet; keep the "
                "copy-ready section to project content"
            )

        for bullet in bullets:
            normalized = _normalized_bullet(bullet)
            if normalized in seen_bullets:
                errors.append(
                    f"duplicate resume bullet in '{title}': also used in "
                    f"'{seen_bullets[normalized]}'"
                )
            else:
                seen_bullets[normalized] = title

    if PLACEHOLDER_RE.search(resume):
        errors.append("resume section contains a placeholder")
    if AUDIT_JARGON_RE.search(resume):
        errors.append("resume section leaks audit jargon into copy-ready text")

    if QUESTION_HEADING in text:
        if text.find(QUESTION_HEADING) < text.find(RESUME_HEADING):
            errors.append("question section must follow the copy-ready resume section")
        question_count = len(QUESTION_RE.findall(_section(text, QUESTION_HEADING)))
        if question_count > MAX_QUESTIONS:
            errors.append(
                f"question section has {question_count} questions; keep to {MAX_QUESTIONS}"
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()

    failed = False
    for path in args.paths:
        for error in validate(path):
            failed = True
            print(f"{path}: {error}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
