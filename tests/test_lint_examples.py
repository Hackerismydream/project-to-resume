from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills/project-to-resume"
SPEC = importlib.util.spec_from_file_location(
    "lint_examples", ROOT / "scripts/lint_examples.py"
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

    def test_accepts_one_two_and_five_bullets(self) -> None:
        for count in (1, 2, 5):
            with self.subTest(count=count):
                self.assertEqual(self.validate_text(example_with_bullets(count)), [])

    def test_rejects_zero_or_more_than_five_bullets(self) -> None:
        errors = self.validate_text(example_with_bullets(0))
        self.assertTrue(any("no bullets" in error for error in errors), errors)
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

    def test_rejects_placeholder_and_audit_jargon(self) -> None:
        errors = self.validate_text(example_with_bullets(1).replace("不同状态", "[待补数据]"))
        self.assertIn("resume section contains a placeholder", errors)
        errors = self.validate_text(example_with_bullets(1).replace("独立工程故事", "Repository Map"))
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

    def test_rejects_question_section_before_resume(self) -> None:
        text = "## 仅在必要时追问\n\n- 问题？\n\n" + example_with_bullets(1)
        errors = self.validate_text(text)
        self.assertIn("question section must follow the copy-ready resume section", errors)

    def test_rejects_missing_technology_description_and_trailing_prose(self) -> None:
        text = example_with_bullets(1).replace("**技术栈：** Python、SQLite\n\n", "")
        self.assertTrue(any("technology line" in error for error in self.validate_text(text)))
        text = example_with_bullets(1).replace(
            "**项目描述：** 面向固定测试场景，实现可验证的状态处理流程。\n\n", ""
        )
        self.assertTrue(any("project description" in error for error in self.validate_text(text)))
        errors = self.validate_text(example_with_bullets(1, suffix="\n额外说明不应进入可复制区。"))
        self.assertTrue(any("prose after its final bullet" in error for error in errors), errors)

    def test_all_repository_examples_are_valid(self) -> None:
        paths = sorted((SKILL_ROOT / "examples").glob("*.md"))
        self.assertGreaterEqual(len(paths), 5)
        failures = {}
        for path in paths:
            errors = LINTER.validate(path)
            if errors:
                failures[path.name] = errors
        self.assertEqual(failures, {})


if __name__ == "__main__":
    unittest.main()
