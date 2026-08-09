<div align="center">

# Project to Resume

**把项目仓库和已有简历，变成岗位匹配、可直接投递的中文项目经历。**

[![Validate](https://github.com/Hackerismydream/project-to-resume/actions/workflows/validate.yml/badge.svg)](https://github.com/Hackerismydream/project-to-resume/actions/workflows/validate.yml)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-2563eb?style=flat-square)](https://agentskills.io)

</div>

## Quick start

安装：

```bash
npx skills add Hackerismydream/project-to-resume
```

然后直接提供你手头已有的材料：

```text
使用 $project-to-resume，根据当前仓库帮我写一段投递 Java 后端的项目经历。
```

```text
使用 $project-to-resume，对照这个仓库优化我简历里的项目描述：
[粘贴简历]
```

```text
使用 $project-to-resume，帮我优化下面的秋招简历。我没有仓库：
[粘贴简历]
```

## 它怎么工作

Skill 会自动识别四种输入：

- **只有仓库**：从项目中生成新的简历经历。
- **简历 + 仓库**：保留业务背景和个人职责，用仓库补强技术故事。
- **只有简历**：直接优化定位、选材和表达，不要求补仓库。
- **叠加 JD**：只调整项目选择、顺序和表达角度，不凭 JD 新增经历。

用户在简历语境中发来的本地仓库，默认按候选人项目处理；如果是公开第三方、团队或开源仓库，则会区分项目能力与个人贡献。Skill 会先给出可直接粘贴的版本，只有缺失信息会明显改变结果时，才追加 1–3 个问题。

默认不会输出证据表、SHA、Claim Ledger、测量计划或多份占位版本。严格核验和面试防御只在明确要求时启用。
成品之后默认停止，不追加审计免责声明或过程汇报。

## 默认产物

```text
项目名称｜角色
技术栈：岗位相关且能够回答的技术

项目描述：业务场景 + 核心链路 + 系统边界 + 个人职责

1. 核心业务链路或建模
2. 最关键的技术问题与设计
3. 异常边界、验证结果或排障闭环
```

没有数字也可以写出强简历；Skill 会使用机制、边界、覆盖链路和验证方式，不会编造指标。

## 内置方法论

使用入口保持很短，复杂判断放在按需加载的方法库中。完整流水线是“输入与岗位定位 → Project Fact Card → 候选故事 → Claim 与指标边界 → 领域专项深挖 → 成品编排 → 面试反向复核”。

- [输入、岗位与项目选择](references/intake-and-positioning.md)：三种材料路线、岗位画像、项目组合与 JD 映射。
- [业务场景与项目故事](references/business-story.md)：Fact Card、场景链、故事排序、语义去重和技术栈选择。
- [Claim 与指标口径](references/claims-and-metrics.md)：个人归属、动词强度、百分比、小样本和无数字降级。
- [后端专项](references/playbook-backend.md)：事务、状态、库存、缓存、MQ、数据库、稳定性、压测和排障。
- [AI / Agent / RAG 专项](references/playbook-ai-agent-rag.md)：任务生命周期、工具、上下文、恢复、检索、评测和结果边界。
- [科研、实习与开源专项](references/playbook-research-internship.md)：实验公平性、团队/个人归属、交付与上游贡献状态。
- [成品编排](references/resume-format.md)、[面试防御](references/interview-defense.md) 与 [严格核验](references/evidence-rules.md)：分别控制投递格式、追问深度和证据审计。

不同主 Lens 与实习、科研、开源 overlay 的组合关系见 [岗位与项目类型路由索引](references/project-playbooks.md)。

`agents/openai.yaml` 只负责 Skill 的展示名称、简介和默认提示，因此刻意保持精简；真正决定生成质量的是 `SKILL.md` 的路由与上述方法库。

## 输入示例

- [只有仓库](examples/repository-only.md)
- [简历 + 仓库](examples/resume-and-repository.md)
- [只有简历](examples/resume-only.md)
- [实习 + 个人项目 + JD](examples/multi-project-jd.md)

## 边界

- 不编造不存在的技术、数字、业务规模、上线状态、奖项或职责。
- 不因为缺少仓库、benchmark 或公开证明而拒绝生成简历。
- 默认只读仓库，不执行代码、不安装依赖、不泄露私有信息。
- 用户明确要求核验时，才进入严格证据审计。

完整规则见 [SKILL.md](SKILL.md)。
