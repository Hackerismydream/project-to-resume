# Project to Resume

把一个软件项目整理成面试官能快速理解、证据能够支持的中文技术简历。

给它一个本地仓库或 GitHub 地址，它会阅读源码、测试、Git 历史和已有实验，提炼项目定位、核心技术与简历要点。没有真实指标时不编数字，而是同时给出当前能用的版本和补齐指标后的推荐版本。

## 它能带来什么

| 输入中的问题 | 输出效果 |
| --- | --- |
| README、源码和内部术语散落在各处 | 整理成项目名称、技术栈、项目描述和 3–5 条简历要点 |
| 简历只写模块名，看不出解决了什么 | 翻译成场景、具体故障和可观察的系统行为 |
| 项目没有性能或效果数字 | 保留可信的当前能力，同时给出需要实测的推荐表达 |
| 数字、贡献范围或发布状态不明确 | 标出证据边界，不把项目能力冒充个人贡献或线上效果 |

默认输出两版：

- **当前证据版**：现在的仓库证据已经支持什么，不含虚构指标。
- **指标增强版**：这段经历最值得怎样表达；缺失指标用具名占位符标记，并附最小测量方法。在实测完成前明确不可投递。

## 安装

Codex：

```bash
git clone https://github.com/Hackerismydream/project-to-resume.git ~/.codex/skills/project-to-resume
```

使用 `~/.agents/skills` 的 Agent：

```bash
git clone https://github.com/Hackerismydream/project-to-resume.git ~/.agents/skills/project-to-resume
```

更新已安装的 skill：

```bash
git -C ~/.codex/skills/project-to-resume pull
```

## 使用方法

在目标项目目录中打开 Agent，直接调用：

```text
使用 $project-to-resume 分析当前仓库，生成中文技术简历。
```

它默认会返回当前证据版、指标增强版、指标验证计划和证据边界。以下是几种常见用法。

### 分析公开仓库

```text
使用 $project-to-resume 分析 https://github.com/owner/repo，
输出当前证据版和指标增强版中文简历。
```

### 分析本地项目

```text
使用 $project-to-resume 分析 /path/to/project。
只读取项目，不执行代码；把结果写到 /path/to/output.md。
```

### 核验已有简历

```text
使用 $project-to-resume 核验下面这些项目经历。
逐条判断哪些可以保留、哪些需要降级、哪些指标缺少证据：

[粘贴现有简历]
```

### 根据岗位 JD 调整

```text
使用 $project-to-resume 分析当前仓库，并根据下面的 JD 重排项目要点。
不要改变事实、数字和我的贡献范围：

[粘贴 JD]
```

如果需要写成个人简历，最好同时提供你的 commit、PR、issue、负责范围或工作记录。只有仓库、没有个人贡献信息时，skill 会先输出以“项目”为主语的项目事实版。

## 输出效果示意

```text
当前证据版：
针对关键词检索漏召回和语义检索误召回的问题，融合两路候选排序；
当前证据能够证明实现存在，但不支持召回率提升数字。

指标增强版（待实测，不可投递）：
在 [待实测：检索 Case 数] 个 held-out Case 上，将 Recall@10 从
[待实测：最佳单路 Recall@10] 提升至 [待实测：融合 Recall@10]，
同时将跨项目泄漏率控制为 [待实测：跨项目泄漏率]。
```

完整实跑结果：

- [TGO：全渠道 AI Agent 客服平台](examples/tgo.md)
- [Crystal DBA：PostgreSQL 运维 AI Agent](examples/crystaldba.md)
- [TestZeus Hercules：端到端测试 Agent](examples/testzeus-hercules.md)

## 边界

- 不根据代码规模、测试数量或 README 宣传估算效果指标。
- 不把“存在测试文件”写成“测试已经通过”。
- 不把历史 benchmark、当前源码、发布版本和线上结果混为一谈。
- 不用仓库作者信息推断候选人的个人贡献。

完整工作规则见 [SKILL.md](SKILL.md)，证据规则与输出格式见 [references](references)。
