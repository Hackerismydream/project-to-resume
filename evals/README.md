# Repository Discovery Eval Contracts

本目录保存确定性的评审输入和 curated gold，不保存“模型已经达到某个成功率”的结论。

- `schema.json`：真实仓库 case 的结构合同。
- `cases/*.yaml`：使用 JSON 语法编写的 YAML 1.2 子集，便于在没有 PyYAML 时用标准库解析。
- `requests/*.json`：Skill 正负触发请求。

每个 case 必须固定公开仓库和 40 位 commit，分别记录 Repository Map 预期、候选故事、可接受替代、禁止 Claim、证据锚点、个人归属边界和必要追问。`curated_gold: true` 只表示维护者人工整理；除非真的执行安装后的 Skill 并保存运行材料，否则 `actual_skill_run` 必须为 `false`。

这些 case 可以用于后续 forward eval，但本仓库的静态校验只证明 schema、锚点和文件结构一致，不判断生成故事是否语义正确。
