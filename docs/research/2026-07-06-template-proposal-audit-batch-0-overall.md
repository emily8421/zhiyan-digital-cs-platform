# Batch 0 文档体系模板提案审计报告

> 定位：本报告是只读审计与模板提案 backlog，不替代 `docs/00-09` 正式文档修订，不直接定义 Phase2 需求或实现范围。
> 评估日期：2026-07-06
> 范围：`docs/00-09`、`docs/design/*`、`ai/doc-standards/*`、现有 `_proposals/TEMPLATE-UPGRADE-*.md` 与 `_archive/proposals/TEMPLATE-UPGRADE-*.md` 摘要对照。

## 1. 评估摘要

本次 Batch 0 只读审计的目标，是先判断当前项目文档体系暴露出的哪些问题属于可回流到 `ai-project-template` 的通用模板规范缺口，并制定后续分批审计与提案计划。

结论：建议采用“每个 Batch 先生成独立审计 / 评估报告，再起草对应模板规范提案”的工作流；Batch 0 本身只做整体评估、拆分计划和流程提案，不直接修订项目正式文档。

关键判断：

- `docs/00-09` 已支撑 Phase1 Demo 闭环，REQ → API / DB / Sprint / TC 的主追溯链基本闭合。
- `docs/09-verification.md` 已记录 Sprint-6 本机验证证据，Phase1 完成事实较充分。
- `docs/08-dev-plan.md` 的“当前进度记录”仍停留在早期状态，与 `README.md` 和 `docs/09-verification.md` 的 Sprint-1~6 完成事实不一致，属于项目回梳问题，也暴露出模板需要强化“进度回写 / 验收证据回写”规范。
- `ai/doc-standards/00-09` 已覆盖许多 00-09 章节级规范，后续提案不应重复已有标准，而应聚焦项目实证中发现的标准缺口、执行流程缺口和跨文档约束缺口。
- `docs/design/*` 除 `frontend-interaction.md` 外，普遍缺少统一的 `0. 文档元信息`、结构化待确认项、实现偏差记录和统一追溯矩阵；这是较明确的通用模板提案方向。
- 现有 `_proposals/` 中仅剩 `TEMPLATE-UPGRADE-derived-sync-powershell-fallback.md`，已提交 issue #102；前端交互、待确认项结构、文档规范镜像等相关提案已归档，后续应避免重复。

## 2. 审计方法

本次审计采用以下方式：

1. 按 `ai/index.md` 要求读取全部规则文件，重点对照 `ai/document-lifecycle-rules.md`、`ai/implementation-lifecycle-rules.md`、`ai/session-rules.md` 和 `ai/project-rules.md`。
2. 读取 `ai/commands/docs-system-audit.md`、`ai/commands/docs-evaluation.md`、`ai/prompts/review/16-docs-system-audit.md`、`ai/prompts/review/19-docs-evaluation.md`，确认审计与评估输出口径。
3. 对照 `ai/doc-standards/00-scenario.md` 至 `ai/doc-standards/09-verification.md`，检查项目 `docs/00-09` 的章节、追溯、阶段标签、验收证据和待确认项结构。
4. 扫描 `docs/design/*`，检查详细设计文档的定位、职责边界、流程、失败处理、Mock / 降级、阶段增量、跨文档追溯和待确认项。
5. 对照 `_proposals/` 与 `_archive/proposals/` 中既有模板提案，识别重复、依赖和已落地方向。
6. 仅记录可通用于多个派生项目的模板改进点；项目自身修订建议不在本报告直接执行。

## 3. 链路健康度总览

| 维度 | 当前观察 | 健康度 | 后续处理 |
|---|---|---|---|
| 纵向追溯链 | `00` 场景到 `01` U-ID、`02` REQ、`03` 功能、`04` 模块、`06` 表、`07` API、`08` Sprint、`09` TC 基本可追溯 | 良好 | Batch 1~4 逐段复核细节 |
| Phase 边界 | Phase1 明确为本机 Demo，真实飞书、真实业务系统、LLM 默认关闭 | 良好 | Phase2 需等待人工确认后再修订正式文档 |
| 验收证据 | `09` 已记录 Sprint-6 验证、三端端口和未验证风险 | 良好 | Batch 4 检查证据粒度是否满足模板长期规范 |
| 进度回写 | `08` 当前进度仍停在 2026-07-03 文档补齐中，与 README / 09 的完成事实不一致 | 需回梳 | Batch 4 输出项目问题与模板提案 |
| 规范基线 | 00-09 多数文档语义等价，但章节名与 `ai/doc-standards/*` 不完全一致 | 可接受但需评估 | 后续按“缺关键结构”而非“逐字改标题”审计 |
| 详细设计 | 多数 `docs/design/*` 有定位和追溯，但缺少统一元信息、待确认项和实现偏差区 | 需规范化 | Batch 5 起草 design 通用规范提案 |
| 横切约束 | Mock / 降级、安全隐私、不编造分散在多文档中，整体一致但缺少统一检查表 | 可接受但可增强 | Batch 6 判断是否独立提案 |

## 4. 00-09 高层观察

| 范围 | 当前观察 | 建议方向 | 后续 Batch |
|---|---|---|---|
| `docs/00-03` | 需求链条完整，已包含场景、U-ID、REQ、Phase 路线图；但 `00/01` 相比规范镜像缺少更结构化的用户操作流、用户验收口径和结构化待确认项 | 不急于修模板，先确认现有 `ai/doc-standards` 是否已覆盖；若提案，聚焦需求链评估报告的标准写法与兼容矩阵 | Batch 1 |
| `docs/04-05` | 架构图、组件、拓扑、技术降级完整；`05` 对依赖 / 配置矩阵和技术风险 → 验证映射可更结构化 | 避免重复已有 `05` 标准，重点评估环境评估、风险验证和 Mock / 降级与 `09` 的映射 | Batch 2 |
| `docs/06-07` | 表清单、字段、ER 图、API 清单、交互图、错误码与矩阵完整；逐接口契约仍是“草案”形态，权限 / 限流为 Phase1 简化 | 提案应聚焦“Demo 契约草案如何标注状态、如何升为 MVP 契约”，而不是重复已有 DB / API 标准 | Batch 3 |
| `docs/08-09` | `09` 验证回填充分；`08` Sprint 总览与当前进度落后，缺 Sprint 完成包和状态回写 | 需要形成“计划 / 验证 / README / 验收记录同步回写”模板规范 | Batch 4 |

## 5. `docs/design/*` 高层观察

| 文档 | 当前观察 | 建议方向 | 后续 Batch |
|---|---|---|---|
| `frontend-interaction.md` | 结构较完整，含元信息、页面清单、用户路径、状态、接口依赖和验收路径 | 作为 design 通用规范的重要参考，但不要把前端特有结构强加给所有子系统 | Batch 5 |
| `backend-service.md` | 有分层、服务职责、流程、错误处理和降级；缺少元信息、统一追溯矩阵、结构化待确认项 | 纳入通用 design 模板：元信息、职责边界、流程、错误 / 降级、REQ/API/TC 追溯 | Batch 5 |
| `h5-dialog.md` / `web-console.md` | 页面结构、状态、流程、接口依赖和验收较清晰；缺少统一元信息和实现偏差记录 | 与 `frontend-interaction.md` 保持“总交互索引 + 单入口细化”的模板关系 | Batch 5 |
| `knowledge-and-policy.md` | 不编造、高风险、知识缺口状态机清晰；缺少 readiness gate 和未来启用 LLM / 向量能力的门槛模板 | 与 Batch 6 的 Mock / AI / 高风险横切规范合并判断 | Batch 5 / 6 |
| `mock-integrations.md` | Mock 适配与真实集成升级条件清晰；可作为 Mock / 降级规范样例 | 判断是否需要独立 Mock / 降级提案，或并入 design 通用规范 | Batch 5 / 6 |
| `scenario-packs.md` | 配置模型和校验规则清晰；缺少统一状态、字段契约、失败处理和验收矩阵 | 纳入 design 通用规范的“配置型子系统”示例 | Batch 5 |

## 6. 模板提案 Backlog

| Batch | 建议报告路径 | 建议提案文件 | 主题 | 优先级 | 当前状态 |
|---|---|---|---|---|---|
| B0 | `docs/research/2026-07-06-template-proposal-audit-batch-0-overall.md` | `_proposals/TEMPLATE-UPGRADE-docs-system-batch-audit-workflow.md` | 文档体系分批审计与提案工作流 | P0 | 本次生成 |
| B1 | `docs/research/2026-07-06-docs-evaluation-batch-1-requirements-00-03.md` | `_proposals/TEMPLATE-UPGRADE-00-03-requirements-chain-standard.md` | 00-03 需求链评估与规范补强 | P0 | 待审计后起草 |
| B2 | `docs/research/2026-07-06-docs-evaluation-batch-2-architecture-tech-04-05.md` | `_proposals/TEMPLATE-UPGRADE-04-05-architecture-tech-standard.md` | 架构 / 技术方案与环境风险验证规范 | P0 | 待审计后起草 |
| B3 | `docs/research/2026-07-06-docs-evaluation-batch-3-db-api-06-07.md` | `_proposals/TEMPLATE-UPGRADE-06-07-db-api-contract-standard.md` | DB / API 契约状态与升阶段规范 | P0 | 待审计后起草 |
| B4 | `docs/research/2026-07-06-docs-evaluation-batch-4-plan-verification-08-09.md` | `_proposals/TEMPLATE-UPGRADE-08-09-plan-verification-evidence-standard.md` | 开发计划、进度回写和验证证据规范 | P0 | 待审计后起草 |
| B5 | `docs/research/2026-07-06-docs-evaluation-batch-5-design-docs.md` | `_proposals/TEMPLATE-UPGRADE-design-doc-standard.md` | `docs/design/*` 通用详细设计规范 | P0 | 待审计后起草 |
| B6 | `docs/research/2026-07-06-template-proposal-audit-batch-6-cross-cutting.md` | `_proposals/TEMPLATE-UPGRADE-cross-cutting-mock-security-standard.md` | Mock / 降级 / 权限安全 / 高风险能力横切规范归并 | P1 | 待 B1~B5 后判断 |

## 7. 每个 Batch 的报告要求

后续每个 Batch 都应先落盘独立报告，再起草对应提案。报告建议包含：

1. 审计范围与输入文档。
2. 对照规范：读取了哪些 `ai/doc-standards/*`、规则或 Prompt。
3. 逐文档观察：合规项、问题项、风险项、修复建议。
4. 可回流模板缺口：必须区分“项目事实问题”和“通用模板缺口”。
5. 与既有提案的重复 / 依赖关系。
6. 建议起草的提案文件名与范围。
7. 是否需要拆分或合并提案。
8. 结构化待人工确认项。

## 8. 待人工确认项

| ID | 待确认项 | AI 建议 | 建议依据 | 备选方案 | 取舍影响 / 阻塞关系 |
|---|---|---|---|---|---|
| C-B0-001 | 是否采用 Batch 0~6 的“报告 + 提案”成对落盘方式 | 建议采用 | 可避免长任务中断、提案重复和范围漂移 | 只写一个总报告或只写提案 | 文件数量更少，但后续难追溯每个提案为何拆分 |
| C-B0-002 | 后续提案是否只写通用模板缺口，不直接修项目正式文档 | 建议采用 | `ai/global-rules.md` 要求通用模板改进走 `_proposals/`，项目事实修订另走文档修订流程 | 在同一任务中顺手修改项目文档 | 容易混淆模板治理与项目事实，增加审查成本 |
| C-B0-003 | `docs/08-dev-plan.md` 进度落后是否另开项目回梳任务 | 建议在 Batch 4 报告中列为项目修订建议，确认后再回梳 | 当前 `README.md` 与 `09` 已记录 Sprint-1~6 完成，但 `08` 当前进度未同步 | 立即修 `08` | 可快速消除不一致，但会打断模板提案审计主线 |
| C-B0-004 | B6 横切规范是否独立成提案 | 建议等 B1~B5 完成后再决定 | Mock / 降级 / 权限安全可能已被 B2 / B5 吸收 | 立即独立起草 | 更清晰但可能与前面提案重复 |

## 9. 后续动作

- 已完成：Batch 0 整体只读审计与提案 Backlog 规划。
- 本次配套提案：`_proposals/TEMPLATE-UPGRADE-docs-system-batch-audit-workflow.md`。
- 下一步：执行 Batch 1，先生成 `00-03` 需求链评估报告，再起草 `TEMPLATE-UPGRADE-00-03-requirements-chain-standard.md`。
- 后续：每个 Batch 均先审计报告，再模板提案；提案成熟后按 `/run submit-proposal` 回流到模板仓 issue。
