# Repository Discovery

本文件负责 repository-first 流程的前半程：建立搜索空间、追踪系统行为、发现候选故事。它不负责最终简历措辞。

## 目标与反目标

要回答：

```text
项目接收什么
→ 维护什么状态
→ 在哪里做关键判断
→ 产生什么副作用
→ 怎样完成、失败或恢复
```

不要：

- 逐目录复述仓库；
- 把 README、框架名或模块列表直接当故事；
- 因 JD 关键词提前收窄搜索；
- 默认扫描完整 history、PR、issue 或 upstream；
- 执行不可信代码来证明能力。

## 1. 固定观察对象

开始前记录：

```text
repository path / URL
working tree / HEAD / fixed commit
branch and dirty state
remote default branch
fork / upstream
available history and remote access
```

必须区分当前工作树、HEAD、发布版本、旧实验和安装产物。公开仓库身份不能证明用户个人归属。

## 2. Repository Map

| 维度 | 要回答的问题 | 常见锚点 |
| --- | --- | --- |
| 身份 | revision、fork、upstream 是什么 | Git 元数据、仓库页面 |
| 结构 | 主要语言、package、service 边界是什么 | tree、manifest、build file |
| 入口 | 什么触发系统行为 | API、CLI、worker、cron、consumer、hook、UI |
| 核心对象 | 哪些实体或任务承载状态 | model、schema、migration、enum |
| 状态 | 谁能写、怎样迁移和持久化 | repository、store、checkpoint、state machine |
| 输入 | 请求、事件、文件、模型输出是什么 | DTO、schema、parser、handler |
| 副作用 | 写库、消息、文件、网络、进程或索引 | client、publisher、writer、adapter |
| 终态 | 用户或下游看到什么 | response、event、status、artifact |
| 失败 | 重试、补偿、回滚、拒绝、取消如何发生 | error、retry、recovery、cleanup |
| 测试 | 断言哪些行为和不变量 | tests、fixture、fault injection |
| 测量与发布 | benchmark、release、migration 在哪里 | reports、tags、changelog、CI |
| Unknown | 什么缺口会改变故事或 Claim | 显式记录 |

Map 的完成标准是能识别主要执行面和核心状态关系，不是看完所有文件。

## 3. 规模与采样

### 小仓库

一条完整行为链路足以覆盖主任务时，不为满足数量寻找第二条。

### 普通仓库

追踪 2–4 条最可能承载工程判断的链路。

### Monorepo

先列 package / service / app，再判断：

- 哪些连接真实入口与核心状态；
- 哪些只是共享库、生成代码或脚手架；
- 哪些由项目主线或用户职责明确指向。

在核心性相当时，目标岗位可以作为深入顺序的次级 tie-breaker，但不能替代岗位无关的首轮 Map。

### 访问不完整

仓库过大、私有依赖缺失、子模块不可见或远端不可访问时：

- 记录实际读取范围；
- 使用“在已观察模块中”等有界判断；
- 不声称完成全仓库审计；
- 只有范围缺口会改变成稿时才追问。

## 4. 默认排除项

首轮通常跳过：

- `node_modules/`、`vendor/` 和第三方源码；
- `dist/`、`build/`、coverage、缓存和生成文件；
- lockfile、压缩包、二进制、快照和大型 fixture；
- 重复 generated client、ORM output 和 API docs；
- 与主链路无关的示例、模板和 benchmark 副本。

候选故事直接依赖依赖版本、生成契约、fixture 边界或构建产物时再读取。

## 5. 选择行为链路

强链路通常：

- 从真实入口进入核心对象；
- 包含状态迁移或资源所有权变化；
- 产生不可随意重放的副作用；
- 存在并发、权限、失败、恢复、兼容性或成本约束；
- 有测试、迁移、history 或运行材料交叉验证；
- 删除该设计后会出现可观察失败。

不要因文件大、目录深、组件高级或 README 篇幅长而优先。

## 6. 行为链路模板

```text
入口
→ 输入校验
→ 核心数据或状态
→ 关键决策
→ 外部副作用
→ 终态或可见输出
→ 异常与恢复
→ 测试或验证
```

### 入口与输入

确定触发者、输入形式、身份和前置状态。关注 schema、权限、路径、版本、幂等键和参数组合。

### 状态与决策

确定核心对象、状态拥有者和分支条件：

- 什么状态允许继续；
- 谁能改变状态；
- 重复、迟到或并发输入如何处理；
- 决策是否可观察、可恢复。

### 副作用与终态

标出数据库写入、消息发送、文件修改、模型调用、索引更新、外部 API 和进程执行。确定完成、失败、取消、部分成功与清理如何呈现。

### 异常与恢复

主动检查超时、重复、部分失败、中断、过期状态、版本漂移、无结果、权限拒绝和补偿。只读正常路径通常不足以形成强故事。

## 7. 测试参与发现

优先观察：

- 测试名称反复出现的 failure、recovery、duplicate、stale、permission、timeout；
- fixture 构造的异常状态；
- 断言关注终态、唯一性、持久化、清理还是证据；
- fault injection 发生在主链路哪个阶段；
- 回归用例是否指向历史缺陷；
- 测试是否覆盖框架默认行为之外的项目设计。

测试可以发现不变量、恢复路径、权限边界、兼容性约束和历史故障线索。

```text
测试文件存在 ≠ 测试运行通过
测试运行通过 ≠ 生产可靠
```

## 8. 条件式历史与 upstream

| 触发器 | 需要回答的问题 |
| --- | --- |
| 当前结构无法解释动机 | 旧方案是什么，为什么替换 |
| fork / 二次开发 | upstream 已有什么，当前增量是什么 |
| README 与源码不一致 | 哪个 revision 或发布状态可信 |
| 回归测试突出某故障 | 是否存在对应修复或迁移 |
| 用户声称重构或性能变化 | baseline、commit 和验证是否一致 |
| 候选依赖 A → B | A、B 和结果是否属于同一口径 |

优先使用本地 history；远端 PR/issue 只有必要且可访问时才读取。commit message 是线索，不自动证明效果。

## 9. Source conflict

- README 说支持、主路径未调用：按未确认处理；
- 测试针对旧接口、当前代码已变化：分别绑定 revision；
- benchmark 来自旧 commit：不得迁移数字；
- 多个入口行为不同：不要用一个故事泛化全部入口；
- upstream 已有同一机制：只写当前项目的 delta；
- 用户陈述强于源码：缩小实现措辞，必要时追问职责或版本。

## 10. 主路径与外围

候选内容分为：

1. 核心行为：缺失后主任务无法完成或状态无法收敛；
2. 质量与治理：控制核心行为的失败、权限、恢复、验证和可解释性；
3. 外围便利：展示、脚手架、普通 CRUD、包装命令和配置。

外围能力只有体现独立工程判断、证据充分且增加岗位信号时才占 bullet。

## 11. 停止条件

停止扩张阅读，当：

- 主要执行面、核心状态、输入输出和测试分布已经进入 Map；
- 足够数量的链路能从入口讲到终态和恢复；
- 强候选在加入反证后保持稳定；
- 每个入选候选都有锚点、归属来源和 Claim 上限；
- 新文件只重复现有机制或补充外围细节；
- 剩余 Unknown 不会改变定位、职责、数字或允许动词。

## 常见误判

- 按目录写故事；
- 把 README 意图写成实现；
- 看见组件立即生成 bullet；
- 把测试源码写成测试通过；
- 把配置参数写成效果；
- 默认全扫 history；
- JD 提前收窄探索；
- fork 冒领 upstream；
- 只读部分仓库却声称完整审计；
- 把内部 Map 和证据表作为默认用户产物。
