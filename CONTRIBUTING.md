# Contributing

感谢你改进 `project-to-resume`。本项目的核心目标不是让简历措辞更夸张，而是让“仓库事实 → 工程故事 → 简历 Claim”这一过程更可靠、可维护、可复核。

## 贡献类型

欢迎提交：

- 对陌生仓库探索、故事选择、Claim 边界和面试反向校验的改进；
- 固定公开仓库与 commit 的 curated eval case；
- 不包含私人信息的 Before / After 案例；
- 示例、文档、安装体验、CI 和确定性校验修复；
- 后端、Agent、RAG、科研或开源项目 Playbook 的可迁移经验。

不接受：

- 编造项目、职责、指标、上线状态、用户反馈或招聘结果；
- 把测试源码写成测试已通过，把 benchmark 写成生产效果；
- 上传私人简历全文、联系方式、内部仓库、客户数据、密钥或日志；
- 为了命中 JD 而加入材料中不存在的技术；
- 将本项目扩成求职平台、简历数据库或需要持久化个人材料的服务。

## 开发环境

需要 Python 3.11+。

```bash
python3 -m pip install -r requirements-dev.txt
make check
```

`make check` 会执行：

1. Python 编译检查；
2. 可复制示例结构校验；
3. Skill 包、YAML、JSON Schema、本地链接和治理文件校验；
4. 单元测试；
5. 隔离安装 smoke test。

## 修改方法论

方法修改应回答：

- 它修复了哪一种错误输出或阅读偏差；
- 为什么现有规则不足；
- 新规则怎样改变候选故事、Claim 上限或停止条件；
- 是否存在反例或副作用；
- 如何用固定 case 验证，而不是只增加说明文字。

优先修改按需加载的 `references/`，保持 `SKILL.md` 是清晰的执行合同。不要让主文件退化成覆盖所有领域术语的百科全书。

## 新增 Eval Case

在 `evals/cases/` 中增加使用 YAML 1.2/JSON 兼容结构的文件，并满足 `evals/schema.json`。每个 case 必须：

- 固定公开 GitHub 仓库和 40 位 commit；
- 描述预期 Repository Map、候选故事和 Claim 上限；
- 提供固定 commit 的源码或测试锚点；
- 分别写清锚点能证明什么、不能证明什么；
- 记录个人归属或 upstream 边界；
- 给出禁止 Claim 与必要追问；
- 明确 `curated_gold` 和 `actual_skill_run`，不能把人工答案冒充真实模型运行。

新增 coverage 标签时，同时更新 `scripts/validate_package.py` 和对应测试。

## 新增 Before / After

遵守 [Showcase 提交规范](showcase/README.md)。只提交与项目有关的少量原文，不提交完整简历。案例必须固定 revision，并获得必要的公开授权。

## Pull Request 要求

PR 应保持单一目标，并在正文中说明：

- 问题与用户可见影响；
- 主要设计和取舍；
- 修改文件；
- 实际运行的验证命令与结果；
- 哪些语义或真实用户效果仍未验证；
- 是否改变触发范围、个人归属、数字或输出合同。

提交前确认：

```bash
make check
git diff --check
```

不要把本地未运行的测试、旧 revision 的 benchmark 或 CI 预期写成已经通过。

## Commit 与 Review

- 使用可解释的提交信息，例如 `fix: reject JD-only generation`；
- 避免把重构、方法变化、案例和宣传素材混在一个不可审查提交中；
- Review 优先检查事实边界、失败模式、反证与用户第一次使用路径；
- 发现安全或隐私问题时不要公开提交，按 [SECURITY.md](SECURITY.md) 报告。

提交贡献即表示你同意贡献内容按照 [Apache License 2.0](LICENSE) 许可。
