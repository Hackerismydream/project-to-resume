# TestZeus Hercules project-level resume draft

Source: [test-zeus-ai/testzeus-hercules](https://github.com/test-zeus-ai/testzeus-hercules)  
Revision: [`fa2b469e1a6a134074171e9e900ae7179b29aa70`](https://github.com/test-zeus-ai/testzeus-hercules/commit/fa2b469e1a6a134074171e9e900ae7179b29aa70)  
Observed: `2026-08-06`  
Checkout: `detached at origin/main`; dirty state: `clean`  
Analysis: `pinned-source, read-only`; target code was not executed.  
Attribution: `project-only` — confirm the candidate's contribution before using personal verbs.

## 简历草稿

**TestZeus Hercules｜自然语言驱动的端到端测试 Agent**

**核心技术：** Python、LangGraph、Playwright、Gherkin / BDD、MCP、JUnit

**项目描述：** 面向 Web 测试脚本维护成本高、执行路径跨 UI/API/安全与外部工具的问题，项目将 Gherkin 场景交给规划 Agent 分解，并路由至专用执行 Agent，最终沉淀机器可读结果和浏览器证据。

1. 项目以 LangGraph 管理 planner、executor 与 assertion 状态，将步骤路由到浏览器、API、安全、SQL、计时、MCP 等专用 Agent，并为规划和执行阶段分别记录 token、成本与耗时字段。
2. 项目为 Agent 执行建立显式终止边界：导航轮次耗尽时返回带错误标记的结果，执行步骤只有在收到终止标记且不含已知失败信号时才记为完成。
3. 项目将解析后的 Gherkin 场景结果、执行时间和成本写入 JUnit XML，再由 XML 生成 HTML 报告，并关联截图、视频、网络日志和运行日志，形成机器可读报告与运行证据包。
4. 项目同时支持消费 MCP 工具与作为 MCP 服务暴露 Gherkin 生成、测试执行和结果读取接口，并对生成与执行子进程设置有界超时。

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
