# TEMPLATE-UPGRADE: 文档体系分批审计与模板提案工作流

> 来源：zhiyan-digital-cs-platform（emily8421/zhiyan-digital-cs-platform）派生项目回流
> 类型：模板优化提案草稿
> 状态：Batch 0 审计后起草，待后续 Batch 实证补充
> 关联：`ai/commands/docs-system-audit.md`、`ai/commands/docs-evaluation.md`、`ai/prompts/review/16-docs-system-audit.md`、`ai/prompts/review/19-docs-evaluation.md`、`ai/document-lifecycle-rules.md`、`ai/session-rules.md`

## 1. 背景与问题

在派生项目完成一轮 `docs/00-09`、`docs/design/*` 和 Phase 验证后，团队常会发现一批问题既不是单个项目 bug，也不是可以一次性写进一个大提案的模板缺口：

- `00-09` 文档链条很长，需求、设计、计划、验证各阶段关注点不同。
- `docs/design/*` 详细设计文档数量不固定，结构差异大，难以用 00-09 的固定标准覆盖。
- 一次性输出“全量模板提案”容易混合项目事实问题、规范基线缺口、横切约束和执行流程问题。
- 长任务跨会话时，如果没有每个 Batch 的报告留痕，后续提案容易重复、遗漏或漂移。
- 既有 `docs-system-audit` 和 `docs-evaluation` 已能做审计 / 评估，但没有明确规定“分批审计报告 + 对应模板提案”的工作流。

因此建议在模板方法论中补充一个可选的“文档体系模板提案分批审计工作流”。

## 2. 设计目标

1. **报告先行**：每个 Batch 先落盘审计 / 评估报告，再起草对应模板提案。
2. **一批一范围**：每个 Batch 聚焦一段文档链或一个横切主题，避免一个大提案覆盖全部文档。
3. **事实与模板分离**：报告中区分项目正式文档回梳建议与可回流模板缺口。
4. **去重可审计**：每个 Batch 都检查 `_proposals/`、`_archive/proposals/` 和已提交 issue，避免重复提案。
5. **可续接**：长任务应把 Batch 计划、已完成报告、待确认项和下一步写入续接文件。

## 3. 建议工作流

### 3.1 触发场景

当用户提出以下意图时，可进入本工作流：

- “评估 00-09 文档和 design 文档，形成模板提案”。
- “做整个文档体系的模板提案审计”。
- “参考另一个派生项目，按 Batch 生成评估报告和提案”。
- “同步方法论后，系统评估项目文档体系暴露出的模板规范缺口”。

### 3.2 Batch 划分建议

| Batch | 范围 | 产物 |
|---|---|---|
| Batch 0 | 整体文档体系、提案 backlog、批次计划 | 总览审计报告 + 工作流提案 |
| Batch 1 | `docs/00-03` | 需求链评估报告 + 需求链规范提案 |
| Batch 2 | `docs/04-05` | 架构 / 技术方案评估报告 + 架构技术规范提案 |
| Batch 3 | `docs/06-07` | DB / API 评估报告 + 契约规范提案 |
| Batch 4 | `docs/08-09` | 开发计划 / 验证评估报告 + 进度和证据规范提案 |
| Batch 5 | `docs/design/*` | 详细设计评估报告 + design 通用规范提案 |
| Batch 6 | 跨文档横切主题 | 去重归并报告 + Mock / 降级 / 权限安全等横切提案 |

项目可根据文档剖面裁剪 Batch，但不得跳过“先报告、后提案”的顺序。

### 3.3 每个 Batch 的执行步骤

1. 读取 `ai/index.md` 及其列出的全部规则文件。
2. 读取 `docs-system-audit` / `docs-evaluation` 命令与 Prompt。
3. 读取本 Batch 范围内的项目文档和对应 `ai/doc-standards/*`。
4. 检查 `_proposals/`、`_archive/proposals/` 与已知回流 issue，识别重复和依赖。
5. 输出并在确认后落盘 Batch 审计 / 评估报告。
6. 基于该报告起草一个或多个 `TEMPLATE-UPGRADE-*.md` 提案。
7. 在报告和提案中记录待人工确认项、后续 Batch 和回流建议。

## 4. 报告模板建议

每个 Batch 报告建议写入：

```text
docs/research/YYYY-MM-DD-docs-evaluation-batch-<N>-<scope>.md
```

报告至少包含：

1. 定位声明：只读审计 / 评估，不替代正式文档修订。
2. 审计日期、范围和输入文档。
3. 规范依据：规则文件、Prompt、`ai/doc-standards/*`。
4. 逐文档观察：合规项、问题项、风险项、修复建议。
5. 模板缺口：明确哪些问题可通用于多个派生项目。
6. 项目事实问题：明确哪些只应另走项目文档回梳。
7. 既有提案去重：列出重复、依赖、可合并项。
8. 建议提案文件名与拆分 / 合并理由。
9. 结构化待人工确认项。
10. 下一 Batch 或回流动作。

## 5. 提案模板补充要求

每个 Batch 对应的模板提案除通用提案字段外，建议额外包含：

| 字段 | 要求 |
|---|---|
| 来源 Batch | 指向对应 `docs/research/*batch-*.md` 报告 |
| 覆盖范围 | 明确适用于哪些文档、阶段或 Prompt |
| 不覆盖范围 | 明确不直接修派生项目正式文档，不替代项目事实回梳 |
| 已有规范对照 | 说明与 `ai/doc-standards/*`、既有提案、已归档提案的关系 |
| 推荐落点 | 建议修改哪些模板文件、Prompt、命令或文档标准 |
| 验收方式 | 说明模板维护者如何验证提案已落地 |

## 6. 拟改范围

本提案建议模板仓库后续评估以下修改点：

### 规则 / 流程

- 在 `ai/document-lifecycle-rules.md` 或相关章节中补充“模板提案分批审计”作为可选工作流。
- 在 `ai/session-rules.md` 中强调跨 Batch 长任务需要记录报告路径、提案路径和下一 Batch。

### 命令路由

- 在 `ai/commands/README.md` 中补充自然语言入口，例如“分批评估文档体系并起草模板提案”。
- 可选择新增命令，或扩展 `docs-system-audit` / `docs-evaluation` 的适用场景，不强制新增命令。

### Prompt

- 在 `ai/prompts/review/16-docs-system-audit.md` 中增加 Batch 模式：Batch 0 总览、Batch 1~N 分段审计。
- 在 `ai/prompts/review/19-docs-evaluation.md` 中增加“评估报告可作为模板提案上游依据”的输出要求。
- 在 `ai/prompts/maintainers/17-submit-proposal.md` 中建议提案正文保留来源 Batch 报告链接或路径。

## 7. 版本影响

建议版本影响：MINOR。

理由：该提案新增一类模板治理工作流和 Prompt 使用模式，不改变既有项目文档语义，也不要求所有派生项目必须采用；但会扩展命令路由、审计输出和提案治理能力。

## 8. 影响面

| 影响对象 | 影响 |
|---|---|
| 派生项目 AI 流程 | 多文档体系评估时更容易拆批执行和续接 |
| 模板维护者 | 收到的提案会带来源 Batch 报告，便于判断动机和去重 |
| `ai/doc-standards/*` | 不直接修改具体标准，但后续 Batch 可能提出标准细化 |
| `docs-system-audit` / `docs-evaluation` | 增加分批报告与提案联动说明 |

## 9. 验收口径

模板维护者可用以下方式验收：

1. `ai/commands/README.md` 能把“分批文档体系评估 + 模板提案”路由到合适 Prompt。
2. `16-docs-system-audit` 或 `19-docs-evaluation` 明确支持 Batch 模式。
3. Prompt 要求每个 Batch 先输出报告，再起草提案。
4. Prompt 要求区分项目事实问题与可回流模板缺口。
5. Prompt 要求检查 `_proposals/`、`_archive/proposals/` 和已知 issue，避免重复。
6. 续接规则能覆盖长任务中断后的 Batch 状态恢复。

## 10. 风险与缓解

| 风险 | 缓解 |
|---|---|
| 文件数量增加 | 仅在用户明确要求模板提案审计或文档体系评估时采用；普通小修不触发 |
| Batch 之间重复提案 | 每个 Batch 报告必须包含既有提案去重检查 |
| 把项目事实问题误写成模板问题 | 报告强制拆分“项目回梳建议”和“模板缺口” |
| 一次执行时间过长 | 允许按 Batch 停下，并用续接文件记录下一步 |

## 11. 待人工确认项

| ID | 待确认项 | AI 建议 | 建议依据 | 备选方案 | 取舍影响 / 阻塞关系 |
|---|---|---|---|---|---|
| C-B0-P-001 | 是否将 Batch 模式做成独立命令 | 建议先扩展现有 `docs-system-audit` / `docs-evaluation`，暂不新增命令 | 现有命令已覆盖审计和评估，新增命令会增加维护面 | 新增 `template-proposal-audit` 命令 | 独立命令更清晰，但需要同步 README、命令索引和 Prompt |
| C-B0-P-002 | 是否固定 Batch 0~6 的划分 | 建议作为推荐默认，不作为强制 | 不同项目文档剖面不同，需要裁剪空间 | 强制固定划分 | 便于统一，但对 Lean 项目过重 |
| C-B0-P-003 | 是否要求提案必须引用来源 Batch 报告 | 建议要求 | 便于模板维护者审查动机、去重和影响范围 | 可选引用 | 可减少约束，但跨仓 issue 中上下文更容易丢失 |
