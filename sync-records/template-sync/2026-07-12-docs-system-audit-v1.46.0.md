# v1.46.0 同步后文档体系全链路审计

## 基本信息

- 项目：zhiyan-digital-cs-platform
- 审计类型：`/run docs-system-audit` 同步后审计模式
- 执行时间：2026-07-12 00:01 +08:00
- 当前分支：`main`
- 当前 HEAD：`ac20622 Merge pull request #37 from emily8421/chore/sync-template-v1.46.0`
- 同步模板版本：`v1.46.0`
- 规范基线：`ai/doc-standards/00-09`、`ai/doc-standards/design-doc.md`、`ai/doc-standards/frontend-interaction.md`、`ai/doc-standards/ui-prototype-strategy.md`
- 同步记录：`sync-records/template-sync/2026-07-11-sync-template-v1.46.0.md`
- 结论口径：本报告只做审计与回梳计划，不直接修改项目事实文档。

## 1. 链路健康度总览表

| 范围 | 健康度 | 主要证据 | 结论 |
|---|---|---|---|
| 00-03 需求链 | 良好，需同步入口口径 | `docs/00-scenario.md:68`、`docs/01-user-requirements.md:47`、`docs/02-srs.md:82`、`docs/03-prd.md:42` | SC → U → REQ → Phase 有矩阵；README 阶段表述落后。 |
| 04-05 总体设计 | 良好，运行环境摘要需回写 | `docs/04-architecture.md:222`、`docs/05-tech-spec.md:188`、`docs/research/2026-07-10-tech-env-evaluation-postgres-pgvector.md:17` | COMP/MOD/Flow、Risk、RG 已有；Docker 可用性在 local-env / project-rules 中残留旧状态。 |
| 06-07 DB / API 契约 | 良好 | `docs/06-db-design.md:240`、`docs/07-api-spec.md:311` | REQ → 表 / API 矩阵存在；当前 Phase 契约足以支撑既有实现与验证。 |
| 08-09 执行闭环 | 良好，入口文档落后 | `docs/08-dev-plan.md:8`、`docs/08-dev-plan.md:29`、`docs/08-dev-plan.md:30`、`docs/09-verification.md:411`、`docs/09-verification.md:522` | Sprint-7/8/9、M10、TC-060 已记录；README 仍停在 Sprint-8 前置 / TC-020。 |
| `docs/design/*` | 可接受兼容差异，P2 回梳 | `docs/research/2026-07-09-docs-open-items.md:136`、多文件未编号 H2 | 旧设计文档已支撑验收；新规范要求的编号 / 元信息 / readiness gate 可按需补齐。 |
| Open items | 存在已关闭项未回填 | `docs/research/2026-07-09-docs-open-items.md:119`、`sync-records/template-sync/2026-07-11-sync-template-v1.46.0.md:126` | DOC-C-006 仍标 #148 open，但同步记录显示 #148 closed 且已归档。 |
| 本地续接 | 需更新 | `.ai/session-handoff.md:8`、`.ai/session-handoff.md:30` | handoff 仍记录 PR #37 open / 待合并；本轮将回写。 |

## 2. 各维度问题清单

### 00-03 需求链断点

未发现阻塞性 SC / U / REQ / Phase 断点。需求链具备 `SC-ID → U-ID → REQ-ID → Phase` 基础矩阵。

### 事实 / 追溯断点

| ID | 严重度 | 文件:行 | 问题 | 权威源 | 建议修复方式 | 是否改业务事实 |
|---|---|---|---|---|---|---|
| DSA-P1-001 | P1 | `README.md:3`、`README.md:7`、`README.md:22`、`README.md:105`、`README.md:118` | README 当前阶段、开发计划和验证范围落后：仍写 Phase2 启动前 / Sprint-8 前置 / TC-001~020。 | `ai/project-rules.md:28`、`:30`；`docs/03-prd.md:8`、`:42`；`docs/08-dev-plan.md:8`、`:29`、`:30`；`docs/09-verification.md:411`、`:428`、`:522` | 最小更新 README 的当前阶段、快速开始说明、开发计划和验证方式。 | 是，更新入口文档事实表述，不新增能力。 |

### 横切传播残留

| ID | 严重度 | 文件:行 | 问题 | 权威源 | 建议修复方式 | 是否改业务事实 |
|---|---|---|---|---|---|---|
| DSA-P1-002 | P1 | `docs/env/local-env.md:36`、`ai/project-rules.md:76`、`ai/project-rules.md:104` | Docker 可用性仍保留旧“当前不可用 / 待修复确认”口径。 | `docs/research/2026-07-10-tech-env-evaluation-postgres-pgvector.md:17`、`:19`、`:70`、`:78`；`docs/05-tech-spec.md:8`、`:194`、`:195` | 回写为“2026-07-10 RG-002 已验证 Docker + PG/pgvector 可用；业务启用仍需单独任务”。 | 是，修正环境状态，不新增功能。 |
| DSA-P2-003 | P2 | `docs/research/2026-07-09-docs-open-items.md:119`~`:134` | DOC-C-006 仍写 #148 open / 待处理。 | `sync-records/template-sync/2026-07-11-sync-template-v1.46.0.md:119`、`:126` | 将 DOC-C-006 标记 closed 或移入已关闭项，记录 #148 已落地并归档。 | 是，更新待确认总览状态。 |

### 横切状态冲突

未发现真实外部系统、LLM、生产飞书或真实客户数据被误升级为已启用。当前权威口径仍为：真实 CRM / ERP / OA / 工单 / 生产飞书 / 生产 LLM 自动答复 No-Go 或后置 Phase3；Demo Sandbox 仅处理模拟数据。

### 规范基线缺口

| ID | 严重度 | 文件:行 | 问题 | 权威源 | 建议修复方式 | 是否改业务事实 |
|---|---|---|---|---|---|---|
| DSA-P2-004 | P2 | `docs/design/backend-service.md:102`、`docs/design/h5-dialog.md:113`、`docs/design/mock-integrations.md:110`、`docs/design/web-console.md:123` 等 | 多个旧 `docs/design/*` 文档后半段 H2 未编号，且与新 `design-doc` 标准的元信息 / readiness gate / 实现偏差区存在兼容差异。 | `docs/research/2026-07-09-docs-open-items.md:136`~`:151`；`ai/doc-standards/design-doc.md` | 触碰对应设计文档时最小补齐；如要批量处理，单独开设计文档结构回梳任务。 | 否，结构规范补齐，不改业务事实。 |

### 04-05 设计门禁缺口

无阻塞项。`docs/04-architecture.md` 已有组件、模块、流程和 REQ 矩阵；`docs/05-tech-spec.md` 已有风险矩阵与 readiness gate。仅 DSA-P1-002 需要把后续 RG-002 状态回写到环境摘要。

### 06-07 契约门禁缺口

无阻塞项。`docs/06-db-design.md` 已保留表结构、迁移 / seed / 安全留存和 REQ → 表矩阵；`docs/07-api-spec.md` 已保留 API-001~012、错误码、权限和 REQ → API 矩阵。

### 08-09 执行闭环缺口

无阻塞项。`docs/08-dev-plan.md` 与 `docs/09-verification.md` 已记录 Sprint-7/8/9、M10、Phase3 准备评估、Demo Sandbox 与 TC-060。缺口集中在 README 入口文档未传播这些事实，见 DSA-P1-001。

### 通用详细设计缺口

见 DSA-P2-004。该缺口已在 DOC-C-007 中登记为 P2，可延后。

### 可行性 / 部署缺口

见 DSA-P1-002。不是技术能力缺失，而是 `local-env` / `project-rules` 的状态摘要未吸收 2026-07-10 RG-002 技术验证结果。

### 前端交互缺口

未发现阻塞项。`docs/design/frontend-interaction.md` 存在，覆盖入口、页面、状态、接口依赖、验收路径和上游追溯。

### UI 原型策略缺口

未发现阻塞项。`ai/project-rules.md:83`~`:90` 已记录 UI 原型策略；`docs/research/2026-07-09-ui-prototype-exploration.md` 与 `docs/research/prototypes/2026-07-09-cs-platform-exploration.html` 提供需求探索原型证据。

### 本地续接状态

| ID | 严重度 | 文件:行 | 问题 | 权威源 | 建议修复方式 | 是否改业务事实 |
|---|---|---|---|---|---|---|
| DSA-P1-005 | P1 | `.ai/session-handoff.md:8`、`:9`、`:12`、`:30` | handoff 仍记录 PR #37 open / 待合并 / 同步分支。 | 本地 `main` 已 fast-forward 到 `ac20622`；用户确认 PR #37 已合并。 | 本轮回写 handoff 为闭环完成与剩余整改项。 | 否，本地续接状态更新。 |

## 3. 回梳计划

| 优先级 | 回梳项 | 建议范围 | 下一步 |
|---|---|---|---|
| P1 | README 状态传播 | `README.md` 当前阶段、开发计划、验证方式 | 另行确认后最小修订 DSA-P1-001。 |
| P1 | Docker / PG 状态传播 | `docs/env/local-env.md`、`ai/project-rules.md` | 另行确认后最小修订 DSA-P1-002。 |
| P2 | Open items 状态收口 | `docs/research/2026-07-09-docs-open-items.md` | 另行确认后关闭 DOC-C-006。 |
| P2 | 设计文档规范兼容 | `docs/design/*` | 触碰对应设计文档时补齐，或单独开批量回梳。 |
| P1 | Handoff 状态 | `.ai/session-handoff.md` | 本轮直接回写，避免续接误导。 |

## 4. 待人工确认事项总览

| ID | 来源文档或位置 | 待确认项 | AI 建议 | 建议依据 | 备选方案 | 取舍影响或阻塞关系 |
|---|---|---|---|---|---|---|
| DSA-C-001 | `README.md` | 是否立即修订 README 入口状态 | 建议修订 | README 与 `03/08/09/project-rules` 冲突，会误导新会话 | 暂仅记录审计发现 | 不阻塞 A13，但影响入口可信度 |
| DSA-C-002 | `docs/env/local-env.md`、`ai/project-rules.md` | 是否回写 Docker / PG 当前状态 | 建议修订为带时间戳的验证状态 | RG-002 已 Go；旧不可用口径残留 | 仅依赖 `05/09` 的验证记录 | 不阻塞 A13，但影响环境权威源一致性 |
| DSA-C-003 | `docs/research/2026-07-09-docs-open-items.md` | 是否关闭 DOC-C-006 | 建议关闭 | #148 已 closed 且本地提案归档 | 暂不改历史 open items | 不阻塞 A13，但影响 open items 准确性 |
| DSA-C-004 | `docs/design/*` | 是否批量补齐设计文档结构规范 | 建议延后或单独任务 | 已有文档支撑验收，批量重写风险较高 | 触碰时补齐 | 不阻塞当前；影响规范一致性 |

## 5. 同步后回梳建议

- 审计摘要：文档体系主链路可用；同步后完整审计已执行；剩余问题主要是入口 / 环境 / open items 的状态传播残留与旧设计文档规范兼容差异。
- 需回梳文档：`README.md`、`docs/env/local-env.md`、`ai/project-rules.md`、`docs/research/2026-07-09-docs-open-items.md`；`docs/design/*` 可延后。
- 阻塞项：无阻塞 A13 的同步治理项；P1 为入口可信度与环境口径问题。
- 可延后项：`docs/design/*` 编号 / 元信息兼容回梳。
- 下一步命令：如用户确认修复，使用文档最小修订流程处理 DSA-C-001~DSA-C-003；不建议与业务开发混入同一提交。

## 6. 同步报告回写建议

- 将 `docs-system-audit` 状态由“轻量执行”更新为“完整执行”。
- 证据路径：`sync-records/template-sync/2026-07-12-docs-system-audit-v1.46.0.md`。
- A13 可改为“完整闭环完成；存在 P1/P2 文档状态传播整改项，不影响模板同步边界”。
