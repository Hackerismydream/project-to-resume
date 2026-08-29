# Contributing

感谢你改进 `project-to-resume`。本项目的目标不是让简历措辞更夸张，而是让“仓库事实 → 工程故事 → 简历 Claim”这一过程更可靠、可维护、可复核。

## 欢迎的贡献

- 改进陌生仓库探索、故事选择、Claim 边界与面试反向校验；
- 增加固定公开仓库和 commit 的 curated eval case；
- 提交不包含私人信息的 Before / After 案例；
- 修复安装、示例、文档、CI 与确定性校验；
- 补充后端、Agent、RAG、科研或开源项目中的可迁移工程经验。

## 不接受的内容

- 编造项目、职责、技术、指标、上线状态、用户反馈或招聘结果；
- 把测试源码写成测试已经通过，把 benchmark 写成生产效果；
- 上传私人简历全文、联系方式、内部仓库、客户数据、密钥或日志；
- 为命中 JD 而加入材料中不存在的技术；
- 将项目扩成求职平台、简历数据库或需要持久化个人材料的服务。

## 开发环境

需要 Python 3.11+。

```bash
python3 -m pip install -r requirements-dev.txt
make check
```

`make check` 会执行 Python 编译、示例结构校验、Skill 包与 Schema 校验、单元测试和隔离安装 smoke test。

## 修改方法论

方法修改应回答：

1. 它修复了哪一种错误输出或阅读偏差；
2. 为什么现有规则不足；
3. 新规则怎样改变候选故事、Claim 上限或停止条件；
4. 是否存在反例或副作用；
5. 如何用固定 case 验证，而不是只增加说明文字。

优先修改按需加载的 `references/`，保持 `SKILL.md` 是清晰的执行合同。不要让主文件退化成覆盖所有领域术语的百科全书。

## 新增 Eval Case

在 `evals/cases/` 中增加满足 `evals/schema.json` 的 YAML 文件。每个 case 必须：

- 固定公开 GitHub 仓库和 40 位 commit；
- 描述预期 Repository Map、候选故事与 Claim 上限；
- 提供固定 commit 的源码或测试锚点；
- 分别写清锚点能证明什么、不能证明什么；
- 记录个人归属或 upstream 边界；
- 给出禁止 Claim 与必要追问；
- 明确 `curated_gold` 和 `actual_skill_run`，不能把人工答案冒充真实模型运行。

新增 coverage 标签时，同时更新验证器与对应测试。

## 新增 Before / After

遵守 [Showcase 提交规范](showcase/README.md)。只提交与项目有关的少量原文，不提交完整简历。案例必须固定 revision，并取得必要的公开授权。

## Pull Request 要求

PR 应保持一个可审查目标，并说明：

- 问题与用户可见影响；
- 主要设计、替代方案与取舍；
- 实际修改范围；
- 运行过的验证命令与结果；
- 哪些语义或真实用户效果仍未验证；
- 是否改变触发范围、个人归属、数字或默认输出合同。

提交前运行：

```bash
make check
git diff --check
```

不要把计划运行的测试、旧 revision 的 benchmark 或预期 CI 写成已经通过。

## Commit 与 Review

- 使用可解释的提交信息，例如 `fix: reject JD-only generation`；
- 避免把方法变化、案例和宣传素材混成一个不可审查提交；
- Review 优先检查事实边界、失败模式、反证与用户首次使用路径；
- 发现安全或隐私问题时不要公开提交，按 [SECURITY.md](SECURITY.md) 报告。

提交贡献即表示你同意贡献内容按照 [Apache License 2.0](LICENSE) 许可。社区行为规范见 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。
