# Batch 5 文档评估报告：`docs/design/*` 详细设计

> 定位：本报告是 `docs/design/*` 详细设计文档的只读审计与模板提案依据，不替代任何正式详细设计文档修订。
> 评估日期：2026-07-06
> 范围：`docs/design/backend-service.md`、`docs/design/frontend-interaction.md`、`docs/design/h5-dialog.md`、`docs/design/knowledge-and-policy.md`、`docs/design/mock-integrations.md`、`docs/design/scenario-packs.md`、`docs/design/web-console.md`。
> 来源 Batch：Batch 0 `docs/research/2026-07-06-template-proposal-audit-batch-0-overall.md`。

## 1. 评估摘要

本次 Batch 5 评估目标，是判断 `docs/design/*` 是否能作为 04-07 与 08-09 之间的详细设计承接层，并识别可回流到模板的通用详细设计规范缺口。

结论：**Conditional Go**。

当前 `docs/design/*` 能支撑 Phase1 Demo：每份文档都有明确主题，能追溯到 REQ / API / TC 中的一部分，且多数关键流程已补 Mermaid 图。但除 `frontend-interaction.md` 外，其余详细设计文档整体偏“轻量设计说明”，缺少统一的 `0. 文档元信息`、阶段 / 状态标签、输入 / 输出职责、结构化待确认项、实现偏差记录、统一追溯矩阵和 readiness gate。模板层面建议建立 `docs/design/*` 通用详细设计标准，并允许按子系统类型裁剪。

最关键判断：

- `frontend-interaction.md` 已形成较完整的前端交互标准样例，可作为通用 design 模板的参考之一，但不能把前端页面结构强加给所有子系统。
- `backend-service.md`、`h5-dialog.md`、`web-console.md`、`knowledge-and-policy.md`、`mock-integrations.md`、`scenario-packs.md` 均有目标、范围、流程或结构、验收，但缺少统一元信息和状态 / 追溯 / 待确认基线。
- Mock / 降级、不编造、高风险转人工、真实集成升级条件等横切事实在 design 文档中表达清楚，但缺少统一的状态枚举与跨文档检查表。
- 模板提案应重点补“详细设计通用骨架 + 子系统类型裁剪 + 实现偏差 / readiness gate / 追溯矩阵”，而不是新增一个只适用于前端交互的模板。

## 2. 评估范围与依据

### 2.1 读取文档

| 类型 | 文档 |
|---|---|
| 详细设计 | `docs/design/backend-service.md`、`docs/design/frontend-interaction.md`、`docs/design/h5-dialog.md`、`docs/design/knowledge-and-policy.md`、`docs/design/mock-integrations.md`、`docs/design/scenario-packs.md`、`docs/design/web-console.md` |
| 上游参照 | `docs/02-srs.md`、`docs/03-prd.md`、`docs/04-architecture.md`、`docs/05-tech-spec.md`、`docs/06-db-design.md`、`docs/07-api-spec.md` |
| 下游参照 | `docs/08-dev-plan.md`、`docs/09-verification.md` |
| 既有提案 | `_archive/proposals/TEMPLATE-UPGRADE-frontend-interaction-design.md` |
| 规则依据 | `ai/document-lifecycle-rules.md`、`ai/global-rules.md`、`ai/project-rules.md` |

### 2.2 评估口径

| 维度 | 口径 |
|---|---|
| 定位清晰度 | 是否声明详细设计定位、上游约束和不替代哪些文档 |
| 追溯性 | 是否能追溯 REQ、API、DB、TC 或 Sprint |
| 阶段边界 | 是否区分 Phase1 Demo、Phase2 MVP、后续愿景 |
| 可实现性 | 是否定义职责、流程、状态、失败 / 降级处理和验收 |
| 横切一致性 | Mock、不编造、隐私、安全、真实集成禁区是否一致 |
| 可维护性 | 是否记录待确认项、实现偏差、状态变更和后续补齐点 |
| 模板回流价值 | 是否暴露出可通用于多个派生项目的 design 文档标准缺口 |

## 3. 逐文档评估

| 文档 | 合规项 | 主要缺口 | 建议 |
|---|---|---|---|
| `backend-service.md` | 有详细设计定位、后端分层 Mermaid 图、服务职责、消息处理流程、错误处理、数据降级策略 | 缺 `0. 文档元信息`、结构化 REQ/API/TC 矩阵、实现偏差记录、结构化待确认项；错误处理未映射到 API 错误码 / TC | 作为服务型子系统模板样例，补服务职责、状态、错误 / 降级、追溯矩阵 |
| `frontend-interaction.md` | 结构最完整，含元信息、覆盖需求、页面清单、用户路径、状态模型、表单校验、文案、接口依赖、响应式、验收路径和延后确认 | 缺实现偏差记录；延后确认项不是结构化待确认表；无 Mermaid 图但不阻塞 | 作为交互型详细设计参考样例，后续补结构化待确认和实现偏差区 |
| `h5-dialog.md` | 有定位、页面结构、状态模型、Mermaid 交互流程、样例问题、接口依赖、安全边界和验收 | 缺元信息、阶段状态、追溯矩阵、失败 / 空态细节、结构化待确认项 | 作为入口页面型子系统模板样例，补页面 / 状态 / 接口 / TC 矩阵 |
| `web-console.md` | 有定位、页面结构、筛选、Mermaid 关键交互、UI 文案约束和验收 | 缺元信息、权限矩阵、状态变更错误处理、实现偏差、结构化待确认项 | 作为管理台型子系统模板样例，补角色 / 动作 / 状态 / 权限检查 |
| `knowledge-and-policy.md` | 有知识类型、匹配策略、不编造策略、知识缺口状态机、高风险规则和验收 | 缺元信息、规则优先级冲突、readiness gate、LLM / 向量候选能力进入条件、结构化追溯 | 作为策略 / 高风险能力模板样例，补安全门槛与不得提前实现声明 |
| `mock-integrations.md` | 有 Mock 适配 Mermaid 图、Mock 数据示例、通知 payload、真实集成升级条件和验收 | 缺元信息、Mock / 真实状态枚举、错误重试细节、凭据边界矩阵、实现偏差 | 与 Batch 6 横切规范联动，补 Mock / 降级 / 真实集成 readiness gate |
| `scenario-packs.md` | 有定位、场景包结构、产品型 / 项目型样例、校验规则和验收 | 缺元信息、字段契约、版本 / 发布状态、校验失败处理、追溯矩阵和待确认项 | 作为配置型子系统模板样例，补字段 / 校验 / 状态 / TC 映射 |

## 4. 通用缺口归纳

| 缺口 | 出现范围 | 影响 | 模板建议 |
|---|---|---|---|
| 缺统一文档元信息 | 除 `frontend-interaction.md` 外多数文档 | 难判断上游、状态、适用阶段和最后更新 | design 通用模板必须包含 `0. 文档元信息` |
| 缺统一追溯矩阵 | 多数文档只散落写 REQ / API / TC | 后续实现任务难以确认完整覆盖 | 增加 REQ / API / DB / TC / Sprint 追溯矩阵 |
| 缺结构化待确认项 | 多数文档只有延后或无待确认区 | 高风险决策不易续接和回填 | 使用统一待确认项表 |
| 缺实现偏差记录 | 全部 design 文档 | Sprint 实现后无法记录“设计 vs 代码”差异 | 增加实现偏差 / 设计回写区 |
| 缺 readiness gate | 高风险、Mock、真实集成、AI / 向量能力相关文档 | 容易提前实现候选能力 | 增加候选能力进入条件、验证证据和禁止事项 |
| 缺子系统类型裁剪 | 当前文档结构各自为政 | 不同 design 文档难以保持最低一致性 | 提供服务型、页面型、策略型、配置型、集成型裁剪指南 |
| 缺状态枚举 | Mock / 降级 / 真实集成多文档分散 | 容易混淆 Mock、候选、默认关闭、已启用 | 与 Batch 6 横切规范合并统一 |

## 5. 问题项

| ID | 优先级 | 类型 | 问题 | 位置 | 影响 | 建议修复方式 |
|---|---|---|---|---|---|---|
| B5-001 | P1 | 规范基线缺口 | `docs/design/*` 缺通用详细设计元信息、状态和追溯结构 | 多数 design 文档 | 后续实现、评审和回写缺统一入口 | 起草 design 通用规范提案 |
| B5-002 | P1 | 可维护性缺口 | 缺实现偏差 / 设计回写区 | 全部 design 文档 | Sprint 完成后设计和代码差异无法沉淀 | 模板新增实现偏差记录 |
| B5-003 | P1 | 风险门禁缺口 | 高风险策略、Mock 集成、真实集成、LLM / 向量候选缺 readiness gate 统一格式 | `knowledge-and-policy.md`、`mock-integrations.md` | 后续阶段可能提前实现候选能力 | design 模板补 readiness gate；Batch 6 横切归并 |
| B5-004 | P1 | 待确认项缺口 | 延后确认项未采用统一结构 | `frontend-interaction.md` 等 | 人工确认、AI 建议和阻塞关系不易追踪 | 使用统一待确认表 |
| B5-005 | P2 | 权限 / 安全细化缺口 | 管理台、Mock 集成和高风险策略缺统一权限 / 安全检查表 | `web-console.md`、`mock-integrations.md`、`knowledge-and-policy.md` | Phase2 试点前权限边界不足 | Batch 6 判断是否形成横切安全提案 |

## 6. 风险项

| ID | 风险 | 是否阻塞 | 说明 |
|---|---|---|---|
| R-B5-001 | 若 Phase2 直接基于轻量 design 文档实现权限、真实飞书或数据库，可能缺少 readiness gate | 条件阻塞 | Phase2 Sprint 前需补对应详细设计或技术验证 |
| R-B5-002 | 若实现后不记录偏差，后续文档回写只能靠 Git / 代码反查 | 不阻塞当前 | 模板应要求 design 文档可记录实现偏差 |
| R-B5-003 | 若把 `frontend-interaction.md` 结构直接套到所有 design 文档，会造成非 UI 子系统文档臃肿 | 不阻塞 | 应采用通用骨架 + 子类型裁剪 |
| R-B5-004 | Mock / 降级 / 真实集成状态若不统一，Phase2 容易误接真实服务 | 条件阻塞 | Batch 6 需要统一横切状态口径 |

## 7. 修复建议

### 7.1 项目正式文档修订建议

本报告不直接修改正式文档。建议后续在人工确认 Phase2 后另开修订任务：

1. 对 `docs/design/*` 追加统一 `0. 文档元信息`，保留原有正文，不机械重写。
2. 为每份 design 文档增加最小追溯矩阵：REQ、API / DB、TC、Sprint。
3. 为 `knowledge-and-policy.md` 和 `mock-integrations.md` 增加 readiness gate，明确 LLM / 向量 / 真实集成不得默认启用。
4. 为 `web-console.md` 增加角色 × 动作 / 权限可见性与后端权限边界说明。
5. 增加实现偏差 / 设计回写区，用于 Sprint 完成后记录代码事实差异。

### 7.2 模板提案建议

本 Batch 配套提案：`_proposals/TEMPLATE-UPGRADE-design-doc-standard.md`。

提案重点：

- `docs/design/*` 通用详细设计骨架。
- 子系统类型裁剪：服务型、页面 / 交互型、策略 / 规则型、配置型、集成适配型。
- 追溯矩阵、待确认项、实现偏差记录、readiness gate。
- 与既有前端交互设计提案的关系：复用其页面 / 状态 / 验收思想，但不重复前端专属标准。

## 8. 可回流模板优化建议

| 建议 | 是否已有规范覆盖 | Batch 5 提案处理 |
|---|---|---|
| 前端交互设计触发规则 | 已由归档提案与现行规则覆盖 | 不重复，只作为 design 子类型参考 |
| `docs/design/*` 通用元信息和追溯结构 | 未形成独立通用标准 | 作为本提案重点 |
| 实现偏差 / 设计回写区 | 现有规则提到代码事实反向同步，但 design 模板缺区块 | 作为本提案重点 |
| readiness gate | 分散在技术评估和 Phase 规则中 | 纳入 design 模板，并与 Batch 6 横切规范衔接 |
| 权限 / 安全 / Mock 横切检查 | 分散覆盖 | Batch 5 先提出，Batch 6 决定归并或独立提案 |

## 9. 待人工确认项

| ID | 待确认项 | AI 建议 | 建议依据 | 备选方案 | 取舍影响 / 阻塞关系 |
|---|---|---|---|---|---|
| C-B5-001 | 是否为现有 `docs/design/*` 追加统一元信息和追溯矩阵 | 建议等 Phase2 确认后按需回梳 | Phase1 已完成，Phase2 前补齐最有价值 | 立即全部补齐 | 可快速统一结构，但会打断模板提案审计主线 |
| C-B5-002 | design 通用规范是否独立成模板提案 | 建议独立 | 当前缺口跨多个非前端子系统，前端交互提案不足以覆盖 | 并入 Batch 6 横切提案 | 会让横切提案过大，降低可落地性 |
| C-B5-003 | Mock / 权限 / 安全是否在 Batch 5 提案内完整解决 | 建议只定义 design 接口，Batch 6 再归并 | 横切主题涉及 04/05/06/07/08/09/design 多处 | 在 Batch 5 一次写完 | 容易与前面提案重复，范围过大 |

## 10. 下一步

- 已完成：Batch 5 `docs/design/*` 详细设计只读评估。
- 本次配套提案：`_proposals/TEMPLATE-UPGRADE-design-doc-standard.md`。
- 下一 Batch：执行 Batch 6，汇总前述 Batch 中 Mock / 降级 / 权限安全 / 高风险能力等横切规范，判断是否独立提案或合并到 Batch 2 / 5。
