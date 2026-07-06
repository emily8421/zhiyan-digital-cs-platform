# Batch 1 文档评估报告：00-03 需求链

> 定位：本报告是 `docs/00-03` 需求链的只读审计与模板提案依据，不替代 `docs/00-scenario.md`、`docs/01-user-requirements.md`、`docs/02-srs.md`、`docs/03-prd.md` 的正式修订。
> 评估日期：2026-07-06
> 范围：`docs/00-scenario.md`、`docs/01-user-requirements.md`、`docs/02-srs.md`、`docs/03-prd.md`，对照 `ai/doc-standards/00-scenario.md` 至 `ai/doc-standards/03-prd.md`。
> 来源 Batch：Batch 0 `docs/research/2026-07-06-template-proposal-audit-batch-0-overall.md`。

## 1. 评估摘要

本次 Batch 1 评估目标，是判断当前 `00-03` 需求链是否足以支撑后续 Phase2 文档规划，并识别可回流到模板的需求链规范缺口。

结论：**Conditional Go**。

`00-03` 已具备可用的需求链主干：场景、角色、U-ID、REQ-ID、Phase 路线图和验收标准基本齐全，可作为后续 Phase2 规划的输入。但在进入 Phase2 正式修订前，应优先处理 `docs/03-prd.md` 中 Phase1 状态滞后的项目事实问题；同时，模板层面建议强化“需求链健康度矩阵、状态传播检查、Phase 证据引用和旧派生兼容补齐方式”。

最关键判断：

- `00` 已将典型场景映射到 U-ID，`01` 已将 U-ID 映射到 REQ-ID，`02` 已将 REQ 映射到模块 / API / TC，`03` 已将 REQ 映射到功能与 Phase。
- Phase1 已在 `README.md` 与 `docs/09-verification.md` 记录完成，但 `docs/03-prd.md` 的 Phase1 状态仍是“骨架，待实现”，这是需求链权威源需要回写的项目问题。
- `00-03` 与最新 `ai/doc-standards/00-03` 语义基本兼容，但若按规范镜像评估，仍缺少更结构化的用户操作流、用户验收口径、约束矩阵、优先级取舍和结构化待确认项。
- 上述缺口多数已有标准覆盖，因此 Batch 1 的模板提案不应重复“新增章节”，而应聚焦如何审计、补齐、兼容和传播状态。

## 2. 评估范围与依据

### 2.1 读取文档

| 类型 | 文档 |
|---|---|
| 项目需求链 | `docs/00-scenario.md`、`docs/01-user-requirements.md`、`docs/02-srs.md`、`docs/03-prd.md` |
| 规范镜像 | `ai/doc-standards/00-scenario.md`、`ai/doc-standards/01-user-requirements.md`、`ai/doc-standards/02-srs.md`、`ai/doc-standards/03-prd.md` |
| 横向事实 | `README.md`、`docs/09-verification.md`、`docs/research/2026-07-06-phase-upgrade-evaluation.md` |
| 规则依据 | `ai/document-lifecycle-rules.md`、`ai/implementation-lifecycle-rules.md`、`ai/project-rules.md` |

### 2.2 评估口径

| 维度 | 口径 |
|---|---|
| 完整性 | 是否有场景、用户需求、系统需求、PRD 范围和 Phase 路线图 |
| 一致性 | Phase 状态、交付物形态、禁止事项是否与下游验证和 README 一致 |
| 追溯性 | 是否能从 SC / U-ID 追到 REQ / 功能 / Phase |
| 可验证性 | 需求和验收标准是否能关联到后续 TC / AC |
| 维护性 | 是否便于后续阶段原位增量演进，不删除 Phase1 历史 |
| 模板回流价值 | 问题是否通用于多个派生项目，而非本项目专属事实 |

## 3. 逐文档评估

### 3.1 `docs/00-scenario.md`

| 项 | 观察 |
|---|---|
| 合规项 | 已包含文档元信息、背景问题、角色、典型业务场景、当前 Phase 场景边界、约束假设和场景到需求追溯。 |
| 追溯情况 | 场景表已包含来源和下游 U-ID，能支撑 `01`。 |
| 规范差异 | 对照 `ai/doc-standards/00-scenario.md`，缺少独立的“上游来源映射”表、“下游影响”段和结构化待人工确认项。 |
| 影响 | 不阻塞当前需求链使用；后续上游输入变更时，影响分析入口不够集中。 |
| 建议 | 项目修订可用最小补充方式追加来源映射 / 下游影响，不必机械重写现有场景表。 |

### 3.2 `docs/01-user-requirements.md`

| 项 | 观察 |
|---|---|
| 合规项 | 已列出 U-001~U-012，包含角色、场景、阶段、来源，并提供 U-ID → REQ-ID 追溯。 |
| 追溯情况 | 每个 U-ID 均能映射到一个或多个 REQ-ID，未发现明显悬空 U-ID。 |
| 规范差异 | 对照 `ai/doc-standards/01-user-requirements.md`，缺少用户操作流、逐 U-ID 用户验收口径、优先级理由、排除需求表和结构化待确认项。 |
| 影响 | 不阻塞 Phase1 事实追溯；若进入 Phase2 试点，用户验收口径不足会影响 MVP 需求验收表达。 |
| 建议 | Batch 1 提案应建议模板提供“兼容补齐矩阵”，允许旧派生项目在不重写全文的前提下补用户流和验收口径。 |

### 3.3 `docs/02-srs.md`

| 项 | 观察 |
|---|---|
| 合规项 | 已包含系统范围、REQ-001~REQ-016、NFR、数据与接口需求、边界异常和 REQ → 模块 / 数据对象 / API / TC 矩阵。 |
| 追溯情况 | REQ 均能回到 U-ID，并向后映射到 API 和 TC。 |
| 规范差异 | 对照 `ai/doc-standards/02-srs.md`，约束与假设未独立成结构化矩阵；异常场景缺少严重度、触发条件、预期处理和验证映射；待确认项不是结构化表。 |
| 影响 | 对 Phase1 Demo 不构成阻塞；对 Phase2 引入真实飞书、权限或数据库验证时，会影响风险门槛表达。 |
| 建议 | 后续修订可补“CON-ID 约束矩阵”和“异常 / 边界 → 验证”矩阵；模板提案聚焦这些矩阵与 REQ 状态传播的审计方式。 |

### 3.4 `docs/03-prd.md`

| 项 | 观察 |
|---|---|
| 合规项 | 已包含产品目标、功能范围、Phase 路线图、Phase1 用户流程、验收标准、不做事项和 REQ → 功能追溯。 |
| 追溯情况 | REQ-001~REQ-016 均映射到 F-ID 和 Phase；Phase 表同时声明功能范围、交付物形态、状态、进入标准和退出标准。 |
| 项目问题 | Phase1 在 `README.md` 与 `docs/09-verification.md` 中已记录完成，但 `docs/03-prd.md` Phase1 状态仍为“骨架，待实现”。 |
| 规范差异 | 缺少独立“优先级与取舍”表；Phase 表没有“完成证据 / 验收引用”列；人工确认记录不是结构化待确认表。 |
| 影响 | 进入 Phase2 文档修订前需要回写 PRD Phase 状态，否则阶段权威源与验证事实冲突。 |
| 建议 | 项目层面另开文档回梳修订；模板层面补强“Phase 状态变化必须引用验收证据并传播到 08/09/README/project-rules”。 |

## 4. 追溯链核对

| 链路 | 核对结果 | 问题 |
|---|---|---|
| SC → U-ID | `00` 场景表和追溯表可覆盖 U-001~U-012 | 来源可信度与下游影响未独立结构化 |
| U-ID → REQ-ID | `01` 显式映射 U-001~U-012 到 REQ-001~REQ-016 | 缺用户验收口径和操作流 |
| REQ-ID → 功能 / Phase | `03` 显式映射 REQ-001~REQ-016 到 F-001~F-009 / 后续功能 | Phase1 状态未回写为已完成 |
| REQ-ID → API / TC | `02` 已预先映射 API 与 TC，为 07 / 09 提供下游锚点 | 对 Batch 1 不阻塞，后续 Batch 3 / 4 细查 |
| Phase → 验收标准 | `03` AC-001~AC-007 与 `09` 阶段验收清单可对齐 | `03` 未引用 `09` 的实际验收记录 |

## 5. 问题项

| ID | 优先级 | 类型 | 问题 | 位置 | 影响 | 建议修复方式 |
|---|---|---|---|---|---|---|
| B1-001 | P0 | 项目事实 / 状态传播 | `03` Phase1 状态仍为“骨架，待实现”，与 `README` / `09` / Phase 升级评估的完成事实不一致 | `docs/03-prd.md` §3 | 阻塞 Phase2 正式修订前的阶段权威源一致性 | 另走文档修订任务，回写 Phase1 状态和验收引用 |
| B1-002 | P1 | 规范基线缺口 | `00` 缺独立上游来源映射、可信度和下游影响段 | `docs/00-scenario.md` | 上游变更时影响分析不够集中 | 最小追加来源映射 / 下游影响表 |
| B1-003 | P1 | 规范基线缺口 | `01` 缺用户操作流、用户验收口径和优先级理由 | `docs/01-user-requirements.md` | Phase2 MVP 需求验收和取舍依据不足 | 追加用户流、验收口径和优先级矩阵 |
| B1-004 | P1 | 规范基线缺口 | `02` 约束、假设、异常场景未形成可验证矩阵 | `docs/02-srs.md` | 真实依赖 / 权限 / 外部服务进入 Phase2 时门槛不够清晰 | 补 CON-ID 与异常验证映射 |
| B1-005 | P1 | 模板流程缺口 | 模板已有章节标准，但缺少“需求链状态传播检查”的明确工作流 | `ai/doc-standards/00-03` / Prompt 层 | 派生项目容易出现 PRD 状态落后于验证事实 | 起草 Batch 1 模板提案 |

## 6. 风险项

| ID | 风险 | 是否阻塞 | 说明 |
|---|---|---|---|
| R-B1-001 | Phase2 修订前若不回写 `03`，会出现阶段权威源与验收事实冲突 | 阻塞 Phase2 正式修订 | `03` 是阶段标签唯一来源，应先同步完成状态 |
| R-B1-002 | 若机械按 `ai/doc-standards` 重写 00-03，可能破坏已确认语义和历史事实 | 不阻塞 | 建议采用兼容追加矩阵，而非全文重写 |
| R-B1-003 | 若模板提案重复已有 doc-standards 章节要求，会增加维护噪音 | 不阻塞 | 提案应聚焦状态传播、证据引用和评估工作流 |

## 7. 修复建议

### 7.1 项目正式文档修订建议

本报告不直接修改正式文档。建议后续单独启动文档回梳任务：

1. 回写 `docs/03-prd.md` Phase1 状态为已完成 / 已验收，并引用 `docs/09-verification.md` 的 Sprint-6 记录。
2. 若接受 Phase2 Conditional Go，再同步更新 `ai/project-rules.md`、`docs/03-prd.md`、`docs/08-dev-plan.md`、`docs/09-verification.md`。
3. 以追加矩阵方式补 `00/01/02` 的来源映射、用户验收口径和约束异常矩阵，不机械重写已确认内容。

### 7.2 模板提案建议

本 Batch 配套提案：`_proposals/TEMPLATE-UPGRADE-00-03-requirements-chain-standard.md`。

提案重点不重复已有 `ai/doc-standards/00-03` 章节，而是建议：

- 增加 00-03 需求链健康度矩阵。
- 强化 Phase 状态变化的验收证据引用。
- 明确旧派生项目按兼容矩阵补齐，而非全文重写。
- 在审计 / 评估 Prompt 中加入“需求链状态传播检查”。

## 8. 可回流模板优化建议

| 建议 | 是否已有规范覆盖 | Batch 1 提案处理 |
|---|---|---|
| `00` 来源映射、下游影响 | 已在 `ai/doc-standards/00-scenario.md` 覆盖 | 不重复，仅建议审计报告检查是否缺失 |
| `01` 用户操作流、验收口径 | 已在 `ai/doc-standards/01-user-requirements.md` 覆盖 | 不重复，仅建议兼容补齐矩阵 |
| `02` 约束 / 异常矩阵 | 已在 `ai/doc-standards/02-srs.md` 覆盖 | 建议强化验证映射和状态审计 |
| `03` Phase 路线图 | 已在 `ai/doc-standards/03-prd.md` 覆盖 | 建议新增完成证据 / 验收引用口径 |
| 需求链状态传播 | 尚未形成独立检查项 | 作为本 Batch 提案重点 |
| 旧派生兼容补齐方式 | 16 号审计 Prompt 已部分覆盖 | 建议扩展到 Batch 评估报告和 00-03 专项提案 |

## 9. 待人工确认项

| ID | 待确认项 | AI 建议 | 建议依据 | 备选方案 | 取舍影响 / 阻塞关系 |
|---|---|---|---|---|---|
| C-B1-001 | 是否把 `docs/03-prd.md` Phase1 状态回写列为 Phase2 修订前置 | 建议是 | `03` 是阶段边界权威源，当前与 `09` / README 完成事实不一致 | 暂不回写，等 Phase2 确认时一起修 | 延后会继续保留状态冲突，影响 Phase2 文档可信度 |
| C-B1-002 | 00-03 是否按规范镜像全文重写 | 建议否，仅追加兼容矩阵 | 现有需求链语义已稳定，机械重写风险高 | 全文按 `ai/doc-standards` 重排 | 结构更统一，但容易引入历史事实偏差 |
| C-B1-003 | Batch 1 提案是否聚焦状态传播而非重复章节标准 | 建议是 | 多数章节缺口已有 doc-standards 覆盖 | 起草完整 00-03 标准重写提案 | 可能与既有标准重复，增加模板维护成本 |

## 10. 下一步

- 已完成：Batch 1 `00-03` 需求链只读评估。
- 本次配套提案：`_proposals/TEMPLATE-UPGRADE-00-03-requirements-chain-standard.md`。
- 下一 Batch：评估 `docs/04-architecture.md` 与 `docs/05-tech-spec.md`，生成 Batch 2 报告和架构 / 技术方案规范提案。
