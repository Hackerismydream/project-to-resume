# Evaluation

`project-to-resume` 需要分开验证四件事：包是否完整、模型是否遵循流程、故事是否选得好、用户是否最终采用。把它们混成一个“测试通过”结论会制造错误信心。

## 1. Deterministic package checks

CI 检查：

- Agent Skills 官方规范；
- `SKILL.md` frontmatter、长度、必需章节和关键 reference；
- `agents/openai.yaml` 与 `allow_implicit_invocation`；
- README 安装入口和本地链接；
- YAML、JSON 与 JSON Schema；
- 示例的项目结构、1–5 条 bullet、占位符、内部审计语言和完全重复；
- 缓存、临时文件和重复 payload；
- 隔离复制、官方 CLI 本地安装和合并后 public-main 安装。

它只能证明包结构和确定性合同，没有判断故事语义。

## 2. Curated repository cases

`evals/cases/` 固定：

- 公开仓库；
- 40 位 commit；
- Repository Map 预期；
- top stories 与可接受替代；
- forbidden claims；
- evidence anchors；
- 个人归属边界；
- 必要追问；
- 预期 bullet 数量。

当前覆盖 README 强但实现证据有限、测试暴露关键故障、只能支持两条强故事、fork/upstream、公开仓库归属未知，以及历史 benchmark 与当前 revision 不一致。

这些是人工 gold，不是 Skill 自动运行结果。

## 3. Model forward eval

真正验证 Skill 行为时，应固定：

```text
Skill revision
host model and version
tool permissions
repository commit
target role / JD
context budget
run count
```

每次保存实际读取文件和历史材料、工具调用、是否追问、Repository Map、候选故事、最终输出和评审理由。

评审维度见 [evals/rubric.md](../evals/rubric.md)。至少分开报告：

- fatal factual errors；
- top-story 与 hidden-story discovery；
- peripheral / framework-default story rate；
- upstream 与 ownership confusion；
- semantic duplication；
- copy-ready 程度；
- 面试可讲性。

不要用一次漂亮输出证明方法普遍有效。

## 4. User outcome

最终产品价值需要真实用户确认：

- 最终采用了哪些 bullet；
- 相比原稿改了什么；
- 是否能解释对应链路与取舍；
- 哪些内容因职责或数字问题被删除；
- 是否愿意匿名公开 Before / After。

招聘通过、面试通过或 Offer 受大量外部因素影响，不能直接归因于本 Skill。

## 当前证据状态

当前仓库具备确定性 package checks、固定 revision 的 curated cases、人工 forward-eval rubric 和匿名 Showcase 入口。

当前仓库没有声明：

- 完成大规模或付费模型 eval；
- 在所有语言和仓库规模上稳定找到最佳故事；
- 提高简历通过率、面试通过率或 Offer 概率；
- 拥有真实用户效果统计。

## 建议的下一轮实验

1. 选择不同语言、规模和项目类型的保留集；
2. 使用相同模型和权限对比旧版与新版；
3. 每个 case 多次运行，观察稳定性；
4. 隐去版本来源，由两名评审做 pairwise 比较；
5. 对 fatal error、故事发现、选择和表达分别复盘；
6. 只有真实用户同意时，收集匿名 Before / After。
