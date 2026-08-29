from __future__ import annotations

import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "smoke_install", ROOT / "scripts" / "smoke_install.py"
)
assert SPEC is not None and SPEC.loader is not None
SMOKE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SMOKE)


class SmokeInstallTest(unittest.TestCase):
    def test_isolated_install_contains_and_validates_package(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "project-to-resume"
            summary = SMOKE.install_skill(ROOT, destination)

            required = (
                "SKILL.md",
                "LICENSE",
                "CONTRIBUTING.md",
                "SECURITY.md",
                "agents/openai.yaml",
                "references/repository-discovery.md",
                "examples/pico-empty-response-recovery.md",
                "scripts/validate_package.py",
                "evals/schema.json",
                "docs/installation.md",
                "docs/evaluation.md",
                ".github/PULL_REQUEST_TEMPLATE.md",
            )
            for relative in required:
                self.assertTrue((destination / relative).is_file(), relative)

            self.assertGreaterEqual(summary["references"], 10)
            self.assertGreaterEqual(summary["examples"], 5)
            self.assertEqual(summary["eval_cases"], 5)
            self.assertEqual(summary["request_fixtures"], 4)
            self.assertEqual(summary["governance_files"], 5)

    def test_wrong_destination_name_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaisesRegex(ValueError, "project-to-resume"):
                SMOKE.install_skill(ROOT, Path(temp_dir) / "wrong-name")

    def test_overlapping_destination_is_rejected(self) -> None:
        destination = ROOT / "tmp" / "project-to-resume"
        with self.assertRaisesRegex(ValueError, "must not overlap"):
            SMOKE.install_skill(ROOT, destination)

    def test_generated_caches_are_not_installed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "source" / "project-to-resume"
            shutil.copytree(
                ROOT,
                source,
                ignore=shutil.ignore_patterns("__pycache__", ".git", ".venv"),
            )
            cache = source / "scripts/__pycache__"
            cache.mkdir()
            (cache / "generated.pyc").write_bytes(b"generated")
            (source / ".DS_Store").write_bytes(b"generated")

            destination = Path(temp_dir) / "installed" / "project-to-resume"
            summary = SMOKE.install_skill(source, destination)

            self.assertFalse((destination / "scripts/__pycache__").exists())
            self.assertFalse((destination / ".DS_Store").exists())
            self.assertEqual(summary["governance_files"], 5)


if __name__ == "__main__":
    unittest.main()
