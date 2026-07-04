# 08 Dev Plan（开发计划）

## 0. 文档元信息

| 项 | 内容 |
|---|---|
| 上游输入 | `docs/03-prd.md`、`docs/04-architecture.md`、`docs/05-tech-spec.md`、`docs/06-db-design.md`、`docs/07-api-spec.md` |
| 当前状态 | 草稿，待人工确认 |
| 最后更新 | 2026-07-03 |
| 当前 Phase | Phase1：本机 Demo |

## 1. Phase1 目标

Phase1 只实现本机可运行 Demo，用最小闭环演示知衍数字客服统一平台的核心价值：H5 客户对话、规则 / 知识 / Mock 回答、转人工、知识缺口、Web 控制台、Mock 通知和日报摘要。

进入开发前必须先人工确认 `docs/03-prd.md` §3 阶段路线图、前端框架、存储降级策略、是否启用真实飞书通知、是否启用 LLM。

## 2. Sprint 总览

| Sprint | 名称 | 目标 | 覆盖功能 | 预计修改范围 |
|---|---|---|---|---|
| Sprint-1 | 后端 API 骨架 | 建立 FastAPI 入口、请求响应模型和健康检查。 | F-001、F-009 | `backend/app/api/`、`backend/app/schemas/`、`tests/api/` |
| Sprint-2 | 场景包与 Mock 服务 | 加载场景包、知识 / 规则和 Mock 业务数据。 | F-002、F-003、F-004、F-005 | `backend/app/services/`、`backend/app/data/`、`tests/scenarios/` |
| Sprint-3 | H5 客户对话闭环 | 实现客户 H5 对话页，与后端消息 API 联通。 | F-001、F-002、F-003、F-006 | `frontend/customer-h5/`、`frontend/shared/`、`tests/acceptance/` |
| Sprint-4 | Web 控制台 | 实现会话、待跟进、缺口、通知、摘要基础列表。 | F-006、F-007、F-008 | `frontend/console/`、`frontend/shared/`、`tests/acceptance/` |
| Sprint-5 | 不编造与风险兜底 | 补充高风险规则、缺口流转、审计日志和验收样例。 | F-003、F-006、F-008、F-009 | `backend/app/services/`、`backend/app/data/`、`tests/scenarios/` |
| Sprint-6 | 本机演示与文档回填 | 跑通端到端 Demo，更新验证记录和 README 快速开始。 | F-001~F-009 | `docs/09-verification.md`、`README.md`、`scripts/` |

## 3. Sprint 详情

### Sprint-1：后端 API 骨架

#### 目标

建立后端最小可运行骨架，提供 FastAPI 入口、请求响应模型、健康检查和基础会话 API 壳。

#### 输入文档

- `docs/02-srs.md`：REQ-001、REQ-002、REQ-013、REQ-015、REQ-016
- `docs/04-architecture.md`：组件视图与模块划分
- `docs/07-api-spec.md`：API-001、API-002 的最小壳与统一错误结构

#### 修改范围

- `backend/app/api/`
- `backend/app/schemas/`
- `tests/api/`

#### 验收标准

- 后端可启动并返回健康检查。
- API-001 / API-002 的最小契约可用。
- 统一响应、错误结构和 Mock 标识字段存在。
- 记录本机启动命令、端口和降级假设，供 TC-015 验证。
- Mock 数据均带 `mock: true` 或等价标识。

#### 禁止事项

- 不连接真实 CRM / ERP / OA / 飞书。
- 不新增 LLM 或外部付费 API。
- 不处理真实客户数据。

### Sprint-2：场景包与 Mock 服务

#### 目标

实现产品型 / 项目型场景包加载、知识 / 规则匹配和 Mock 业务数据查询。

#### 输入文档

- `docs/02-srs.md`：REQ-003、REQ-004、REQ-007、REQ-008、REQ-014、REQ-016
- `docs/design/scenario-packs.md`
- `docs/design/knowledge-and-policy.md`
- `docs/design/mock-integrations.md`

#### 修改范围

- `backend/app/services/`
- `backend/app/data/`
- `tests/scenarios/`

#### 验收标准

- API-007 / API-010 / API-011 可用。
- 产品型与项目型场景包 seed 数据可加载。
- Mock 数据均带 `mock: true` 或等价标识。

#### 禁止事项

- 不连接真实 CRM / ERP / OA / 飞书。
- 不新增 LLM 或外部付费 API。
- 不处理真实客户数据。

### Sprint-3：H5 客户对话闭环

#### 目标

实现 H5 对话页，让客户可创建会话、发送问题、看到回答、Mock 标识和转人工说明。

#### 输入文档

- `docs/02-srs.md`：REQ-001、REQ-003、REQ-004、REQ-005、REQ-006、REQ-013、REQ-016
- `docs/03-prd.md`：F-001、F-002、F-003、F-006、F-009
- `docs/07-api-spec.md`：API-001、API-002
- `docs/design/h5-dialog.md`
- `docs/design/frontend-interaction.md`：H5 页面状态、边界文案、接口依赖与验收路径

#### 修改范围

- `frontend/customer-h5/`
- `frontend/shared/`

#### 验收标准

- 可从浏览器打开 H5 页面。
- 至少 6 类样例问题可返回自动回复、Mock 查询或转人工。
- 高风险问题展示不承诺和转人工状态。
- 转人工响应包含原因、状态和可在控制台查看的关联 ID。

#### 禁止事项

- 不做正式登录、支付、客户资料采集。
- 不保存真实联系方式。

### Sprint-4：Web 控制台

#### 目标

实现员工 / 运营控制台基础列表，用于查看会话、待跟进、知识缺口、Mock 通知和日报摘要。

#### 输入文档

- `docs/02-srs.md`：REQ-006、REQ-009、REQ-010、REQ-011、REQ-012、REQ-016
- `docs/03-prd.md`：F-006、F-007、F-008
- `docs/07-api-spec.md`：API-003、API-004、API-005、API-008、API-009、API-012
- `docs/design/web-console.md`
- `docs/design/frontend-interaction.md`：Console 页面状态、列表详情、边界文案与验收路径

#### 修改范围

- `frontend/console/`
- `frontend/shared/`
- `tests/acceptance/`

#### 验收标准

- 控制台可查看会话列表、转人工、缺口、通知、摘要。
- 可更新转人工 / 缺口的 Demo 状态。
- 所有列表明确标明 Mock 或 Demo。

#### 禁止事项

- 不实现生产权限、多租户和真实员工组织数据。

### Sprint-5：不编造与风险兜底

#### 目标

完善高风险规则、知识缺口、审计日志和验收样例，确保系统不会为了演示而编造事实。

#### 输入文档

- `docs/02-srs.md`：REQ-005、REQ-006、REQ-009、REQ-011、REQ-012、REQ-016
- `docs/design/knowledge-and-policy.md`
- `docs/decisions/ADR-0004-no-fabrication-and-human-handoff.md`

#### 修改范围

- `backend/app/services/`
- `backend/app/data/`
- `tests/scenarios/`
- `tests/acceptance/`

#### 验收标准

- 无依据问题生成知识缺口。
- 高风险问题生成转人工，不返回承诺性答案。
- 审计日志不包含真实敏感信息。

#### 禁止事项

- 不用随机生成内容冒充业务事实。
- 不把未确认规则写成客户承诺。

### Sprint-6：本机演示与文档回填

#### 目标

跑通端到端 Demo，补充验证记录、运行说明和未确认风险。

#### 输入文档

- `docs/09-verification.md`
- `README.md`
- `docs/env/local-env.md`

#### 修改范围

- `README.md`
- `docs/09-verification.md`
- `scripts/`（如需启动脚本，需另行确认）

#### 验收标准

- 本机能启动后端、H5、控制台。
- 完成 TC-001~TC-016 验证记录。
- 覆盖 REQ-015 的本机运行验证和资源记录。
- README 快速开始可复现 Demo。

#### 禁止事项

- 不为通过演示而打开真实外部服务。

## 4. 任务拆分规则

- 一个 Sprint 如超过 1~3 个模块，应拆分 `tasks/task-00X-*.md`。
- 每个任务只覆盖一组 REQ，不跨越多个独立功能。
- 执行任务前必须读取对应 `docs/`、`docs/design/` 和任务单。
- 修改文档、引入依赖、运行写入命令前仍需遵守项目确认规则。

## 5. 依赖与里程碑

| 里程碑 | 前置条件 | 输出 |
|---|---|---|
| M1 文档确认 | `docs/00-09` 与设计 / 决策审计通过 | 允许进入 Sprint-1 |
| M2 后端 API 可用 | Sprint-1 完成 | API 壳与契约可验证 |
| M3 场景与 Mock 可用 | Sprint-2 完成 | H5 与控制台可集成业务数据 |
| M4 H5 闭环 | Sprint-3 完成 | 可演示客户侧体验 |
| M5 控制台闭环 | Sprint-4 完成 | 可演示员工侧运营 |
| M6 风险兜底 | Sprint-5 完成 | 可演示不编造和转人工 |
| M7 Demo 验收 | Sprint-6 完成 | Phase1 可对外演示 |

## 6. 当前进度记录

| 日期 | 进度 | 说明 |
|---|---|---|
| 2026-07-03 | 文档补齐中 | 生成 `docs/00-09`、`docs/design/*`、`docs/decisions/*` 草稿。 |

## 7. 待人工确认

- 是否按 Sprint-1 开始后端 API 骨架。
- 是否允许安装 / 使用前后端依赖。
- Phase1 存储采用哪种降级方式。
- 是否需要拆分 Sprint-1 为正式 `tasks/task-001-backend-skeleton.md`。
