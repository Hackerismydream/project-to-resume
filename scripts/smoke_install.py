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

    shutil.copytree(skill_source, destination)
    validator = _load_validator(repo_root)
    errors = validator.validate_skill(destination)
    if errors:
        raise RuntimeError("installed Skill validation failed:\n" + "\n".join(errors))

    return {
        "files": sum(1 for path in destination.rglob("*") if path.is_file()),
        "references": len(list((destination / "references").glob("*.md"))),
        "examples": len(list((destination / "examples").glob("*.md"))),
        "agent_configs": len(list((destination / "agents").glob("*.yaml"))),
    }


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
