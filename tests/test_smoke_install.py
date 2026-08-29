from __future__ import annotations

import importlib.util
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
            self.assertTrue((destination / "SKILL.md").is_file())
            self.assertTrue((destination / "agents/openai.yaml").is_file())
            self.assertTrue((destination / "references/repository-discovery.md").is_file())
            self.assertTrue((destination / "examples/pico-empty-response-recovery.md").is_file())
            self.assertTrue((destination / "scripts/validate_package.py").is_file())
            self.assertTrue((destination / "evals/schema.json").is_file())
            self.assertTrue((destination / "docs/assets/repository-to-resume-before-after.svg").is_file())
            self.assertGreaterEqual(summary["references"], 10)
            self.assertGreaterEqual(summary["examples"], 5)
            self.assertEqual(summary["eval_cases"], 5)
            self.assertEqual(summary["request_fixtures"], 4)

    def test_wrong_destination_name_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaisesRegex(ValueError, "project-to-resume"):
                SMOKE.install_skill(ROOT, Path(temp_dir) / "wrong-name")


if __name__ == "__main__":
    unittest.main()
