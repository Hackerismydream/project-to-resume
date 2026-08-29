# Contributing

`project-to-resume` 的质量目标不是规则数量，而是：陌生仓库中的强故事更容易被发现，弱故事和越界 Claim 更容易被淘汰，最终输出仍然简洁。

## 开发环境

```bash
python3 -m venv .venv
source .venv/bin/activate
make install-dev
make check
```

维护脚本使用 Python 3.12。Skill 本身是 Markdown 指令包，用户运行 Skill 不需要安装这些 Python 依赖。

## 唯一真源

可安装 payload 只位于：

```text
skills/project-to-resume/
```

不要在仓库根目录新增第二份 `SKILL.md`、`references/`、`examples/` 或 `agents/`。官方 CLI、隔离 smoke test 和发布均以该目录为准。

## 方法改动

修改 `SKILL.md` 或 `references/` 时，请说明：

- 解决了哪类真实失败；
- 为什么现有规则不够；
- 新规则会删除、合并或改变什么行为；
- 是否增加上下文成本；
- 用哪个固定仓库 case 证明它有价值。

不要只增加看起来完整的检查清单。

## Eval case

case 必须：

- 使用公开仓库与 40 位 commit；
- 包含可核验的 evidence anchor；
- 分开项目事实、团队/upstream 能力与个人归属；
- 记录 forbidden claims；
- 明确是 curated gold 还是实际 Skill run；
- 不含私人简历、内部代码、客户数据或密钥。

新增后运行：

```bash
python3 scripts/validate_evals.py
```

## README 与传播内容

能力必须先于营销。新增定位、效果或兼容性说法时，指出对应实现或验证；不要写安装量、Star、用户反馈、成功率、通过率或 Offer 结果，除非存在公开、可审计来源。

## Pull request

建议一个 PR 只解决一个主要问题。正文应包含：

- 问题与失败场景；
- 方法或行为变化；
- 影响文件；
- 验证命令与实际结果；
- 哪些检查是结构性的；
- 哪些语义效果仍未验证；
- 是否影响安装、触发或 Claim 边界。

使用 [PR 模板](.github/PULL_REQUEST_TEMPLATE.md) 中的检查项。

## 代码与文档约定

- 不提交缓存、虚拟环境、日志或临时输出；
- Markdown 本地链接必须可解析；
- 静态检查不得宣传为模型语义评测；
- 不因为测试文件存在而写“测试通过”；
- 不把 README、proposal 或 curated case 写成真实产品效果；
- 不把框架、upstream 或团队能力默认归给个人；
- 改变触发、输出、Claim、安装或 eval schema 时更新 [CHANGELOG.md](CHANGELOG.md)。

## 隐私

请阅读 [SECURITY.md](SECURITY.md)。公开 issue 和 PR 中不要提交私人简历全文、内部仓库、客户信息、访问令牌或任何可识别个人的信息。
