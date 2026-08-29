#!/usr/bin/env python3
"""Copy only the runtime Skill payload into an isolated directory and validate it."""

from __future__ import annotations

import argparse
import importlib.util
import shutil
import tempfile
from pathlib import Path

SKILL_NAME = "project-to-resume"


def _load_validator(repo_root: Path):
    script = repo_root / "scripts/validate_package.py"
    spec = importlib.util.spec_from_file_location("validate_package", script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load validator: {script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _summary(root: Path) -> dict[str, int]:
    return {
        "files": sum(1 for path in root.rglob("*") if path.is_file()),
        "references": len(list((root / "references").glob("*.md"))),
        "examples": len(list((root / "examples").glob("*.md"))),
        "agent_configs": len(list((root / "agents").glob("*.yaml"))),
    }


def install_skill(source: Path, destination: Path) -> dict[str, int]:
    repo_root = source.resolve()
    skill_source = repo_root / "skills" / SKILL_NAME
    destination = destination.resolve()

    if not skill_source.is_dir():
        raise FileNotFoundError(skill_source)
    if destination.name != SKILL_NAME:
        raise ValueError(f"destination directory must be named '{SKILL_NAME}'")
    if destination.exists():
        raise FileExistsError(destination)
    if destination == repo_root or _is_relative_to(destination, repo_root):
        raise ValueError("destination must be outside the source repository")

    shutil.copytree(
        skill_source,
        destination,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache"),
    )
    validator = _load_validator(repo_root)
    errors = validator.validate_tree(
        destination,
        profile="installed",
        strict_directory_name=True,
    )
    if errors:
        raise RuntimeError("installed Skill validation failed:\n" + "\n".join(errors))

    source_summary = _summary(skill_source)
    installed_summary = _summary(destination)
    if source_summary != installed_summary:
        raise RuntimeError(
            "installed Skill differs from canonical payload: "
            f"source={source_summary}, installed={installed_summary}"
        )
    return installed_summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path(__file__).parents[1])
    parser.add_argument("--destination", type=Path)
    args = parser.parse_args()

    if args.destination:
        summary = install_skill(args.source, args.destination)
        print(f"isolated Skill install valid: {args.destination.resolve()}")
    else:
        with tempfile.TemporaryDirectory(prefix="project-to-resume-smoke-") as temp_dir:
            destination = Path(temp_dir) / SKILL_NAME
            summary = install_skill(args.source, destination)
            print("isolated Skill install valid: temporary project-to-resume directory")

    print(" ".join(f"{key}={value}" for key, value in summary.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
