"""Tests for the recruiter-ready example contract."""

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


PROJECT_ONE = """**交易系统｜Java 后端开发**

**技术栈：** Java、Redis、MySQL

**项目描述：** 面向营销交易链路，处理库存、订单和支付状态流转。

1. 负责订单核心链路建模，覆盖创建、支付和退款状态。
2. 使用 Redis Lua 合并库存与资格校验，缩小并发竞态窗口。
3. 通过幂等消费与补偿任务处理消息重复和短暂失败。
"""

PROJECT_TWO = """**知识问答系统｜AI 应用开发**

**技术栈：** Python、BM25、Rerank

**项目描述：** 面向内部知识查询，构建检索、重排与引用回答链路。

1. 负责文档解析与结构化切分，保留标题层级和来源信息。
2. 融合词法与向量候选，并通过重排统一相关性顺序。
3. 为低相关和无结果查询设计拒答路径，避免无依据回答。
"""

VALID = f"""# Example

## 可直接粘贴的简历版本

{PROJECT_ONE}"""


class LintExamplesTest(unittest.TestCase):
    def _write(self, text: str) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "example.md"
        path.write_text(text, encoding="utf-8")
        return path

    def test_accepts_copy_ready_example_without_questions(self) -> None:
        self.assertEqual(MODULE.validate(self._write(VALID)), [])

    def test_accepts_unordered_resume_bullets(self) -> None:
        text = VALID.replace("1. ", "- ").replace("2. ", "- ").replace("3. ", "- ")
        self.assertEqual(MODULE.validate(self._write(text)), [])

    def test_accepts_multiple_projects_with_three_to_five_each(self) -> None:
        text = VALID + "\n" + PROJECT_TWO
        self.assertEqual(MODULE.validate(self._write(text)), [])

    def test_accepts_user_confirmed_metric_without_evidence_appendix(self) -> None:
        text = VALID.replace(
            "缩小并发竞态窗口",
            "在固定并发压测中将 P95 从 320ms 降至 110ms",
        )
        self.assertEqual(MODULE.validate(self._write(text)), [])

    def test_rejects_missing_resume_heading(self) -> None:
        errors = MODULE.validate(
            self._write(VALID.replace("## 可直接粘贴的简历版本", "## 草稿"))
        )
        self.assertIn("missing heading: ## 可直接粘贴的简历版本", errors)

    def test_rejects_too_few_bullets_per_project(self) -> None:
        text = (VALID + "\n" + PROJECT_TWO).replace(
            "3. 为低相关和无结果查询设计拒答路径，避免无依据回答。\n",
            "",
        )
        self.assertIn(
            "project '知识问答系统｜AI 应用开发' has 2 bullets; keep each project to 3-5",
            MODULE.validate(self._write(text)),
        )

    def test_rejects_too_many_bullets_per_project(self) -> None:
        text = VALID + "4. 第四条。\n5. 第五条。\n6. 第六条。\n"
        self.assertIn(
            "project '交易系统｜Java 后端开发' has 6 bullets; keep each project to 3-5",
            MODULE.validate(self._write(text)),
        )

    def test_rejects_missing_technology_on_second_project(self) -> None:
        text = VALID + "\n" + PROJECT_TWO.replace(
            "**技术栈：** Python、BM25、Rerank\n\n",
            "",
        )
        self.assertIn(
            "project '知识问答系统｜AI 应用开发' is missing a non-empty technology line",
            MODULE.validate(self._write(text)),
        )

    def test_rejects_missing_description_on_second_project(self) -> None:
        text = VALID + "\n" + PROJECT_TWO.replace(
            "**项目描述：** 面向内部知识查询，构建检索、重排与引用回答链路。\n\n",
            "",
        )
        self.assertIn(
            "project '知识问答系统｜AI 应用开发' is missing a non-empty project description",
            MODULE.validate(self._write(text)),
        )

    def test_rejects_duplicate_bullet_across_projects(self) -> None:
        duplicate = "1. 负责订单核心链路建模，覆盖创建、支付和退款状态。\n"
        text = VALID + "\n" + PROJECT_TWO.replace(
            "1. 负责文档解析与结构化切分，保留标题层级和来源信息。\n",
            duplicate,
        )
        errors = MODULE.validate(self._write(text))
        self.assertTrue(any(error.startswith("duplicate resume bullet") for error in errors))

    def test_rejects_duplicate_project_title(self) -> None:
        errors = MODULE.validate(self._write(VALID + "\n" + PROJECT_ONE))
        self.assertIn("duplicate project title: 交易系统｜Java 后端开发", errors)

    def test_rejects_unheaded_analysis_after_final_project(self) -> None:
        text = VALID + "\n这个数字暂时不应保留，因为缺少完整口径。\n"
        self.assertIn(
            "project '交易系统｜Java 后端开发' has prose after its final bullet; "
            "keep the copy-ready section to project content",
            MODULE.validate(self._write(text)),
        )

    def test_rejects_placeholder_in_copy_ready_text(self) -> None:
        text = VALID.replace("缩小并发竞态窗口", "将 P95 降至 [待实测：结果]")
        self.assertIn(
            "resume section contains a placeholder",
            MODULE.validate(self._write(text)),
        )

    def test_rejects_audit_jargon_in_copy_ready_text(self) -> None:
        text = VALID.replace("负责订单核心链路建模", "当前证据支持订单核心链路建模")
        self.assertIn(
            "resume section leaks audit jargon into copy-ready text",
            MODULE.validate(self._write(text)),
        )

    def test_accepts_up_to_three_questions(self) -> None:
        text = VALID + """
## 仅在必要时追问

- 谁在使用？
- 你怎么验证？
- 最难的故障是什么？
"""
        self.assertEqual(MODULE.validate(self._write(text)), [])

    def test_rejects_more_than_three_questions(self) -> None:
        text = VALID + """
## 仅在必要时追问

- 问题一？
- 问题二？
- 问题三？
- 问题四？
"""
        self.assertIn(
            "question section has 4 questions; keep to 3",
            MODULE.validate(self._write(text)),
        )


if __name__ == "__main__":
    unittest.main()
