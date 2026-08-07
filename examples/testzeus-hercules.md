# TestZeus Hercules project-level resume draft

Source: [test-zeus-ai/testzeus-hercules](https://github.com/test-zeus-ai/testzeus-hercules)  
Revision: [`fa2b469e1a6a134074171e9e900ae7179b29aa70`](https://github.com/test-zeus-ai/testzeus-hercules/commit/fa2b469e1a6a134074171e9e900ae7179b29aa70)  
Observed: `2026-08-06`  
Checkout: `detached at origin/main`; dirty state: `clean`  
Analysis: `pinned-source, read-only`; target code was not executed.  
Attribution: `project-only` — confirm the candidate's contribution before using personal verbs.

## 当前证据版（证据可用）

**TestZeus Hercules｜自然语言驱动的端到端测试 Agent**

**核心技术：** Python、LangGraph、Playwright、Gherkin / BDD、MCP、JUnit

**项目描述：** 面向 Web 测试脚本维护成本高、执行路径跨 UI/API/安全与外部工具的问题，项目将 Gherkin 场景交给规划 Agent 分解，并路由至专用执行 Agent，最终沉淀机器可读结果和浏览器证据。

1. 项目以 LangGraph 管理 planner、executor 与 assertion 状态，将步骤路由到浏览器、API、安全、SQL、计时、MCP 等专用 Agent，并为规划和执行阶段分别记录 token、成本与耗时字段。
2. 项目为 Agent 执行建立显式终止边界：导航轮次耗尽时返回带错误标记的结果，执行步骤只有在收到终止标记且不含已知失败信号时才记为完成。
3. 项目将解析后的 Gherkin 场景结果、执行时间和成本写入 JUnit XML，再由 XML 生成 HTML 报告，并关联截图、视频、网络日志和运行日志，形成机器可读报告与运行证据包。
4. 项目同时支持消费 MCP 工具与作为 MCP 服务暴露 Gherkin 生成、测试执行和结果读取接口，并对生成与执行子进程设置有界超时。

## 指标增强版（推荐目标，待实测，不可投递）

**TestZeus Hercules｜自然语言驱动的端到端测试 Agent**

**核心技术：** Python、LangGraph、Playwright、Gherkin / BDD、MCP、JUnit

**项目描述：** 面向 Web 测试脚本维护成本高、执行路径跨 UI/API/安全与外部工具的问题，项目将 Gherkin 场景交给规划 Agent 分解，并路由至专用执行 Agent，最终沉淀机器可读结果和浏览器证据。

1. 针对单一 Agent 在跨 UI、API、安全与 SQL 场景中规划不稳的问题，采用 planner、executor 与专用 Agent 的图编排；在 [待实测：Gherkin 场景数] 个冻结场景上，相较单 Agent 基线将通过数从 [待实测：单 Agent 通过数] 提升至 [待实测：图编排通过数]，同时将单任务成本从 [待实测：单 Agent 单任务成本] 控制为 [待实测：图编排单任务成本]。
2. 针对模型输出文本可能被误判为任务成功的问题，建立终止标记、失败信号与导航轮次上限；在 [待实测：异常终止 Case 数] 个故障 Case 上，相较仅依据最终文本的基线，将误报成功率从 [待实测：文本判定误报成功率] 降至 [待实测：终止逻辑误报成功率]。
3. 针对外部 Agent 通过 MCP 调用测试能力时的互操作与超时问题，在 [待实测：MCP 互操作 Case 数] 个冻结调用上，相较直接 CLI 基线达到 [待实测：MCP 端到端通过率] 的任务通过率，P95 额外开销为 [待实测：MCP P95 额外开销]，超时结果正确分类率为 [待实测：超时正确分类率]。

## 指标验证计划

| Claim | Values to fill | Baseline | Frozen workload and sample | Metric and success gate | Artifact |
| --- | --- | --- | --- | --- | --- |
| 多 Agent 图编排 | [待实测：Gherkin 场景数], [待实测：单 Agent 通过数], [待实测：图编排通过数], [待实测：单 Agent 单任务成本], [待实测：图编排单任务成本] | 同模型、同工具、同预算的单 Agent 执行器 | 固定 Gherkin 场景、模型、浏览器、工具目录与重试规则 | Verifier-backed 通过数提升；成本变化只在成功率不下降时可写 | run manifest、provider journal、proof bundle、verdict |
| 终止正确性 | [待实测：异常终止 Case 数], [待实测：文本判定误报成功率], [待实测：终止逻辑误报成功率] | 仅依据最终文本判断成功 | 空摘要、不可解析摘要、工具错误、轮次耗尽与正常终止 Case | 误报成功率下降；正常完成不得被误拒绝 | 逐 Case terminal state、JUnit、自动 verifier 结果 |
| MCP 互操作 | [待实测：MCP 互操作 Case 数], [待实测：MCP 端到端通过率], [待实测：MCP P95 额外开销], [待实测：超时正确分类率] | 相同任务直接通过 CLI 调用 | 固定 generate、run、get-results 与超时调用 | 任务结果一致；无永久挂起；超时显式分类 | MCP transcript、子进程记录、JUnit 与聚合报告 |

## 证据索引

| # | Claim | Evidence | Class | Boundary |
| --- | --- | --- | --- | --- |
| 1 | LangGraph planner/executor routing and accounting | [`simple_hercules.py`](https://github.com/test-zeus-ai/testzeus-hercules/blob/fa2b469e1a6a134074171e9e900ae7179b29aa70/testzeus_hercules/core/simple_hercules.py#L51-L75), [`simple_hercules.py`](https://github.com/test-zeus-ai/testzeus-hercules/blob/fa2b469e1a6a134074171e9e900ae7179b29aa70/testzeus_hercules/core/simple_hercules.py#L444-L545), [`simple_hercules.py`](https://github.com/test-zeus-ai/testzeus-hercules/blob/fa2b469e1a6a134074171e9e900ae7179b29aa70/testzeus_hercules/core/simple_hercules.py#L726-L839), [`simple_hercules.py`](https://github.com/test-zeus-ai/testzeus-hercules/blob/fa2b469e1a6a134074171e9e900ae7179b29aa70/testzeus_hercules/core/simple_hercules.py#L1072-L1089) | implementation | No task-success or cost benchmark |
| 2 | Explicit completion and failure handling | [`simple_hercules.py`](https://github.com/test-zeus-ai/testzeus-hercules/blob/fa2b469e1a6a134074171e9e900ae7179b29aa70/testzeus_hercules/core/simple_hercules.py#L105-L124), [`simple_hercules.py`](https://github.com/test-zeus-ai/testzeus-hercules/blob/fa2b469e1a6a134074171e9e900ae7179b29aa70/testzeus_hercules/core/simple_hercules.py#L993-L1007) | implementation | Failure-marker matching is heuristic; no live task-success result |
| 3 | JUnit XML, derived HTML, and browser proof bundle | [`__main__.py`](https://github.com/test-zeus-ai/testzeus-hercules/blob/fa2b469e1a6a134074171e9e900ae7179b29aa70/testzeus_hercules/__main__.py#L59-L124), [`junit_helper.py`](https://github.com/test-zeus-ai/testzeus-hercules/blob/fa2b469e1a6a134074171e9e900ae7179b29aa70/testzeus_hercules/utils/junit_helper.py#L70-L189) | implementation | Status depends on parsed planner output; an unparseable summary can reach JUnit as an empty result without a failure marker; HTML property preservation was not inspected |
| 4 | MCP client and server surfaces | [`mcp_tools.py`](https://github.com/test-zeus-ai/testzeus-hercules/blob/fa2b469e1a6a134074171e9e900ae7179b29aa70/testzeus_hercules/core/tools/mcp_tools.py#L8-L39), [`mcp_server.py`](https://github.com/test-zeus-ai/testzeus-hercules/blob/fa2b469e1a6a134074171e9e900ae7179b29aa70/testzeus_hercules/mcp_server.py#L72-L250) | implementation | No MCP interoperability or reliability run |

## 证据边界

The pinned main-branch source and public GitHub metadata were inspected without
executing project code. The [current-head CI run](https://github.com/test-zeus-ai/testzeus-hercules/actions/runs/30897119621)
was green, but the pinned [main workflow](https://github.com/test-zeus-ai/testzeus-hercules/blob/fa2b469e1a6a134074171e9e900ae7179b29aa70/.github/workflows/main-push.yml#L46-L53)
had the test step commented out and therefore supported only an install/lint-path
observation, not a test-pass claim. Release
[`1.0.2`](https://github.com/test-zeus-ai/testzeus-hercules/releases/tag/1.0.2)
points to commit [`9064893e004162b69693bfe65b9ebb251b338242`](https://github.com/test-zeus-ai/testzeus-hercules/commit/9064893e004162b69693bfe65b9ebb251b338242),
which differs from the pinned source whose
[`pyproject.toml`](https://github.com/test-zeus-ai/testzeus-hercules/blob/fa2b469e1a6a134074171e9e900ae7179b29aa70/pyproject.toml#L1-L4)
declares `1.0.1`; these were kept as separate evidence surfaces. No live LLM,
browser, MCP server, benchmark, success-rate, latency, or production result was
claimed.
