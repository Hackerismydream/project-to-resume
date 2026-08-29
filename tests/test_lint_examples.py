from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "skills/project-to-resume/examples"
SPEC = importlib.util.spec_from_file_location("lint_examples", ROOT / "scripts/lint_examples.py")
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

    def test_accepts_one_to_five_bullets(self) -> None:
        for count in range(1, 6):
            with self.subTest(count=count):
                self.assertEqual(self.validate_text(example_with_bullets(count)), [])

    def test_rejects_zero_and_more_than_five_bullets(self) -> None:
        self.assertTrue(any("no bullets" in e for e in self.validate_text(example_with_bullets(0))))
        self.assertTrue(any("at most 5" in e for e in self.validate_text(example_with_bullets(6))))

    def test_rejects_duplicate_placeholder_audit_and_trailing_prose(self) -> None:
        duplicate = """# duplicate

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
        self.assertTrue(any("duplicate resume bullet" in e for e in self.validate_text(duplicate)))
        self.assertIn(
            "resume section contains a placeholder",
            self.validate_text(example_with_bullets(1).replace("不同状态", "[待补数据]")),
        )
        self.assertIn(
            "resume section leaks audit jargon into copy-ready text",
            self.validate_text(example_with_bullets(1).replace("独立工程故事", "Claim Ledger")),
        )
        self.assertTrue(
            any(
                "prose after its final bullet" in e
                for e in self.validate_text(example_with_bullets(1, suffix="\n额外说明。"))
            )
        )

    def test_rejects_too_many_questions(self) -> None:
        text = example_with_bullets(1) + """

## 仅在必要时追问

- 问题一？
- 问题二？
- 问题三？
- 问题四？
"""
        self.assertTrue(any("question section has 4" in e for e in self.validate_text(text)))

    def test_all_runtime_examples_are_valid(self) -> None:
        paths = sorted(EXAMPLES.glob("*.md"))
        self.assertGreaterEqual(len(paths), 5)
        failures = {path.name: LINTER.validate(path) for path in paths if LINTER.validate(path)}
        self.assertEqual(failures, {})


if __name__ == "__main__":
    unittest.main()
