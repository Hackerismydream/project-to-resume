# TGO project-level resume draft

Source: [tgoai/tgo](https://github.com/tgoai/tgo)  
Revision: [`995da4577f6f91edb87d0f56fc9ea4c129f1a4eb`](https://github.com/tgoai/tgo/commit/995da4577f6f91edb87d0f56fc9ea4c129f1a4eb)  
Observed: `2026-08-06`  
Checkout: `detached at origin/main`; dirty state: `clean`  
Analysis: `pinned-source, read-only`; target code was not executed.  
Attribution: `project-only` — confirm the candidate's contribution before using personal verbs.

## 简历草稿

**TGO｜开源全渠道 AI Agent 客服平台**

**核心技术：** Python、FastAPI、React、RAG、Hybrid Retrieval、Workflow DAG、Multi-channel Messaging

**项目描述：** 面向 AI 客服在多渠道接入、Agent 编排、知识检索与人工协作中的工程问题，项目以多服务架构统一消息、工作流、RAG、管理端与 Widget 接入边界。

1. 项目在平台路由从多 Agent 数组迁移到单 Agent 时，将持久化、API 与前端请求统一为 `agent_id`；后端兼容归一旧字段，前端类型契约阻止继续产生旧数组负载。
2. 项目将流式回复中的增量、完成和失败映射为独立的 `delta / close / finish / error` 协议状态，为下游区分内容传输、正常结束与工作流失败提供明确边界。
3. 项目在工作流发布入口校验触发节点、回答节点、双向可达性与环依赖，拒绝发布不满足 DAG 约束的流程定义，避免结构错误延迟到运行阶段。
4. 项目将不同聊天渠道转换为统一消息信封，并在应用生命周期内集中启动、停止、取消和回收后台监听任务，隔离渠道字段与连接管理差异。
5. 项目对查询变体并行执行关键词与语义检索，通过 RRF 融合候选排序，并保留两路排名元数据以支持结果追踪；当前证据不支持召回率或延迟提升数字。

## 证据索引

| # | Claim | Evidence | Class | Boundary |
| --- | --- | --- | --- | --- |
| 1 | 单 Agent 路由契约迁移 | [`platform_schema.py`](https://github.com/tgoai/tgo/blob/995da4577f6f91edb87d0f56fc9ea4c129f1a4eb/repos/tgo-api/app/schemas/platform_schema.py#L14-L128), [`platform.py`](https://github.com/tgoai/tgo/blob/995da4577f6f91edb87d0f56fc9ea4c129f1a4eb/repos/tgo-api/app/models/platform.py#L164-L169), [`test_agent_only_persistence.py`](https://github.com/tgoai/tgo/blob/995da4577f6f91edb87d0f56fc9ea4c129f1a4eb/repos/tgo-api/tests/test_agent_only_persistence.py#L23-L52), [`platformsApi.ts`](https://github.com/tgoai/tgo/blob/995da4577f6f91edb87d0f56fc9ea4c129f1a4eb/repos/tgo-web/src/services/platformsApi.ts#L17-L60), [`platformAgentRouting.ts`](https://github.com/tgoai/tgo/blob/995da4577f6f91edb87d0f56fc9ea4c129f1a4eb/repos/tgo-web/src/types/__typecheck__/platformAgentRouting.ts#L6-L19) | implementation + test source | Tests were not executed |
| 2 | Typed streaming states | [`chat_service.py`](https://github.com/tgoai/tgo/blob/995da4577f6f91edb87d0f56fc9ea4c129f1a4eb/repos/tgo-api/app/services/chat_service.py#L147-L237), [`test_chat_agent_streaming.py`](https://github.com/tgoai/tgo/blob/995da4577f6f91edb87d0f56fc9ea4c129f1a4eb/repos/tgo-api/tests/test_chat_agent_streaming.py#L14-L86) | implementation + test source | No real IM/provider run |
| 3 | DAG publication validation | [`validation_service.py`](https://github.com/tgoai/tgo/blob/995da4577f6f91edb87d0f56fc9ea4c129f1a4eb/repos/tgo-workflow/app/services/validation_service.py#L12-L83), [`workflows.py`](https://github.com/tgoai/tgo/blob/995da4577f6f91edb87d0f56fc9ea4c129f1a4eb/repos/tgo-workflow/app/api/workflows.py#L175-L194) | implementation | No workflow success-rate claim |
| 4 | Channel envelope and listener lifecycle | [`entities.py`](https://github.com/tgoai/tgo/blob/995da4577f6f91edb87d0f56fc9ea4c129f1a4eb/repos/tgo-platform/app/domain/entities.py#L6-L14), [`normalizer.py`](https://github.com/tgoai/tgo/blob/995da4577f6f91edb87d0f56fc9ea4c129f1a4eb/repos/tgo-platform/app/domain/services/normalizer.py#L6-L20), [`feishu_listener.py`](https://github.com/tgoai/tgo/blob/995da4577f6f91edb87d0f56fc9ea4c129f1a4eb/repos/tgo-platform/app/domain/services/listeners/feishu_listener.py#L186-L213), [`feishu_listener.py`](https://github.com/tgoai/tgo/blob/995da4577f6f91edb87d0f56fc9ea4c129f1a4eb/repos/tgo-platform/app/domain/services/listeners/feishu_listener.py#L340-L352), [`wecom_listener.py`](https://github.com/tgoai/tgo/blob/995da4577f6f91edb87d0f56fc9ea4c129f1a4eb/repos/tgo-platform/app/domain/services/listeners/wecom_listener.py#L428-L442), [`main.py`](https://github.com/tgoai/tgo/blob/995da4577f6f91edb87d0f56fc9ea4c129f1a4eb/repos/tgo-platform/app/main.py#L34-L136) | implementation | No live-channel E2E evidence |
| 5 | Hybrid retrieval and RRF ranking | [`search.py`](https://github.com/tgoai/tgo/blob/995da4577f6f91edb87d0f56fc9ea4c129f1a4eb/repos/tgo-rag/src/rag_service/services/search.py#L33-L80), [`search.py`](https://github.com/tgoai/tgo/blob/995da4577f6f91edb87d0f56fc9ea4c129f1a4eb/repos/tgo-rag/src/rag_service/services/search.py#L127-L381) | implementation | No benchmark/raw retrieval aggregate |

## 证据边界

This run inspected the clean pinned source tree only. It did not execute tests,
install dependencies, inspect live workflow runs, call a provider, or exercise a
real messaging channel. README scale/latency statements, test counts, retrieval
metrics, and personal contribution claims were excluded. The draft proves that
the implementation paths exist at the pinned revision; it does not prove
production adoption or effect size.
