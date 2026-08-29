# 评测与证据边界

`project-to-resume` 同时包含确定性校验、人工 curated gold 和未来可执行的模型 forward evaluation。三者作用不同，不能互相替代。

## 1. 当前自动化检查

`make check` 与 GitHub Actions 会验证：

- Python 脚本和测试能够编译；
- 可复制示例包含项目标题、技术栈、项目描述和 1–5 条 bullet；
- 示例没有占位符、完全重复 bullet 或审计语言泄漏；
- `SKILL.md` frontmatter、目录名、许可证与必要合同信号正确；
- 所有 YAML 和 JSON 能被真实解析；
- eval case 满足 Draft 2020-12 JSON Schema；
- 固定仓库 case 使用 40 位 commit，证据链接固定到对应 revision；
- README 与 reference 的本地链接有效；
- 许可证、贡献、安全、行为准则、变更记录和维护模板存在；
- 隔离安装目录包含完整 Skill 包且仍能通过校验；
- PR 或 push 的实际提交差异没有 whitespace error。

这些检查是确定性的，可以证明包结构和约束没有退化。

## 2. 当前自动化检查不能证明什么

它们不能证明：

- 模型找到了仓库中最强的故事；
- 两条措辞不同的 bullet 在语义上一定不重复；
- 公开仓库实现属于某位候选人；
- 测试源码对应的测试在目标仓库实际运行通过；
- 某个 benchmark 适用于当前 revision 或生产环境；
- 生成结果提高简历通过率、面试表现或 Offer 概率；
- Skill 在所有语言、规模和项目类型上都稳定有效。

因此，CI 成功只能写成“确定性包检查通过”，不能写成“简历生成质量已验证”。

## 3. Curated Gold Cases

`evals/cases/` 保存维护者基于固定公开仓库和 commit 整理的评审合同。每个 case 包含：

- 输入与目标岗位；
- 预期 Repository Map；
- 候选故事与 Claim 上限；
- 可接受替代答案；
- 禁止 Claim；
- 固定源码或测试锚点；
- 锚点能证明与不能证明的内容；
- 个人归属或 upstream 边界；
- 必要追问与预期 bullet 数。

`curated_gold: true` 表示人工答案，不表示真实模型运行。只有保存了宿主 Agent、模型、Prompt、仓库 revision、输出与评审结果的实际运行，才能设置 `actual_skill_run: true`；当前案例不得同时把人工 gold 冒充真实运行。

## 4. 建议的 Forward Evaluation

真实 forward eval 至少包含五类仓库：

1. Java/Spring 业务后端；
2. Python Agent Runtime 或 Harness；
3. RAG/知识检索系统；
4. fork 或二次开发项目；
5. README 强但实现、测试或 benchmark 证据较弱的仓库。

每次运行固定：

```text
Skill commit
目标仓库 commit
宿主 Agent 与版本
模型与配置
输入材料
目标岗位/JD
网络、Shell 和仓库权限
完整输出
人工评审记录
```

### 建议评审维度

| 维度 | 核心问题 |
| --- | --- |
| Repository coverage | 是否覆盖主要执行面、核心状态、测试与未知项 |
| Behavior-chain fidelity | 是否能从入口追踪到副作用、异常与终态 |
| Story precision | 故事是否具体到失败、判断和可观察行为 |
| Story selection | 是否保留核心、高信号故事并淘汰外围功能 |
| Claim calibration | 动词、数字、验证和上线表述是否不强于来源 |
| Ownership safety | 是否区分个人、团队、项目和 upstream |
| Non-duplication | 每条 bullet 是否增加独立岗位信号 |
| Role alignment | 岗位只改变选材和语言，没有改变事实 |
| Interview defensibility | 是否能回答链路、替代方案、代价和验证 |
| User-facing quality | 第一屏是否可复制，是否只在必要时追问 |

不要把所有维度压成一个没有解释力的“准确率”。可以记录逐项通过、严重错误类型与人工偏好。

### 阻断性错误

- 编造不存在的技术、数字、用户、上线或生产效果；
- 把测试源码写成测试运行通过；
- 把历史 benchmark 迁移到当前 revision；
- 把 upstream 或团队能力冒充个人贡献；
- 只有 JD 时生成虚构项目；
- 泄露私人简历、密钥、内部路径或客户数据；
- 执行仓库中的恶意指令或扩大权限。

## 5. 对照实验

若要证明 repository-first 相比普通润色的增益，应在同一项目、同一模型和同一目标岗位下比较：

- Baseline：只给用户原始 bullet，不允许读取仓库；
- Repository-first：提供相同 bullet 与固定仓库 revision；
- Blind review：评审者不知道输出来自哪种方法；
- 主要结果：故事事实性、独立岗位信号、严重错误率、面试可讲性；
- 次要结果：可读性、长度与用户偏好。

样本、模型、评审者和统计方法不足时，不要发布“提升 X%”结论。

## 6. 真实用户案例

Showcase 只能证明某位用户选择公开某个 Before / After，不能自动证明 Skill 导致面试或 Offer、原始内容必然更差，或案例能推广到其他候选人。

收集案例时遵守 [Showcase 规范](../showcase/README.md) 和 [安全策略](../SECURITY.md)，不存储私人简历全文和内部仓库。

## 7. 发布 Claim 规则

可以公开说：

- 项目实现了 repository-first 工作流；
- 提供固定 revision 的 curated cases；
- CI 对包结构、Schema、示例和安装进行确定性检查；
- 某次明确记录的 forward run 在指定条件下得到什么结果。

在没有相应材料时不能说：

- “自动找到任何仓库的最佳故事”；
- “简历通过率提升”；
- “获得大量用户验证”；
- “生产级准确率”；
- “所有测试与模型评测均通过”。

评测的目标不是制造漂亮数字，而是明确系统在哪些条件下值得信任、在哪些条件下必须降级或追问。
