#!/usr/bin/env python3
"""Validate the distributable project-to-resume Skill package.

The validator checks package structure, Agent Skill metadata, YAML/JSON syntax,
JSON Schema conformance, local links, fixed-revision eval anchors, governance
files, and generated-file hygiene. It deliberately does not claim to validate
story quality, factual attribution, model behavior, or resume outcomes.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError


SKILL_NAME = "project-to-resume"
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
REPOSITORY_URL_RE = re.compile(r"^https://github\.com/[^/]+/[^/]+/?$")
FIXED_GITHUB_ANCHOR_RE = re.compile(
    r"^https://github\.com/[^/]+/[^/]+/(?:blob|commit)/[0-9a-f]{40}(?:/.*)?$"
)
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")

REQUIRED_PATHS = (
    "SKILL.md",
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    ".editorconfig",
    "Makefile",
    "requirements-dev.txt",
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
    "docs/installation.md",
    "docs/evaluation.md",
    "showcase/README.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/ISSUE_TEMPLATE/showcase.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/workflows/validate.yml",
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

EVAL_REQUIRED_FIELDS = {
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
}

STALE_README_PHRASES = (
    "codex/repository-discovery-v2",
    "stacked Draft PR",
    "公开安装命令默认取得的仍可能是",
    "This PR should not be merged directly",
)

IGNORED_DIRS = {".git", ".venv", "venv", "node_modules"}
PROHIBITED_DIRS = {"__pycache__", "__pypackages__"}
PROHIBITED_FILES = {".DS_Store"}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _iter_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        relative_parts = path.relative_to(root).parts
        if any(part in IGNORED_DIRS for part in relative_parts):
            continue
        if path.is_file():
            yield path


def _load_yaml(path: Path, root: Path) -> tuple[Any | None, list[str]]:
    rel = _relative(path, root)
    try:
        return yaml.safe_load(_read(path)), []
    except (UnicodeDecodeError, yaml.YAMLError) as exc:
        return None, [f"{rel} is invalid YAML: {exc}"]


def _load_json(path: Path, root: Path) -> tuple[Any | None, list[str]]:
    rel = _relative(path, root)
    try:
        return json.loads(_read(path)), []
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        return None, [f"{rel} is invalid JSON: {exc}"]


def _frontmatter(text: str) -> tuple[dict[str, Any] | None, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    try:
        end = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        return None, text

    raw = "\n".join(lines[1:end])
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError:
        return None, text
    if not isinstance(data, dict):
        return None, text
    return data, "\n".join(lines[end + 1 :])


def _validate_skill(root: Path) -> list[str]:
    path = root / "SKILL.md"
    if not path.exists():
        return ["missing required file: SKILL.md"]

    text = _read(path)
    values, body = _frontmatter(text)
    if values is None:
        return ["SKILL.md has invalid or missing YAML frontmatter"]

    errors: list[str] = []
    name = values.get("name")
    description = values.get("description")
    license_id = values.get("license")

    if name != SKILL_NAME:
        errors.append(f"SKILL.md name must be '{SKILL_NAME}', got {name!r}")
    if not isinstance(name, str) or not SKILL_NAME_RE.fullmatch(name) or len(name) > 64:
        errors.append("SKILL.md name must be lowercase kebab-case and at most 64 characters")
    if root.name != SKILL_NAME:
        errors.append(f"skill directory must be named '{SKILL_NAME}', got '{root.name}'")

    if not isinstance(description, str) or not description.strip():
        errors.append("SKILL.md description must be a non-empty string")
    else:
        if len(description) > 1024:
            errors.append("SKILL.md description must be at most 1024 characters")
        lowered = description.casefold()
        if "repository" not in lowered or "resume" not in lowered:
            errors.append("SKILL.md description must identify repository-to-resume use")
        if "ordinary code review" not in lowered:
            errors.append("SKILL.md description must exclude ordinary code review")

    if license_id != "Apache-2.0":
        errors.append("SKILL.md frontmatter license must be Apache-2.0")
    if not body.strip():
        errors.append("SKILL.md body must be non-empty")
    if len(text.encode("utf-8")) > 24_000:
        errors.append("SKILL.md exceeds the 24 KB maintainability budget")

    required_body_signals = (
        "Repository-first",
        "只有 JD",
        "1–5 条",
        "安全边界",
        "测试源码存在",
    )
    for signal in required_body_signals:
        if signal not in body:
            errors.append(f"SKILL.md is missing required contract signal: {signal}")

    return errors


def _validate_openai_yaml(root: Path) -> list[str]:
    path = root / "agents/openai.yaml"
    if not path.exists():
        return ["missing required file: agents/openai.yaml"]

    data, errors = _load_yaml(path, root)
    if errors:
        return errors
    if not isinstance(data, dict):
        return ["agents/openai.yaml must contain a mapping"]

    interface = data.get("interface")
    policy = data.get("policy")
    if not isinstance(interface, dict):
        errors.append("agents/openai.yaml interface must be a mapping")
    else:
        for key in ("display_name", "short_description", "default_prompt"):
            if not isinstance(interface.get(key), str) or not interface[key].strip():
                errors.append(f"agents/openai.yaml interface.{key} must be non-empty")
        if "$project-to-resume" not in str(interface.get("default_prompt", "")):
            errors.append("agents/openai.yaml default_prompt must invoke $project-to-resume")

    if not isinstance(policy, dict):
        errors.append("agents/openai.yaml policy must be a mapping")
    elif policy.get("allow_implicit_invocation") is not True:
        errors.append("agents/openai.yaml must keep allow_implicit_invocation: true")

    return errors


def _validate_markdown(path: Path, root: Path) -> list[str]:
    text = _read(path)
    rel = _relative(path, root)
    errors: list[str] = []

    for marker in ("<<<<<<<", "=======", ">>>>>>>"):
        if marker in text:
            errors.append(f"{rel} contains a merge-conflict marker")
    if "\x00" in text:
        errors.append(f"{rel} contains a NUL byte")

    fence: str | None = None
    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.lstrip()
        match = re.match(r"(`{3,}|~{3,})", stripped)
        if not match:
            continue
        marker = match.group(1)
        family = marker[0]
        if fence is None:
            fence = family
        elif fence == family:
            fence = None
    if fence is not None:
        errors.append(f"{rel} has an unbalanced fenced code block")

    for raw_target in MARKDOWN_LINK_RE.findall(text):
        target = raw_target.strip().split()[0].strip("<>")
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = unquote(target.split("#", 1)[0])
        if not target:
            continue
        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(root.resolve())
        except ValueError:
            errors.append(f"{rel} links outside the skill package: {raw_target}")
            continue
        if not resolved.exists():
            errors.append(f"{rel} has a broken local link: {raw_target}")

    return errors


def _validate_eval_case(
    path: Path,
    root: Path,
    schema_validator: Draft202012Validator,
) -> tuple[list[str], set[str], str | None]:
    rel = _relative(path, root)
    data, errors = _load_yaml(path, root)
    if errors:
        return errors, set(), None
    if not isinstance(data, dict):
        return [f"{rel} must contain an object"], set(), None

    for error in sorted(schema_validator.iter_errors(data), key=lambda item: list(item.absolute_path)):
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        errors.append(f"{rel} schema violation at {location}: {error.message}")

    case_id = data.get("case_id") if isinstance(data.get("case_id"), str) else None
    coverage = {
        item for item in data.get("coverage", []) if isinstance(item, str) and item
    }

    repository = data.get("repository")
    if isinstance(repository, dict):
        url = repository.get("url")
        commit = repository.get("commit")
        if not isinstance(url, str) or not REPOSITORY_URL_RE.fullmatch(url):
            errors.append(f"{rel} repository.url must be a GitHub repository URL")
        if not isinstance(commit, str) or not FULL_SHA_RE.fullmatch(commit):
            errors.append(f"{rel} repository.commit must be a full 40-character SHA")

    anchors = data.get("evidence_anchors")
    if isinstance(anchors, list):
        for index, anchor in enumerate(anchors):
            if not isinstance(anchor, dict):
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

    if data.get("curated_gold") and data.get("actual_skill_run"):
        errors.append(f"{rel} cannot mark curated gold as an actual skill run")

    return errors, coverage, case_id


def _validate_evals(root: Path) -> list[str]:
    schema_path = root / "evals/schema.json"
    schema, errors = _load_json(schema_path, root)
    if errors:
        return errors
    if not isinstance(schema, dict):
        return ["evals/schema.json must define an object schema"]

    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        return [f"evals/schema.json is not a valid Draft 2020-12 schema: {exc.message}"]

    required = schema.get("required")
    properties = schema.get("properties")
    if not isinstance(required, list) or not EVAL_REQUIRED_FIELDS.issubset(required):
        errors.append("evals/schema.json required fields do not cover the eval contract")
    if not isinstance(properties, dict) or not EVAL_REQUIRED_FIELDS.issubset(properties):
        errors.append("evals/schema.json properties do not cover the eval contract")

    validator = Draft202012Validator(schema)
    case_paths = sorted((root / "evals/cases").glob("*.yaml"))
    if len(case_paths) < 5:
        errors.append("evals/cases must contain at least 5 representative cases")

    seen_coverage: set[str] = set()
    seen_case_ids: set[str] = set()
    for path in case_paths:
        case_errors, coverage, case_id = _validate_eval_case(path, root, validator)
        errors.extend(case_errors)
        seen_coverage.update(coverage)
        if case_id:
            if case_id in seen_case_ids:
                errors.append(f"duplicate eval case_id: {case_id}")
            seen_case_ids.add(case_id)

    missing_coverage = sorted(EXPECTED_COVERAGE - seen_coverage)
    if missing_coverage:
        errors.append("eval cases are missing required coverage: " + ", ".join(missing_coverage))

    return errors


def _validate_request_data(root: Path) -> list[str]:
    request_dir = root / "evals/requests"
    errors: list[str] = []
    seen_true = False
    seen_false = False
    seen_ids: set[str] = set()
    paths = sorted(request_dir.glob("*.json"))
    if len(paths) < 4:
        errors.append("evals/requests must contain at least 4 trigger fixtures")

    for path in paths:
        rel = _relative(path, root)
        data, load_errors = _load_json(path, root)
        errors.extend(load_errors)
        if load_errors:
            continue
        if not isinstance(data, dict):
            errors.append(f"{rel} must contain an object")
            continue

        for field in ("id", "should_invoke", "request", "expected_reason"):
            if field not in data:
                errors.append(f"{rel} is missing request field: {field}")
        fixture_id = data.get("id")
        if isinstance(fixture_id, str):
            if fixture_id in seen_ids:
                errors.append(f"duplicate request fixture id: {fixture_id}")
            seen_ids.add(fixture_id)
        if isinstance(data.get("should_invoke"), bool):
            seen_true |= data["should_invoke"]
            seen_false |= not data["should_invoke"]
        else:
            errors.append(f"{rel} should_invoke must be boolean")
        if not isinstance(data.get("request"), str) or not data.get("request", "").strip():
            errors.append(f"{rel} request must be non-empty")
        if not isinstance(data.get("expected_reason"), str) or not data.get("expected_reason", "").strip():
            errors.append(f"{rel} expected_reason must be non-empty")

    if not seen_true:
        errors.append("eval request data must include at least one positive trigger")
    if not seen_false:
        errors.append("eval request data must include at least one negative trigger")
    return errors


def _validate_project_hygiene(root: Path) -> list[str]:
    errors: list[str] = []
    for path in root.rglob("*"):
        try:
            relative = path.relative_to(root)
        except ValueError:
            continue
        if any(part in IGNORED_DIRS for part in relative.parts):
            continue
        if path.is_dir() and path.name in PROHIBITED_DIRS:
            errors.append(f"generated directory must not be committed: {relative.as_posix()}")
        if path.is_file() and (path.name in PROHIBITED_FILES or path.suffix == ".pyc"):
            errors.append(f"generated file must not be committed: {relative.as_posix()}")

    license_text = _read(root / "LICENSE") if (root / "LICENSE").exists() else ""
    if "Apache License" not in license_text or "Version 2.0" not in license_text:
        errors.append("LICENSE must contain the Apache License 2.0 text")

    changelog = _read(root / "CHANGELOG.md") if (root / "CHANGELOG.md").exists() else ""
    if "## [Unreleased]" not in changelog:
        errors.append("CHANGELOG.md must contain an [Unreleased] section")

    readme = _read(root / "README.md") if (root / "README.md").exists() else ""
    for phrase in STALE_README_PHRASES:
        if phrase in readme:
            errors.append(f"README.md contains stale branch/PR text: {phrase}")
    for required_link_text in (
        "docs/installation.md",
        "docs/evaluation.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "LICENSE",
    ):
        if required_link_text not in readme:
            errors.append(f"README.md must link to {required_link_text}")

    return errors


def validate_tree(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []

    for rel in REQUIRED_PATHS:
        if not (root / rel).exists():
            errors.append(f"missing required file: {rel}")

    # Avoid secondary exceptions when validating a deliberately incomplete copy.
    if (root / "SKILL.md").exists():
        errors.extend(_validate_skill(root))
    if (root / "agents/openai.yaml").exists():
        errors.extend(_validate_openai_yaml(root))

    for path in sorted(_iter_files(root)):
        if path.suffix.lower() == ".md":
            errors.extend(_validate_markdown(path, root))
        elif path.suffix.lower() in {".yml", ".yaml"}:
            _, yaml_errors = _load_yaml(path, root)
            errors.extend(yaml_errors)
        elif path.suffix.lower() == ".json":
            _, json_errors = _load_json(path, root)
            errors.extend(json_errors)

    if (root / "evals/schema.json").exists():
        errors.extend(_validate_evals(root))
    if (root / "evals/requests").exists():
        errors.extend(_validate_request_data(root))
    if (root / "LICENSE").exists() and (root / "CHANGELOG.md").exists() and (root / "README.md").exists():
        errors.extend(_validate_project_hygiene(root))

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
    print("package contracts valid (deterministic checks only)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
