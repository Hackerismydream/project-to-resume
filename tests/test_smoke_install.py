from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills/project-to-resume"
SPEC = importlib.util.spec_from_file_location(
    "smoke_install", ROOT / "scripts/smoke_install.py"
)
assert SPEC is not None and SPEC.loader is not None
SMOKE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SMOKE)


class SmokeInstallTest(unittest.TestCase):
    def test_isolated_install_contains_complete_runtime_payload(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "project-to-resume"
            summary = SMOKE.install_skill(ROOT, destination)
            for rel in (
                "SKILL.md",
                "LICENSE",
                "agents/openai.yaml",
                "references/repository-discovery.md",
                "examples/pico-empty-response-recovery.md",
            ):
                self.assertTrue((destination / rel).is_file(), rel)
            for rel in ("tests", "evals", ".github", "scripts"):
                self.assertFalse((destination / rel).exists(), rel)
            self.assertEqual(summary["files"], sum(1 for path in SKILL_ROOT.rglob("*") if path.is_file()))
            self.assertEqual(summary["references"], len(list((SKILL_ROOT / "references").glob("*.md"))))
            self.assertEqual(summary["examples"], len(list((SKILL_ROOT / "examples").glob("*.md"))))
            self.assertEqual(summary["agent_configs"], 1)

    def test_wrong_or_nested_destination_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaisesRegex(ValueError, "project-to-resume"):
                SMOKE.install_skill(ROOT, Path(temp_dir) / "wrong-name")
        with self.assertRaisesRegex(ValueError, "outside the source repository"):
            SMOKE.install_skill(ROOT, ROOT / "tmp/project-to-resume")


if __name__ == "__main__":
    unittest.main()
