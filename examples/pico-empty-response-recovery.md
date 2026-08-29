# Curated Gold Case：Pico 空响应恢复

> 本案例由维护者基于固定公开仓库和固定 commit 人工整理，是 forward eval 的 curated gold，不是安装后 Skill 的真实模型运行结果，也不代表真实用户效果。

## 用户最初可能写出的普通版本

```text
使用 Python 开发 Agent，支持模型调用、工具调用、上下文管理和异常重试。
```

这段话列出了能力名词，但没有说明 Agent 在什么失败下会中断、系统如何恢复、恢复行为怎样受约束，以及哪些状态不会污染后续会话。

## 固定材料

- 仓库：https://github.com/Hackerismydream/pico
- Commit：`aedcaf2cf928af145ef349fb0312b8e66d12ae74`
- 目标岗位：Agent Runtime / Agent 应用工程
- 个人归属：本案例只演示项目事实到简历故事的转换，不据公开仓库推断某位候选人的个人贡献。

## Repository Map 摘要

- 主要语言与形态：Python Agent Harness；README 描述 CLI、TUI、Gateway、Cron 和消息渠道共享 Turn Runtime。
- 相关执行面：Agent Loop 接收模型响应并决定继续、调用工具或结束 Turn。
- 核心状态：本轮恢复计数、前一轮是否存在工具调用、结构化 reasoning、可见正文和会话消息。
- 外部可见结果：正常正文，或预算耗尽后的 bounded fallback。
- 相关测试：空响应分类、恢复预算、工具后空响应、thinking-only、fallback 与 synthetic message 持久化边界。
- 未知项：本案例没有真实模型 forward run、生产流量或候选人个人贡献材料。

## 实际追踪的行为链路

### 链路 A：模型只返回思考或空正文

```text
Agent Loop 收到无可见正文的 LLMResponse
→ 检查 reasoning_content / thinking_blocks / inline think marker
→ classify_empty_response 选择 PREFILL 或 RETRY
→ 按本轮预算继续请求
→ 得到可见正文，或预算耗尽后交付 fallback
```

### 链路 B：工具调用后模型返回空正文

```text
前一轮已经执行工具
→ 下一次模型响应没有可见正文且不含 thinking
→ 分类为 NUDGE
→ 注入短提示要求消费工具结果或给出最终答案
→ 继续 Agent Loop
→ synthetic recovery message 在持久化前被移除
```

## 候选故事竞争

| 候选 | 结论 | 原因 |
| --- | --- | --- |
| 按空响应类型选择 bounded recovery | 入选 | 位于主任务收敛链路，包含失败分类、优先级和预算约束 |
| 将判断抽成纯函数并清理 synthetic state | 入选 | 增加可测试性与会话状态卫生的独立信号 |
| 多入口共享 Runtime | 淘汰为单独 bullet | README 支持项目定位，但本案例没有继续追踪实现链路，不占用有限版面 |
| “显著提升成功率” | 禁止 | 没有同 revision 的测量数据 |
| “所有恢复测试均通过” | 禁止 | 测试源码存在不等于本案例实际运行过测试 |

## 证据锚点

- [README：项目定位与多入口 Runtime](https://github.com/Hackerismydream/pico/blob/aedcaf2cf928af145ef349fb0312b8e66d12ae74/README.md)
- [恢复分类纯函数与预算](https://github.com/Hackerismydream/pico/blob/aedcaf2cf928af145ef349fb0312b8e66d12ae74/pico/agent/loop/recovery.py)
- [空响应恢复回归场景](https://github.com/Hackerismydream/pico/blob/aedcaf2cf928af145ef349fb0312b8e66d12ae74/tests/test_agent_loop_empty_recovery.py)

## 可直接粘贴的简历版本

**Pico 多入口 Agent Runtime｜Agent Runtime 开发**

**技术栈：** Python、大语言模型、Tool Calling、状态管理、Pytest

**项目描述：** 面向 CLI、TUI、Gateway、Cron 与消息渠道共享运行时的 Agent Harness，聚焦工具调用后的任务收敛、模型空响应恢复与会话状态边界。

1. 将无可见正文的模型响应按 thinking-only、工具后空响应和普通空响应分类，分别采用推理回填、短提示和原样重试，并以每轮独立预算限制恢复次数，避免任务直接交付空答案或陷入无限循环。
2. 将恢复决策抽成无 I/O 纯函数，由 Agent Loop 统一执行消息注入、计数和持久化清理；围绕优先级、预算耗尽、fallback 及 synthetic message 不落盘编写回归测试场景。

## 禁止使用的越界表述

- “空响应恢复使任务成功率提升 30%”：没有固定样本、baseline 和运行结果。
- “已在生产环境稳定运行”：没有发布与线上使用证据。
- “独立主导 Pico 全部 Runtime 设计”：公开仓库不能自动证明个人归属。
- “所有恢复测试通过”：本案例没有实际执行测试。

## 常见面试追问

1. 为什么 thinking-only 应优先于工具后 nudge，预算耗尽后为什么还允许 plain retry？
2. synthetic message 为什么不能持久化，若落盘会怎样影响下一轮上下文？
3. 怎样设计 forward eval，判断恢复真正提高了任务完成率而不是增加无效调用？
