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

    def test_accepts_pending_metric_version_with_plan(self) -> None:
        path = self._write(
            """# Example

Revision: 0123456789abcdef0123456789abcdef01234567

## 当前证据版（证据可用）

1. 项目实现确定性状态转换。

## 指标增强版（推荐目标，待实测，不可投递）

1. 相较共享状态基线，将错误数从 [待实测：基线错误数] 降至 [待实测：方案错误数]。

## 指标验证计划

| Claim | Values to fill | Baseline | Workload | Gate | Artifact |
| --- | --- | --- | --- | --- | --- |
| 状态转换 | [待实测：基线错误数], [待实测：方案错误数] | 共享状态 | 固定事件集 | 正确率不下降 | raw.json |

## 证据索引

| # | Claim | Evidence | Class | Boundary |
| --- | --- | --- | --- | --- |
| 1 | 状态转换 | source.py | implementation | 未测量性能 |

## 证据边界

仅证明实现存在。
"""
        )
        self.assertEqual(MODULE.validate(path), [])

    def test_accepts_ready_metric_version_with_evidence(self) -> None:
        path = self._write(
            """# Example

Revision: 0123456789abcdef0123456789abcdef01234567

## 当前证据版（证据可用）

1. 项目实现确定性状态转换。

## 指标增强版（推荐版，指标已验证）

1. 在 20 个 Case 上将通过数从 18 提升至 20。

## 指标验证计划

已完成，无待填值。

## 证据索引

| # | Claim | Evidence | Class | Boundary |
| --- | --- | --- | --- | --- |
| 1 | 状态转换 | raw.json | benchmark | 20 个 Case；18 提升至 20 |

## 证据边界

仅覆盖固定 Case。
"""
        )
        self.assertEqual(MODULE.validate(path), [])

    def test_rejects_placeholder_in_current_and_orphaned_number(self) -> None:
        path = self._write(
            """# Example

Revision: 0123456789abcdef0123456789abcdef01234567

## 当前证据版（证据可用）

1. 项目将延迟降低 50%，最终值为 [待实测：方案 P95]。

## 指标增强版（推荐目标，待实测，不可投递）

1. 项目将延迟降至 [待实测：方案 P95]。

## 指标验证计划

[待实测：方案 P95]

## 证据索引

| # | Claim | Evidence | Class | Boundary |
| --- | --- | --- | --- | --- |

## 证据边界

没有原始实验。
"""
        )
        errors = MODULE.validate(path)
        self.assertIn("current/evidence count mismatch: 1 bullets, 0 rows", errors)
        self.assertIn(
            "current-evidence version contains a pending metric placeholder: "
            "[待实测：方案 P95]",
            errors,
        )
        self.assertIn("numeric token has no evidence mention: 50%", errors)

    def test_rejects_unmapped_enhanced_placeholder(self) -> None:
        path = self._write(
            """# Example

Revision: 0123456789abcdef0123456789abcdef01234567

## 当前证据版（证据可用）

1. 项目实现确定性状态转换。

## 指标增强版（推荐目标，待实测，不可投递）

1. 项目将错误数降至 [待实测：方案错误数]。

## 指标验证计划

计划尚未建立。

## 证据索引

| # | Claim | Evidence | Class | Boundary |
| --- | --- | --- | --- | --- |
| 1 | 状态转换 | source.py | implementation | 未测量性能 |

## 证据边界

仅证明实现存在。
"""
        )
        self.assertIn(
            "enhanced placeholder has no measurement plan: [待实测：方案错误数]",
            MODULE.validate(path),
        )

    def test_rejects_placeholder_outside_values_to_fill_column(self) -> None:
        path = self._write(
            """# Example

Revision: 0123456789abcdef0123456789abcdef01234567

## 当前证据版（证据可用）

1. 项目实现确定性状态转换。

## 指标增强版（推荐目标，待实测，不可投递）

1. 项目将错误数降至 [待实测：方案错误数]。

## 指标验证计划

| Claim | Values to fill | Baseline | Workload | Gate | Artifact |
| --- | --- | --- | --- | --- | --- |
| 状态转换 | [待实测：别的值] | 共享状态 | 固定事件集 | [待实测：方案错误数] | raw.json |

## 证据索引

| # | Claim | Evidence | Class | Boundary |
| --- | --- | --- | --- | --- |
| 1 | 状态转换 | source.py | implementation | 未测量性能 |

## 证据边界

仅证明实现存在。
"""
        )
        self.assertIn(
            "enhanced placeholder has no measurement plan: [待实测：方案错误数]",
            MODULE.validate(path),
        )


if __name__ == "__main__":
    unittest.main()
