from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "lint_examples", ROOT / "scripts" / "lint_examples.py"
)
assert SPEC is not None and SPEC.loader is not None
LINTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LINTER)


def example_with_bullets(count: int, *, suffix: str = "") -> str:
    bullets = "\n".join(
        f"{index}. 实现第 {index} 条独立工程故事，覆盖不同状态与失败边界。"
        for index in range(1, count + 1)
    )
    return f"""# 测试示例

## 可直接粘贴的简历版本

**测试项目｜后端开发**

**技术栈：** Python、SQLite

**项目描述：** 面向固定测试场景，实现可验证的状态处理流程。

{bullets}{suffix}
"""


class LintExamplesTest(unittest.TestCase):
    def validate_text(self, text: str) -> list[str]:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "example.md"
            path.write_text(text, encoding="utf-8")
            return LINTER.validate(path)

    def test_accepts_one_strong_bullet(self) -> None:
        self.assertEqual(self.validate_text(example_with_bullets(1)), [])

    def test_accepts_two_strong_bullets(self) -> None:
        self.assertEqual(self.validate_text(example_with_bullets(2)), [])

    def test_accepts_five_bullets(self) -> None:
        self.assertEqual(self.validate_text(example_with_bullets(5)), [])

    def test_rejects_zero_bullets(self) -> None:
        errors = self.validate_text(example_with_bullets(0))
        self.assertTrue(any("no bullets" in error for error in errors), errors)

    def test_rejects_more_than_five_bullets(self) -> None:
        errors = self.validate_text(example_with_bullets(6))
        self.assertTrue(any("at most 5" in error for error in errors), errors)

    def test_rejects_exact_normalized_duplicate_across_projects(self) -> None:
        text = """# duplicate

## 可直接粘贴的简历版本

**项目 A｜后端开发**

**技术栈：** Python

**项目描述：** 描述 A。

1. 实现状态机，处理失败恢复。

**项目 B｜后端开发**

**技术栈：** Java

**项目描述：** 描述 B。

1. 实现状态机 处理失败恢复
"""
        errors = self.validate_text(text)
        self.assertTrue(any("duplicate resume bullet" in error for error in errors), errors)

    def test_rejects_placeholder(self) -> None:
        errors = self.validate_text(example_with_bullets(1).replace("不同状态", "[待补数据]"))
        self.assertIn("resume section contains a placeholder", errors)

    def test_rejects_audit_jargon(self) -> None:
        errors = self.validate_text(example_with_bullets(1).replace("独立工程故事", "Claim Ledger"))
        self.assertIn("resume section leaks audit jargon into copy-ready text", errors)

    def test_rejects_more_than_three_questions(self) -> None:
        text = example_with_bullets(1) + """

## 仅在必要时追问

- 问题一？
- 问题二？
- 问题三？
- 问题四？
"""
        errors = self.validate_text(text)
        self.assertTrue(any("question section has 4" in error for error in errors), errors)

    def test_rejects_missing_technology_or_description(self) -> None:
        text = example_with_bullets(1).replace("**技术栈：** Python、SQLite\n\n", "")
        errors = self.validate_text(text)
        self.assertTrue(any("technology line" in error for error in errors), errors)

        text = example_with_bullets(1).replace(
            "**项目描述：** 面向固定测试场景，实现可验证的状态处理流程。\n\n", ""
        )
        errors = self.validate_text(text)
        self.assertTrue(any("project description" in error for error in errors), errors)

    def test_rejects_prose_after_final_bullet(self) -> None:
        errors = self.validate_text(example_with_bullets(1, suffix="\n额外说明不应进入可复制区。"))
        self.assertTrue(any("prose after its final bullet" in error for error in errors), errors)

    def test_all_repository_examples_are_valid(self) -> None:
        paths = sorted((ROOT / "examples").glob("*.md"))
        self.assertGreaterEqual(len(paths), 5)
        failures = {path.name: LINTER.validate(path) for path in paths if LINTER.validate(path)}
        self.assertEqual(failures, {})


if __name__ == "__main__":
    unittest.main()
