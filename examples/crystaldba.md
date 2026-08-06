# Crystal DBA project-level resume draft

Source: [crystaldba/crystaldba](https://github.com/crystaldba/crystaldba)  
Revision: [`028cc6023237c929c01849604b0ce79e57e0e2f4`](https://github.com/crystaldba/crystaldba/commit/028cc6023237c929c01849604b0ce79e57e0e2f4)  
Observed: `2026-08-06`  
Checkout: `detached at origin/main`; dirty state: `clean`  
Analysis: `pinned-source, read-only`; target code was not executed.  
Attribution: `project-only` — confirm the candidate's contribution before using personal verbs.

## 简历草稿

**Crystal DBA｜PostgreSQL 运维 AI Agent**

**核心技术：** Python、Go、PostgreSQL、Prometheus、SQLite、Docker

**项目描述：** 面向数据库诊断中 SQL 执行、活动数据查询、历史快照回放和远端 Agent 通信的可靠性问题，项目将自然语言交互与 PostgreSQL/Prometheus 数据链路组合为可观察、可约束的运维辅助系统。

1. 项目为 Agent 数据库会话设置语句超时，仅对连接或超时类故障执行有界指数退避，并将查询结果、Schema 与执行错误统一返回为类型化协议消息。
2. 项目为出站 Agent API 请求加入系统标识、时效窗口和随机 nonce，并使用 ECDSA P-256 覆盖请求方法、目标地址及请求体摘要；当前证据只支持客户端签名，不支持端到端防重放结论。
3. 项目采用结构化节点生成 PromQL 聚合、筛选与分页表达式，在执行前校验维度、时间范围和样本上限，并为长时间范围切换预聚合规则。
4. 项目在历史回放期间缓存实时快照任务，按数据库系统并行、同一系统内串行处理，并将查询文本批量写入 SQLite、指标统一写入 Prometheus。

## 证据索引

| # | Claim | Evidence | Class | Boundary |
| --- | --- | --- | --- | --- |
| 1 | SQL timeout, bounded retry, typed result/error | [`startup.py`](https://github.com/crystaldba/crystaldba/blob/028cc6023237c929c01849604b0ce79e57e0e2f4/agent/crystaldba/cli/startup.py#L42-L50), [`chat_response_followup.py`](https://github.com/crystaldba/crystaldba/blob/028cc6023237c929c01849604b0ce79e57e0e2f4/agent/crystaldba/cli/chat_response_followup.py#L51-L143) | implementation | Tests were not executed |
| 2 | Client-side ECDSA P-256 request signing | [`secure_session.py`](https://github.com/crystaldba/crystaldba/blob/028cc6023237c929c01849604b0ce79e57e0e2f4/agent/crystaldba/shared/secure_session.py#L35-L84), [`test_secure_session.py`](https://github.com/crystaldba/crystaldba/blob/028cc6023237c929c01849604b0ce79e57e0e2f4/agent/crystaldba/shared/test/test_secure_session.py#L22-L66) | implementation + test source | No server verifier or replay E2E; P-256 is an algorithm choice, not a measured result |
| 3 | Structured and bounded PromQL generation | [`promql_codegen.go`](https://github.com/crystaldba/crystaldba/blob/028cc6023237c929c01849604b0ce79e57e0e2f4/bff/pkg/server/promql_codegen.go#L11-L208), [`server.go`](https://github.com/crystaldba/crystaldba/blob/028cc6023237c929c01849604b0ce79e57e0e2f4/bff/pkg/server/server.go#L354-L371), [`server.go`](https://github.com/crystaldba/crystaldba/blob/028cc6023237c929c01849604b0ce79e57e0e2f4/bff/pkg/server/server.go#L448-L513), [`server.go`](https://github.com/crystaldba/crystaldba/blob/028cc6023237c929c01849604b0ce79e57e0e2f4/bff/pkg/server/server.go#L801-L812) | implementation | No latency or load-reduction benchmark |
| 4 | Historical/live snapshot scheduling | [`main.go`](https://github.com/crystaldba/crystaldba/blob/028cc6023237c929c01849604b0ce79e57e0e2f4/collector-api/cmd/server/main.go#L42-L55), [`queue.go`](https://github.com/crystaldba/crystaldba/blob/028cc6023237c929c01849604b0ce79e57e0e2f4/collector-api/internal/api/queue.go#L18-L78), [`reprocess.go`](https://github.com/crystaldba/crystaldba/blob/028cc6023237c929c01849604b0ce79e57e0e2f4/collector-api/internal/api/reprocess.go#L18-L28), [`snapshots.go`](https://github.com/crystaldba/crystaldba/blob/028cc6023237c929c01849604b0ce79e57e0e2f4/collector-api/internal/api/snapshots.go#L90-L121), [`snapshots.go`](https://github.com/crystaldba/crystaldba/blob/028cc6023237c929c01849604b0ce79e57e0e2f4/collector-api/internal/api/snapshots.go#L184-L295), [`snapshots.go`](https://github.com/crystaldba/crystaldba/blob/028cc6023237c929c01849604b0ce79e57e0e2f4/collector-api/internal/api/snapshots.go#L470-L503), [`sqlite_query_storage.go`](https://github.com/crystaldba/crystaldba/blob/028cc6023237c929c01849604b0ce79e57e0e2f4/collector-api/internal/storage/sqlite_query_storage.go#L12-L103) | implementation | No executed concurrency or scale test |

## 证据边界

This is a pinned-source reconstruction of an unreleased post-RC checkout. Tests,
CI runs, release artifacts, Docker manifests, real PostgreSQL systems, and live
Agent providers were not executed or inspected. Configuration constants such as
timeouts, retries, sample guards, and batch sizes were not converted into
performance claims. No checked-in benchmark manifest/raw aggregate supported a
percentage, throughput, latency, availability, or compatibility result.
