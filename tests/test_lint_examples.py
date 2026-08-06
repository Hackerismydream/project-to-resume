"""Tests for the deliberately small example linter."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "lint_examples.py"
SPEC = importlib.util.spec_from_file_location("lint_examples", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class LintExamplesTest(unittest.TestCase):
    """Exercise structural checks without pretending to verify semantics."""

    def _write(self, text: str) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "example.md"
        path.write_text(text, encoding="utf-8")
        return path

    def test_accepts_minimal_grounded_example(self) -> None:
        path = self._write(
            """# Example

Revision: 0123456789abcdef0123456789abcdef01234567

## 简历草稿

1. 项目实现确定性状态转换。

## 证据索引

| # | Claim | Evidence | Class | Boundary |
| --- | --- | --- | --- | --- |
| 1 | 状态转换 | source.py | implementation | 未测量性能 |

## 证据边界

仅证明实现存在。
"""
        )
        self.assertEqual(MODULE.validate(path), [])

    def test_rejects_orphaned_number_and_missing_evidence_row(self) -> None:
        path = self._write(
            """# Example

Revision: 0123456789abcdef0123456789abcdef01234567

## 简历草稿

1. 项目将延迟降低 50%。

## 证据索引

| # | Claim | Evidence | Class | Boundary |
| --- | --- | --- | --- | --- |

## 证据边界

没有原始实验。
"""
        )
        errors = MODULE.validate(path)
        self.assertIn("resume/evidence count mismatch: 1 bullets, 0 rows", errors)
        self.assertIn("numeric token has no evidence mention: 50%", errors)


if __name__ == "__main__":
    unittest.main()
