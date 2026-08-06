# Project to Resume

把一个软件项目翻译成面试官能理解、证据能够支持的中文技术简历。

这个 skill 只做一件事：读取项目证据，先判断什么是真的，再把项目内部抽象翻译成具体故障、可观察行为和有边界的结果。它不会估算缺失指标，也不会把源码存在、测试文件存在或绿色 CI 自动写成效果结论。

## 方法

```text
固定仓库与实验身份
        ↓
建立 Claim Ledger（主张 ↔ 证据 ↔ 边界 ↔ 归因）
        ↓
场景 → 故障 → 可观察行为 → 对照方案 → 结果指标 → 证据边界
        ↓
简历项目段落 + 证据索引 + 拒绝项
```

核心约束：

- 源码只能证明某个实现存在，不能单独证明正确性、规模或效果。
- 测试文件不等于测试通过；绿色 CI 只证明实际执行且成功的步骤。
- 百分比必须有基线；“0”必须说明统计对象和观察范围。
- 历史实验、当前源码、发布制品、安装版本和线上结果分别陈述。
- 仓库不能证明候选人本人做过什么。没有贡献证据时，只输出“项目主体版”草稿。
- 没有合格数字时写架构与行为，不编造数字；没有主张通过时，交付证据缺口而不是硬写简历。

完整规则见 [SKILL.md](SKILL.md)、[evidence-rules.md](references/evidence-rules.md) 与 [resume-format.md](references/resume-format.md)。

## 安装

把仓库放到 Agent 能发现的 skills 目录：

```bash
git clone https://github.com/Hackerismydream/project-to-resume.git ~/.agents/skills/project-to-resume
```

若宿主使用其他目录，例如 Codex 的 `~/.codex/skills`，将目标路径替换为对应的 skills 根目录即可。

## 使用

显式调用，避免在普通代码阅读中误触发：

```text
使用 $project-to-resume 分析当前仓库，输出中文简历项目段落和逐条证据索引。
```

也可以给出公开仓库 URL：

```text
使用 $project-to-resume 分析 https://github.com/owner/repo，固定到完整 commit，
不要执行仓库代码；输出项目主体版简历、证据边界和待补的个人归因。
```

已有简历时，可以要求逐条核验；给 JD 时，只允许在已有 Claim Ledger 内重排和改写。只有用户明确要求深度、多轮或独立调查时，才进入可选的 `$deep-investigate` 分支；本 skill 本身不依赖它。

## 三个公开仓库方法实跑（静态审计）

以下结果生成于 2026-08-06。三次分析都只读取固定 commit 的源码与公开元数据，没有安装依赖或执行目标仓库代码。完整逐条证据链接和拒绝项位于对应示例文件。

### TGO

审计对象：[tgoai/tgo@995da4577f6f91edb87d0f56fc9ea4c129f1a4eb](https://github.com/tgoai/tgo/tree/995da4577f6f91edb87d0f56fc9ea4c129f1a4eb) · [完整证据稿](examples/tgo.md)

**TGO｜开源全渠道 AI Agent 客服平台**

**核心技术：** Python、FastAPI、React、RAG、Hybrid Retrieval、Workflow DAG、Multi-channel Messaging

**项目描述：** 面向 AI 客服在多渠道接入、Agent 编排、知识检索与人工协作中的工程问题，项目以多服务架构统一消息、工作流、RAG、管理端与 Widget 接入边界。

1. 项目在平台路由从多 Agent 数组迁移到单 Agent 时，将持久化、API 与前端请求统一为 `agent_id`；后端兼容归一旧字段，前端类型契约阻止继续产生旧数组负载。
2. 项目将流式回复中的增量、完成和失败映射为独立的 `delta / close / finish / error` 协议状态，为下游区分内容传输、正常结束与工作流失败提供明确边界。
3. 项目在工作流发布入口校验触发节点、回答节点、双向可达性与环依赖，拒绝发布不满足 DAG 约束的流程定义，避免结构错误延迟到运行阶段。
4. 项目将不同聊天渠道转换为统一消息信封，并在应用生命周期内集中启动、停止、取消和回收后台监听任务，隔离渠道字段与连接管理差异。
5. 项目对查询变体并行执行关键词与语义检索，通过 RRF 融合候选排序，并保留两路排名元数据以支持结果追踪；当前证据不支持召回率或延迟提升数字。

### Crystal DBA

审计对象：[crystaldba/crystaldba@028cc6023237c929c01849604b0ce79e57e0e2f4](https://github.com/crystaldba/crystaldba/tree/028cc6023237c929c01849604b0ce79e57e0e2f4) · [完整证据稿](examples/crystaldba.md)

**Crystal DBA｜PostgreSQL 运维 AI Agent**

**核心技术：** Python、Go、PostgreSQL、Prometheus、SQLite、Docker

**项目描述：** 面向数据库诊断中 SQL 执行、活动数据查询、历史快照回放和远端 Agent 通信的可靠性问题，项目将自然语言交互与 PostgreSQL/Prometheus 数据链路组合为可观察、可约束的运维辅助系统。

1. 项目为 Agent 数据库会话设置语句超时，仅对连接或超时类故障执行有界指数退避，并将查询结果、Schema 与执行错误统一返回为类型化协议消息。
2. 项目为出站 Agent API 请求加入系统标识、时效窗口和随机 nonce，并使用 ECDSA P-256 覆盖请求方法、目标地址及请求体摘要；当前证据只支持客户端签名，不支持端到端防重放结论。
3. 项目采用结构化节点生成 PromQL 聚合、筛选与分页表达式，在执行前校验维度、时间范围和样本上限，并为长时间范围切换预聚合规则。
4. 项目在历史回放期间缓存实时快照任务，按数据库系统并行、同一系统内串行处理，并将查询文本批量写入 SQLite、指标统一写入 Prometheus。

### TestZeus Hercules

审计对象：[test-zeus-ai/testzeus-hercules@fa2b469e1a6a134074171e9e900ae7179b29aa70](https://github.com/test-zeus-ai/testzeus-hercules/tree/fa2b469e1a6a134074171e9e900ae7179b29aa70) · [完整证据稿](examples/testzeus-hercules.md)

**TestZeus Hercules｜自然语言驱动的端到端测试 Agent**

**核心技术：** Python、LangGraph、Playwright、Gherkin / BDD、MCP、JUnit

**项目描述：** 面向 Web 测试脚本维护成本高、执行路径跨 UI/API/安全与外部工具的问题，项目将 Gherkin 场景交给规划 Agent 分解，并路由至专用执行 Agent，最终沉淀机器可读结果和浏览器证据。

1. 项目以 LangGraph 管理 planner、executor 与 assertion 状态，将步骤路由到浏览器、API、安全、SQL、计时、MCP 等专用 Agent，并为规划和执行阶段分别记录 token、成本与耗时字段。
2. 项目为 Agent 执行建立显式终止边界：导航轮次耗尽时返回带错误标记的结果，执行步骤只有在收到终止标记且不含已知失败信号时才记为完成。
3. 项目将解析后的 Gherkin 场景结果、执行时间和成本写入 JUnit XML，再由 XML 生成 HTML 报告，并关联截图、视频、网络日志和运行日志，形成机器可读报告与运行证据包。
4. 项目同时支持消费 MCP 工具与作为 MCP 服务暴露 Gherkin 生成、测试执行和结果读取接口，并对生成与执行子进程设置有界超时。

这三份都是项目事实版，不代表本仓库作者参与了这些项目。转成个人简历前，应补充候选人的 commit、PR、issue、工作记录或明确陈述的职责范围。特别地，Hercules 当前 HEAD 的公开 CI 虽为绿色，但测试步骤被注释，因此示例没有写“测试通过”；其最新 release 与当前源码也被视为不同证据面。该项目对不可解析 planner 摘要的 JUnit 失败标记仍有缺口，示例因此只写报告与证据包的生成行为，不把它包装成可靠的成功判定。

## 输出契约

默认返回四部分：

1. 三到五条简历项目要点；
2. 每条要点对应的精确 revision、文件或 artifact、证据类别和边界；
3. 被拒绝、需要测量或需要确认个人归因的主张；
4. 用户需要时，从同一份 Claim Ledger 生成的面试故事。

`scripts/lint_examples.py` 只检查示例结构、完整 SHA、若干常见未替换占位符、要点与证据行数量，以及孤立数字。它不会把结构校验冒充语义或实验真实性验证。

```bash
python3 scripts/lint_examples.py examples/*.md
python3 -m unittest discover -s tests -v
```

## 方法来源与许可

方法吸收了 ResumeSkills 的真实改写与 bullet 组织、Matt Pocock skills 的短分支路由与渐进披露，以及“场景—故障—行为—对照—指标—证据边界”六步翻译法；没有采用估算缺失指标、每条强塞数字或伪精确 ATS 评分。详细版本与许可见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

本项目采用 [MIT License](LICENSE)。
