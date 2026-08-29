from __future__ import annotations

import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_evals", ROOT / "scripts/validate_evals.py"
)
assert SPEC is not None and SPEC.loader is not None
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class ValidateEvalsTest(unittest.TestCase):
    def copied_repository(self):
        temp = tempfile.TemporaryDirectory()
        destination = Path(temp.name) / "project-to-resume"
        shutil.copytree(
            ROOT,
            destination,
            ignore=shutil.ignore_patterns("__pycache__", ".git", ".pytest_cache", "*.pyc", ".venv"),
        )
        return temp, destination

    def test_real_eval_contracts_validate(self) -> None:
        self.assertEqual(VALIDATOR.validate_eval_contracts(ROOT), [])

    def test_short_commit_is_rejected(self) -> None:
        temp, repository = self.copied_repository()
        self.addCleanup(temp.cleanup)
        path = repository / "evals/cases/pico-empty-response-recovery.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        data["repository"]["commit"] = "abc123"
        path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
        errors = VALIDATOR.validate_eval_contracts(repository)
        self.assertTrue(any("40-character SHA" in error for error in errors), errors)

    def test_unpinned_evidence_anchor_is_rejected(self) -> None:
        temp, repository = self.copied_repository()
        self.addCleanup(temp.cleanup)
        path = repository / "evals/cases/pico-empty-response-recovery.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        data["evidence_anchors"][0]["url"] = "https://github.com/Hackerismydream/pico/blob/main/README.md"
        path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
        errors = VALIDATOR.validate_eval_contracts(repository)
        self.assertTrue(any("must pin a full GitHub commit" in error for error in errors), errors)

    def test_duplicate_case_id_is_rejected(self) -> None:
        temp, repository = self.copied_repository()
        self.addCleanup(temp.cleanup)
        source = repository / "evals/cases/pico-empty-response-recovery.yaml"
        duplicate = repository / "evals/cases/duplicate.yaml"
        duplicate.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        errors = VALIDATOR.validate_eval_contracts(repository)
        self.assertTrue(any("duplicate eval case_id" in error for error in errors), errors)

    def test_curated_gold_cannot_claim_actual_run(self) -> None:
        temp, repository = self.copied_repository()
        self.addCleanup(temp.cleanup)
        path = repository / "evals/cases/pico-empty-response-recovery.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        data["actual_skill_run"] = True
        path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
        errors = VALIDATOR.validate_eval_contracts(repository)
        self.assertTrue(any("must not be represented" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
