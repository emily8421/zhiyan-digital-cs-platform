# Batch 2 文档评估报告：04-05 架构与技术方案

> 定位：本报告是 `docs/04-architecture.md` 与 `docs/05-tech-spec.md` 的只读审计与模板提案依据，不替代正式架构或技术方案修订。
> 评估日期：2026-07-06
> 范围：`docs/04-architecture.md`、`docs/05-tech-spec.md`，对照 `ai/doc-standards/04-architecture.md` 与 `ai/doc-standards/05-tech-spec.md`。
> 来源 Batch：Batch 0 `docs/research/2026-07-06-template-proposal-audit-batch-0-overall.md`。

## 1. 评估摘要

本次 Batch 2 评估目标，是判断 `04-05` 是否把已确认需求转化为可执行、可验证、可降级的架构与技术方案，并识别可回流到模板的规范缺口。

结论：**Conditional Go**。

`04-05` 对 Phase1 Demo 的架构、模块、拓扑、技术栈、环境约束和 Mock / 降级策略描述较完整，足以支撑 Phase1 已完成事实；但若进入 Phase2 / MVP 试点规划，需要补强“技术风险 → 验证证据 → Phase 解锁条件”的结构化表达。模板层面建议强化架构 / 技术方案中的环境评估、依赖配置、风险验证映射、Mock / 降级状态标识和升阶段门槛。

最关键判断：

- `docs/04-architecture.md` 已包含系统上下文图、组件视图、模块划分、关键流程、运行拓扑、架构决策和 REQ → 模块矩阵。
- `docs/05-tech-spec.md` 已明确 React + Vite + TypeScript、FastAPI、PostgreSQL / pgvector 计划方向、飞书 Mock、LLM 默认关闭和本机资源降级策略。
- 04 / 05 对 Phase1 仍是可用设计，但未系统记录技术风险 ID、验证方式、对应用例 / 任务、当前验证证据和后续解锁条件。
- `05` 的依赖与配置矩阵不够细，安全 / 隐私 / 合规边界较清楚但缺少“技术风险 → `09` 验证 / Phase2 readiness gate”的统一表。
- 这些问题既有项目回梳价值，也有模板通用价值，适合形成 Batch 2 提案。

## 2. 评估范围与依据

### 2.1 读取文档

| 类型 | 文档 |
|---|---|
| 项目总体设计 | `docs/04-architecture.md`、`docs/05-tech-spec.md` |
| 规范镜像 | `ai/doc-standards/04-architecture.md`、`ai/doc-standards/05-tech-spec.md` |
| 上游 / 下游参照 | `docs/02-srs.md`、`docs/03-prd.md`、`docs/06-db-design.md`、`docs/07-api-spec.md`、`docs/09-verification.md` |
| 环境事实 | `docs/env/local-env.md`、`ai/project-rules.md` |
| 规则依据 | `ai/document-lifecycle-rules.md`、`ai/implementation-lifecycle-rules.md` |

### 2.2 评估口径

| 维度 | 口径 |
|---|---|
| 完整性 | 是否覆盖架构目标、上下文图、模块、流程、拓扑、技术栈、资源约束 |
| 合理性 | 是否只承接已授权 REQ 和 Phase 范围，不提前实现后续能力 |
| 可行性 | 是否结合本机资源、Docker 状态、外部服务权限和降级策略 |
| 一致性 | Mock / 降级、真实服务禁用、LLM 关闭等横切事实是否一致 |
| 追溯性 | 模块 / 技术决策是否能追溯到 REQ、Phase、环境约束或 ADR |
| 可验证性 | 风险、依赖和技术决策是否映射到 `09` 的 TC 或资源验证 |
| 模板回流价值 | 是否暴露出通用架构 / 技术方案标准缺口 |

## 3. 逐文档评估

### 3.1 `docs/04-architecture.md`

| 项 | 观察 |
|---|---|
| 合规项 | 已包含文档元信息、架构目标、系统上下文 Mermaid 图、组件视图、模块划分 Mermaid 图、关键流程、Phase1 / Phase2+ 运行拓扑、ADR 和 REQ → 模块矩阵。 |
| 追溯情况 | REQ-001~REQ-016 已映射到前端、后端服务、数据 / 适配和设计文档。 |
| Phase 边界 | 明确 Phase1 本机 Demo、外部系统 Mock、飞书 Mock、LLM 默认关闭、PostgreSQL / pgvector 可降级。 |
| 规范差异 | 对照 `ai/doc-standards/04-architecture.md`，架构决策已有 ADR 表，但缺少更结构化的“约束来源 / 备选方案 / 取舍 / 验证方式”；关键流程未统一映射到 API / TC。 |
| 影响 | 不阻塞 Phase1；Phase2 规划真实飞书、权限、PostgreSQL 或部署时，需要更明确的 readiness gate 和技术验证任务。 |
| 建议 | 后续项目回梳可追加“架构风险与验证映射表”，不必重写现有图和模块矩阵。 |

### 3.2 `docs/05-tech-spec.md`

| 项 | 观察 |
|---|---|
| 合规项 | 已包含技术栈、本机环境约束、关键技术决策、后端 / 前端 / 数据 / 接口方案、安全合规、资源评估与降级策略、编码约定和确认记录。 |
| 追溯情况 | 技术方案与 `ai/project-rules.md`、`docs/env/local-env.md`、`docs/04-architecture.md` 基本一致。 |
| Phase 边界 | 明确数据库为计划方向但 Phase1 可降级；飞书真实通知、外部业务系统和 LLM 默认关闭。 |
| 规范差异 | 对照 `ai/doc-standards/05-tech-spec.md`，缺少独立依赖与配置矩阵，缺少技术风险 ID、验证方式、对应用例 / 任务的结构化表，技术环境评估结论未以独立章节引用。 |
| 影响 | 不影响 Phase1 Demo；但 Phase2 若要引入真实服务或数据库验证，缺少清晰的技术门禁和验收映射。 |
| 建议 | 模板提案应补强“技术风险 / 依赖 / 配置 / 验证映射”标准，并要求 `05` 与 `09` 保持证据闭环。 |

## 4. 关键维度核对

| 维度 | 当前状态 | 问题 / 缺口 | 建议 |
|---|---|---|---|
| 架构视图 | 上下文图、模块图、运行拓扑均已有 Mermaid | 缺少统一视图清单与“流程 → API / TC”映射 | Batch 2 提案建议补架构视图检查表 |
| ADR / 决策 | 已有 ADR-0001~ADR-0004 | 缺少备选方案、取舍影响、验证方式字段 | 模板建议扩展 ADR 最低字段 |
| 环境约束 | 已引用本机 Windows、Python、Node、Docker 不可用 | 未把环境风险拆成风险 ID / 验证项 | 与 `09` 资源验证形成映射 |
| 依赖与配置 | 技术栈已清晰 | 缺包级 / 服务级依赖矩阵、配置来源、密钥边界 | `05` 标准增加依赖 / 配置矩阵门槛 |
| Mock / 降级 | PostgreSQL、pgvector、飞书、LLM 均有降级口径 | 缺少统一状态枚举：默认关闭 / Mock / 候选 / 已验证 / 已启用 | Batch 2 或 Batch 6 合并处理 |
| 技术风险验证 | 有资源降级表和未验证风险 | 缺少 Risk-ID、验证命令、TC / Sprint 映射 | 模板应要求“风险 → 验证 → 解锁条件”矩阵 |
| Phase2 readiness | 已在 Phase 升级评估报告中列条件 | `04/05` 暂未原位吸收 Phase2 技术门槛 | 等人工确认 Phase2 后另走正式修订 |

## 5. 问题项

| ID | 优先级 | 类型 | 问题 | 位置 | 影响 | 建议修复方式 |
|---|---|---|---|---|---|---|
| B2-001 | P1 | 项目回梳 / 技术门禁 | Phase2 可能解锁飞书沙箱、PostgreSQL / pgvector、部署脚本等，但 `04/05` 尚未形成 readiness gate | `docs/04-architecture.md`、`docs/05-tech-spec.md` | Phase2 规划时容易把候选能力误当作已启用能力 | 等 Phase2 人工确认后追加技术门禁矩阵 |
| B2-002 | P1 | 规范基线缺口 | `05` 缺独立依赖与配置矩阵，包括配置来源、默认值、密钥边界和是否 Phase1 启用 | `docs/05-tech-spec.md` | 依赖安装 / 配置变更审核成本高 | 追加依赖 / 配置矩阵 |
| B2-003 | P1 | 可验证性缺口 | 技术风险未使用 Risk-ID 映射到 `docs/09-verification.md` 用例、资源验证或 Sprint 任务 | `docs/05-tech-spec.md` §9 | 未验证风险难以驱动后续任务 | 追加风险验证矩阵 |
| B2-004 | P2 | 架构决策缺口 | ADR 表缺少备选方案、取舍影响、验证方式 | `docs/04-architecture.md` §7 | 后续复盘决策时证据不足 | 扩展 ADR 最低字段或补 ADR 详情 |
| B2-005 | P2 | 横切规范缺口 | Mock / 降级状态分散在 `04/05/09/design`，缺少统一状态枚举 | 多文档 | 后续可能混淆“候选、默认关闭、Mock、已验证、已启用” | Batch 6 判断是否独立横切提案 |

## 6. 风险项

| ID | 风险 | 是否阻塞 | 说明 |
|---|---|---|---|
| R-B2-001 | Phase2 若直接修改技术栈或真实集成范围，可能绕过当前安全默认关闭边界 | 阻塞真实集成类 Sprint | 需先人工确认、技术评估和安全边界 |
| R-B2-002 | Docker / PostgreSQL / pgvector 未验证可用，若作为 Phase2 前置会阻塞开发节奏 | 条件阻塞 | 建议作为技术验证任务，不作为全部 Phase2 功能前置 |
| R-B2-003 | LLM 能力如进入 Phase2，当前 `04/05` 不足以约束证据、成本、不编造和兜底 | 阻塞 LLM 自动答复 | 只能先评估，不默认启用 |
| R-B2-004 | 只在 `09` 写未验证风险，不在 `05` 建立技术风险 ID，会导致技术债难追踪 | 不阻塞 Phase1 | 模板层面应强化 `05 ↔ 09` 闭环 |

## 7. 修复建议

### 7.1 项目正式文档修订建议

本报告不直接修改正式文档。建议后续在人工确认 Phase2 后另开修订任务：

1. 在 `docs/04-architecture.md` 增补 Phase2 readiness gate：真实飞书、PostgreSQL / pgvector、部署脚本、权限、LLM 分别列前置条件。
2. 在 `docs/05-tech-spec.md` 增补依赖 / 配置矩阵：包、服务、配置项、默认值、密钥边界、启用阶段、验证方式。
3. 在 `docs/05-tech-spec.md` 增补技术风险矩阵：Risk-ID、风险、影响、验证方式、对应 TC / Sprint、当前状态。
4. 同步检查 `docs/09-verification.md` 是否已有对应资源验证或技术验证用例。

### 7.2 模板提案建议

本 Batch 配套提案：`_proposals/TEMPLATE-UPGRADE-04-05-architecture-tech-standard.md`。

提案重点：

- 架构视图完整性检查表。
- ADR 最低字段补强。
- 技术依赖与配置矩阵。
- 技术风险 → 验证 → 解锁条件矩阵。
- Mock / 降级 / 默认关闭 / 候选能力的状态标识口径。

## 8. 可回流模板优化建议

| 建议 | 是否已有规范覆盖 | Batch 2 提案处理 |
|---|---|---|
| 04 架构目标、上下文图、组件图、拓扑 | 已在 `ai/doc-standards/04-architecture.md` 覆盖 | 不重复，仅建议加视图检查表 |
| 05 技术栈、环境、依赖、配置、安全、风险 | 已在 `ai/doc-standards/05-tech-spec.md` 覆盖 | 强化矩阵字段和与 `09` 的映射 |
| ADR 取舍与验证 | 部分覆盖 | 建议补最低字段 |
| 技术风险 readiness gate | 部分覆盖 | 作为本提案重点 |
| Mock / 降级状态枚举 | 分散覆盖 | Batch 2 先提出，Batch 6 决定是否独立横切提案 |

## 9. 待人工确认项

| ID | 待确认项 | AI 建议 | 建议依据 | 备选方案 | 取舍影响 / 阻塞关系 |
|---|---|---|---|---|---|
| C-B2-001 | Phase2 前是否先补 `04/05` readiness gate | 建议是 | Phase 升级评估已列真实飞书、PostgreSQL、LLM 等条件 | 进入具体 Sprint 时再补 | 提前补可减少越界风险；延后会让 Sprint 规划依据不足 |
| C-B2-002 | 技术风险矩阵应写在 `05` 还是只写 `09` | 建议 `05` 定义风险，`09` 记录验证证据 | `05` 是技术方案权威源，`09` 是验证记录 | 全部写在 `09` | `09` 集中但技术决策来源不够清晰 |
| C-B2-003 | Mock / 降级状态枚举是否独立成 Batch 6 提案 | 建议等 Batch 5 完成后决定 | 该问题横跨 04/05/09/design | 立即独立提案 | 可能更清晰，但会与 Batch 2 / 5 重复 |

## 10. 下一步

- 已完成：Batch 2 `04-05` 架构与技术方案只读评估。
- 本次配套提案：`_proposals/TEMPLATE-UPGRADE-04-05-architecture-tech-standard.md`。
- 下一 Batch：评估 `docs/06-db-design.md` 与 `docs/07-api-spec.md`，生成 Batch 3 报告和 DB / API 契约规范提案。
