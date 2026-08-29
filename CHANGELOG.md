# Changelog

本项目记录会改变用户行为、事实边界、安装或评测方式的变化。

## [Unreleased]

暂无。

## [0.2.0] - 2026-08-29

### Added

- Repository-first 的岗位无关广度扫描与规模适配。
- 从入口到终态的行为链路追踪。
- 测试参与故事发现，而不只作为尾部证据。
- 条件式 history、PR、issue 与 upstream 差异读取。
- Story Hypothesis、反证、候选竞争、语义去重和淘汰原因。
- 固定 revision 的 YAML eval contracts、JSON Schema 与人工 rubric。
- Apache-2.0 License、贡献指南、安全策略、Issue/PR 模板和 Dependabot。
- 官方 Agent Skills 规范校验、官方 `skills` CLI 本地安装和合并后公开安装检查。

### Changed

- 唯一可安装真源移动到 `skills/project-to-resume/`，根目录不再保留重复 payload。
- 目标岗位和 JD 延后到初始候选池形成后介入。
- 每个项目允许 1–5 条 bullet，以新增岗位信号作为停止条件。
- Skill frontmatter 增加 license、compatibility 和版本 metadata。
- Pico 示例明确用户负责范围，并减少简历成稿中的内部审计术语。

### Fixed

- 防止被截断或缺少 frontmatter 的 `SKILL.md` 通过校验。
- 防止浅克隆环境中的 whitespace check 退化为空检查。
- 防止公开仓库能力在归属未知时被直接写成个人强主张。
- 防止隔离文件复制被描述成官方安装验证。

## Earlier development

早期版本建立了 copy-ready 默认输出、Claim/指标分层、后端与 Agent/RAG Playbook、面试反向校验和示例 linter。历史细节保留在 Git 记录中。
