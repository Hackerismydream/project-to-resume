# Roadmap

路线图描述问题顺序，不承诺发布日期、用户规模或商业化方向。只有进入 `main` 且通过对应验证的能力才算当前能力。

## 当前基线

- Repository-first 的陌生仓库探索；
- 岗位无关 Repository Map 与 2–4 条行为链路；
- 测试参与故事发现与 Claim 上限判断；
- 条件式 history、PR、issue 和 upstream 读取；
- Story Hypothesis、反证、候选竞争和语义去重；
- 后置岗位/JD 排序；
- 1–5 条按新增信号停止的中文项目经历；
- 后端、AI/Agent/RAG、科研/实习/开源 Playbook；
- 固定 revision 的 curated eval contracts；
- YAML、JSON、JSON Schema、示例和安装的确定性校验。

## 下一阶段：真实 forward evaluation

目标是测量 Skill 是否真的比普通改写更稳定地发现核心故事，而不是增加更多模板。

计划补充：

- Java 后端、Python Agent、RAG、CLI、数据流水线和 fork 项目的固定仓库集；
- 不同宿主模型在相同 commit 上的实际运行记录；
- Repository Map 覆盖、核心故事召回、禁止 Claim 违规、个人归属违规、语义重复和必要追问数量；
- 与“只读 README”“只按 JD 搜关键词”“直接润色原 bullet”的对照；
- 失败样例和 evaluator 分歧，而不只发布成功案例。

在这些运行真正完成前，`evals/cases/` 仍只称为 curated contracts，不称为 benchmark 结果。

## 后续：真实用户案例

- 使用公开仓库和固定 commit 收集匿名 Before / After；
- 记录用户实际采用、修改或拒绝了哪些 bullet；
- 分开记录“事实正确”“表达有用”“面试能讲”三类反馈；
- 只在获得明确授权后展示 GitHub 用户名或项目背景；
- 不收集私人简历全文、联系方式、Offer 或公司内部材料。

## 可能探索

- 更稳定的语义去重 evaluator；
- 大仓库的预算化 Repository Map 与增量读取；
- upstream delta 和 monorepo 多项目边界的专门案例；
- 中英文项目经历输出，但继续以中文技术求职为主场景；
- 与更多 Agent Skills 宿主的安装兼容性矩阵。

## 明确不做

- 招聘、投递、账号、用户画像或简历数据库平台；
- 自动编造业务规模、性能、上线、用户评价或求职结果；
- 为命中 JD 而向项目添加不存在的技术；
- 默认执行被分析仓库的代码或上传私有材料；
- 用静态测试结果冒充模型语义质量或招聘效果；
- 在没有稳定真实需求前建设服务端、遥测或托管 SaaS。
