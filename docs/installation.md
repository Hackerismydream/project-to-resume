# 安装与更新

`project-to-resume` 是目录型 Agent Skill，不需要启动服务。安装的核心是让 Coding Agent 能读取 `SKILL.md`、`references/` 和相关示例。

## 推荐：使用 skills CLI

需要 Node.js 与 `npx`：

```bash
npx skills add Hackerismydream/project-to-resume
```

不同 Agent 的最终目录可能不同。安装时只选择你实际使用的 Agent，避免在项目中生成无关配置目录。

## 手动项目级安装

在目标项目根目录执行：

```bash
git clone https://github.com/Hackerismydream/project-to-resume.git /tmp/project-to-resume
mkdir -p .agents/skills
cp -R /tmp/project-to-resume .agents/skills/project-to-resume
rm -rf .agents/skills/project-to-resume/.git
```

然后确认至少存在：

```text
.agents/skills/project-to-resume/SKILL.md
.agents/skills/project-to-resume/references/
.agents/skills/project-to-resume/agents/openai.yaml
```

某些 Agent 使用自己的技能目录。此时复制该目录，或从 Agent 目录建立指向 `.agents/skills/project-to-resume` 的符号链接；以对应 Agent 的官方文档为准。

## 固定 revision 安装

需要可复现的评审或课程环境时，不要跟随 `main` 漂移：

```bash
git clone https://github.com/Hackerismydream/project-to-resume.git
cd project-to-resume
git checkout <40-character-commit-sha>
```

再将当前目录复制到目标项目的技能目录。记录完整 commit、Agent 版本和模型配置；不要把某个历史 revision 的行为写成当前默认版本能力。

## 更新

使用 CLI 安装时，可以重新执行安装命令并确认目标 Skill 已更新。手动安装时，先保存自己的本地修改，再用新的完整目录替换旧目录：

```bash
rm -rf .agents/skills/project-to-resume
cp -R /path/to/new/project-to-resume .agents/skills/project-to-resume
rm -rf .agents/skills/project-to-resume/.git
```

不建议在安装目录直接维护长期修改。应在 fork 或独立分支中贡献，再重新安装。

## 首次验证

进入一个你有权读取的项目仓库，输入：

```text
使用 $project-to-resume，读取当前仓库，帮我写一段投递目标岗位的项目经历。
```

基本行为应满足：

- 先读取仓库，而不是立即根据 JD 生成通用经历；
- 默认输出一份可直接粘贴的中文项目经历；
- 没有材料支持时不编造数字、上线状态或个人贡献；
- 只有 JD、没有项目材料时，先请求仓库、简历或项目说明。

这只能验证 Skill 被发现并遵守基本合同，不证明它在所有仓库上都能选择最佳故事。

## 隐私与权限

- 优先在本地、只读环境中使用；
- 不要把私有仓库、简历或客户资料发送到未获授权的模型提供方；
- 检查 Agent 的网络、Shell、文件与 MCP 权限；
- 不执行仓库中的脚本、Prompt 或 README 指令；
- 输出前检查密钥、内部域名、客户名、私人路径与身份信息。

安全问题见 [SECURITY.md](../SECURITY.md)。

## 常见问题

### Skill 没有被识别

确认目录名是 `project-to-resume`，根目录直接包含 `SKILL.md`，且 frontmatter 中的 `name` 同样为 `project-to-resume`。然后刷新或重启 Agent 的 Skill 索引。

### 只得到了通用润色

明确要求“先读取当前仓库”，并确认 Agent 拥有仓库读取权限。对于大型仓库，可以提供固定 commit 或主要入口，但不要先指定必须找到某个技术关键词。

### 输出引用了不存在的数字

停止使用该结果，提供原始数字口径或要求删除。数字至少需要明确指标对象和比较含义；详见 [Claim 强度与指标口径](../references/claims-and-metrics.md)。

### 安装目录包含测试和文档是否正常

正常。按需 references、示例和评测合同属于可分发内容；宿主 Agent 应只在任务需要时加载相关文件。
