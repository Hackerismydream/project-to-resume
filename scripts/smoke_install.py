#!/usr/bin/env python3
"""Copy the Skill into an isolated directory and validate installed contents.

The public skills installer copies a Skill directory recursively. This smoke
test mirrors that package-level behavior without requiring network access,
while excluding repository metadata and generated caches.
"""

from __future__ import annotations

import argparse
import importlib.util
import shutil
import tempfile
from pathlib import Path


EXCLUDED_NAMES = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    "__pypackages__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".DS_Store",
}


def _load_validator(source: Path):
    script = source / "scripts/validate_package.py"
    spec = importlib.util.spec_from_file_location("validate_package", script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load validator: {script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _ignored(_directory: str, names: list[str]) -> set[str]:
    return {
        name
        for name in names
        if name in EXCLUDED_NAMES or name.endswith(".pyc")
    }


def _is_inside(parent: Path, child: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def install_skill(source: Path, destination: Path) -> dict[str, int]:
    source = source.resolve()
    destination = destination.resolve()

    if destination.name != "project-to-resume":
        raise ValueError("destination directory must be named 'project-to-resume'")
    if destination.exists():
        raise FileExistsError(destination)
    if _is_inside(source, destination) or _is_inside(destination, source):
        raise ValueError("source and destination must not overlap")

    shutil.copytree(
        source,
        destination,
        ignore=_ignored,
        symlinks=False,
    )

    validator = _load_validator(destination)
    errors = validator.validate_tree(destination)
    if errors:
        raise RuntimeError("installed package validation failed:\n" + "\n".join(errors))

    return {
        "references": len(list((destination / "references").glob("*.md"))),
        "examples": len(list((destination / "examples").glob("*.md"))),
        "scripts": len(list((destination / "scripts").glob("*.py"))),
        "eval_cases": len(list((destination / "evals/cases").glob("*.yaml"))),
        "request_fixtures": len(list((destination / "evals/requests").glob("*.json"))),
        "governance_files": sum(
            (destination / name).exists()
            for name in (
                "LICENSE",
                "CHANGELOG.md",
                "CONTRIBUTING.md",
                "CODE_OF_CONDUCT.md",
                "SECURITY.md",
            )
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path(__file__).parents[1])
    parser.add_argument("--destination", type=Path)
    args = parser.parse_args()

    if args.destination:
        summary = install_skill(args.source, args.destination)
        print(f"isolated install valid: {args.destination.resolve()}")
        print(" ".join(f"{key}={value}" for key, value in summary.items()))
        return 0

    with tempfile.TemporaryDirectory(prefix="project-to-resume-smoke-") as temp_dir:
        destination = Path(temp_dir) / "project-to-resume"
        summary = install_skill(args.source, destination)
        print("isolated install valid: temporary project-to-resume directory")
        print(" ".join(f"{key}={value}" for key, value in summary.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
