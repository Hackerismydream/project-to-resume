<div align="center">

# project-to-resume

**先读项目仓库，再写技术简历。**

从代码、测试和必要的历史变化中发现可追溯、可归属、能被面试追问的工程故事，生成一份可直接粘贴的中文项目经历。

[![Validate](https://github.com/Hackerismydream/project-to-resume/actions/workflows/validate.yml/badge.svg)](https://github.com/Hackerismydream/project-to-resume/actions/workflows/validate.yml)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-2563eb?style=flat-square)](https://agentskills.io)
[![License](https://img.shields.io/badge/license-Apache--2.0-0b7285?style=flat-square)](LICENSE)

[一分钟开始](#一分钟开始) · [完整案例](examples/pico-empty-response-recovery.md) · [工作原理](#工作原理) · [事实边界](#事实边界) · [贡献指南](CONTRIBUTING.md)

</div>

![从项目仓库到简历故事](docs/assets/repository-to-resume-before-after.svg)

## 为什么不是普通简历润色

普通润色只能改写你已经写出来的句子。`project-to-resume` 把仓库作为系统行为和实现事实的主要来源：先建立轻量 Repository Map，沿入口、状态、关键决策、副作用、异常和终态追踪核心链路，让测试暴露项目真正担心的失败与不变量，再让候选故事经过反证、竞争和语义去重。目标岗位和 JD 最后才负责选材、排序与语言转换。

输入通常只需要：

```text
项目仓库 + 目标岗位
```

默认输出只有一份可直接粘贴的项目经历，不会把内部 Map、Story Card、完整 SHA 或证据表塞进简历。

## 一分钟开始

### 1. 安装

```bash
npx skills add Hackerismydream/project-to-resume
```

也可以按照 [安装与更新说明](docs/installation.md) 进行项目级或手动安装。

### 2. 打开自己的项目仓库

在支持 Agent Skills 的 Coding Agent 中进入仓库目录。

### 3. 输入目标岗位

```text
使用 $project-to-resume，读取当前仓库，帮我写一段投递 Agent 工程岗位的项目经历。
```

Java 后端示例：

```text
使用 $project-to-resume，先独立审计当前仓库，再帮我写成投递 Java 后端岗位的项目经历。不要编造压测数字。
```

已有简历示例：

```text
使用 $project-to-resume，对照当前仓库重写下面两条项目经历，并保留我真实负责的业务范围：
[粘贴原文]
```

首次使用路径保持单一：

```text
安装 → 打开仓库 → 输入目标岗位 → 得到可直接粘贴的项目经历
```

## Before / After

下面来自 [Pico 空响应恢复案例](examples/pico-empty-response-recovery.md)。案例由维护者基于固定公开 commit 人工整理，用于展示方法与事实边界；它不是自动模型运行结果，也不代表简历通过率或真实用户效果。

**Before**

> 使用 Python 开发 Agent，支持模型调用、工具调用、上下文管理和异常重试。

**After（节选）**

> 将无可见正文的模型响应按 thinking-only、工具后空响应和普通空响应分类，分别采用推理回填、短提示和原样重试，并以每轮独立预算限制恢复次数，避免任务直接交付空答案或陷入无限循环。

差异不在于句子更长，而在于先回答了：失败发生在哪里、系统做了什么判断、状态如何收敛、测试证明到哪一层、哪些结果不能声称。

## 工作原理

```text
陌生仓库
→ Repository Map
→ 2–4 条行为链路
→ 测试参与故事发现
→ 条件式 history / PR / issue / upstream
→ Story Hypothesis 与 Story Card
→ 反证、竞争、去重与淘汰
→ 岗位与 JD 排序
→ Claim 校准
→ 1–5 条可直接粘贴的 bullet
```

Repository Map 会检查：

- 仓库身份、固定 revision、fork 与 upstream；
- API、CLI、worker、consumer、cron、daemon、hook 等执行面；
- 核心对象、状态迁移、输入输出与外部副作用；
- 超时、重复、部分成功、恢复、补偿、权限和兼容性；
- 测试、benchmark、发布材料、migration 与必要历史；
- 仍会改变定位、归属或 Claim 的未知项。

下一条 bullet 不再增加新的岗位信号时就停止。只有两个强故事就写两条，只有一个可归属的强故事就写一条，不为了数量拆分同一机制、抬高外围功能或补造数字。

完整执行合同见 [SKILL.md](SKILL.md)。详细方法按需拆分在 [`references/`](references/) 中。

## 支持的输入

| 输入 | 处理方式 |
| --- | --- |
| 仓库 + 岗位/JD | 先做岗位无关发现，再按岗位排序 |
| 仓库 + 现有简历 | 仓库确认行为，简历补充业务背景、个人职责与数字 |
| 多个仓库或项目 | 分别轻量发现，选择 1–2 个互补项目 |
| 只有简历或项目说明 | 仅优化已有事实，不脑补代码实现 |
| 只有 JD | 不生成虚构经历；请求仓库、简历或项目材料 |

## 事实边界

- README 与设计文档说明意图，不自动证明实现；
- 源码可以支持确定性行为，不自动支持性能提升、生产可用或业务效果；
- 测试文件存在不等于测试已经运行通过；
- benchmark 只代表固定 revision、环境、样本与 baseline；
- 公开仓库事实不能自动变成候选人的个人贡献；
- fork、团队项目与二次开发必须区分 upstream、团队结果和个人动作；
- 没有可信数字时，优先写机制、边界、状态收敛与验证方式。

本仓库的自动化检查验证包结构、YAML/JSON Schema、示例格式、固定 commit 锚点、本地链接和隔离安装，不声称能够自动证明故事选择正确、事实归属正确或简历效果提升。

## 案例与评测合同

- [Pico 空响应恢复完整案例](examples/pico-empty-response-recovery.md)：Repository Map、行为链路、候选竞争、淘汰、源码与测试锚点、两条最终 bullet、越界表述和面试追问。
- [Eval contracts](evals/README.md)：固定公开仓库和 commit 的人工 gold cases，覆盖测试暴露故障、upstream 边界、公开仓库归属未知和历史 benchmark 失配。
- [`evals/requests/`](evals/requests/)：正负触发请求；普通 code review 和架构总结不应触发本 Skill。
- [评测与证据说明](docs/evaluation.md)：自动检查能够证明什么、不能证明什么，以及怎样补充真实 forward evaluation。

这些材料是评审合同，不是用户成功案例、招聘结果或自动模型评测分数。

## 本地开发

需要 Python 3.11+。

```bash
python3 -m pip install -r requirements-dev.txt
make check
```

等价命令：

```bash
python3 -m py_compile scripts/*.py tests/*.py
python3 scripts/lint_examples.py examples/*.md
python3 scripts/validate_package.py
python3 -m unittest discover -s tests -v
python3 scripts/smoke_install.py --source .
```

CI 对 push 和 pull request 执行同一组确定性检查，并使用完整 Git 历史检查实际提交差异中的 whitespace error。

## 项目结构

```text
SKILL.md                 Skill 入口与执行合同
agents/openai.yaml       Agent Skills 展示配置
references/              按需加载的方法与领域 Playbook
examples/                可复制示例与固定案例
evals/                   Schema、curated gold 与触发合同
scripts/                 示例、包结构和隔离安装检查
tests/                   确定性回归测试
docs/                    安装、评测和视觉材料
showcase/                公开 Before / After 提交规范
.github/                 CI、Issue 与 PR 模板
```

## 贡献与维护

- 提交代码、案例或方法修订前阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。
- 行为规范见 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。
- 安全与隐私问题按 [SECURITY.md](SECURITY.md) 私下报告，不要在公开 Issue 中粘贴简历、密钥或内部代码。
- 版本变化记录在 [CHANGELOG.md](CHANGELOG.md)。
- 公开 Before / After 应遵守 [Showcase 规范](showcase/README.md)，只提交公开仓库、固定 commit 与经授权的匿名化内容。

## License

[Apache License 2.0](LICENSE)
