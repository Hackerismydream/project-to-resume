# Forward-eval rubric

本 rubric 用于比较安装后的 Skill 输出与 curated gold。它不是录用概率、简历通过率或产品成功率评分。

## Fatal errors

出现任一项，case 直接标记为事实失败：

- 虚构技术、职责、数字、上线、生产或业务效果；
- 把测试源码写成测试已运行；
- 把历史 benchmark 迁移到不匹配的 revision；
- 把 upstream、模板或团队能力写成个人实现；
- 与固定 commit 的可观察实现明显冲突。

## Review dimensions

### Repository understanding

- 是否识别主要执行面、核心对象、状态、输入输出与副作用；
- 是否在有限范围内说明观察边界；
- 是否避开 generated、vendor 和外围目录噪声。

### Story discovery

- 是否命中 curated top story；
- 是否发现 README 没直接写出的失败、不变量或恢复故事；
- 是否把测试用于发现，而不只用于尾部背书；
- 是否识别反证、版本和 upstream 风险。

### Selection

- 入选故事是否位于核心链路；
- 是否体现项目自己的工程判断；
- 故事之间是否语义独立；
- 是否在下一条不再增加岗位信号时停止。

### Claim and ownership

- 动词是否不强于来源；
- 数字是否保留指标、baseline、样本/负载和 revision；
- 项目能力与个人贡献是否分开；
- 必要追问是否少而具体。

### Resume quality

- 非项目成员是否能理解场景与系统边界；
- 技术机制是否与失败存在因果关系；
- 是否可直接粘贴；
- 是否能够展开成面试中的链路、取舍和验证。

## Comparison protocol

1. 固定模型、工具权限、仓库 commit、目标岗位和上下文预算；
2. 对 current 与 candidate 版本分别运行多次以观察稳定性；
3. 隐去版本来源，由两名评审做 pairwise 判断；
4. 保存读取文件、工具调用、最终输出和评审理由；
5. 分开报告 fatal error、故事发现、选择质量、表达质量和用户最终采用情况。

本仓库当前只提供合同与 curated gold；没有声明已完成大规模或付费模型评测。
