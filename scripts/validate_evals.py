#!/usr/bin/env python3
"""Validate repository-discovery eval cases and invocation fixtures."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
FIXED_GITHUB_ANCHOR_RE = re.compile(
    r"^https://github\.com/[^/]+/[^/]+/(?:blob|commit)/[0-9a-f]{40}(?:/.*)?$"
)
EXPECTED_COVERAGE = {
    "readme-strong-implementation-ordinary",
    "test-reveals-failure-story",
    "only-two-strong-stories",
    "fork-or-upstream",
    "public-repo-ownership-unknown",
    "historical-benchmark-stale",
}


def _load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _location(error: Any) -> str:
    parts = [str(part) for part in error.absolute_path]
    return ".".join(parts) if parts else "<root>"


def validate_eval_contracts(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    schema_path = root / "evals/schema.json"
    case_dir = root / "evals/cases"
    request_dir = root / "evals/requests"

    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return [f"evals/schema.json is invalid: {exc}"]

    validator = Draft202012Validator(schema)
    case_paths = sorted(case_dir.glob("*.yaml"))
    if len(case_paths) < 5:
        errors.append("evals/cases must contain at least 5 representative cases")

    case_ids: set[str] = set()
    coverage: set[str] = set()
    for path in case_paths:
        rel = path.relative_to(root).as_posix()
        try:
            data = _load_yaml(path)
        except (OSError, yaml.YAMLError) as exc:
            errors.append(f"{rel} is invalid YAML: {exc}")
            continue
        if not isinstance(data, dict):
            errors.append(f"{rel} must contain a mapping")
            continue

        for error in sorted(
            validator.iter_errors(data), key=lambda item: list(item.absolute_path)
        ):
            errors.append(f"{rel}:{_location(error)}: {error.message}")

        case_id = data.get("case_id")
        if isinstance(case_id, str):
            if case_id in case_ids:
                errors.append(f"duplicate eval case_id: {case_id}")
            case_ids.add(case_id)

        values = data.get("coverage")
        if isinstance(values, list):
            coverage.update(item for item in values if isinstance(item, str))

        repository = data.get("repository")
        if isinstance(repository, dict):
            commit = repository.get("commit")
            if isinstance(commit, str) and not FULL_SHA_RE.fullmatch(commit):
                errors.append(f"{rel}: repository.commit must be a full 40-character SHA")

        anchors = data.get("evidence_anchors")
        if isinstance(anchors, list):
            for index, anchor in enumerate(anchors):
                if not isinstance(anchor, dict):
                    continue
                url = anchor.get("url")
                if isinstance(url, str) and not FIXED_GITHUB_ANCHOR_RE.fullmatch(url):
                    errors.append(
                        f"{rel}: evidence_anchors[{index}].url must pin a full GitHub commit"
                    )

        if data.get("curated_gold") and data.get("actual_skill_run"):
            errors.append(f"{rel}: curated gold must not be represented as an actual skill run")

    missing = sorted(EXPECTED_COVERAGE - coverage)
    if missing:
        errors.append("eval cases are missing required coverage: " + ", ".join(missing))

    request_ids: set[str] = set()
    seen_positive = False
    seen_negative = False
    request_paths = sorted(request_dir.glob("*.json"))
    if not request_paths:
        errors.append("evals/requests must contain invocation fixtures")

    for path in request_paths:
        rel = path.relative_to(root).as_posix()
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{rel} is invalid JSON: {exc}")
            continue
        if not isinstance(data, dict):
            errors.append(f"{rel} must contain an object")
            continue

        for field in ("id", "should_invoke", "request", "expected_reason"):
            if field not in data:
                errors.append(f"{rel} is missing request field: {field}")

        request_id = data.get("id")
        if isinstance(request_id, str):
            if request_id in request_ids:
                errors.append(f"duplicate request fixture id: {request_id}")
            request_ids.add(request_id)

        should_invoke = data.get("should_invoke")
        if isinstance(should_invoke, bool):
            seen_positive |= should_invoke
            seen_negative |= not should_invoke
        else:
            errors.append(f"{rel}: should_invoke must be boolean")

        for field in ("request", "expected_reason"):
            value = data.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{rel}: {field} must be a non-empty string")

    if not seen_positive:
        errors.append("invocation fixtures must include a positive request")
    if not seen_negative:
        errors.append("invocation fixtures must include a negative request")
    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).parents[1])
    args = parser.parse_args()
    errors = validate_eval_contracts(args.root)
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        return 1
    print("eval contracts valid (schema and deterministic cross-file checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
