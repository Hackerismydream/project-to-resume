from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
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
        shutil.copytree(
            ROOT,
            destination,
            ignore=shutil.ignore_patterns("__pycache__", ".git", ".venv"),
        )
        return temp, destination

    def test_real_package_validates(self) -> None:
        self.assertEqual(VALIDATOR.validate_tree(ROOT), [])

    def test_missing_required_file_is_rejected(self) -> None:
        temp, package = self.copied_package()
        self.addCleanup(temp.cleanup)
        (package / "CONTRIBUTING.md").unlink()
        errors = VALIDATOR.validate_tree(package)
        self.assertIn("missing required file: CONTRIBUTING.md", errors)

    def test_broken_local_markdown_link_is_rejected(self) -> None:
        temp, package = self.copied_package()
        self.addCleanup(temp.cleanup)
        with (package / "README.md").open("a", encoding="utf-8") as handle:
            handle.write("\n[broken](docs/missing.md)\n")
        errors = VALIDATOR.validate_tree(package)
        self.assertTrue(any("broken local link" in error for error in errors), errors)

    def test_invalid_yaml_is_rejected_by_real_parser(self) -> None:
        temp, package = self.copied_package()
        self.addCleanup(temp.cleanup)
        path = package / "agents/openai.yaml"
        path.write_text("interface: [unterminated\n", encoding="utf-8")
        errors = VALIDATOR.validate_tree(package)
        self.assertTrue(any("invalid YAML" in error for error in errors), errors)

    def test_invalid_json_is_rejected(self) -> None:
        temp, package = self.copied_package()
        self.addCleanup(temp.cleanup)
        path = package / "evals/requests/positive-repository-role.json"
        path.write_text('{"id": ', encoding="utf-8")
        errors = VALIDATOR.validate_tree(package)
        self.assertTrue(any("invalid JSON" in error for error in errors), errors)

    def test_eval_schema_violation_is_rejected(self) -> None:
        temp, package = self.copied_package()
        self.addCleanup(temp.cleanup)
        path = package / "evals/cases/pico-empty-response-recovery.yaml"
        data = json.loads(path.read_text(encoding="utf-8"))
        del data["top_stories"]
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        errors = VALIDATOR.validate_tree(package)
        self.assertTrue(any("schema violation" in error for error in errors), errors)

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
        data["evidence_anchors"][0]["url"] = (
            "https://github.com/Hackerismydream/pico/blob/main/README.md"
        )
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
        self.assertTrue(
            any(
                "schema violation" in error and "expected_questions" in error
                for error in errors
            ),
            errors,
        )

    def test_duplicate_eval_case_id_is_rejected(self) -> None:
        temp, package = self.copied_package()
        self.addCleanup(temp.cleanup)
        source = package / "evals/cases/pico-empty-response-recovery.yaml"
        duplicate = package / "evals/cases/duplicate-case.yaml"
        duplicate.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        errors = VALIDATOR.validate_tree(package)
        self.assertTrue(any("duplicate eval case_id" in error for error in errors), errors)

    def test_skill_directory_name_is_checked(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        destination = Path(temp.name) / "wrong-name"
        shutil.copytree(
            ROOT,
            destination,
            ignore=shutil.ignore_patterns("__pycache__", ".git", ".venv"),
        )
        errors = VALIDATOR.validate_tree(destination)
        self.assertTrue(any("skill directory must be named" in error for error in errors), errors)

    def test_skill_license_frontmatter_is_required(self) -> None:
        temp, package = self.copied_package()
        self.addCleanup(temp.cleanup)
        path = package / "SKILL.md"
        text = path.read_text(encoding="utf-8").replace(
            "license: Apache-2.0\n", "license: Proprietary\n", 1
        )
        path.write_text(text, encoding="utf-8")
        errors = VALIDATOR.validate_tree(package)
        self.assertIn("SKILL.md frontmatter license must be Apache-2.0", errors)

    def test_stale_branch_text_is_rejected(self) -> None:
        temp, package = self.copied_package()
        self.addCleanup(temp.cleanup)
        with (package / "README.md").open("a", encoding="utf-8") as handle:
            handle.write("\n当前版本在 codex/repository-discovery-v2。\n")
        errors = VALIDATOR.validate_tree(package)
        self.assertTrue(any("stale branch/PR text" in error for error in errors), errors)

    def test_tracked_generated_artifact_is_rejected(self) -> None:
        temp, package = self.copied_package()
        self.addCleanup(temp.cleanup)
        subprocess.run(["git", "init", "-q", str(package)], check=True)
        artifact = package / "scripts/__pycache__/bad.pyc"
        artifact.parent.mkdir()
        artifact.write_bytes(b"not bytecode")
        subprocess.run(
            ["git", "-C", str(package), "add", "-f", "scripts/__pycache__/bad.pyc"],
            check=True,
        )
        errors = VALIDATOR.validate_tree(package)
        self.assertTrue(
            any("generated artifact must not be tracked" in error for error in errors),
            errors,
        )

    def test_changelog_requires_unreleased_section(self) -> None:
        temp, package = self.copied_package()
        self.addCleanup(temp.cleanup)
        path = package / "CHANGELOG.md"
        path.write_text("# Changelog\n", encoding="utf-8")
        errors = VALIDATOR.validate_tree(package)
        self.assertIn("CHANGELOG.md must contain an [Unreleased] section", errors)

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

    def test_readme_links_core_maintenance_docs(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for path in (
            "docs/installation.md",
            "docs/evaluation.md",
            "CONTRIBUTING.md",
            "SECURITY.md",
            "CODE_OF_CONDUCT.md",
            "CHANGELOG.md",
            "LICENSE",
        ):
            self.assertIn(path, readme)


if __name__ == "__main__":
    unittest.main()
