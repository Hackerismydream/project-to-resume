# 岗位与项目类型路由索引

这是供维护者和读者快速浏览的索引。Skill 运行时不需要先加载本索引。

领域 Playbook 必须在 Repository Map、行为链路和初始 Story Hypothesis 已形成之后使用。它们负责检查候选故事是否遗漏领域边界，不能预先规定仓库必须出现哪些熟悉技术。

## 发现与选择顺序

1. 使用 [repository-discovery.md](repository-discovery.md) 建立岗位无关的 Repository Map，并追踪 2–4 条行为链路。
2. 使用 [story-selection.md](story-selection.md) 建立 Story Card，检查反证、竞争、语义去重和淘汰。
3. 再使用 [intake-and-positioning.md](intake-and-positioning.md) 应用目标岗位和 JD。
4. 只加载一个主 Lens；存在实习、科研或开源边界时叠加一个 Overlay。
5. 涉及数字时读取 [claims-and-metrics.md](claims-and-metrics.md)。
6. 最后使用 [business-story.md](business-story.md) 与 [resume-format.md](resume-format.md) 编排成品。

## 主 Lens

| 已形成候选的中心问题 | 主 Lens | 读取 |
| --- | --- | --- |
| 业务状态、数据边界、并发、事务、缓存和异步一致性 | Java / 后端 | [playbook-backend.md](playbook-backend.md) |
| 模型进入确定业务流程，输出如何约束和兜底 | AI 应用 | [playbook-ai-agent-rag.md](playbook-ai-agent-rag.md) |
| 多步任务如何在工具、状态、上下文、终止和恢复约束下推进 | Agent / Harness | [playbook-ai-agent-rag.md](playbook-ai-agent-rag.md) |
| 知识如何清洗、索引、召回、重排、引用和更新 | RAG / 知识系统 | [playbook-ai-agent-rag.md](playbook-ai-agent-rag.md) |
| 数据、baseline、方法变化、实验公平性和误差边界 | 算法 / 科研 | [playbook-research-internship.md](playbook-research-internship.md) |

混合项目只选择一个主 Lens：问“这个系统失败时，最难处理的是业务状态、模型输出、任务执行、知识召回，还是实验结论？”答案决定主线，最多再叠加一个次 Lens，避免同一链路重复写三遍。

## Overlay

| 经历类型 | 额外读取 | 必须守住的边界 |
| --- | --- | --- |
| 实习 / 团队项目 | [playbook-research-internship.md](playbook-research-internship.md) | 团队系统、团队结果与个人动作分开 |
| 开源 / 二次开发 | [playbook-research-internship.md](playbook-research-internship.md) | 上游已有能力与本人新增能力分开 |
| 科研实习 | AI/后端专项 + 科研实习专项 | 先说明团队接口，再讲实验或工程贡献 |
| 垂直行业 AI | AI 专项 + 对应行业事实 | 行业对象、流程和容错约束先于 AI 名词 |
| 课程 / 竞赛项目 | 对应技术专项 | 写问题、个人负责和验收，不虚构生产规模 |
