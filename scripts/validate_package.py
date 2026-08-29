#!/usr/bin/env python3
"""Deterministic structure validation for the project-to-resume Skill package.

The checks prove package shape and local consistency only. They do not prove
semantic story quality, model behavior, factual attribution, or resume impact.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


SKILL_NAME = "project-to-resume"
FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
REPOSITORY_URL_RE = re.compile(r"^https://github\.com/[^/]+/[^/]+/?$")
FIXED_GITHUB_ANCHOR_RE = re.compile(
    r"^https://github\.com/[^/]+/[^/]+/(?:blob|commit)/[0-9a-f]{40}(?:/.*)?$"
)
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
YAML_MAPPING_RE = re.compile(r"^[^:#][^:]*:(?:\s+.*)?$")

REQUIRED_PATHS = (
    "SKILL.md",
    "README.md",
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
    "scripts/lint_examples.py",
    "scripts/validate_package.py",
    "scripts/smoke_install.py",
    "evals/schema.json",
    "evals/cases/pico-empty-response-recovery.yaml",
    "evals/requests/positive-repository-role.json",
    "evals/requests/negative-code-review.json",
    "examples/pico-empty-response-recovery.md",
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
    values: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            return None
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def _validate_skill(root: Path) -> list[str]:
    errors: list[str] = []
    path = root / "SKILL.md"
    if not path.exists():
        return ["missing required file: SKILL.md"]
    values = _frontmatter(_read(path))
    if values is None:
        return ["SKILL.md has invalid or missing YAML frontmatter"]
    if values.get("name") != SKILL_NAME:
        errors.append(
            f"SKILL.md name must be '{SKILL_NAME}', got {values.get('name')!r}"
        )
    description = values.get("description", "")
    if not description:
        errors.append("SKILL.md description must be non-empty")
    if "ordinary code review" not in description.casefold():
        errors.append("SKILL.md description must exclude ordinary code review")
    if root.name != SKILL_NAME:
        errors.append(
            f"skill directory must be named '{SKILL_NAME}', got '{root.name}'"
        )
    return errors


def _validate_openai_yaml(root: Path) -> list[str]:
    path = root / "agents/openai.yaml"
    if not path.exists():
        return ["missing required file: agents/openai.yaml"]
    text = _read(path)
    errors = _validate_yaml_shape(path, text)
    required_patterns = {
        "interface mapping": r"(?m)^interface:\s*$",
        "display_name": r"(?m)^\s{2}display_name:\s*\S",
        "short_description": r"(?m)^\s{2}short_description:\s*\S",
        "default_prompt": r"(?m)^\s{2}default_prompt:\s*.*\$project-to-resume",
        "policy mapping": r"(?m)^policy:\s*$",
        "allow_implicit_invocation true": r"(?m)^\s{2}allow_implicit_invocation:\s*true\s*$",
    }
    for label, pattern in required_patterns.items():
        if not re.search(pattern, text):
            errors.append(f"agents/openai.yaml is missing {label}")
    return errors


def _validate_yaml_shape(path: Path, text: str) -> list[str]:
    """Perform dependency-free, deterministic YAML sanity checks.

    This is deliberately a shape check rather than a complete YAML parser. It
    catches tabs, merge markers, malformed mapping/list lines, and block scalar
    indentation while keeping the installed Skill free of parser dependencies.
    """
    errors: list[str] = []
    rel = path.as_posix()
    if "\t" in text:
        errors.append(f"{rel} contains a tab; YAML indentation must use spaces")
    for marker in ("<<<<<<<", "=======", ">>>>>>>"):
        if marker in text:
            errors.append(f"{rel} contains a merge-conflict marker")

    block_indent: int | None = None
    bracket_balance = 0
    for line_number, line in enumerate(text.splitlines(), start=1):
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

        # Plain scalar list items such as "- showcase" are legal YAML.
        if stripped.startswith("- "):
            continue

        errors.append(f"{rel}:{line_number} is not a basic YAML mapping/list line")

    if block_indent is not None:
        # An empty block scalar is legal, so no error is needed.
        block_indent = None
    if bracket_balance != 0:
        errors.append(f"{rel} has unbalanced inline YAML brackets")
    return errors


def _validate_markdown(path: Path, root: Path) -> list[str]:
    text = _read(path)
    rel = path.relative_to(root).as_posix()
    errors: list[str] = []
    for marker in ("<<<<<<<", "=======", ">>>>>>>"):
        if marker in text:
            errors.append(f"{rel} contains a merge-conflict marker")
    fence_count = sum(
        1 for line in text.splitlines() if line.lstrip().startswith(("```", "~~~"))
    )
    if fence_count % 2:
        errors.append(f"{rel} has an unbalanced fenced code block")
    if "\x00" in text:
        errors.append(f"{rel} contains a NUL byte")

    for raw_target in MARKDOWN_LINK_RE.findall(text):
        target = raw_target.strip().split()[0].strip("<>")
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = unquote(target.split("#", 1)[0])
        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(root.resolve())
        except ValueError:
            errors.append(f"{rel} links outside the skill package: {raw_target}")
            continue
        if not resolved.exists():
            errors.append(f"{rel} has a broken local link: {raw_target}")
    return errors


def _load_json_compatible_yaml(path: Path) -> object:
    # Eval fixtures intentionally use JSON syntax with a .yaml extension. JSON
    # is a YAML 1.2 subset, so this keeps validation dependency-free.
    return json.loads(_read(path))


def _validate_eval_case(path: Path, root: Path) -> list[str]:
    rel = path.relative_to(root).as_posix()
    try:
        data = _load_json_compatible_yaml(path)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        return [f"{rel} is not valid JSON-compatible YAML: {exc}"]
    if not isinstance(data, dict):
        return [f"{rel} must contain an object"]

    errors: list[str] = []
    for field in EVAL_REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"{rel} is missing eval field: {field}")

    repository = data.get("repository")
    if isinstance(repository, dict):
        url = repository.get("url")
        commit = repository.get("commit")
        if not isinstance(url, str) or not REPOSITORY_URL_RE.fullmatch(url):
            errors.append(f"{rel} repository.url must be a GitHub repository URL")
        if not isinstance(commit, str) or not FULL_SHA_RE.fullmatch(commit):
            errors.append(f"{rel} repository.commit must be a full 40-character SHA")
    elif "repository" in data:
        errors.append(f"{rel} repository must be an object")

    for field in ("top_stories", "forbidden_claims", "evidence_anchors"):
        value = data.get(field)
        if not isinstance(value, list) or not value:
            errors.append(f"{rel} {field} must be a non-empty list")

    coverage = data.get("coverage")
    if not isinstance(coverage, list) or not coverage or not all(
        isinstance(item, str) and item for item in coverage
    ):
        errors.append(f"{rel} coverage must be a non-empty list of strings")

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
            if not isinstance(url, str) or not FIXED_GITHUB_ANCHOR_RE.fullmatch(url):
                errors.append(
                    f"{rel} evidence_anchors[{index}].url must pin a full GitHub commit"
                )
            if not anchor.get("supports") or not anchor.get("does_not_support"):
                errors.append(
                    f"{rel} evidence_anchors[{index}] must state supports and does_not_support"
                )

    for field in ("curated_gold", "actual_skill_run"):
        if field in data and not isinstance(data[field], bool):
            errors.append(f"{rel} {field} must be boolean")

    if data.get("curated_gold") and data.get("actual_skill_run"):
        # This is allowed in principle, but the current repository must not blur
        # the curated demonstration with a real forward run.
        errors.append(
            f"{rel} cannot mark the current curated gold as an actual skill run"
        )

    return errors


def _validate_request_data(root: Path) -> list[str]:
    request_dir = root / "evals/requests"
    errors: list[str] = []
    seen_true = False
    seen_false = False
    for path in sorted(request_dir.glob("*.json")):
        rel = path.relative_to(root).as_posix()
        try:
            data = json.loads(_read(path))
        except json.JSONDecodeError as exc:
            errors.append(f"{rel} is invalid JSON: {exc}")
            continue
        if not isinstance(data, dict):
            errors.append(f"{rel} must contain an object")
            continue
        for field in ("id", "should_invoke", "request", "expected_reason"):
            if field not in data:
                errors.append(f"{rel} is missing request field: {field}")
        if isinstance(data.get("should_invoke"), bool):
            seen_true |= data["should_invoke"]
            seen_false |= not data["should_invoke"]
        else:
            errors.append(f"{rel} should_invoke must be boolean")
    if not seen_true:
        errors.append("eval request data must include at least one positive trigger")
    if not seen_false:
        errors.append("eval request data must include at least one negative trigger")
    return errors


def validate_tree(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []

    for rel in REQUIRED_PATHS:
        if not (root / rel).exists():
            errors.append(f"missing required file: {rel}")

    errors.extend(_validate_skill(root))
    errors.extend(_validate_openai_yaml(root))

    schema_path = root / "evals/schema.json"
    if schema_path.exists():
        try:
            schema = json.loads(_read(schema_path))
            if not isinstance(schema, dict) or schema.get("type") != "object":
                errors.append("evals/schema.json must define an object schema")
            else:
                required = schema.get("required")
                if not isinstance(required, list) or not set(EVAL_REQUIRED_FIELDS).issubset(required):
                    errors.append("evals/schema.json required fields do not cover the eval contract")
                properties = schema.get("properties")
                if not isinstance(properties, dict) or not set(EVAL_REQUIRED_FIELDS).issubset(properties):
                    errors.append("evals/schema.json properties do not cover the eval contract")
        except json.JSONDecodeError as exc:
            errors.append(f"evals/schema.json is invalid JSON: {exc}")

    for path in sorted(root.rglob("*.md")):
        errors.extend(_validate_markdown(path, root))

    case_paths = sorted((root / "evals/cases").glob("*.yaml"))
    if len(case_paths) < 5:
        errors.append("evals/cases must contain at least 5 representative cases")
    seen_coverage: set[str] = set()
    for path in case_paths:
        errors.extend(_validate_eval_case(path, root))
        try:
            data = _load_json_compatible_yaml(path)
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        if isinstance(data, dict) and isinstance(data.get("coverage"), list):
            seen_coverage.update(item for item in data["coverage"] if isinstance(item, str))
    missing_coverage = sorted(EXPECTED_COVERAGE - seen_coverage)
    if missing_coverage:
        errors.append("eval cases are missing required coverage: " + ", ".join(missing_coverage))

    for path in sorted(root.rglob("*.yml")) + sorted(root.rglob("*.yaml")):
        if path.parent != root / "evals/cases":
            errors.extend(_validate_yaml_shape(path, _read(path)))

    for path in sorted(root.rglob("*.json")):
        try:
            json.loads(_read(path))
        except json.JSONDecodeError as exc:
            errors.append(f"{path.relative_to(root).as_posix()} is invalid JSON: {exc}")

    errors.extend(_validate_request_data(root))
    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).parents[1])
    args = parser.parse_args()

    errors = validate_tree(args.root)
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        return 1
    print("package structure valid (deterministic checks only)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
