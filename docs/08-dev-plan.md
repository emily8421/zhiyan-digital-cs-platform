# 08 Dev Plan（开发计划）

## 0. 文档元信息

| 项 | 内容 |
|---|---|
| 上游输入 | `docs/03-prd.md`、`docs/04-architecture.md`、`docs/05-tech-spec.md`、`docs/06-db-design.md`、`docs/07-api-spec.md` |
| 当前状态 | Phase1 Sprint-1~6 已完成并通过本机 Demo 验收；Phase2 MVP 验收通过（M10，2026-07-11）；Sprint-7/8/9 全部完成；RG-001/RG-002 Go、RG-003 Conditional Go；TC-017~052 通过，见 §2/§3 |
| 最后更新 | 2026-07-11 |
| 当前 Phase | Phase2：MVP 试点 |

## 1. Phase1 目标

Phase1 只实现本机可运行 Demo，用最小闭环演示知衍数字客服统一平台的核心价值：H5 客户对话、规则 / 知识 / Mock 回答、转人工、知识缺口、Web 控制台、Mock 通知和日报摘要。

开发按已确认口径推进：Phase1 本机 Demo；前端采用 React + Vite + TypeScript；存储优先 JSON / SQLite / 内存 Mock；飞书仅 Mock payload；LLM 默认关闭。每个 Sprint 开始前仍需确认本次修改范围。

## 2. Sprint 总览

| Sprint | 名称 | 目标 | 覆盖功能 | 预计修改范围 | 状态 |
|---|---|---|---|---|---|
| Sprint-1 | 后端 API 骨架 | 建立 FastAPI 入口、请求响应模型和健康检查。 | F-001、F-009 | `backend/app/api/`、`backend/app/schemas/`、`tests/api/` | 已完成 |
| Sprint-2 | 场景包与 Mock 服务 | 加载场景包、知识 / 规则和 Mock 业务数据。 | F-002、F-003、F-004、F-005 | `backend/app/services/`、`backend/app/data/`、`tests/scenarios/` | 已完成 |
| Sprint-3 | H5 客户对话闭环 | 实现客户 H5 对话页，与后端消息 API 联通。 | F-001、F-002、F-003、F-006 | `frontend/customer-h5/`、`frontend/shared/`、`tests/acceptance/` | 已完成 |
| Sprint-4 | Web 控制台 | 实现会话、待跟进、缺口、通知、摘要基础列表。 | F-006、F-007、F-008 | `frontend/console/`、`frontend/shared/`、`tests/acceptance/` | 已完成 |
| Sprint-5 | 不编造与风险兜底 | 补充高风险规则、缺口流转、审计日志和验收样例。 | F-003、F-006、F-008、F-009 | `backend/app/services/`、`backend/app/data/`、`tests/scenarios/` | 已完成 |
| Sprint-6 | 本机演示与文档回填 | 跑通端到端 Demo，更新验证记录和 README 快速开始。 | F-001~F-009 | `docs/09-verification.md`、`README.md`、`scripts/` | 已通过验收 |
| Sprint-7 | 试点部署与运营配置（Phase2） | 单个试点客户部署、运营流程、基础权限 / 角色可见性。 | F-007、F-008 | `backend/`、`frontend/console/`、`docs/env/` | 已完成（PR #34，2026-07-10） |
| Sprint-8 | 飞书沙箱联调 + DB 技术验证（Phase2） | 飞书通知沙箱 / 试点评估（不接真实组织数据）；PostgreSQL/pgvector 技术验证。 | F-006、F-010 | `backend/app/adapters/`、`backend/app/services/`、`docker/`、`docs/research/`、`tasks/` | 已完成（2026-07-11，RG-001 / RG-002 Go，TC-021~046） |
| Sprint-9 | 知识运营强化 + LLM 评估（Phase2） | 知识缺口流转 / 审核强化、运营配置；LLM 专项评估（不默认启用）。 | F-008、F-011 | `backend/app/services/`、`docs/research/` | LLM 评估已完成（Conditional Go，2026-07-11）；知识运营强化已完成（2026-07-11，缺口 accepted 入库 + API-006，TC-050~052 通过） |

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
- 不把未纳入 Phase1 的规则或能力写成客户承诺。

### Sprint-6：本机演示与文档回填

#### 目标

跑通端到端 Demo，补充验证记录、运行说明和已知风险。

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

### Sprint-7：试点部署与运营配置（Phase2）

> 状态：已细化（2026-07-10）。业务输入已确认：单实例双场景包（古晶产品型 + 乐式项目型，不做多租户）、本机演示优先部署、权限最小集（管理员可写 / 其余只读）。

#### 目标

在 Phase1 本机 Demo 基础上，完成 Phase2 单个试点客户的 MVP 部署、运营流程与基础权限 / 角色可见性。试点形态为**单实例 + 双场景包**：同一本机实例同时承载古晶（产品型，签约目标）与乐式（项目型，数据 / 验证来源）两个场景包做演示，验证「统一架构 + 场景包可复制」核心假设；**不做多租户、不做客户级数据隔离**（Phase4）。

#### 输入文档

- `docs/03-prd.md` Phase2（F-007 / F-008）、`docs/04-architecture.md`、`docs/05-tech-spec.md` §12 Phase 技术约束、§14 Readiness Gate
- `docs/design/web-console.md`（WC-C-001 后端权限补齐口径）、`docs/design/frontend-interaction.md`（Console 页面状态 / 运营入口）
- 关联 REQ：REQ-010、REQ-011、REQ-012（F-007 / F-008）；权限部分 REQ-016

#### 修改范围

- `backend/`：权限 / 角色可见性最小集（控制台写操作后端按角色放行，管理员可写、其余只读；对应 WC-C-001）。
- `frontend/console/`：运营配置入口（当前演示场景包选择 / 切换、双场景包数据查看）。
- `docs/env/`：试点部署预案（本机演示优先；端口 8000 / 5173 / 5174；Mock / 降级保留）。

#### 验收标准与验证包

- 单实例双场景包主链路跑通（TC-017）。
- 基础权限 / 角色可见性由后端执行，不依赖前端隐藏（TC-018）。
- 运营配置入口可用，双场景包可切换 / 查看（TC-019）。
- 本机试点部署预案可复现（TC-020）；Mock / 降级路径保留。
- 验证包：后端 `pytest tests/api tests/scenarios tests/acceptance`；前端 `npm run build`（customer-h5 / console）；本机三端部署手工验收。

#### 禁止事项

- 不接真实 CRM/ERP/OA/工单（Phase3）。
- 不实现多租户 / 计费 / 客户级数据隔离（Phase4）。
- 不处理真实客户隐私 / 生产会话。
- 不引入新依赖、Docker 镜像、外部 SaaS API 或付费服务（需先人工确认）。

### Sprint-8：飞书沙箱联调 + DB 技术验证（Phase2）

#### 目标

将飞书通知从 Mock payload 推进到沙箱 / 试点评估（DOC-C-003，不接真实组织数据）；完成 PostgreSQL / pgvector 技术验证（DOC-C-004，不作全部功能前置）。

> 2026-07-10 已拆出并完成 Sprint-8A「DB 持久化基础设施」：仅搭建 PostgreSQL + pgvector 本机数据库地基，不把后端业务逻辑切到数据库；详见 `tasks/task-008a-db-foundation.md` 与 `docs/env/postgres-pgvector-runbook.md`。
> 2026-07-10 已拆出并完成 Sprint-8B「静态数据读库」：场景包、知识、规则、Mock 业务记录可在显式启用后从 PostgreSQL 读取，并保留 JSON 降级；详见 `tasks/task-008b-static-data-postgres.md`。
> 2026-07-10 已拆出并完成 Sprint-8C-A「会话与消息持久化」：新建会话、客户消息和助手回答可在显式启用后写入 PostgreSQL，并保留内存降级；详见 `tasks/task-008c-a-conversation-message-postgres.md`。
> 2026-07-10 已拆出并完成 Sprint-8C-B「运营数据持久化（转人工 / 知识缺口）」：高风险转人工与无依据知识缺口可在显式启用后写入 PostgreSQL，并保留内存降级；通知、日报和审计日志仍后置。详见 `tasks/task-008c-b-operational-data-postgres.md`。
> 2026-07-10 已拆出并完成 Sprint-8D「飞书沙箱启动前评估」：已明确出站通知凭据清单、默认 Mock / 显式 sandbox / 失败降级、回调后置边界；2026-07-11 TC-039 沙箱实发通过，RG-001 出站通知沙箱 Go。详见 `tasks/task-008d-feishu-sandbox-readiness.md` 与 `docs/research/2026-07-10-tech-env-evaluation-feishu-sandbox.md`。
> 2026-07-10 已拆出并完成 Sprint-8E「Feishu 通知适配器骨架」：默认 Mock、显式 sandbox、缺配置 / 发送失败降级，不提交真实凭据、不启用事件回调；2026-07-11 TC-039 沙箱实发通过。详见 `tasks/task-008e-feishu-notification-adapter.md`。
> 2026-07-10 已拆出并完成 Sprint-8F「通知记录持久化」：API-009 创建的通知记录可在显式启用后写入 PostgreSQL，并保留内存降级；日报和审计日志仍后置。详见 `tasks/task-008f-notification-postgres.md`。
> 2026-07-11 Sprint-8 阶段性收尾：RG-001 飞书出站通知沙箱 Go，RG-002 PostgreSQL/pgvector Go；DB 可选持久化已覆盖静态数据、会话、消息、转人工、知识缺口、通知记录。后置项明确为日报持久化、审计日志 PG 化、飞书事件回调、真实生产群 / 生产组织数据、LLM RG-003。

#### 输入文档

- `docs/05-tech-spec.md` §13 技术风险、§14 Readiness Gate（对应 doc-standards §8/§9）
- `docs/design/mock-integrations.md`、`docs/06-db-design.md`

#### 修改范围

- `backend/app/adapters/`（飞书适配沙箱）
- `docker/`（PostgreSQL/pgvector 编排，待 Docker 可用）
- `docs/research/*tech-env-evaluation*.md`（技术环境评估）
- `tasks/task-008a-db-foundation.md`、`docker/docker-compose.pgvector.yml`、`docker/postgres/init/*.sql`、`docs/env/postgres-pgvector-runbook.md`（Sprint-8A DB 地基，已完成）
- `tasks/task-008b-static-data-postgres.md`、`backend/app/services/static_data_source.py`、`backend/app/services/postgres_static_data_repository.py`、`backend/app/services/scenario_pack_service.py`（Sprint-8B 静态数据读库，已完成）
- `tasks/task-008c-a-conversation-message-postgres.md`、`backend/app/services/conversation_store.py`、`backend/app/services/conversation_service.py`（Sprint-8C-A 会话与消息持久化，已完成）
- `tasks/task-008c-b-operational-data-postgres.md`、`backend/app/services/console_store.py`、`backend/app/services/console_service.py`（Sprint-8C-B 转人工 / 知识缺口持久化，已完成）
- `tasks/task-008d-feishu-sandbox-readiness.md`、`docs/research/2026-07-10-tech-env-evaluation-feishu-sandbox.md`（Sprint-8D 飞书沙箱启动前评估，已完成）
- `tasks/task-008e-feishu-notification-adapter.md`、`backend/app/adapters/feishu_notification_adapter.py`、`backend/app/services/console_service.py`（Sprint-8E Feishu 通知适配器骨架，已完成）
- `tasks/task-008f-notification-postgres.md`、`backend/app/services/console_store.py`、`backend/app/services/console_service.py`（Sprint-8F 通知记录持久化，已完成）

#### 验收标准

- 飞书沙箱联调通过，真实组织数据默认不接入。
- PostgreSQL/pgvector 技术验证有 Go / Conditional Go 结论。
- Sprint-8A DB 地基可本机启动，pgvector 扩展、11 张 `zycs_` 表与 Demo seed 数据可验证；不等同于业务已启用 PG。
- Sprint-8B 静态数据读库可在环境变量显式启用后读取 PostgreSQL seed，并在未配置 / 不可用时回退 JSON。
- Sprint-8C-A 会话与消息可在环境变量显式启用后写入 PostgreSQL，并在未配置 / 不可用时回退内存；不等同于转人工 / 缺口 / 通知 / 日报已持久化。
- Sprint-8C-B 转人工与知识缺口可在环境变量显式启用后写入 PostgreSQL，并在未配置 / 不可用时回退内存；不等同于通知 / 日报 / 审计日志已持久化。
- Sprint-8D / 8E 飞书出站通知沙箱已通过 TC-039：默认 Mock 保留，显式 sandbox 可实发到测试群；事件回调、真实生产群和生产组织数据仍后置。
- Sprint-8F 通知记录可在环境变量显式启用后写入 PostgreSQL，并在未配置 / 不可用时回退内存；不等同于日报 / 审计日志已持久化。
- 不真实发送未经授权的通知。

#### 禁止事项

- 不默认接入真实飞书组织数据。
- 不把 DB 技术验证成功等同于功能已启用。
- 不把 RG-001 出站通知沙箱 Go 等同于真实生产飞书集成；不得启用事件回调，不得接真实生产群或生产组织数据。

### Sprint-9：知识运营强化 + LLM 评估（Phase2）

#### 目标

强化知识缺口流转 / 审核、运营配置；完成 LLM 专项评估（DOC-C-005，仅评估，不默认启用自动答复）。

#### 输入文档

- `docs/design/knowledge-and-policy.md`、`docs/decisions/ADR-0004-no-fabrication-and-human-handoff.md`
- `docs/05-tech-spec.md` §14 Readiness Gate（LLM，对应 doc-standards §9）

#### 修改范围

- `backend/app/services/`（缺口流转 / 审核）
- `docs/research/`（LLM 专项评估报告）

#### 验收标准

- 知识缺口流转 / 审核流程可用。
- LLM 专项评估输出证据约束 / 不编造 / 成本 / 兜底结论。
- LLM 默认仍关闭。

#### 禁止事项

- 不默认启用 LLM 自动答复。
- 不把 LLM 评估结论等同于已启用。

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
| M8 试点部署 | Sprint-7 完成 | 单个试点客户可部署 |
| M9 技术验证 | Sprint-8 完成 | 飞书沙箱 + DB 技术验证结论 |
| M10 Phase2 MVP 验收 | Sprint-9 完成 | 试点客户可用，运营流程跑通 |

## 6. 当前进度记录

| 日期 | 进度 | 说明 |
|---|---|---|
| 2026-07-03 | 文档补齐中 | 生成 `docs/00-09`、`docs/design/*`、`docs/decisions/*` 草稿。 |
| 2026-07-06 | Phase1 Sprint-1~Sprint-6 已完成 | 后端 API 测试 `19 passed`；H5 / Console build 通过；HTTP 场景验证 TC-001~TC-016 全部通过；三端本机运行端口 `8000` / `5173` / `5174` 可访问，详见 `docs/09-verification.md` §6。 |
| 2026-07-06 | Phase2 规划待人工确认 | `docs/research/2026-07-06-phase-upgrade-evaluation.md` 结论为 Conditional Go，是否进入 Phase2 / MVP 试点规划仍待人工确认。 |
| 2026-07-09 | Phase2 Conditional Go 已确认 | DOC-C-001~C-005 全按 AI 推荐；新增 Phase2 Sprint-7/8/9 草案与 M8~M10 里程碑。 |
| 2026-07-10 | Sprint-7 已完成并通过验收 | 单实例双场景包（古晶产品型 + 乐式项目型）部署、控制台角色权限最小集（WC-C-001，Demo 级 `X-Console-Role`）、运营配置入口（角色切换 + 场景包过滤）、试点部署预案；后端 `30 passed`、两端 build 通过、TC-017~020 手工验收通过。PR #34 已合并。 |
| 2026-07-10 | Sprint-8A DB 地基已完成 | 新增 PostgreSQL + pgvector Compose、本机 schema / seed 初始化和运行手册；验证通过：Compose config、容器 healthy、pgvector `0.8.0`、11 张 `zycs_` 表、2 个场景包 seed、5 条 Mock 业务记录。后端业务尚未切 PG，Mock / 本地临时数据链路保留。 |
| 2026-07-10 | Sprint-8B 静态数据读库已完成 | 新增 `psycopg[binary]`、静态数据源开关和 PostgreSQL 静态读取仓库；默认 JSON，`ZYCS_STATIC_DATA_SOURCE=postgres` 时优先读 PG，失败回退 JSON；PG 模式 `tests/api/test_static_data_source.py` 3 passed，默认全量后端 33 passed、1 skipped。后续会话 / 消息 / 转人工 / 缺口 / 通知已由 Sprint-8C-A/B/F 分步闭环，日报仍后置。 |
| 2026-07-10 | Sprint-8C-A 会话与消息持久化已完成 | 新增会话存储开关和 PostgreSQL 会话 / 消息仓库；默认内存，`ZYCS_CONVERSATION_STORE=postgres` 时写入 PG，失败回退内存；PG 模式 `tests/api/test_conversation_store.py` 4 passed，默认全量后端 35 passed、3 skipped。后续转人工 / 知识缺口 / 通知已由 Sprint-8C-B/F 分步闭环，日报仍后置。 |
| 2026-07-10 | Sprint-8C-B / 8F 运营数据持久化已完成 | 转人工、知识缺口、通知记录可在 `ZYCS_CONVERSATION_STORE=postgres` 时写入 PostgreSQL，失败回退内存；PG 专项分别覆盖转人工 / 缺口与通知记录，默认全量后端回归通过。日报和审计日志仍后置。 |
| 2026-07-11 | Sprint-8D / 8E 飞书出站通知沙箱已通过 | 完成 RG-001 启动前评估、默认 Mock / 显式 sandbox 适配器骨架和 TC-039 沙箱实发；飞书测试群已收到通知，默认 Mock 保留，事件回调、真实生产群和生产组织数据后置。 |
| 2026-07-11 | Sprint-8 阶段性完成 | RG-001（飞书出站通知沙箱）Go，RG-002（PostgreSQL/pgvector）Go；TC-021~046 已通过或完成记录，Sprint-8 可作为 Phase2 技术验证闭环进入 Sprint-9 前置评估。 |
| 2026-07-11 | RG-003 LLM 专项评估完成 | 完成 LLM 证据约束 / 不编造 / 成本 / 兜底评估，结论 Conditional Go；RG-003 从「待评估」推进，LLM 默认仍关闭，真实接入后置 Phase3 / 授权任务；新增 RISK-P2-007~010（候选 / 未启用）、TC-047~049。见 `docs/research/2026-07-11-tech-env-evaluation-llm.md`。 |
| 2026-07-11 | Sprint-9 知识运营强化完成 | 知识缺口 `accepted` 自动入库为 `draft` 知识条目（`zycs_knowledge_items`）；新增 API-006 `GET/POST /knowledge-items`（写操作需 admin）；内存默认 + PG 可选持久化。TC-050~052 通过；默认全量 48 passed、5 skipped，PG 专项 11 passed。见 `tasks/task-009b-knowledge-items-and-gap-acceptance.md`。 |
| 2026-07-11 | M10 Phase2 MVP 验收通过 | Phase2 Sprint-7/8/9 全部完成；TC-017~052 通过；RG-001/RG-002 Go、RG-003 Conditional Go；默认全量 48 passed、6 skipped，PG 专项 11 passed；试点客户主链路可用，真实 CRM/ERP/OA/工单/LLM 未解锁（后置 Phase3）。见 `docs/09-verification.md` §10.15。 |
| 2026-07-11 | 知识闭环完成（task-009c） | 知识条目 `PATCH` 转正（draft→active→archived，需 admin）；`active` 知识进入问答检索链路（与 seed 统一评分）；draft/archived 不参与。TC-053/054 通过；默认全量 54 passed、6 skipped，PG 专项 11 passed。见 `tasks/task-009c-knowledge-item-active-retrieval.md`。 |
| 2026-07-11 | 前端知识条目管理页完成（task-009d） | Console 新增「知识条目」Tab（独立）：列表（active/draft/archived 颜色区分）、转正（draft→active）、归档、新增表单（admin）；viewer 只读；接 API-006 GET/POST/PATCH。`npm run build` 通过，TC-055 人工浏览器验收暂未发现问题。见 `tasks/task-009d-console-knowledge-tab.md`。 |
| 2026-07-11 | Phase3 升级评估完成 | 结论：Conditional Go（仅进入 Phase3 准备规划）+ No-Go（暂不解锁真实 CRM/ERP/OA/工单/LLM 实施接入）。Phase3 真实实施仍需试点客户接口与授权、安全评审、沙箱 / 测试账号、字段映射和验收场景。见 `docs/research/2026-07-11-phase3-upgrade-evaluation.md` 与 `docs/09-verification.md` §10.18。 |
| 2026-07-11 | Phase3 准备材料已补 | 新增真实集成接口问卷与安全 / 数据边界评审清单，明确客户 / IT / 安全需提供系统清单、接口文档、授权范围、沙箱 / 测试账号、字段映射、验收场景和凭据 / 日志 / LLM 红线。见 `docs/research/2026-07-11-phase3-integration-questionnaire.md`、`docs/research/2026-07-11-phase3-security-data-boundary-review.md` 与 `docs/09-verification.md` §10.19。 |
| 2026-07-11 | Phase3 适配层契约设计已补 | 新增 `docs/design/integration-adapters.md`，定义 ExternalBusinessAdapter、运行模式（disabled / mock / sandbox / production_readonly）、统一查询结果、错误降级、字段脱敏、日志审计和 RG-004~RG-008 对应关系；仅设计 Mock / sandbox 骨架，不接真实系统。见 `docs/09-verification.md` §10.20。 |

## 7. 已确认口径与待执行

- Phase1 Sprint-1~Sprint-6 已完成并通过本机 Demo 验收；后续不再从 Sprint-1 重新开始。
- Phase2 Conditional Go 已确认（2026-07-09，DOC-C-001~C-005）；Sprint-7 与 Sprint-8 已阶段性完成，Sprint-9 启动前仍需确认本次修改范围。
- Phase2 存储优先继续 JSON / SQLite / 内存 Mock 降级；PostgreSQL / pgvector 已完成 Sprint-8 技术验证与可选持久化，不作全部功能前置（DOC-C-004）。
- 飞书通知 Phase2 已完成出站通知沙箱验证，不默认接真实组织数据；事件回调、真实生产群和生产组织数据后置（DOC-C-003）；LLM 仅评估，不默认启用（DOC-C-005）。
- Phase3 升级评估已完成（2026-07-11）：仅建议进入 Phase3 准备规划，不解锁真实外部系统或真实 LLM 接入；下一步优先真实集成接口问卷 + 安全与数据边界评审。
- Phase3 真实集成接口问卷 + 安全与数据边界评审清单已落盘；客户 / IT / 安全负责人填写并确认前，真实集成实施仍为 No-Go。
- Phase3 外部系统适配层契约已落盘；后续若进入编码，必须先只实现抽象 / Disabled / Mock 包装和 sandbox 骨架，不改变现有 API 行为、不调用真实生产接口。
