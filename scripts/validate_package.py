#!/usr/bin/env python3
"""Validate the project-to-resume repository and installed Skill payload.

The checks prove package shape, local consistency, and explicit contracts. They
do not prove semantic story quality, factual attribution, model behavior, or
resume outcomes.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from validate_evals import validate_eval_contracts  # noqa: E402

SKILL_NAME = "project-to-resume"
SKILL_REL = Path("skills") / SKILL_NAME
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*]\(([^)]+)\)")
FORBIDDEN_ARTIFACT_PARTS = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".DS_Store",
    ".venv",
}
FORBIDDEN_ARTIFACT_SUFFIXES = {".pyc", ".pyo"}

SKILL_REQUIRED = (
    "SKILL.md",
    "LICENSE",
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
    "examples/repository-only.md",
    "examples/resume-and-repository.md",
    "examples/resume-only.md",
    "examples/multi-project-jd.md",
    "examples/pico-empty-response-recovery.md",
)
REPOSITORY_REQUIRED = (
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "Makefile",
    "requirements-dev.txt",
    ".gitignore",
    ".github/workflows/validate.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/ISSUE_TEMPLATE/showcase.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/dependabot.yml",
    "docs/evaluation.md",
    "docs/assets/repository-to-resume-before-after.svg",
    "evals/README.md",
    "evals/rubric.md",
    "evals/schema.json",
    "scripts/lint_examples.py",
    "scripts/validate_package.py",
    "scripts/validate_evals.py",
    "scripts/smoke_install.py",
    "showcase/README.md",
    "tests/test_lint_examples.py",
    "tests/test_validate_package.py",
    "tests/test_validate_evals.py",
    "tests/test_smoke_install.py",
)
REQUIRED_SKILL_LINKS = {
    "references/repository-discovery.md",
    "references/story-selection.md",
    "references/claims-and-metrics.md",
    "references/resume-format.md",
}
REQUIRED_SKILL_MARKERS = (
    "## 默认交付",
    "## 核心工作流",
    "## 必要追问",
    "## 安全边界",
    "## 完成标准",
)
ROOT_PAYLOAD_DUPLICATES = ("SKILL.md", "agents", "references", "examples")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_frontmatter(path: Path) -> tuple[dict[str, object] | None, str, str | None]:
    text = _read(path)
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text, "missing opening YAML frontmatter delimiter"
    try:
        end = next(
            index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"
        )
    except StopIteration:
        return None, text, "missing closing YAML frontmatter delimiter"

    raw = "\n".join(lines[1:end])
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        return None, text, f"invalid YAML frontmatter: {exc}"
    if not isinstance(data, dict):
        return None, text, "frontmatter must be a mapping"
    body = "\n".join(lines[end + 1 :]).strip()
    return data, body, None


def _validate_markdown(path: Path, boundary: Path) -> list[str]:
    text = _read(path)
    rel = path.relative_to(boundary).as_posix()
    errors: list[str] = []
    for marker in ("<<<<<<<", "=======", ">>>>>>>"):
        if marker in text:
            errors.append(f"{rel} contains a merge-conflict marker")
    if "\x00" in text:
        errors.append(f"{rel} contains a NUL byte")

    fence: str | None = None
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            token = stripped[:3]
            if fence is None:
                fence = token
            elif token == fence:
                fence = None
    if fence is not None:
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


def _validate_serialized_files(root: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(root.rglob("*.json")):
        try:
            json.loads(_read(path))
        except json.JSONDecodeError as exc:
            errors.append(f"{path.relative_to(root).as_posix()} is invalid JSON: {exc}")
    for path in sorted(root.rglob("*.yml")) + sorted(root.rglob("*.yaml")):
        try:
            yaml.safe_load(_read(path))
        except yaml.YAMLError as exc:
            errors.append(f"{path.relative_to(root).as_posix()} is invalid YAML: {exc}")
    return errors


def _validate_license(path: Path, rel: str) -> list[str]:
    if not path.exists():
        return [f"missing required file: {rel}"]
    text = _read(path)
    if "Apache License" not in text or "Version 2.0, January 2004" not in text:
        return [f"{rel} is not the Apache License 2.0 text"]
    return []


def validate_skill(skill_root: Path, *, strict_directory_name: bool = True) -> list[str]:
    skill_root = skill_root.resolve()
    errors: list[str] = []
    for rel in SKILL_REQUIRED:
        if not (skill_root / rel).exists():
            errors.append(f"missing installed Skill file: {rel}")
    if strict_directory_name and skill_root.name != SKILL_NAME:
        errors.append(f"Skill directory must be named '{SKILL_NAME}'")

    skill_md = skill_root / "SKILL.md"
    if skill_md.exists():
        data, body, error = _load_frontmatter(skill_md)
        if error:
            errors.append(f"SKILL.md {error}")
        else:
            assert data is not None
            name = data.get("name")
            if name != SKILL_NAME:
                errors.append("SKILL.md name does not match Skill directory")
            if not isinstance(name, str) or len(name) > 64 or not NAME_RE.fullmatch(name):
                errors.append("SKILL.md name must be 1–64 lowercase letters, digits, and hyphens")

            description = data.get("description")
            if not isinstance(description, str) or not description.strip():
                errors.append("SKILL.md description must be non-empty")
            elif len(description) > 1024:
                errors.append("SKILL.md description must be at most 1024 characters")
            else:
                lowered = description.casefold()
                if "repository" not in lowered or "resume" not in lowered:
                    errors.append("SKILL.md description must state the repository-to-resume purpose")
                if not any(term in lowered for term in ("code review", "debugging", "summaries")):
                    errors.append("SKILL.md description must include a negative routing boundary")

            if data.get("license") != "Apache-2.0":
                errors.append("SKILL.md license must be Apache-2.0")
            compatibility = data.get("compatibility")
            if not isinstance(compatibility, str) or not compatibility.strip():
                errors.append("SKILL.md compatibility must be non-empty")
            elif len(compatibility) > 500:
                errors.append("SKILL.md compatibility must be at most 500 characters")

            metadata = data.get("metadata")
            if not isinstance(metadata, dict):
                errors.append("SKILL.md metadata must be a mapping")
            elif not all(
                isinstance(key, str) and isinstance(value, str)
                for key, value in metadata.items()
            ):
                errors.append("SKILL.md metadata keys and values must be strings")

            if len(body) < 2500:
                errors.append("SKILL.md body is unexpectedly short; possible truncation")
            if len(body.splitlines()) > 500:
                errors.append("SKILL.md body must stay under 500 lines")
            for marker in REQUIRED_SKILL_MARKERS:
                if marker not in body:
                    errors.append(f"SKILL.md is missing required section: {marker}")

            linked_targets = {
                unquote(target.split("#", 1)[0].strip().split()[0].strip("<>"))
                for target in MARKDOWN_LINK_RE.findall(body)
                if target and not target.startswith(("http://", "https://", "mailto:", "#"))
            }
            missing_links = sorted(REQUIRED_SKILL_LINKS - linked_targets)
            if missing_links:
                errors.append(
                    "SKILL.md is missing required local references: " + ", ".join(missing_links)
                )

    openai = skill_root / "agents/openai.yaml"
    if openai.exists():
        try:
            data = yaml.safe_load(_read(openai))
        except yaml.YAMLError as exc:
            errors.append(f"agents/openai.yaml is invalid YAML: {exc}")
        else:
            if not isinstance(data, dict):
                errors.append("agents/openai.yaml must contain a mapping")
            else:
                interface = data.get("interface")
                policy = data.get("policy")
                if not isinstance(interface, dict):
                    errors.append("agents/openai.yaml interface must be a mapping")
                else:
                    for field in ("display_name", "short_description", "default_prompt"):
                        value = interface.get(field)
                        if not isinstance(value, str) or not value.strip():
                            errors.append(f"agents/openai.yaml interface.{field} must be non-empty")
                    prompt = interface.get("default_prompt")
                    if isinstance(prompt, str) and "$project-to-resume" not in prompt:
                        errors.append("agents/openai.yaml default_prompt must mention $project-to-resume")
                if not isinstance(policy, dict) or policy.get("allow_implicit_invocation") is not True:
                    errors.append("agents/openai.yaml must keep allow_implicit_invocation: true")

    for junk in ("tests", "evals", ".github", "__pycache__", ".pytest_cache"):
        if (skill_root / junk).exists():
            errors.append(f"installed Skill contains development-only path: {junk}")

    errors.extend(_validate_license(skill_root / "LICENSE", "LICENSE"))
    errors.extend(_validate_serialized_files(skill_root))
    for path in sorted(skill_root.rglob("*.md")):
        errors.extend(_validate_markdown(path, skill_root))
    return sorted(set(errors))


def _validate_readme(root: Path) -> list[str]:
    path = root / "README.md"
    if not path.exists():
        return ["missing required file: README.md"]
    text = _read(path)
    errors: list[str] = []
    required = {
        "official install command": "npx skills add Hackerismydream/project-to-resume",
        "explicit Skill selection": "--skill project-to-resume",
        "minimal prompt": "$project-to-resume",
        "evaluation documentation": "docs/evaluation.md",
        "contributing guide": "CONTRIBUTING.md",
        "security policy": "SECURITY.md",
        "changelog": "CHANGELOG.md",
        "license": "LICENSE",
    }
    for label, marker in required.items():
        if marker not in text:
            errors.append(f"README.md is missing {label}")
    for stale in ("stacked Draft PR", "codex/repository-discovery-v2", "仍可能是 `main` 上的旧版"):
        if stale in text:
            errors.append(f"README.md contains pre-release branch text: {stale}")
    return errors


def _validate_artifacts(root: Path) -> list[str]:
    if not (root / ".git").exists():
        return []
    try:
        output = subprocess.check_output(
            ["git", "-C", str(root), "ls-files", "-z"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError):
        return []

    errors: list[str] = []
    for raw in output.split("\0"):
        if not raw:
            continue
        rel = Path(raw)
        if any(part in FORBIDDEN_ARTIFACT_PARTS for part in rel.parts):
            errors.append(f"repository tracks generated artifact: {rel.as_posix()}")
        if rel.suffix in FORBIDDEN_ARTIFACT_SUFFIXES:
            errors.append(f"repository tracks generated artifact: {rel.as_posix()}")
    return errors


def _validate_gitignore(root: Path) -> list[str]:
    path = root / ".gitignore"
    if not path.exists():
        return ["missing required file: .gitignore"]
    text = _read(path)
    required = (
        "__pycache__/",
        "*.py[cod]",
        ".venv/",
        ".pytest_cache/",
        ".agents/",
        "skills-lock.json",
    )
    return [
        f".gitignore is missing generated-artifact pattern: {pattern}"
        for pattern in required
        if pattern not in text
    ]


def validate_repository(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    for duplicate in ROOT_PAYLOAD_DUPLICATES:
        if (root / duplicate).exists():
            errors.append(
                f"repository root must not contain '{duplicate}'; "
                "skills/project-to-resume is the canonical payload"
            )
    for rel in REPOSITORY_REQUIRED:
        if not (root / rel).exists():
            errors.append(f"missing repository file: {rel}")

    errors.extend(validate_skill(root / SKILL_REL))
    errors.extend(_validate_readme(root))
    errors.extend(_validate_license(root / "LICENSE", "LICENSE"))
    errors.extend(_validate_gitignore(root))
    errors.extend(_validate_serialized_files(root))
    errors.extend(_validate_artifacts(root))
    for path in sorted(root.rglob("*.md")):
        errors.extend(_validate_markdown(path, root))
    if (root / "evals/schema.json").exists():
        errors.extend(validate_eval_contracts(root))
    return sorted(set(errors))


def validate_tree(
    root: Path,
    *,
    profile: str = "repository",
    strict_directory_name: bool = False,
) -> list[str]:
    if profile == "repository":
        return validate_repository(root)
    if profile == "installed":
        return validate_skill(root, strict_directory_name=strict_directory_name)
    return [f"unknown validation profile: {profile}"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).parents[1])
    parser.add_argument("--profile", choices=("repository", "installed"), default="repository")
    parser.add_argument("--strict-directory-name", action="store_true")
    args = parser.parse_args()

    errors = validate_tree(
        args.root,
        profile=args.profile,
        strict_directory_name=args.strict_directory_name,
    )
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        return 1
    print(f"{args.profile} package valid (deterministic checks only)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
