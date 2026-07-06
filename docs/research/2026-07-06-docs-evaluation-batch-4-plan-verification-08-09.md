# Batch 4 文档评估报告：08-09 开发计划与验证证据

> 定位：本报告是 `docs/08-dev-plan.md` 与 `docs/09-verification.md` 的只读审计与模板提案依据，不替代正式开发计划或验证计划修订。
> 评估日期：2026-07-06
> 范围：`docs/08-dev-plan.md`、`docs/09-verification.md`，对照 `ai/doc-standards/08-dev-plan.md` 与 `ai/doc-standards/09-verification.md`。
> 来源 Batch：Batch 0 `docs/research/2026-07-06-template-proposal-audit-batch-0-overall.md`。

## 1. 评估摘要

本次 Batch 4 评估目标，是判断 `08-09` 是否把已确认设计转化为可执行 Sprint、可追溯验收和可复现证据，并识别可回流到模板的开发计划 / 验证证据规范缺口。

结论：**Conditional Go**。

`09` 已较好完成 Phase1 验证回填，包含 TC-001~TC-016、本机资源验证、阶段验收清单、Sprint-6 验收记录和未验证风险；`08` 的 Sprint 计划结构完整，但当前进度记录明显滞后，仍停留在 2026-07-03 文档补齐 / Sprint-1 前口径，与 `README.md` 和 `09` 中 Sprint-1~6 已完成事实不一致。

最关键判断：

- `08` 已具备 Phase1 目标、Sprint 总览、Sprint-1~6 详情、任务拆分规则和里程碑，能支撑开发执行。
- `09` 已具备 REQ → TC 矩阵、TC 详情、资源验证、AC 状态、验收记录和未验证风险，能支撑 Phase1 验收事实。
- `08` 缺少每个 Sprint 的状态列、验证包状态、Sprint 完成包、改动文件、验证命令和残留风险记录；导致计划文档无法反映 Sprint-1~6 已完成。
- `09` 的验证记录有效，但缺少标准化 Sprint 验收包表、缺陷 / 回归记录和技术环境评估验证映射；这些已在 `ai/doc-standards/09-verification.md` 中有规范，项目可后续按最小方式补齐。
- 模板层面建议强化 `08 ↔ 09 ↔ README ↔ PRD` 的状态回写规则：完成 Sprint 或 Phase 后，不能只更新验证计划和 README，必须同步检查开发计划进度与 Phase 状态。

## 2. 评估范围与依据

### 2.1 读取文档

| 类型 | 文档 |
|---|---|
| 开发与验证 | `docs/08-dev-plan.md`、`docs/09-verification.md` |
| 规范镜像 | `ai/doc-standards/08-dev-plan.md`、`ai/doc-standards/09-verification.md` |
| 上游参照 | `docs/03-prd.md`、`docs/04-architecture.md`、`docs/05-tech-spec.md`、`docs/06-db-design.md`、`docs/07-api-spec.md` |
| 状态参照 | `README.md`、`docs/research/2026-07-06-phase-upgrade-evaluation.md`、`.ai/session-handoff.md` |
| 规则依据 | `ai/implementation-lifecycle-rules.md`、`ai/document-lifecycle-rules.md`、`ai/session-rules.md` |

### 2.2 评估口径

| 维度 | 口径 |
|---|---|
| 完整性 | 是否包含 Phase 目标、Sprint 总览、Sprint 详情、任务拆分、里程碑、TC 矩阵、资源验证和验收记录 |
| 执行性 | Sprint 是否粒度清晰、输入文档明确、修改范围和验收标准可执行 |
| 追溯性 | Sprint / TC 是否能追溯到 REQ、功能和设计文档 |
| 可验证性 | 验证方式、命令、结果、资源记录和未验证风险是否可复现 |
| 状态一致性 | `08`、`09`、README、PRD 和 Phase 升级评估的状态是否一致 |
| 维护性 | 完成 Sprint / Phase 后是否有回写机制，避免计划滞后 |
| 模板回流价值 | 是否暴露出通用计划 / 验证证据模板缺口 |

## 3. 逐文档评估

### 3.1 `docs/08-dev-plan.md`

| 项 | 观察 |
|---|---|
| 合规项 | 已包含文档元信息、Phase1 目标、Sprint 总览、Sprint-1~6 详情、任务拆分规则、依赖与里程碑、当前进度记录和已确认口径。 |
| 执行性 | 每个 Sprint 均有目标、输入文档、修改范围、验收标准和禁止事项；Sprint-6 明确需回填 README 和 `09`。 |
| 追溯情况 | Sprint 输入文档关联 REQ、API、design、verification；M1~M7 里程碑清晰。 |
| 项目问题 | 当前进度记录仍为 2026-07-03 文档补齐中；“已确认可按 Sprint-1 开始”已过时，与 README 中 Sprint-1~6 已完成和 `09` Sprint-6 验收记录冲突。 |
| 规范差异 | 对照 `ai/doc-standards/08-dev-plan.md`，Sprint 总览缺状态列、测试等级 / 验证包列；Sprint 详情缺“验证包”和“Sprint 完成包”；当前进度记录缺 Sprint / Task、验证结果和下一步。 |
| 影响 | 进入 Phase2 前需回写或归档 Phase1 进度，否则计划文档无法作为当前执行状态依据。 |

### 3.2 `docs/09-verification.md`

| 项 | 观察 |
|---|---|
| 合规项 | 已包含验证策略、REQ → TC 矩阵、TC-001~TC-016 详情、本机资源验证、阶段验收清单、验收记录、自动化与手工验证建议、未验证风险和人工确认记录。 |
| 证据情况 | 2026-07-06 Sprint-6 记录包含后端 API 测试 `19 passed`、H5 / Console build、HTTP 场景验证和三端端口。 |
| 资源验证 | 已记录 Python 后端、Node 前端、内存、GPU、磁盘、Docker、PostgreSQL / pgvector、Mock 数据、外部网络状态。 |
| 规范差异 | 对照 `ai/doc-standards/09-verification.md`，缺测试等级矩阵、Phase 测试大纲、技术环境评估验证区、Sprint 验收包、缺陷与回归记录表；验收记录缺执行人、验证证据字段的结构化列。 |
| 影响 | 不影响 Phase1 已验收事实；但后续进入 Phase2 / MVP 试点时，验证证据粒度与回归记录应更结构化。 |
| 建议 | 项目后续可最小补充 Sprint 验收包和回归记录表；模板提案聚焦完成回写和证据标准。 |

## 4. 状态一致性核对

| 状态源 | 当前状态 | 与其他文档关系 | 结论 |
|---|---|---|---|
| `docs/08-dev-plan.md` | 当前进度停在文档补齐 / Sprint-1 前 | 落后于 README、`09` 和 Phase 升级评估 | 需回梳 |
| `docs/09-verification.md` | Sprint-6 已通过，Phase1 AC 已满足 | 与 README 和 Phase 升级评估一致 | 可信 |
| `README.md` | Sprint-1~6 已完成，Phase1 Demo 已跑通 | 与 `09` 一致；领先于 `08` / `03` | 可信但需传播 |
| `docs/03-prd.md` | Phase1 状态仍为骨架 / 待实现 | 落后于 `09` / README | Batch 1 已列 P0 |
| Phase 升级评估 | Conditional Go，建议进入 Phase2 规划 | 依据 `09` 和 README | 需人工确认后传播 |

## 5. 问题项

| ID | 优先级 | 类型 | 问题 | 位置 | 影响 | 建议修复方式 |
|---|---|---|---|---|---|---|
| B4-001 | P0 | 项目事实 / 状态传播 | `08` 当前进度记录和已确认口径明显滞后于 Sprint-1~6 完成事实 | `docs/08-dev-plan.md` §6 / §7 | 进入 Phase2 前计划文档不可信 | 另走文档回梳，补 Phase1 Sprint 完成状态和下一步 Phase2 规划入口 |
| B4-002 | P1 | 计划证据缺口 | Sprint 总览缺状态、验证包、验收方式、完成包字段 | `docs/08-dev-plan.md` §2 / §3 | 难以从计划文档快速判断每个 Sprint 是否完成 | 补 Sprint 状态与完成包矩阵 |
| B4-003 | P1 | 验证证据缺口 | `09` 有验收记录，但缺标准化 Sprint 验收包表 | `docs/09-verification.md` §6 | 后续复盘改动文件、命令和残留风险不够集中 | 补 Sprint 验收包表 |
| B4-004 | P1 | 回归治理缺口 | 缺陷与回归记录未结构化 | `docs/09-verification.md` | Phase2 修复 / 增强后难以追踪回归范围 | 补缺陷与回归记录表 |
| B4-005 | P2 | 模板流程缺口 | 完成 Sprint / Phase 后未强制检查 `08/09/README/03/project-rules` 状态同步 | Prompt / 工作流层 | 多派生项目可能重复出现进度文档滞后 | Batch 4 提案补完成回写清单 |

## 6. 风险项

| ID | 风险 | 是否阻塞 | 说明 |
|---|---|---|---|
| R-B4-001 | 若不回写 `08`，后续 AI 可能误以为仍应从 Sprint-1 开始 | 阻塞 Phase2 正式规划 | 计划文档是实现生命周期权威来源之一 |
| R-B4-002 | 若 `09` 只写一句验收通过，不记录命令 / 证据 / 失败项，后续无法复现验收 | 不阻塞当前，但影响维护 | 当前项目已有一定证据，但可结构化增强 |
| R-B4-003 | 若 Phase 升级后不更新 `03/project-rules/08/09`，会出现阶段边界冲突 | 条件阻塞 | 需等待人工确认 Phase2 后同步修订 |
| R-B4-004 | 若真实集成进入 Phase2，而回归记录仍缺失，修复或增强可能破坏 Phase1 Demo | 条件阻塞 | Phase2 前应建立回归记录区 |

## 7. 修复建议

### 7.1 项目正式文档修订建议

本报告不直接修改正式文档。建议后续单独启动项目文档回梳：

1. 在 `docs/08-dev-plan.md` 回写 Sprint-1~Sprint-6 状态、验证摘要和当前下一步。
2. 为 Sprint 总览增加状态 / 验证包 / 验收方式列，或追加 Phase1 完成矩阵。
3. 在 `docs/08-dev-plan.md` 增加 Sprint 完成包摘要，记录改动文件、验证命令、验收记录、残留风险。
4. 在 `docs/09-verification.md` 增加 Sprint 验收包表和缺陷 / 回归记录表。
5. 若接受 Phase2 Conditional Go，再同步更新 `03`、`project-rules`、`08`、`09` 的 Phase2 范围与验证计划。

### 7.2 模板提案建议

本 Batch 配套提案：`_proposals/TEMPLATE-UPGRADE-08-09-plan-verification-evidence-standard.md`。

提案重点：

- Sprint 总览状态与验证包字段。
- Sprint 完成包最低结构。
- 验证证据最低字段。
- 完成后跨文档状态回写清单。
- 缺陷 / 回归记录触发条件。

## 8. 可回流模板优化建议

| 建议 | 是否已有规范覆盖 | Batch 4 提案处理 |
|---|---|---|
| 08 Sprint 状态、验证包、完成包 | 已在 `ai/doc-standards/08-dev-plan.md` 部分覆盖 | 强化完成后必须回写与检查清单 |
| 09 Sprint 验收包、缺陷回归、风险 | 已在 `ai/doc-standards/09-verification.md` 覆盖 | 强化证据最低字段和状态同步触发 |
| README / PRD / project-rules 同步 | 分散在生命周期规则中 | 作为本提案重点 |
| 验证记录可复现性 | 部分覆盖 | 明确命令、环境、结果、失败项、残留风险最低字段 |

## 9. 待人工确认项

| ID | 待确认项 | AI 建议 | 建议依据 | 备选方案 | 取舍影响 / 阻塞关系 |
|---|---|---|---|---|---|
| C-B4-001 | 是否将 `docs/08-dev-plan.md` 进度回写列为 Phase2 修订前置 | 建议是 | 当前 `08` 与 `09` / README 状态冲突 | 暂等 Phase2 确认后一并修 | 延后会继续保留执行计划不可信问题 |
| C-B4-002 | 是否在 `09` 补 Sprint 验收包和回归记录 | 建议 Phase2 前补最小表 | Phase2 真实集成和增强会需要回归证据 | 仅保留现有验收记录 | 文件更简洁，但后续追踪成本高 |
| C-B4-003 | 模板是否强制完成 Sprint 后检查 `08/09/README/03/project-rules` | 建议作为完成清单 | 当前项目已实证出现 `08/03` 状态落后 | 仅依赖人工记忆 | 人工记忆易漏，跨 AI 会话时风险更高 |

## 10. 下一步

- 已完成：Batch 4 `08-09` 开发计划与验证证据只读评估。
- 本次配套提案：`_proposals/TEMPLATE-UPGRADE-08-09-plan-verification-evidence-standard.md`。
- 下一 Batch：评估 `docs/design/*`，生成 Batch 5 报告和详细设计通用规范提案。
