<div align="center">

# project-to-resume

## 把项目仓库，变成面试官看得懂、问得下去的简历经历。

先读代码、测试和必要的历史变化，再生成一份可直接投递、经得住追问的中文项目经历。

[一分钟开始](#一分钟开始) · [完整案例](examples/pico-empty-response-recovery.md) · [事实边界](#为什么不会随便编造) · [提交案例](showcase/README.md)

</div>

![从项目仓库到简历故事](docs/assets/repository-to-resume-before-after.svg)

## 它与普通简历润色有什么不同

普通润色只能重写你已经写出来的句子。`project-to-resume` 先把仓库当主要事实来源：建立轻量 Repository Map，沿入口、状态、决策、副作用、异常与终态追踪 2–4 条行为链路，让测试帮助发现故障与不变量，再让候选故事经过反证、竞争和语义去重。目标岗位和 JD 只在故事形成后决定选择、顺序和表达。

输入只需要：**项目仓库 + 目标岗位**。默认输出只有一份可直接粘贴的中文项目经历，内部的 Map、Story Card 和 Claim 判断不会占满你的简历。

### 一个固定公开仓库的 Before / After

下面来自 [Pico 空响应恢复 curated case](examples/pico-empty-response-recovery.md)。它由维护者基于固定 commit 人工整理，不是安装后 Skill 的真实模型运行结果。

**Before**

> 使用 Python 开发 Agent，支持模型调用、工具调用、上下文管理和异常重试。

**After（节选）**

> 将无可见正文的模型响应按 thinking-only、工具后空响应和普通空响应分类，分别采用推理回填、短提示和原样重试，并以每轮独立预算限制恢复次数，避免任务直接交付空答案或陷入无限循环。

差异不在于把句子写长，而在于先从源码和测试中找到：失败发生在哪里、系统做了什么判断、状态怎样收敛、证据允许说到什么程度。

## 一分钟开始

安装 Skill：

```bash
npx skills add Hackerismydream/project-to-resume
```

打开自己的项目仓库，在支持 Agent Skills 的编码 Agent 中输入：

```text
使用 $project-to-resume，读取当前仓库，帮我写一段投递 Agent 工程岗位的项目经历。
```

首次路径保持单一：

```text
安装 → 打开自己的项目仓库 → 输入目标岗位 → 得到一份可直接粘贴的项目经历
```

> 当前 repository-first v2 位于 stacked Draft PR 分支。在该 PR 合并前，上面的公开安装命令默认取得的仍可能是 `main` 上的旧版；评审新版本应安装或检出 `codex/repository-discovery-v2`。本地分支 smoke test 只证明包结构和安装内容完整，不等于公开 `main` 已包含新版，也不等于真实模型语义效果已经验证。

## 它会读什么

- 代码入口、构建系统、API、CLI、worker、定时任务、consumer 等执行面；
- 核心对象、状态迁移、输入输出和外部副作用；
- 测试名称、故障注入、断言与回归场景；
- 在必要时读取 git history、PR、issue 或 upstream diff；
- 可选的现有简历、项目说明和目标 JD。

仓库扫描先于岗位匹配。领域 Playbook 只在候选故事形成后作为检查 Lens，不会因为 JD 出现 Redis、MQ、RAG 或 Checkpoint 就只搜索这些组件。

## 内部怎样工作

```text
陌生仓库
→ Repository Map
→ 2–4 条行为链路
→ 测试参与故事发现
→ 条件式 history / upstream
→ Story Hypothesis
→ 候选竞争、反证和淘汰
→ 岗位与 JD 排序
→ Claim 校准
→ 1–5 条可直接粘贴的 bullet
```

下一条 bullet 不再增加新的岗位信号时就停止。只有两个强故事就写两条，只有一个可归属的强故事就写一条，不为了“看起来完整”拆分同一机制或补造数字。

## 为什么不会随便编造

- 实现存在、测试源码、测试运行、测量、发布和生产效果是不同证据层级；
- 源码不能自动写成性能提升，测试文件不能自动写成“测试通过”，benchmark 不能自动写成生产效果；
- 公开仓库事实不能自动变成候选人的个人贡献，fork 或二次开发必须区分 upstream；
- JD 只能改变故事选择与表达，不能改变仓库事实；
- 数字缺少指标对象、baseline、样本或 revision 时，先写机制与边界，最多追问三个会改变成稿的问题。

完整规则见 [SKILL.md](SKILL.md)。

## Curated case 与 eval contracts

- [Pico 空响应恢复完整案例](examples/pico-empty-response-recovery.md)：包含 Repository Map、两条行为链路、候选竞争、淘汰、固定源码/测试锚点、两条最终 bullet、越界表述和面试追问。
- [Eval contracts](evals/README.md) 与 [`evals/cases/`](evals/cases/)：保存固定仓库与 commit 的 curated gold，包括 README 强但实现证据有限、测试暴露故障、只能支持两条强故事、upstream 边界、公开仓库归属未知、历史 benchmark 失配。
- [`evals/requests/`](evals/requests/)：保存正负触发请求；普通 code review 和架构总结不应触发本 Skill。

这些材料是人工策划的评审合同，不得写成真实用户结果或自动模型运行结果。

## 校验

```bash
python3 scripts/lint_examples.py examples/*.md
python3 scripts/validate_package.py
python3 -m unittest discover -s tests -v
python3 scripts/smoke_install.py --source .
git diff --check
```

静态校验检查 frontmatter、名称、`agents/openai.yaml`、本地链接、示例格式、eval schema、固定 commit 锚点和必需文件；它不验证模型是否真的找到了最佳故事，也不证明简历效果。

## 提交真实 Before / After

[`showcase/README.md`](showcase/README.md) 提供轻量提交格式，也可以使用 [Showcase Issue 模板](.github/ISSUE_TEMPLATE/showcase.yml)。只接受公开仓库和固定 commit；不收集私人简历全文、电话、邮箱、学校、身份证明、公司内部仓库或客户数据，未经明确许可不公开姓名、公司和求职状态。
