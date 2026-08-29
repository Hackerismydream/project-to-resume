from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_package", ROOT / "scripts" / "validate_package.py"
)
assert SPEC is not None and SPEC.loader is not None
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class ValidatePackageTest(unittest.TestCase):
    def copied_package(self):
        temp = tempfile.TemporaryDirectory()
        destination = Path(temp.name) / "project-to-resume"
        shutil.copytree(ROOT, destination, ignore=shutil.ignore_patterns("__pycache__", ".git"))
        return temp, destination

    def test_real_package_validates(self) -> None:
        self.assertEqual(VALIDATOR.validate_tree(ROOT), [])

    def test_missing_required_file_is_rejected(self) -> None:
        temp, package = self.copied_package()
        self.addCleanup(temp.cleanup)
        (package / "references/story-selection.md").unlink()
        errors = VALIDATOR.validate_tree(package)
        self.assertIn("missing required file: references/story-selection.md", errors)

    def test_broken_local_markdown_link_is_rejected(self) -> None:
        temp, package = self.copied_package()
        self.addCleanup(temp.cleanup)
        with (package / "README.md").open("a", encoding="utf-8") as handle:
            handle.write("\n[broken](docs/missing.md)\n")
        errors = VALIDATOR.validate_tree(package)
        self.assertTrue(any("broken local link" in error for error in errors), errors)

    def test_eval_commit_must_be_full_sha(self) -> None:
        temp, package = self.copied_package()
        self.addCleanup(temp.cleanup)
        path = package / "evals/cases/pico-empty-response-recovery.yaml"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["repository"]["commit"] = "abc123"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        errors = VALIDATOR.validate_tree(package)
        self.assertTrue(any("full 40-character SHA" in error for error in errors), errors)

    def test_evidence_anchor_must_pin_commit(self) -> None:
        temp, package = self.copied_package()
        self.addCleanup(temp.cleanup)
        path = package / "evals/cases/pico-empty-response-recovery.yaml"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["evidence_anchors"][0]["url"] = "https://github.com/Hackerismydream/pico/blob/main/README.md"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        errors = VALIDATOR.validate_tree(package)
        self.assertTrue(any("must pin a full GitHub commit" in error for error in errors), errors)

    def test_eval_questions_are_capped_at_three(self) -> None:
        temp, package = self.copied_package()
        self.addCleanup(temp.cleanup)
        path = package / "evals/cases/pico-empty-response-recovery.yaml"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["expected_questions"] = ["1", "2", "3", "4"]
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        errors = VALIDATOR.validate_tree(package)
        self.assertTrue(any("at most 3" in error for error in errors), errors)

    def test_skill_directory_name_is_checked(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        destination = Path(temp.name) / "wrong-name"
        shutil.copytree(ROOT, destination, ignore=shutil.ignore_patterns("__pycache__", ".git"))
        errors = VALIDATOR.validate_tree(destination)
        self.assertTrue(any("skill directory must be named" in error for error in errors), errors)

    def test_trigger_fixtures_contain_positive_and_negative_requests(self) -> None:
        fixtures = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in sorted((ROOT / "evals/requests").glob("*.json"))
        ]
        self.assertTrue(any(item["should_invoke"] for item in fixtures))
        self.assertTrue(any(not item["should_invoke"] for item in fixtures))
        negative_requests = "\n".join(
            item["request"] for item in fixtures if not item["should_invoke"]
        )
        self.assertIn("code review", negative_requests.casefold())

    def test_eval_cases_cover_all_required_scenarios(self) -> None:
        cases = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in sorted((ROOT / "evals/cases").glob("*.yaml"))
        ]
        coverage = {entry for case in cases for entry in case["coverage"]}
        self.assertEqual(VALIDATOR.EXPECTED_COVERAGE - coverage, set())
        self.assertTrue(all(case["curated_gold"] for case in cases))
        self.assertTrue(all(not case["actual_skill_run"] for case in cases))


if __name__ == "__main__":
    unittest.main()
