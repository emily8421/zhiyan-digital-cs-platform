# Batch 3 文档评估报告：06-07 数据库与 API 契约

> 定位：本报告是 `docs/06-db-design.md` 与 `docs/07-api-spec.md` 的只读审计与模板提案依据，不替代正式数据库设计或 API 设计修订。
> 评估日期：2026-07-06
> 范围：`docs/06-db-design.md`、`docs/07-api-spec.md`，对照 `ai/doc-standards/06-db-design.md` 与 `ai/doc-standards/07-api-spec.md`。
> 来源 Batch：Batch 0 `docs/research/2026-07-06-template-proposal-audit-batch-0-overall.md`。

## 1. 评估摘要

本次 Batch 3 评估目标，是判断 `06-07` 是否把需求与架构转化为可实现、可验证、可升阶段演进的数据模型与接口契约，并识别可回流到模板的 DB / API 契约规范缺口。

结论：**Conditional Go**。

`06-07` 已能支撑 Phase1 Demo：数据库设计保留目标结构并允许 JSON / SQLite / 内存 Mock 降级，API 设计覆盖 H5、Web 控制台、Mock 业务查询、通知和日报摘要；REQ → 表、REQ → API 追溯基本完整。但若进入 Phase2 / MVP 试点，需要补强“契约状态、字段级约束、迁移 / seed / 回滚、敏感字段、错误 / 权限 / 兼容性矩阵、Demo 草案升为 MVP 契约的门槛”。

最关键判断：

- `docs/06-db-design.md` 已包含 ER 图、表清单、11 张 `zycs_` 表、索引、种子数据、安全留存和 REQ → 表追溯。
- `docs/07-api-spec.md` 已包含统一响应 / 错误结构、API-001~API-012、接口交互图、契约草案、错误码、权限安全、版本演进和 REQ → API 矩阵。
- 当前契约适合 Phase1 Demo，但多处仍是“草案 / Phase1 简化”表达，缺少逐字段必填、默认值、约束、敏感性、兼容性和契约状态标识。
- 数据库目标结构与 Phase1 运行降级之间关系清楚，但缺少“设计目标表 / 当前实现存储 / 迁移状态 / seed 状态”的对照矩阵。
- 模板提案应聚焦 DB / API 的契约状态、Mock / 降级与真实实现的差异标识、升阶段门槛，而不是重复已有表结构 / 接口章节骨架。

## 2. 评估范围与依据

### 2.1 读取文档

| 类型 | 文档 |
|---|---|
| 详细设计 | `docs/06-db-design.md`、`docs/07-api-spec.md` |
| 规范镜像 | `ai/doc-standards/06-db-design.md`、`ai/doc-standards/07-api-spec.md` |
| 上游 / 下游参照 | `docs/02-srs.md`、`docs/03-prd.md`、`docs/04-architecture.md`、`docs/05-tech-spec.md`、`docs/09-verification.md` |
| 项目规则 | `ai/project-rules.md` |

### 2.2 评估口径

| 维度 | 口径 |
|---|---|
| 完整性 | 是否包含数据对象、表清单、字段、索引、迁移、API 清单、契约、错误码、权限和版本 |
| 追溯性 | 每张表、每个 API 是否能追溯到 REQ 或非功能约束 |
| 可实现性 | 设计是否能支持 Phase1 Mock / 降级实现，并为后续 PostgreSQL / API 稳定契约留口 |
| 可验证性 | DB / API 设计是否映射到 TC、资源验证或集成测试 |
| 阶段边界 | 是否把 Demo 草案、Mock、候选、目标结构和已实现能力区分清楚 |
| 安全与合规 | 敏感字段、日志、token、真实客户数据、权限和外部调用是否明确禁用或约束 |
| 模板回流价值 | 是否暴露出通用 DB / API 契约模板缺口 |

## 3. 逐文档评估

### 3.1 `docs/06-db-design.md`

| 项 | 观察 |
|---|---|
| 合规项 | 已说明保留 / 省略决策、上游输入、当前阶段、PostgreSQL + pgvector 目标、Phase1 可 Mock / 本地临时数据降级、`zycs_` 表前缀和 Mock 标识要求。 |
| 数据模型 | 已提供 Mermaid ER 图，覆盖场景包、会话、消息、知识、规则、Mock 业务记录、转人工、知识缺口、通知、日报和审计日志。 |
| 表结构 | 已列出 11 张表和字段；字段包含类型与说明，能支撑 Phase1 Demo 与后续目标结构。 |
| 追溯情况 | REQ-001~REQ-016 均在 REQ → 表追溯中有对应或明确“不适用”。 |
| 规范差异 | 对照 `ai/doc-standards/06-db-design.md`，缺少数据需求概览矩阵、字段级必填 / 默认值 / 约束 / 来源列、迁移工具 / 迁移路径 / 回滚策略、敏感字段与留存矩阵。 |
| 影响 | 不阻塞 Phase1；Phase2 若启用 PostgreSQL 或真实试点数据，需补迁移、seed、敏感字段、删除策略和权限模型。 |

### 3.2 `docs/07-api-spec.md`

| 项 | 观察 |
|---|---|
| 合规项 | 已说明保留 / 省略决策、上游输入、API 前缀、统一响应 / 错误结构、安全约定、API-001~API-012 清单、接口交互图、错误码、权限安全、版本演进和 REQ → API 矩阵。 |
| 契约内容 | API-001 / API-002 给出完整请求响应示例，其余接口多以路径和响应字段摘要表示。 |
| 追溯情况 | REQ-001~REQ-016 均映射到 API 或明确运行验证不适用。 |
| Phase 边界 | 明确 Phase1 不实现生产鉴权，不接真实 token，不真实发送飞书，Phase2 / Phase3 再补登录、权限、真实集成。 |
| 规范差异 | 对照 `ai/doc-standards/07-api-spec.md`，逐接口请求 / 响应 / 错误 / 权限 / 限流 / 兼容性尚未完整展开；API 状态未区分草案、已实现、已验证、Mock、候选。 |
| 影响 | 不阻塞 Phase1；Phase2 若对试点客户开放接口或接真实服务，需补 endpoint 级契约、权限矩阵和兼容策略。 |

## 4. 关键维度核对

| 维度 | 当前状态 | 问题 / 缺口 | 建议 |
|---|---|---|---|
| DB 适用性 | `06` 明确保留，目标 PostgreSQL + pgvector，Phase1 可降级 | 缺设计目标与当前实现存储的状态对照 | 增加“目标表 / 当前实现 / 迁移状态”矩阵 |
| 数据字段 | 字段名、类型、说明完整度较好 | 缺必填、默认值、约束、敏感性、来源 | 模板建议字段级最低列 |
| 迁移与 seed | 有 Phase1 种子数据清单 | 缺迁移工具、路径、回滚、seed 文件定位和验证方式 | 补 migration / seed 标准表 |
| 安全留存 | 已禁止真实客户数据，要求脱敏 | 缺字段级敏感分类、留存 / 删除策略、审计边界 | Phase2 前补敏感字段矩阵 |
| API 契约 | API 清单与关键示例存在 | 多数接口仅字段摘要，缺 endpoint 级完整契约 | 按契约状态逐步补齐 |
| 错误 / 权限 | 有错误码和 Phase1 安全约定 | 缺 endpoint 级错误、权限、限流和审计矩阵 | 模板建议 API contract matrix |
| 版本兼容 | 有 v1 Phase1 / Phase2 / v2 Phase3 | 缺兼容原则、弃用策略、客户端影响 | MVP 前补兼容策略 |
| Mock / 真实边界 | `mock: true`、`send_status: mocked` 明确 | 缺统一 API / DB 契约状态枚举 | Batch 3 提案补状态字段；Batch 6 横切归并 |

## 5. 问题项

| ID | 优先级 | 类型 | 问题 | 位置 | 影响 | 建议修复方式 |
|---|---|---|---|---|---|---|
| B3-001 | P1 | 契约状态缺口 | DB 表与 API 未统一标注“目标设计 / 当前实现 / 已验证 / Mock / 候选 / 后续阶段”状态 | `docs/06-db-design.md`、`docs/07-api-spec.md` | Phase2 可能混淆 Demo 草案与 MVP 契约 | 增加契约状态枚举和矩阵 |
| B3-002 | P1 | DB 规范缺口 | 字段表缺少必填、默认值、约束、敏感性、来源列 | `docs/06-db-design.md` §4 | 真实数据库迁移和安全评审前信息不足 | Phase2 前补字段级契约 |
| B3-003 | P1 | DB 运维缺口 | 迁移与种子数据缺少工具、路径、回滚、验证命令 | `docs/06-db-design.md` §6 | PostgreSQL / pgvector 技术验证时缺入口 | 补 migration / seed matrix |
| B3-004 | P1 | API 契约缺口 | API-003~API-012 多为字段摘要，缺完整请求 / 响应 / 错误 / 权限契约 | `docs/07-api-spec.md` §4 | 试点或前后端并行开发时契约歧义增加 | 按优先级补 endpoint 级契约 |
| B3-005 | P2 | 兼容性缺口 | 版本演进仅列范围，缺兼容原则、弃用策略和客户端影响 | `docs/07-api-spec.md` §7 | 后续 API 变更治理不足 | MVP 前补兼容策略 |
| B3-006 | P2 | 权限 / 限流缺口 | Phase1 简化权限合理，但缺“何时必须补权限矩阵”的门槛 | `docs/07-api-spec.md` §6 | 对试点部署边界不够清晰 | 提案中加入权限矩阵触发条件 |

## 6. 风险项

| ID | 风险 | 是否阻塞 | 说明 |
|---|---|---|---|
| R-B3-001 | 若 Phase2 直接启用 PostgreSQL，而 `06` 不补迁移 / seed / 回滚，会导致环境验证和数据初始化不可复现 | 条件阻塞 | 数据库技术验证 Sprint 前必须补齐 |
| R-B3-002 | 若 API 对试点客户或真实前端团队开放，而 `07` 仍保持字段摘要，会导致契约理解不一致 | 条件阻塞 | 试点接口前需补 endpoint 级契约 |
| R-B3-003 | 若真实数据进入系统但字段敏感性和留存策略未补，会触碰项目禁区 | 阻塞真实数据处理 | 真实客户数据仍禁止，除非另有合规边界确认 |
| R-B3-004 | 若 Mock / Demo 响应未统一状态标识，后续可能把 Mock 数据误当真实数据 | 不阻塞 Phase1 | 模板层面需强化状态字段 |

## 7. 修复建议

### 7.1 项目正式文档修订建议

本报告不直接修改正式文档。建议后续在人工确认 Phase2 后另开修订任务：

1. 在 `docs/06-db-design.md` 增加“数据需求概览”和“目标设计 / 当前实现 / 迁移状态”矩阵。
2. 为 Phase2 可能启用的表补字段级必填、默认值、约束、敏感性、来源和索引说明。
3. 在 `docs/06-db-design.md` 增加迁移工具、迁移路径、seed 文件、回滚策略和验证命令。
4. 在 `docs/07-api-spec.md` 为 Phase2 需要稳定的 endpoint 补请求 / 响应 / 错误 / 权限 / 限流 / 审计契约。
5. 增加 API 兼容原则、弃用策略和客户端影响说明。
6. 同步 `docs/09-verification.md` 的 API / DB 验证用例和资源验证项。

### 7.2 模板提案建议

本 Batch 配套提案：`_proposals/TEMPLATE-UPGRADE-06-07-db-api-contract-standard.md`。

提案重点：

- DB / API 契约状态枚举。
- DB 字段级最低契约列。
- 迁移 / seed / 回滚 / 验证矩阵。
- Endpoint 级 API contract matrix。
- 权限 / 限流 / 兼容性触发条件。
- Demo 草案升为 MVP 契约的门槛。

## 8. 可回流模板优化建议

| 建议 | 是否已有规范覆盖 | Batch 3 提案处理 |
|---|---|---|
| DB 数据需求、概念模型、表清单、字段、索引、迁移、安全、追溯 | 已在 `ai/doc-standards/06-db-design.md` 覆盖 | 强化状态、字段级列和迁移验证 |
| API 统一约定、接口清单、请求响应、错误、权限、版本、追溯 | 已在 `ai/doc-standards/07-api-spec.md` 覆盖 | 强化 endpoint contract matrix 和状态枚举 |
| Demo / Mock / 目标结构区分 | 分散覆盖 | 本提案先定义 DB / API 契约状态，Batch 6 再横切归并 |
| 升阶段契约门槛 | 部分覆盖 | 作为本提案重点 |

## 9. 待人工确认项

| ID | 待确认项 | AI 建议 | 建议依据 | 备选方案 | 取舍影响 / 阻塞关系 |
|---|---|---|---|---|---|
| C-B3-001 | Phase2 前是否需要把 `06` 从目标结构补到可迁移契约 | 建议仅对 Phase2 必用表补齐 | Phase1 可降级，Phase2 是否启用 PostgreSQL 仍待确认 | 一次性补全全部表 | 全部补齐更完整但成本高，且可能提前写死后续字段 |
| C-B3-002 | API-003~API-012 是否全部补 endpoint 级完整契约 | 建议按 Phase2 必用接口优先 | 当前 Phase1 已跑通，试点前才需要稳定契约 | 立即补全全部 API | 减少歧义但会增加维护成本 |
| C-B3-003 | DB / API 契约状态枚举是否独立成模板规范 | 建议是 | Demo 草案与 MVP 契约混淆是多项目通用风险 | 只在本项目报告中记录 | 不回流会导致其他派生项目重复遇到同类问题 |

## 10. 下一步

- 已完成：Batch 3 `06-07` 数据库与 API 契约只读评估。
- 本次配套提案：`_proposals/TEMPLATE-UPGRADE-06-07-db-api-contract-standard.md`。
- 下一 Batch：评估 `docs/08-dev-plan.md` 与 `docs/09-verification.md`，生成 Batch 4 报告和开发计划 / 验证证据规范提案。
