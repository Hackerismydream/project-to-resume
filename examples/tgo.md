# TGO project-level resume draft

Source: [tgoai/tgo](https://github.com/tgoai/tgo)  
Revision: [`995da4577f6f91edb87d0f56fc9ea4c129f1a4eb`](https://github.com/tgoai/tgo/commit/995da4577f6f91edb87d0f56fc9ea4c129f1a4eb)  
Observed: `2026-08-06`  
Checkout: `detached at origin/main`; dirty state: `clean`  
Analysis: `pinned-source, read-only`; target code was not executed.  
Attribution: `project-only` — confirm the candidate's contribution before using personal verbs.

## 当前证据版（证据可用）

**TGO｜开源全渠道 AI Agent 客服平台**

**核心技术：** Python、FastAPI、React、RAG、Hybrid Retrieval、Workflow DAG、Multi-channel Messaging

**项目描述：** 面向 AI 客服在多渠道接入、Agent 编排、知识检索与人工协作中的工程问题，项目以多服务架构统一消息、工作流、RAG、管理端与 Widget 接入边界。

1. 项目在平台路由从多 Agent 数组迁移到单 Agent 时，将持久化、API 与前端请求统一为 `agent_id`；后端兼容归一旧字段，前端类型契约阻止继续产生旧数组负载。
2. 项目将流式回复中的增量、完成和失败映射为独立的 `delta / close / finish / error` 协议状态，为下游区分内容传输、正常结束与工作流失败提供明确边界。
3. 项目在工作流发布入口校验触发节点、回答节点、双向可达性与环依赖，拒绝发布不满足 DAG 约束的流程定义，避免结构错误延迟到运行阶段。
4. 项目将不同聊天渠道转换为统一消息信封，并在应用生命周期内集中启动、停止、取消和回收后台监听任务，隔离渠道字段与连接管理差异。
5. 项目对查询变体并行执行关键词与语义检索，通过 RRF 融合候选排序，并保留两路排名元数据以支持结果追踪；当前证据不支持召回率或延迟提升数字。

## 指标增强版（推荐目标，待实测，不可投递）

**TGO｜开源全渠道 AI Agent 客服平台**

**核心技术：** Python、FastAPI、React、RAG、Hybrid Retrieval、Workflow DAG、Multi-channel Messaging

**项目描述：** 面向 AI 客服在多渠道接入、Agent 编排、知识检索与人工协作中的工程问题，项目以多服务架构统一消息、工作流、RAG、管理端与 Widget 接入边界。

1. 针对流式回复中增量、完成与失败容易混淆的问题，建立独立协议状态；相较仅依据最终文本的基线，在 [待实测：流式事件场景数] 个冻结场景中将终态误判数从 [待实测：文本基线终态误判数] 降至 [待实测：协议状态终态误判数]，同时保持已接收事件无丢失、无重复终态。
2. 针对缺少入口、出口、可达性或存在环依赖的工作流可能延迟到运行期失败的问题，在发布前执行 DAG 校验；相较无校验基线，在 [待实测：无效 DAG Case 数] 个 Case 上将拦截率从 [待实测：无校验基线拦截率] 提升至 [待实测：发布校验拦截率]，并将合法流程误拒率控制为 [待实测：合法流程误拒率]。
3. 针对关键词检索漏召回与语义检索误召回的问题，融合两路候选排序；在 [待实测：检索 Case 数] 个 held-out Case 上，将 Recall@10 从最佳单路的 [待实测：最佳单路 Recall@10] 提升至 [待实测：融合 Recall@10]，同时将跨项目泄漏率控制为 [待实测：跨项目泄漏率]。

## 指标验证计划

| Claim | Values to fill | Baseline | Frozen workload and sample | Metric and success gate | Artifact |
| --- | --- | --- | --- | --- | --- |
| 流式终态 | [待实测：流式事件场景数], [待实测：文本基线终态误判数], [待实测：协议状态终态误判数] | 仅依据最终文本判断完成 | 固定事件序列、故障注入与并发顺序；样本为全部冻结场景 | 终态误判下降；事件无丢失、无重复终态、无永久未决 | commit-bound manifest、逐事件结果、聚合报告 |
| DAG 发布校验 | [待实测：无效 DAG Case 数], [待实测：无校验基线拦截率], [待实测：发布校验拦截率], [待实测：合法流程误拒率] | 保存后直接运行图定义 | 缺入口、缺出口、不可达、环依赖及合法图的冻结 Case | 无效图拦截率提升；合法图误拒率不增加 | Case 清单、校验输出、raw verdict |
| 混合检索 | [待实测：检索 Case 数], [待实测：最佳单路 Recall@10], [待实测：融合 Recall@10], [待实测：跨项目泄漏率] | 关键词单路与语义单路中的最佳者 | 固定项目过滤、索引快照与 held-out 查询 | Recall@10 提升；Precision、泄漏与任务成功率不得退化 | manifest、逐查询候选、聚合指标 |

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
