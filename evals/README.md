# Evaluation contracts

本目录保存固定仓库、固定 commit 的人工评审合同。

- `schema.json`：case 的 JSON Schema；
- `cases/*.yaml`：Repository Map、候选故事、禁止 Claim、证据锚点和个人归属边界；
- `requests/*.json`：Skill 的正负触发请求；
- `rubric.md`：人工或模型 forward eval 的评审方式。

`curated_gold: true` 只表示维护者人工整理；只有实际执行安装后的 Skill 并保存完整运行材料时，才能把 `actual_skill_run` 设为 `true`。静态校验不证明模型能找到最佳故事，也不证明简历结果更好。
