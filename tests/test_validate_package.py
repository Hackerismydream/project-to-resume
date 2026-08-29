from __future__ import annotations

import importlib.util
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills/project-to-resume"
SPEC = importlib.util.spec_from_file_location(
    "validate_package", ROOT / "scripts/validate_package.py"
)
assert SPEC is not None and SPEC.loader is not None
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class ValidatePackageTest(unittest.TestCase):
    def copied_repository(self, name: str = "renamed-checkout"):
        temp = tempfile.TemporaryDirectory()
        destination = Path(temp.name) / name
        shutil.copytree(
            ROOT,
            destination,
            ignore=shutil.ignore_patterns("__pycache__", ".git", ".pytest_cache", "*.pyc", ".venv"),
        )
        return temp, destination

    def copied_skill(self, name: str = "project-to-resume"):
        temp = tempfile.TemporaryDirectory()
        destination = Path(temp.name) / name
        shutil.copytree(
            SKILL_ROOT,
            destination,
            ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.pyc"),
        )
        return temp, destination

    def test_real_repository_validates(self) -> None:
        self.assertEqual(VALIDATOR.validate_tree(ROOT), [])

    def test_installed_profile_validates(self) -> None:
        temp, skill = self.copied_skill()
        self.addCleanup(temp.cleanup)
        self.assertEqual(
            VALIDATOR.validate_tree(skill, profile="installed", strict_directory_name=True),
            [],
        )

    def test_repository_checkout_name_is_not_constrained(self) -> None:
        temp, repository = self.copied_repository()
        self.addCleanup(temp.cleanup)
        self.assertEqual(VALIDATOR.validate_tree(repository), [])

    def test_installed_skill_name_can_be_strict(self) -> None:
        temp, skill = self.copied_skill("wrong-name")
        self.addCleanup(temp.cleanup)
        errors = VALIDATOR.validate_tree(skill, profile="installed", strict_directory_name=True)
        self.assertTrue(any("must be named" in error for error in errors), errors)

    def test_root_payload_duplicate_is_rejected(self) -> None:
        temp, repository = self.copied_repository()
        self.addCleanup(temp.cleanup)
        (repository / "SKILL.md").write_text("duplicate\n", encoding="utf-8")
        errors = VALIDATOR.validate_tree(repository)
        self.assertTrue(any("canonical payload" in error for error in errors), errors)

    def test_truncated_skill_is_rejected(self) -> None:
        temp, repository = self.copied_repository()
        self.addCleanup(temp.cleanup)
        (repository / "skills/project-to-resume/SKILL.md").write_text("test\n", encoding="utf-8")
        errors = VALIDATOR.validate_tree(repository)
        self.assertTrue(any("frontmatter" in error for error in errors), errors)

    def test_frontmatter_contract_is_enforced(self) -> None:
        temp, repository = self.copied_repository()
        self.addCleanup(temp.cleanup)
        path = repository / "skills/project-to-resume/SKILL.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace("license: Apache-2.0", "license: Proprietary", 1)
        path.write_text(text, encoding="utf-8")
        errors = VALIDATOR.validate_tree(repository)
        self.assertIn("SKILL.md license must be Apache-2.0", errors)

    def test_description_limit_is_enforced(self) -> None:
        temp, repository = self.copied_repository()
        self.addCleanup(temp.cleanup)
        path = repository / "skills/project-to-resume/SKILL.md"
        data, body, error = VALIDATOR._load_frontmatter(path)
        self.assertIsNone(error)
        assert data is not None
        data["description"] = "repository resume " + "x" * 1100
        frontmatter = yaml.safe_dump(data, allow_unicode=True, sort_keys=False).strip()
        path.write_text(f"---\n{frontmatter}\n---\n\n{body}\n", encoding="utf-8")
        errors = VALIDATOR.validate_tree(repository)
        self.assertIn("SKILL.md description must be at most 1024 characters", errors)

    def test_missing_required_skill_file_is_rejected(self) -> None:
        temp, repository = self.copied_repository()
        self.addCleanup(temp.cleanup)
        (repository / "skills/project-to-resume/LICENSE").unlink()
        errors = VALIDATOR.validate_tree(repository)
        self.assertTrue(any("missing installed Skill file: LICENSE" in error for error in errors), errors)

    def test_broken_local_markdown_link_is_rejected(self) -> None:
        temp, repository = self.copied_repository()
        self.addCleanup(temp.cleanup)
        with (repository / "README.md").open("a", encoding="utf-8") as handle:
            handle.write("\n[broken](docs/missing.md)\n")
        errors = VALIDATOR.validate_tree(repository)
        self.assertTrue(any("broken local link" in error for error in errors), errors)

    def test_readme_pre_release_text_is_rejected(self) -> None:
        temp, repository = self.copied_repository()
        self.addCleanup(temp.cleanup)
        with (repository / "README.md").open("a", encoding="utf-8") as handle:
            handle.write("\nstacked Draft PR codex/repository-discovery-v2\n")
        errors = VALIDATOR.validate_tree(repository)
        self.assertTrue(any("pre-release branch text" in error for error in errors), errors)

    def test_generated_artifacts_are_rejected_when_tracked(self) -> None:
        temp, repository = self.copied_repository()
        self.addCleanup(temp.cleanup)
        subprocess.run(["git", "init", "-q", str(repository)], check=True)
        cache = repository / "scripts/__pycache__"
        cache.mkdir()
        artifact = cache / "validator.pyc"
        artifact.write_bytes(b"x")
        subprocess.run(
            ["git", "-C", str(repository), "add", "-f", artifact.relative_to(repository).as_posix()],
            check=True,
        )
        errors = VALIDATOR.validate_tree(repository)
        self.assertTrue(any("generated artifact" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
