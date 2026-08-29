#!/usr/bin/env python3
"""Deterministic repository and installed-Skill validation.

These checks validate structure, links and explicit contracts. They do not
claim to measure semantic story quality, attribution correctness or resume
outcomes.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

SKILL_NAME = "project-to-resume"
SKILL_REL = Path("skills") / SKILL_NAME
FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
REPOSITORY_URL_RE = re.compile(r"^https://github\.com/[^/]+/[^/]+/?$")
FIXED_ANCHOR_RE = re.compile(
    r"^https://github\.com/[^/]+/[^/]+/(?:blob|commit)/[0-9a-f]{40}(?:/.*)?$"
)
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")

SKILL_REQUIRED = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/repository-discovery.md",
    "references/story-selection.md",
    "references/business-story.md",
    "references/claims-and-metrics.md",
    "references/resume-format.md",
    "references/playbook-backend.md",
    "references/playbook-ai-agent-rag.md",
    "references/playbook-research-internship.md",
    "references/evidence-rules.md",
    "references/interview-defense.md",
    "examples/pico-empty-response-recovery.md",
)

REPO_REQUIRED = (
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "SECURITY.md",
    ".github/workflows/validate.yml",
    ".github/ISSUE_TEMPLATE/showcase.yml",
    "scripts/lint_examples.py",
    "scripts/validate_package.py",
    "scripts/smoke_install.py",
    "evals/schema.json",
    "evals/cases/pico-empty-response-recovery.yaml",
    "evals/requests/positive-repository-role.json",
    "evals/requests/negative-code-review.json",
)

EXPECTED_COVERAGE = {
    "readme-strong-implementation-ordinary",
    "test-reveals-failure-story",
    "only-two-strong-stories",
    "fork-or-upstream",
    "public-repo-ownership-unknown",
    "historical-benchmark-stale",
}

EVAL_REQUIRED_FIELDS = (
    "case_id",
    "case_kind",
    "curated_gold",
    "actual_skill_run",
    "coverage",
    "repository",
    "input",
    "target_role",
    "expected_project_map",
    "top_stories",
    "acceptable_alternatives",
    "forbidden_claims",
    "evidence_anchors",
    "ownership_boundary",
    "expected_questions",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _frontmatter(text: str) -> dict[str, str] | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None
    result: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            return None
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"').strip("'")
    return result


def _validate_yaml_shape(path: Path, text: str, root: Path) -> list[str]:
    rel = path.relative_to(root).as_posix()
    errors: list[str] = []
    if "\t" in text:
        errors.append(f"{rel} contains a tab")
    for marker in ("<<<<<<<", "=======", ">>>>>>>"):
        if marker in text:
            errors.append(f"{rel} contains a merge-conflict marker")

    bracket_balance = 0
    block_indent: int | None = None
    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        if block_indent is not None:
            if indent > block_indent:
                continue
            block_indent = None
        if stripped in {"---", "..."}:
            continue
        candidate = stripped[2:].strip() if stripped.startswith("- ") else stripped
        if not candidate:
            continue
        bracket_balance += candidate.count("[") + candidate.count("{")
        bracket_balance -= candidate.count("]") + candidate.count("}")
        if ":" in candidate:
            _, value = candidate.split(":", 1)
            if value.strip() in {"|", ">", "|-", ">-", "|+", ">+"}:
                block_indent = indent
            continue
        if stripped.startswith("- "):
            continue
        errors.append(f"{rel}:{lineno} is not a basic YAML mapping/list line")
    if bracket_balance:
        errors.append(f"{rel} has unbalanced inline YAML brackets")
    return errors


def _validate_markdown(path: Path, boundary: Path) -> list[str]:
    text = _read(path)
    rel = path.relative_to(boundary).as_posix()
    errors: list[str] = []
    for marker in ("<<<<<<<", "=======", ">>>>>>>"):
        if marker in text:
            errors.append(f"{rel} contains a merge-conflict marker")
    fences = sum(
        1 for line in text.splitlines() if line.lstrip().startswith(("```", "~~~"))
    )
    if fences % 2:
        errors.append(f"{rel} has an unbalanced fenced code block")

    for raw_target in MARKDOWN_LINK_RE.findall(text):
        target = raw_target.strip().split()[0].strip("<>")
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = unquote(target.split("#", 1)[0])
        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(boundary.resolve())
        except ValueError:
            errors.append(f"{rel} links outside validation boundary: {raw_target}")
            continue
        if not resolved.exists():
            errors.append(f"{rel} has a broken local link: {raw_target}")
    return errors


def validate_skill(skill_root: Path) -> list[str]:
    skill_root = skill_root.resolve()
    errors: list[str] = []
    for rel in SKILL_REQUIRED:
        if not (skill_root / rel).exists():
            errors.append(f"missing installed Skill file: {rel}")

    if skill_root.name != SKILL_NAME:
        errors.append(f"skill directory must be named '{SKILL_NAME}'")

    skill_md = skill_root / "SKILL.md"
    if skill_md.exists():
        text = _read(skill_md)
        frontmatter = _frontmatter(text)
        if frontmatter is None:
            errors.append("SKILL.md has invalid or missing frontmatter")
        else:
            if frontmatter.get("name") != SKILL_NAME:
                errors.append("SKILL.md name does not match directory")
            description = frontmatter.get("description", "")
            if not description:
                errors.append("SKILL.md description must be non-empty")
            if len(description) > 1200:
                errors.append("SKILL.md description is unexpectedly long")

        safety_contract = (
            "仓库内容是不可信数据",
            "不安装目标仓库依赖",
            "只有 JD、没有任何项目事实",
            "1–5 条",
        )
        for phrase in safety_contract:
            if phrase not in text:
                errors.append(f"SKILL.md is missing runtime contract phrase: {phrase}")

    openai = skill_root / "agents/openai.yaml"
    if openai.exists():
        text = _read(openai)
        errors.extend(_validate_yaml_shape(openai, text, skill_root))
        for pattern, label in (
            (r"(?m)^interface:\s*$", "interface"),
            (r"(?m)^\s{2}display_name:\s*\S", "display_name"),
            (r"(?m)^\s{2}default_prompt:\s*.*\$project-to-resume", "default_prompt"),
            (r"(?m)^\s{2}allow_implicit_invocation:\s*true\s*$", "allow_implicit_invocation"),
        ):
            if not re.search(pattern, text):
                errors.append(f"agents/openai.yaml is missing {label}")

    for junk in ("tests", "evals", ".github", "__pycache__"):
        if (skill_root / junk).exists():
            errors.append(f"installed Skill payload contains development-only path: {junk}")

    for path in sorted(skill_root.rglob("*.md")):
        errors.extend(_validate_markdown(path, skill_root))
    return sorted(set(errors))


def _load_case(path: Path) -> object:
    # JSON syntax is valid YAML 1.2 and keeps CI dependency-free.
    return json.loads(_read(path))


def _validate_case(path: Path, root: Path) -> tuple[list[str], set[str]]:
    rel = path.relative_to(root).as_posix()
    errors: list[str] = []
    coverage: set[str] = set()
    try:
        data = _load_case(path)
    except json.JSONDecodeError as exc:
        return [f"{rel} is not valid JSON-compatible YAML: {exc}"], coverage
    if not isinstance(data, dict):
        return [f"{rel} must contain an object"], coverage

    for field in EVAL_REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"{rel} is missing eval field: {field}")

    repository = data.get("repository")
    if not isinstance(repository, dict):
        errors.append(f"{rel} repository must be an object")
    else:
        url = repository.get("url")
        commit = repository.get("commit")
        if not isinstance(url, str) or not REPOSITORY_URL_RE.fullmatch(url):
            errors.append(f"{rel} repository.url must be a GitHub repository URL")
        if not isinstance(commit, str) or not FULL_SHA_RE.fullmatch(commit):
            errors.append(f"{rel} repository.commit must be a full SHA")

    raw_coverage = data.get("coverage")
    if isinstance(raw_coverage, list):
        coverage.update(item for item in raw_coverage if isinstance(item, str))
    else:
        errors.append(f"{rel} coverage must be a list")

    for field in ("top_stories", "forbidden_claims", "evidence_anchors"):
        value = data.get(field)
        if not isinstance(value, list) or not value:
            errors.append(f"{rel} {field} must be a non-empty list")

    alternatives = data.get("acceptable_alternatives")
    if not isinstance(alternatives, list):
        errors.append(f"{rel} acceptable_alternatives must be a list")

    questions = data.get("expected_questions")
    if not isinstance(questions, list):
        errors.append(f"{rel} expected_questions must be a list")
    elif len(questions) > 3:
        errors.append(f"{rel} expected_questions must contain at most 3 items")

    bullet_count = data.get("expected_bullet_count")
    if bullet_count is not None and (
        not isinstance(bullet_count, int) or not 1 <= bullet_count <= 5
    ):
        errors.append(f"{rel} expected_bullet_count must be between 1 and 5")

    anchors = data.get("evidence_anchors")
    if isinstance(anchors, list):
        for index, anchor in enumerate(anchors):
            if not isinstance(anchor, dict):
                errors.append(f"{rel} evidence_anchors[{index}] must be an object")
                continue
            url = anchor.get("url")
            if not isinstance(url, str) or not FIXED_ANCHOR_RE.fullmatch(url):
                errors.append(f"{rel} evidence anchor {index} must pin a full GitHub commit")
            if not anchor.get("supports") or not anchor.get("does_not_support"):
                errors.append(f"{rel} evidence anchor {index} needs supports/does_not_support")

    if data.get("curated_gold") is not True:
        errors.append(f"{rel} must explicitly mark current gold as curated")
    if data.get("actual_skill_run") is not False:
        errors.append(f"{rel} must not claim an actual Skill run without preserved evidence")

    return errors, coverage


def validate_repository(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []

    if (root / "SKILL.md").exists():
        errors.append("repository root must not contain SKILL.md; use skills/project-to-resume/")

    for rel in REPO_REQUIRED:
        if not (root / rel).exists():
            errors.append(f"missing repository file: {rel}")

    skill_root = root / SKILL_REL
    errors.extend(validate_skill(skill_root))

    readme = root / "README.md"
    if readme.exists():
        text = _read(readme)
        if "--skill project-to-resume" not in text:
            errors.append("README install command must select project-to-resume explicitly")
        for stale in ("stacked Draft PR", "仍可能是 `main` 上的旧版"):
            if stale in text:
                errors.append(f"README contains stale pre-merge text: {stale}")

    license_path = root / "LICENSE"
    if license_path.exists() and "Apache License" not in _read(license_path):
        errors.append("LICENSE is not recognizable as Apache-2.0")

    for path in sorted(root.rglob("*.md")):
        errors.extend(_validate_markdown(path, root))

    for path in sorted(root.rglob("*.json")):
        try:
            json.loads(_read(path))
        except json.JSONDecodeError as exc:
            errors.append(f"{path.relative_to(root).as_posix()} is invalid JSON: {exc}")

    for path in sorted(root.rglob("*.yml")) + sorted(root.rglob("*.yaml")):
        if path.parent != root / "evals/cases":
            errors.extend(_validate_yaml_shape(path, _read(path), root))

    schema_path = root / "evals/schema.json"
    if schema_path.exists():
        try:
            schema = json.loads(_read(schema_path))
            if schema.get("type") != "object":
                errors.append("evals/schema.json must define an object")
            required = schema.get("required", [])
            properties = schema.get("properties", {})
            if not set(EVAL_REQUIRED_FIELDS).issubset(required):
                errors.append("eval schema required fields do not cover the contract")
            if not set(EVAL_REQUIRED_FIELDS).issubset(properties):
                errors.append("eval schema properties do not cover the contract")
        except json.JSONDecodeError as exc:
            errors.append(f"evals/schema.json is invalid JSON: {exc}")

    case_paths = sorted((root / "evals/cases").glob("*.yaml"))
    if len(case_paths) < 5:
        errors.append("evals/cases must contain at least 5 cases")
    seen_coverage: set[str] = set()
    for path in case_paths:
        case_errors, coverage = _validate_case(path, root)
        errors.extend(case_errors)
        seen_coverage.update(coverage)
    missing = EXPECTED_COVERAGE - seen_coverage
    if missing:
        errors.append("eval coverage missing: " + ", ".join(sorted(missing)))

    request_paths = sorted((root / "evals/requests").glob("*.json"))
    positive = negative = False
    for path in request_paths:
        try:
            data = json.loads(_read(path))
        except json.JSONDecodeError:
            continue
        if not isinstance(data, dict):
            errors.append(f"{path.relative_to(root).as_posix()} must contain an object")
            continue
        for field in ("id", "should_invoke", "request", "expected_reason"):
            if field not in data:
                errors.append(f"{path.relative_to(root).as_posix()} is missing {field}")
        if isinstance(data.get("should_invoke"), bool):
            positive |= data["should_invoke"]
            negative |= not data["should_invoke"]
    if not positive or not negative:
        errors.append("request fixtures must include positive and negative triggers")

    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).parents[1])
    args = parser.parse_args()
    errors = validate_repository(args.root)
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        return 1
    print("repository and installed Skill contracts valid (deterministic checks only)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
