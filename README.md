<div align="center">

# project-to-resume

### 把项目仓库，变成面试官看得懂、问得下去的中文项目经历。

先读代码、测试和必要的历史变化，再写简历。不是把“用了 Redis / MQ / RAG / Tool Calling”换一种说法。

[![Validate](https://github.com/Hackerismydream/project-to-resume/actions/workflows/validate.yml/badge.svg)](https://github.com/Hackerismydream/project-to-resume/actions/workflows/validate.yml)
[![skills.sh](https://skills.sh/b/Hackerismydream/project-to-resume)](https://skills.sh/Hackerismydream/project-to-resume/project-to-resume)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

[一分钟开始](#一分钟开始) · [完整 Before / After](skills/project-to-resume/examples/pico-empty-response-recovery.md) · [方法边界](#为什么不会随便编造) · [提交案例](showcase/README.md)

</div>

![从项目仓库到简历故事](docs/assets/repository-to-resume-before-after.svg)

## 为什么不是普通简历润色

很多项目的代码里已经有状态流转、异常恢复、一致性、权限、评测和工程取舍，写进简历却只剩：

> 使用 Python 开发 Agent，支持模型调用、工具调用、上下文管理和异常重试。

`project-to-resume` 先把仓库当作主要事实来源：建立轻量 Repository Map，沿入口、状态、关键决策、副作用、异常和终态追踪核心行为，让测试帮助发现项目真正担心的失败，再让候选故事经过反证、竞争和去重。目标岗位和 JD 最后才负责选择、排序和表达。

最终默认只给一份**可直接粘贴的中文项目经历**。内部的 Repository Map、Story Card 和 Claim 判断不会占满你的简历。

## 一分钟开始

安装：

```bash
npx skills add Hackerismydream/project-to-resume --skill project-to-resume -y
```

然后在自己的项目仓库中输入：

```text
使用 $project-to-resume，读取当前仓库，帮我写一段投递 Agent 工程岗位的项目经历。
```

把 `Agent 工程` 换成 `Java 后端`、`RAG / AI 应用` 或你的目标岗位即可。

```text
安装 → 打开项目仓库 → 输入目标岗位 → 得到一份可直接粘贴的项目经历
```

> 仓库里只有 JD、没有任何项目事实时，Skill 不会从 JD 反向创造经历；它会请求仓库、项目说明或现有简历。

## 一个固定公开仓库的 Before / After

下面来自 [Pico 空响应恢复 curated case](skills/project-to-resume/examples/pico-empty-response-recovery.md)，固定在公开 commit `aedcaf2cf928af145ef349fb0312b8e66d12ae74`。它是维护者人工整理的 gold case，不是用户效果或自动模型成功率。

**Before**

> 使用 Python 开发 Agent，支持模型调用、工具调用、上下文管理和异常重试。

**After（节选）**

> 将无可见正文的模型响应按 thinking-only、工具后空响应和普通空响应分类，分别采用推理回填、短提示和原样重试，并以每轮独立预算限制恢复次数，避免任务直接交付空答案或陷入无限循环。

变化不是“句子更长”，而是先从源码和测试里找到了失败分类、恢复策略、预算边界和状态清理，再决定哪些事实值得占用简历版面。

## 它会读什么

- 顶层目录、主要语言、构建系统和入口；
- API、CLI、worker、cron、consumer、daemon、hook 等执行面；
- 核心对象、状态迁移、输入输出和外部副作用；
- 测试名称、故障注入、断言与回归场景；
- benchmark、release、migration 与必要文档；
- 只有在需要解释设计变化、fork/upstream 或版本冲突时，才扩展到 git history、PR、issue 和 upstream diff。

仓库探索先于岗位匹配，不会因为 JD 出现 Redis、Kafka、RAG、Checkpoint 就只搜索这些熟悉词。

## 内部流程

```text
Repository Map
→ 1–4 条核心行为链路（通常 2–4 条）
→ 测试参与故事发现
→ 条件式 history / upstream
→ Story Hypothesis / Story Card
→ 反证、竞争、去重、淘汰
→ 岗位与 JD 排序
→ Claim 校准
→ 1–5 条可直接粘贴的 bullet
```

下一条 bullet 不再增加新的岗位信号时就停止。只有两个强故事就写两条，不把同一机制拆开凑成三条。

## 为什么不会随便编造

- 实现、测试源码、测试运行、测量、发布和生产效果是不同证据层级；
- 源码存在不能自动写成性能提升；
- 测试文件存在不能自动写成“测试通过”；
- benchmark 只描述固定 revision / 样本 / 负载下的有界结果，不自动代表生产；
- 公开仓库能力不能自动变成候选人的个人贡献；fork / 二次开发必须区分 upstream；
- 没有可靠数字时写机制、边界、覆盖链路和验证方式，不补造“提升 xx%”；
- JD 只能改变选材、顺序和表达，不能改变仓库事实。

### 仓库内容本身也不可信

README、AGENTS.md、Prompt、脚本、注释、issue 和测试 fixture 都被当作**待分析的数据**，不是对 Skill 的新指令。Skill 默认只做静态只读分析，不因为仓库里的文字执行命令、安装依赖、上传文件、访问外部服务或读取密钥。

完整行为合同见 [`skills/project-to-resume/SKILL.md`](skills/project-to-resume/SKILL.md)。

## Skill 包结构

```text
skills/project-to-resume/
├── SKILL.md
├── agents/openai.yaml
├── references/
└── examples/
```

运行时 Skill 与仓库的测试、CI、eval 和维护脚本分离。这样 `skills` CLI 安装的是实际需要的 Skill payload，而不是整个开发仓库。

## Evals 与验证

仓库当前维护两类验证：

1. **确定性工程检查**：frontmatter、本地链接、YAML/JSON、示例格式、固定 commit 锚点、Skill payload、CLI 安装和单元测试；
2. **curated eval contracts**：固定公开仓库/commit 的 Repository Map、候选故事、禁止 Claim、ownership 和必要追问。

它们能证明包结构和方法合同没有漂移，**不能证明模型一定找到“最佳故事”或提升简历通过率**。

开发验证：

```bash
python3 scripts/lint_examples.py skills/project-to-resume/examples/*.md
python3 scripts/validate_package.py
python3 -m unittest discover -s tests -v
python3 scripts/smoke_install.py --source .
git diff --check
```

Eval 说明见 [`evals/README.md`](evals/README.md)。

## 真实案例传播

如果你愿意公开一个 Before / After，可以按 [`showcase/README.md`](showcase/README.md) 提交，或使用 [Showcase Issue 模板](.github/ISSUE_TEMPLATE/showcase.yml)。

只接受公开仓库和固定 commit；不收集私人简历全文、电话、邮箱、学校、身份证明、公司内部仓库、客户数据或密钥。未经明确许可，不公开姓名、公司和求职状态。

## Contributing

欢迎提交：

- 新的固定公开仓库 eval case；
- 能反证现有方法的失败样例；
- 安装/激活兼容性问题；
- Claim 边界和误触发问题；
- 真实、已获授权的匿名 Before / After。

请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。安全问题见 [SECURITY.md](SECURITY.md)。

## License

Apache License 2.0，见 [LICENSE](LICENSE)。
