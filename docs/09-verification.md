# 09 Verification（验证计划）

## 0. 文档元信息

| 项 | 内容 |
|---|---|
| 上游输入 | `docs/02-srs.md`、`docs/03-prd.md`、`docs/08-dev-plan.md` |
| 当前状态 | Phase1 已通过验收；Phase2 MVP 验收通过（M10，2026-07-11）；Sprint-7/8/9 全部完成；RG-001 飞书出站通知沙箱 Go、RG-002 PostgreSQL/pgvector Go、RG-003 LLM Conditional Go；TC-017~052 通过，见 §6 / §10.2 / §10.4~§10.15 |
| 最后更新 | 2026-07-11 |
| 当前 Phase | Phase2：MVP 试点 |

## 1. 验证策略

Phase1 采用“接口验证 + 场景样例 + 手工端到端演示”的组合方式。由于当前不接真实外部系统，所有订单、项目、售后、飞书通知和业务数据验证均以 Mock 数据为准，并必须明确标识 Mock。

验证优先级：

1. P0：H5 对话、意图路由、知识 / 规则回答、不编造、转人工。
2. P1：场景包切换、Mock 进度查询、Web 控制台、知识缺口、日报摘要。
3. P2：本机资源、日志脱敏、外部集成默认关闭。

## 2. REQ 到用例矩阵

| REQ-ID | 用例 | 类型 | 阶段 |
|---|---|---|---|
| REQ-001 | TC-001 | 手工 + API | Phase1 |
| REQ-002 | TC-002 | API | Phase1 |
| REQ-003 | TC-003 | 场景样例 | Phase1 |
| REQ-004 | TC-004 | 场景样例 | Phase1 |
| REQ-005 | TC-005 | 场景样例 | Phase1 |
| REQ-006 | TC-006 | API + 控制台 | Phase1 |
| REQ-007 | TC-007 | 配置 / 场景 | Phase1 |
| REQ-008 | TC-008 | API + 场景 | Phase1 Mock |
| REQ-009 | TC-009 | API + 日志 | Phase1 Mock |
| REQ-010 | TC-010 | 手工 | Phase1 |
| REQ-011 | TC-011 | API + 控制台 | Phase1 |
| REQ-012 | TC-012 | API + 手工 | Phase1 |
| REQ-013 | TC-013 | API 契约 | Phase1 |
| REQ-014 | TC-014 | 配置 / 数据 | Phase1 |
| REQ-015 | TC-015 | 本机运行 | Phase1 |
| REQ-016 | TC-016 | 安全检查 | Phase1 |

## 3. 用例详情

### TC-001 H5 创建会话并发送消息

- 依据：`docs/design/h5-dialog.md`、`docs/design/frontend-interaction.md`。
- 前置：后端与 H5 启动。
- 步骤：打开 H5，选择产品型场景包，发送产品参数问题。
- 期望：页面展示回答、来源类型、会话 ID，且没有真实客户数据。

### TC-002 会话状态保持

- 前置：已有会话。
- 步骤：连续发送 2 条消息，通过 API 查询会话列表。
- 期望：会话状态、消息数量、更新时间正确。

### TC-003 意图识别与路由

- 样例：产品咨询、项目咨询、订单进度、项目进度、售后规则、投诉 / 高风险、未知问题。
- 期望：每类问题进入正确流程，未知问题不误答。

### TC-004 知识 / 规则回答

- 步骤：输入命中知识库和规则库的问题。
- 期望：回答包含 `answer_type` 和 `source_ref`。

### TC-005 不编造与高风险保护

- 依据：`docs/design/knowledge-and-policy.md`、`docs/design/frontend-interaction.md`。
- 步骤：输入赔付承诺、合同责任、真实交期承诺或无来源事实问题。
- 期望：系统不承诺，生成转人工或知识缺口。

### TC-006 转人工流转

- 依据：`docs/design/web-console.md`、`docs/design/frontend-interaction.md`。
- 步骤：触发高风险问题，在控制台查看并更新转人工状态。
- 期望：转人工记录包含原因、状态、建议负责人、来源会话。

### TC-007 场景包切换

- 步骤：分别使用产品型和项目型场景包发送问题。
- 期望：不同场景包加载不同知识、规则和 Mock 数据。

### TC-008 Mock 进度查询

- 依据：`docs/design/mock-integrations.md`、`docs/design/frontend-interaction.md`。
- 步骤：查询样例订单号、项目号、售后单号。
- 期望：返回 Mock 状态、下一步、更新时间，并标明 `mock: true`。

### TC-009 Mock 通知

- 步骤：触发转人工和知识缺口，调用或查看通知记录。
- 期望：通知 payload 被记录，状态为 `mocked`，不真实发送。

### TC-010 Web 控制台查看运营列表

- 依据：`docs/design/web-console.md`、`docs/design/frontend-interaction.md`。
- 步骤：打开控制台，查看会话、待跟进、缺口、通知、摘要。
- 期望：列表数据完整，Mock / Demo 标识明确。

### TC-011 知识缺口生命周期

- 依据：`docs/design/knowledge-and-policy.md`、`docs/design/frontend-interaction.md`。
- 步骤：触发未知问题，在控制台更新缺口状态。
- 期望：缺口从 `new` 更新到 `reviewing` 或关闭状态。

### TC-012 日报摘要

- 依据：`docs/design/web-console.md`、`docs/design/frontend-interaction.md`。
- 步骤：完成多轮会话后查看日报摘要。
- 期望：摘要包含会话数、转人工数、缺口数、未结案数。

### TC-013 API 契约

- 步骤：按 `docs/07-api-spec.md` 调用 API-001~API-012。
- 期望：响应结构、错误结构和 Mock 标识符合契约。

### TC-014 配置与 Mock 数据可替换

- 步骤：替换或新增一个场景包样例数据。
- 期望：不改业务逻辑即可被 API 读取。

### TC-015 本机运行验证

- 步骤：按 README 启动后端、H5、控制台。
- 期望：在当前 Windows 本机可完成端到端演示；Docker 不可用时降级路径可用。

### TC-016 安全与隐私检查

- 步骤：检查日志、Mock 数据、响应和文档样例。
- 期望：无 token、真实联系方式、真实订单、真实合同和真实客户隐私。

## 4. 本机资源验证

| 验证项 | 方法 | 通过标准 | 当前状态 |
|---|---|---|---|
| Python 后端 | 启动 FastAPI | 服务可访问健康检查；端口 `8000` | 已通过（2026-07-06，约 54.3 MB 工作集） |
| Node 前端 | 启动 H5 / Console | 浏览器可打开页面；H5 端口 `5173`，Console 端口 `5174` | 已通过（2026-07-06，约 8.7 MB / 8.6 MB 工作集） |
| 内存 | 观察 Demo 运行占用 | 以当前本机约 31.73 GB 内存可完成 H5 + 后端 + 控制台 + Mock 数据演示为准 | 已通过；三端合计约 71.6 MB 工作集，不含浏览器进程 |
| 显存 / GPU | 检查是否依赖 GPU | Phase1 不依赖 GPU；本机未检测到 GPU 信息 | 已确认不依赖 GPU |
| 磁盘 | 检查依赖、Mock 数据和日志占用 | 控制在本机 Demo 所需最小范围；不得写入真实生产数据 | 已通过；仅使用已有 `node_modules`、构建产物与 Mock 数据，未写入生产数据 |
| Docker | 检查 Docker 服务 | 可选；不可用时走降级 | 当前记录为不可用 |
| PostgreSQL / pgvector | 启动或连接本地服务 | 可选；Phase1 已确认可降级为 JSON / SQLite / 内存 Mock | 可选 |
| Mock 数据 | 加载场景包和样例记录 | 两类场景包均可用 | 已通过；`product_business` / `project_business` 均可读取 |
| 外部网络 | 飞书 / LLM 等 | 默认不需要，真实调用需人工确认 | 默认关闭 |

## 5. 阶段验收清单

| 验收项 | 对应 AC | 状态 |
|---|---|---|
| H5 完成 6 类样例问答 / 转人工 | AC-001 | 已通过（API 场景验证覆盖知识、Mock、转人工、缺口） |
| 产品型与项目型场景包可切换 | AC-002 | 已通过 |
| Mock 进度查询不接真实系统 | AC-003 | 已通过 |
| 高风险 / 无依据不编造 | AC-004 | 已通过 |
| Web 控制台展示运营列表 | AC-005 | 已通过 |
| 日志和样例数据不含敏感信息 | AC-006 | 已通过（样例响应检查未发现 token / 真实联系方式 / 真实订单合同隐私） |
| 文档链路可追溯 | AC-007 | 已回梳，人工已接受 |

## 6. 验收记录

| 日期 | 范围 | 结果 | 备注 |
|---|---|---|---|
| 2026-07-04 | 同步后文档体系回梳 | 已回梳，人工已接受 | 补齐 04 / 06 / 07 与 `docs/design/*` Mermaid 图表；统一 03 / 09 审计状态。 |
| 2026-07-06 | Sprint-6 本机演示与文档回填 | 已通过 | 后端 API 测试 `19 passed`；H5 / Console build 通过；HTTP 场景验证 TC-001~TC-016 全部通过；三端本机运行端口 `8000` / `5173` / `5174` 可访问。 |
| 2026-07-10 | Sprint-7 试点部署与运营配置 | 已通过 | 后端 `30 passed`（含 5 权限用例）；console / customer-h5 build 通过；本机三端 4/4 reachable；TC-017 双场景包主链路、TC-018 后端角色权限（403 / 200）、TC-019 控制台运营配置入口、TC-020 本机部署预案均通过（PR #34）。 |

## 7. 自动化与手工验证建议

- Sprint-1 优先补 API 测试：创建会话、发送消息、Mock 查询、场景包列表。
- Sprint-2 / Sprint-3 补最小前端手工验收清单，不强制引入 E2E 框架。
- Sprint-4 补场景样例测试，尤其是高风险与未知问题。
- Sprint-5 汇总验证记录，回填本文件状态。
- Sprint-6 已完成本机 Demo 验证，后续若新增真实集成或自动化 E2E，再补对应测试层级。

## 8. 未验证风险

- Docker / PostgreSQL / pgvector 当前未验证可用。
- React + Vite + TypeScript 构建已验证；沙箱内 Vite 会因 `spawn EPERM` 失败，非沙箱本机运行通过。
- Python 3.14.3 与当前 FastAPI 测试通过；仍有 `fastapi.testclient` / `httpx` deprecation warning，后续依赖升级任务处理。
- 真实飞书通知、真实业务系统和 LLM 均未纳入 Phase1 验证。

## 9. 人工确认记录与延后项

1. Phase1 已确认以手工 + API 测试为主，按 Sprint 逐步增加自动化验证。
2. Phase1 不强制加入自动化前端测试；若 Sprint-3 / Sprint-4 需要，可补最小手工验收或轻量前端测试。
3. Python / Node 版本调整需在依赖兼容性验证后单独说明原因、影响范围并确认。
4. Phase2 Conditional Go 已确认（2026-07-09，DOC-C-001~C-005）；Phase2 验证以试点客户 MVP + 技术验证任务为主，真实 CRM/ERP/OA/工单/LLM 不在本阶段解锁。

## 10. Phase2 验证范围（草案）

> Phase2 Conditional Go 已确认（2026-07-09）。本节为草案，各 Sprint 启动前细化；不替代 Sprint 验收标准。

### 10.1 验证优先级（Phase2）

1. P0：试点客户主链路部署可用（Sprint-7）、基础权限由后端执行。
2. P1：飞书沙箱联调（Sprint-8，不接真实组织数据）、PostgreSQL/pgvector 技术验证结论。
3. P2：知识缺口流转 / 审核（Sprint-9）、LLM 专项评估结论（不默认启用）。

### 10.2 Phase2 readiness gate 验证项

| Gate | 验证对象 | 进入标准 | 证据 | 状态 |
|---|---|---|---|---|
| RG-001 | 飞书真实通知 | 沙箱联调通过 + 权限/回调边界确认 | `docs/research/2026-07-10-tech-env-evaluation-feishu-sandbox.md` | Go（2026-07-11；TC-036~043 通过，事件回调后置） |
| RG-002 | PostgreSQL/pgvector | 技术验证 Go/Conditional Go | `docs/research/2026-07-10-tech-env-evaluation-postgres-pgvector.md` | Go（2026-07-10） |
| RG-003 | LLM | 证据约束/不编造/成本/兜底评估完成 | `docs/research/2026-07-11-tech-env-evaluation-llm.md` | Conditional Go（2026-07-11，评估完成；LLM 默认仍关闭） |

### 10.3 Phase2 不解锁验证

- 真实 CRM/ERP/OA/工单集成（Phase3）。
- 多租户/计费/监控/审计（Phase4）。
- LLM 自动答复默认启用。

### 10.4 Sprint-7 验证用例（试点部署与运营配置）

> 2026-07-10 细化。业务输入：单实例双场景包（古晶产品型 + 乐式项目型，不做多租户）、本机演示优先部署、权限最小集（管理员可写 / 其余只读）。

| TC-ID | 依据 | 关联 REQ | 步骤要点 | 通过标准 |
|---|---|---|---|---|
| TC-017 | `docs/design/frontend-interaction.md`、`docs/design/h5-dialog.md` | REQ-010、REQ-011 | 本机部署后，在产品型（古晶）与项目型（乐式）两个场景包分别创建会话、走通问答 / 转人工 / 缺口 | 两个场景包主链路均跑通，`scenario_pack_id` 正确区分，Mock 标识明确 |
| TC-018 | `docs/design/web-console.md`（WC-C-001）、`docs/02-srs.md` REQ-016 | REQ-016 | 以管理员与只读角色分别调用控制台写操作（转人工 / 缺口 / 知识候选状态更新） | 后端按角色放行：管理员可写、其余只读；前端隐藏 / 禁用不能绕过后端 |
| TC-019 | `docs/design/web-console.md`、`docs/design/frontend-interaction.md` | REQ-010、REQ-012 | 控制台运营配置入口切换当前演示场景包、查看双场景包数据与日报摘要 | 可切换 / 查看双场景包数据，运营流程跑通，列表标明 Mock / Demo |
| TC-020 | `docs/env/`（试点部署预案）、本文件 §4 | REQ-015 | 按 `docs/env` 试点部署预案本机部署三端（8000 / 5173 / 5174） | 三端可达，端到端演示可复现，Mock / 降级路径保留 |

### 10.5 Sprint-8A 验证用例（DB 持久化基础设施）

> 2026-07-10 细化并执行。范围：仅搭建 PostgreSQL + pgvector 本机数据库地基，不改后端业务逻辑，不把 Demo 链路切到 PostgreSQL。

| TC-ID | 依据 | 关联 REQ / Gate | 步骤要点 | 通过标准 | 结果 |
|---|---|---|---|---|---|
| TC-021 | `docs/env/postgres-pgvector-runbook.md`、`docs/research/2026-07-10-tech-env-evaluation-postgres-pgvector.md` | RG-002 | 执行 `docker compose -f docker/docker-compose.pgvector.yml config` | Compose 配置可解析，无错误 | 通过（2026-07-10） |
| TC-022 | `docker/docker-compose.pgvector.yml` | RG-002 | 启动 `docker compose -f docker/docker-compose.pgvector.yml up -d` 并等待 healthcheck | `zycs-postgres-pgvector` 进入 `healthy` | 通过（2026-07-10） |
| TC-023 | `docker/postgres/init/001_schema.sql`、`docs/06-db-design.md` | REQ-001~REQ-012、REQ-014、REQ-016 | 查询 pgvector 扩展与 `zycs_` 表数量 | pgvector 扩展版本 `0.8.0`；`zycs_` 表数量 = 11 | 通过（2026-07-10） |
| TC-024 | `docker/postgres/init/002_seed.sql`、`docs/06-db-design.md` §6 | REQ-007、REQ-008、REQ-014 | 查询场景包和 Mock 业务记录 seed | 场景包 = 2；Mock 业务记录 = 5，含 `HC-ORDER-001`、`XS-PROJ-001`、`XS-TICKET-001` | 通过（2026-07-10） |

#### Sprint-8A 验收记录（2026-07-10）

- 执行范围：`tasks/task-008a-db-foundation.md`。
- 改动范围：`docker/docker-compose.pgvector.yml`、`docker/postgres/init/001_schema.sql`、`docker/postgres/init/002_seed.sql`、`docs/env/postgres-pgvector-runbook.md`。
- 验证结果：TC-021~TC-024 均通过。
- 边界说明：后端业务未切 PostgreSQL；H5 / Console 仍走现有 Mock / 本地临时数据；embedding 字段保留但向量检索业务未启用。
- 后续闭环：DB 业务读写已由 Sprint-8B~8F 分步落地；飞书 RG-001 出站通知沙箱已于 2026-07-11 通过，事件回调仍后置。

### 10.6 Sprint-8B 验证用例（静态数据读库）

> 2026-07-10 细化并执行。范围：仅让场景包、知识、规则、Mock 业务记录可在显式启用时从 PostgreSQL 读取；默认仍走 JSON，失败回退 JSON。

| TC-ID | 依据 | 关联 REQ / Gate | 步骤要点 | 通过标准 | 结果 |
|---|---|---|---|---|---|
| TC-025 | `tasks/task-008b-static-data-postgres.md`、`backend/app/services/static_data_source.py` | RG-002、REQ-007、REQ-014 | 不设置 `ZYCS_STATIC_DATA_SOURCE`，运行静态数据相关接口测试 | 场景包、Mock 查询、知识问答仍走 JSON，既有测试通过 | 通过（2026-07-10） |
| TC-026 | `backend/app/services/scenario_pack_service.py` | RG-002、REQ-015 | 设置 `ZYCS_STATIC_DATA_SOURCE=postgres` 但不设置 `ZYCS_DATABASE_URL` | 自动回退 JSON，Demo 不受影响 | 通过（2026-07-10） |
| TC-027 | `backend/app/services/postgres_static_data_repository.py`、`docs/env/postgres-pgvector-runbook.md` | RG-002、REQ-007、REQ-008、REQ-014 | 设置 `ZYCS_TEST_DATABASE_URL=postgresql://zycs:zycs_demo_password@127.0.0.1:5432/zycs`，运行 `tests/api/test_static_data_source.py` | PG 模式可读取 2 个场景包、Mock 业务记录和知识问答；测试 3 passed | 通过（2026-07-10） |

#### Sprint-8B 验收记录（2026-07-10）

- 执行范围：`tasks/task-008b-static-data-postgres.md`。
- 改动范围：`backend/requirements.txt`、`backend/app/services/static_data_source.py`、`backend/app/services/postgres_static_data_repository.py`、`backend/app/services/scenario_pack_service.py`、`tests/api/test_static_data_source.py`、`docs/env/postgres-pgvector-runbook.md`。
- 验证结果：TC-025~TC-027 均通过；默认全量后端回归 `tests/api tests/scenarios tests/acceptance` 为 33 passed、1 skipped（PG 专项在未设置 `ZYCS_TEST_DATABASE_URL` 时跳过）。
- 边界说明：会话、消息、转人工、知识缺口、通知和日报未切 PostgreSQL；PG 读取需显式环境变量启用；数据库不可用时保留 JSON 降级。
- 后续闭环：业务写库已由 Sprint-8C-A/B/F 分步落地；飞书 RG-001 出站通知沙箱已于 2026-07-11 通过，事件回调仍后置。

### 10.7 Sprint-8C-A 验证用例（会话与消息持久化）

> 2026-07-10 细化并执行。范围：仅让新建会话、客户消息和助手回答可在显式启用时写入 PostgreSQL；默认仍走内存，失败回退内存。

| TC-ID | 依据 | 关联 REQ / Gate | 步骤要点 | 通过标准 | 结果 |
|---|---|---|---|---|---|
| TC-028 | `tasks/task-008c-a-conversation-message-postgres.md`、`backend/app/services/conversation_store.py` | RG-002、REQ-001、REQ-002 | 不设置 `ZYCS_CONVERSATION_STORE`，运行会话相关测试 | 现有会话创建、发消息、高风险、缺口链路仍走内存，测试通过 | 通过（2026-07-10） |
| TC-029 | `backend/app/services/conversation_service.py` | RG-002、REQ-015 | 设置 `ZYCS_CONVERSATION_STORE=postgres` 但不设置 `ZYCS_DATABASE_URL` | 自动回退内存，Demo 不受影响 | 通过（2026-07-10） |
| TC-030 | `backend/app/services/conversation_store.py`、`docs/env/postgres-pgvector-runbook.md` | RG-002、REQ-001、REQ-002 | 设置 `ZYCS_TEST_DATABASE_URL=postgresql://zycs:zycs_demo_password@127.0.0.1:5432/zycs`，创建会话并发送知识问答 | `zycs_conversations` 写入会话；`zycs_messages` 写入客户消息和助手回答；列表 API 可查回 | 通过（2026-07-10） |
| TC-031 | `backend/app/services/conversation_store.py`、`docs/06-db-design.md` | RG-002、REQ-006、REQ-016 | PG 模式下发送高风险问题 | `zycs_conversations.status` 更新为 `handoff`，`risk_level` 更新为 `high`；转人工详情仍走现有内存逻辑 | 通过（2026-07-10） |

#### Sprint-8C-A 验收记录（2026-07-10）

- 执行范围：`tasks/task-008c-a-conversation-message-postgres.md`。
- 改动范围：`backend/app/services/conversation_store.py`、`backend/app/services/conversation_service.py`、`tests/api/test_conversation_store.py`、`docs/env/postgres-pgvector-runbook.md`。
- 验证结果：TC-028~TC-031 均通过；默认全量后端回归 `tests/api tests/scenarios tests/acceptance` 为 35 passed、3 skipped。
- 边界说明：转人工详情、知识缺口、通知、日报、审计日志未切 PostgreSQL；PG 写入需显式环境变量启用；数据库不可用时保留内存降级。
- 后续闭环：运营数据持久化已由 Sprint-8C-B / 8F 分步落地；飞书 RG-001 出站通知沙箱已于 2026-07-11 通过，事件回调仍后置。

### 10.8 Sprint-8C-B 验证用例（转人工与知识缺口持久化）

> 2026-07-10 细化并执行。范围：仅让客户消息触发的转人工与知识缺口可在显式启用时写入 PostgreSQL，控制台列表和状态更新优先读写 PostgreSQL；默认仍走内存，失败回退内存。

| TC-ID | 依据 | 关联 REQ / Gate | 步骤要点 | 通过标准 | 结果 |
|---|---|---|---|---|---|
| TC-032 | `tasks/task-008c-b-operational-data-postgres.md`、`backend/app/services/console_service.py` | RG-002、REQ-006、REQ-011 | 设置 `ZYCS_CONVERSATION_STORE=postgres` 但不设置 `ZYCS_DATABASE_URL`，触发高风险转人工 | 自动回退内存，控制台转人工列表可查到本轮记录，Demo 不受影响 | 通过（2026-07-10） |
| TC-033 | `backend/app/services/console_store.py`、`docs/06-db-design.md` | RG-002、REQ-006、REQ-016 | PG 模式下发送高风险问题 | `zycs_human_handoffs` 写入转人工记录；控制台列表可按 `status=open` 查回 | 通过（2026-07-10） |
| TC-034 | `backend/app/services/console_store.py`、`docs/06-db-design.md` | RG-002、REQ-011、REQ-016 | PG 模式下发送无依据问题 | `zycs_knowledge_gaps` 写入知识缺口与 `suggested_tags`；控制台列表可按 `status=new` / `tag=待确认` 查回 | 通过（2026-07-10） |
| TC-035 | `docs/07-api-spec.md` API-004 / API-005 | RG-002、REQ-010、REQ-011 | PG 模式下调用控制台 `PATCH /handoffs/{id}` 与 `PATCH /knowledge-gaps/{id}` | 转人工状态写回 `zycs_human_handoffs`；知识缺口状态与处理说明写回 `zycs_knowledge_gaps` | 通过（2026-07-10） |

#### Sprint-8C-B 验收记录（2026-07-10）

- 执行范围：`tasks/task-008c-b-operational-data-postgres.md`。
- 改动范围：`backend/app/services/console_store.py`、`backend/app/services/console_service.py`、`tests/api/test_console_store.py`、`docs/env/postgres-pgvector-runbook.md`。
- 验证结果：TC-032~TC-035 均通过；PG 专项 `tests/api/test_console_store.py tests/api/test_conversation_store.py` 为 6 passed；默认全量后端回归 `tests/api tests/scenarios tests/acceptance` 为 36 passed、4 skipped。
- 边界说明：通知、日报、审计日志未切 PostgreSQL；飞书沙箱、LLM、真实业务系统未接入；PG 写入需显式环境变量启用，数据库不可用时保留内存降级。
- 残留风险：`zycs_human_handoffs` 当前表结构无 `summary` / `resolution_note` 字段，PG 列表中的 `summary` 临时沿用 `reason`，转人工处理说明不写入 PG；如需完整运营工单字段，应另拆 schema 演进任务。

### 10.9 Sprint-8D 验证用例（飞书沙箱启动前评估 / RG-001）

> 2026-07-10 细化并执行。范围：仅确认飞书出站通知沙箱所需凭据、默认 Mock / 显式 sandbox / 失败降级、回调后置边界；不真实发送飞书通知，不接真实组织数据。

| TC-ID | 依据 | 关联 REQ / Gate | 步骤要点 | 通过标准 | 结果 |
|---|---|---|---|---|---|
| TC-036 | `tasks/task-008d-feishu-sandbox-readiness.md`、`docs/05-tech-spec.md` | RG-001、REQ-009、REQ-016 | 梳理出站通知配置项与密钥存放边界 | 明确 `ZYCS_FEISHU_NOTIFY_MODE`、`ZYCS_FEISHU_WEBHOOK_URL`、`ZYCS_FEISHU_WEBHOOK_SECRET`；密钥不落库不提交 | 通过（2026-07-10） |
| TC-037 | `docs/research/2026-07-10-tech-env-evaluation-feishu-sandbox.md` | RG-001、REQ-009 | 定义飞书通知出站行为 | 默认 Mock；仅显式 sandbox + URL + secret 时允许真实发送；失败回退不阻塞主链路 | 通过（2026-07-10） |
| TC-038 | `docs/research/2026-07-10-tech-env-evaluation-feishu-sandbox.md` | RG-001、NFR-002、NFR-003 | 定义事件回调边界 | 回调后置，启用前必须补验签 / 解密 / 去重 / 限流 / 脱敏日志，不接真实组织数据 | 通过（2026-07-10） |
| TC-039 | `docs/research/2026-07-10-tech-env-evaluation-feishu-sandbox.md` | RG-001、REQ-009 | 人工提供沙箱 webhook URL / secret 后执行实发 | 沙箱群收到转人工 / 知识缺口通知，日志无密钥；失败可回退 Mock | 通过（2026-07-11） |

#### Sprint-8D 验收记录（2026-07-10）

- 执行范围：`tasks/task-008d-feishu-sandbox-readiness.md`。
- 改动范围：`docs/research/2026-07-10-tech-env-evaluation-feishu-sandbox.md`、`docs/05-tech-spec.md`、`docs/08-dev-plan.md`、`docs/09-verification.md`。
- 验证结果：TC-036~TC-039 通过；2026-07-11 用户在本机 PowerShell 配置沙箱 webhook URL / secret 后触发 API-009，返回 `send_status=sent`、`mock=False`、`notify_mode=sandbox`，并确认飞书测试群收到通知。
- RG-001 结论：Go（出站通知沙箱）。默认 Mock 仍保留；真实生产群 / 生产组织数据仍不解锁；事件回调另拆任务。
- 边界说明：本次未写入真实 webhook、token、secret、用户 ID、组织 ID 或生产数据；未启用事件回调；未改变现有 H5 / Console 默认 Mock 演示链路。

### 10.10 Sprint-8E 验证用例（Feishu 通知适配器骨架）

> 2026-07-10 细化并执行。范围：实现默认 Mock / 显式 sandbox 的 Feishu 出站通知适配器骨架；不提交真实凭据，不执行沙箱实发，不启用事件回调。

| TC-ID | 依据 | 关联 REQ / Gate | 步骤要点 | 通过标准 | 结果 |
|---|---|---|---|---|---|
| TC-040 | `tasks/task-008e-feishu-notification-adapter.md`、`backend/app/adapters/feishu_notification_adapter.py` | RG-001、REQ-009 | 不设置 `ZYCS_FEISHU_NOTIFY_MODE`，创建 Mock 通知 | 仍返回 `send_status=mocked`、`mock=true`，默认演示链路不变 | 通过（2026-07-10） |
| TC-041 | `backend/app/adapters/feishu_notification_adapter.py` | RG-001、REQ-009、REQ-016 | 校验 Feishu 签名构造 | 签名按时间戳 + secret 生成 HMAC-SHA256 + Base64；请求体不暴露 secret | 通过（2026-07-10） |
| TC-042 | `backend/app/services/console_service.py`、API-009 | RG-001、REQ-009 | 设置 `ZYCS_FEISHU_NOTIFY_MODE=sandbox` 但缺少 secret，调用 `POST /api/v1/notifications/mock` | 不报错，不外发，降级 `send_status=mocked`，payload 不包含 webhook / secret | 通过（2026-07-10） |
| TC-043 | `backend/app/adapters/feishu_notification_adapter.py`、`docs/research/2026-07-10-tech-env-evaluation-feishu-sandbox.md` | RG-001、NFR-002、NFR-003 | 构造 Feishu sandbox 文本消息 | 消息只包含事件类型、关联 ID、风险 / 缺口摘要和 sandbox 说明，不包含真实客户隐私或生产数据 | 通过（2026-07-10） |

#### Sprint-8E 验收记录（2026-07-10）

- 执行范围：`tasks/task-008e-feishu-notification-adapter.md`。
- 改动范围：`backend/app/adapters/feishu_notification_adapter.py`、`backend/app/adapters/__init__.py`、`backend/app/services/console_service.py`、`tests/api/test_feishu_notification_adapter.py`、`tests/api/test_console.py`、`docs/env/postgres-pgvector-runbook.md`。
- 验证结果：TC-040~TC-043 均通过；专项测试 `tests/api/test_feishu_notification_adapter.py tests/api/test_console.py` 为 18 passed；默认全量后端回归 `tests/api tests/scenarios tests/acceptance` 为 43 passed、4 skipped。
- 边界说明：未提交真实 webhook / token / secret；TC-039 已于 2026-07-11 通过；未启用事件回调；缺配置或发送失败时不阻塞主链路并降级。

### 10.11 Sprint-8F 验证用例（通知记录持久化）

> 2026-07-10 细化并执行。范围：仅让 API-009 创建的通知记录可在显式启用时写入 PostgreSQL；默认仍走内存，失败回退内存。日报和审计日志仍后置。

| TC-ID | 依据 | 关联 REQ / Gate | 步骤要点 | 通过标准 | 结果 |
|---|---|---|---|---|---|
| TC-044 | `tasks/task-008f-notification-postgres.md`、`backend/app/services/console_service.py` | RG-002、REQ-009 | 不设置 `ZYCS_CONVERSATION_STORE`，创建 / 查询通知 | API-009 仍走内存 Mock，现有控制台测试通过 | 通过（2026-07-10） |
| TC-045 | `backend/app/services/console_store.py`、`docs/06-db-design.md` | RG-002、REQ-009、REQ-016 | PG 模式下调用 `POST /api/v1/notifications/mock` | `zycs_notifications` 写入通知记录，`payload`、`send_status`、`is_mock` 正确 | 通过（2026-07-10） |
| TC-046 | `backend/app/services/console_store.py`、API-009 | RG-002、REQ-009 | PG 模式下按 `event_type` / `send_status` 查询通知列表 | `GET /api/v1/notifications/mock` 可从 PostgreSQL 查回本轮记录 | 通过（2026-07-10） |

#### Sprint-8F 验收记录（2026-07-10）

- 执行范围：`tasks/task-008f-notification-postgres.md`。
- 改动范围：`backend/app/services/console_store.py`、`backend/app/services/console_service.py`、`tests/api/test_console_store.py`、`docs/env/postgres-pgvector-runbook.md`。
- 验证结果：TC-044~TC-046 均通过；PG 专项 `tests/api/test_console_store.py tests/api/test_conversation_store.py tests/api/test_static_data_source.py` 为 10 passed；默认全量后端回归 `tests/api tests/scenarios tests/acceptance` 为 43 passed、5 skipped。
- 边界说明：日报、审计日志未切 PostgreSQL；TC-039 已于 2026-07-11 通过；未启用事件回调；缺配置或数据库不可用时回退内存。

### 10.12 Sprint-8 阶段性总体验收（飞书沙箱联调 + DB 技术验证）

> 2026-07-11 收尾。Sprint-8 按 8A~8F 拆分执行，覆盖 RG-001 飞书出站通知沙箱与 RG-002 PostgreSQL/pgvector 技术验证；不接真实生产群 / 生产组织数据，不启用飞书事件回调，不默认启用 LLM。

| 维度 | 验收结论 | 证据 |
|---|---|---|
| RG-001 飞书出站通知沙箱 | Go | TC-036~TC-043 通过；TC-039 于 2026-07-11 实发到飞书测试群，API-009 返回 `send_status=sent`、`mock=False`、`notify_mode=sandbox` |
| RG-002 PostgreSQL/pgvector | Go | TC-021~TC-024 通过；pgvector `0.8.0`、11 张 `zycs_` 表、seed 数据验证通过 |
| 静态数据读库 | 通过 | TC-025~TC-027 通过；场景包、知识、规则、Mock 业务记录可显式启用 PostgreSQL，默认 JSON 回退 |
| 会话与消息持久化 | 通过 | TC-028~TC-031 通过；新建会话、客户消息、助手回答可显式写入 PostgreSQL，默认内存回退 |
| 运营数据持久化 | 通过 | TC-032~TC-035、TC-044~TC-046 通过；转人工、知识缺口、通知记录可显式写入 PostgreSQL，默认内存回退 |
| 安全边界 | 通过 | 未提交 webhook / secret；真实生产群、生产组织数据、飞书事件回调、日报 PG 化、审计日志 PG 化仍后置 |

#### Sprint-8 收尾记录（2026-07-11）

- 执行范围：Sprint-8A~8F，任务单 `tasks/task-008a-db-foundation.md` 至 `tasks/task-008f-notification-postgres.md`。
- 总体验收：TC-021~TC-046 均已完成记录；RG-001 / RG-002 均为 Go。
- 保留降级：默认仍保留 JSON / 内存 / Mock 路径；PostgreSQL 与 Feishu sandbox 均需显式环境变量启用。
- 后置项：`zycs_daily_summaries`、`zycs_audit_logs`、飞书事件回调、真实生产群 / 生产组织数据、RG-003 LLM 评估。
- 下一阶段建议：进入 Sprint-9 前先执行 RG-003 LLM 专项评估，只评估不接 API、不启用自动答复。

### 10.13 Sprint-9 验证用例（RG-003 LLM 专项评估）

> 2026-07-11 细化并执行。范围：仅完成 LLM 证据约束 / 不编造 / 成本 / 兜底评估，输出 Conditional Go 结论；不接真实 LLM API，不安装依赖，不写 API key，不启用自动答复。

| TC-ID | 依据 | 关联 REQ / Gate | 步骤要点 | 通过标准 | 结果 |
|---|---|---|---|---|---|
| TC-047 | `docs/research/2026-07-11-tech-env-evaluation-llm.md` | RG-003、REQ-005 | 核对 LLM 评估是否覆盖证据约束 / 不编造 / 成本 / 兜底四项边界 | 四项边界均已盘点，结论 Conditional Go | 通过（2026-07-11，评估类） |
| TC-048 | `docs/research/2026-07-11-tech-env-evaluation-llm.md`、`ai/project-rules.md` §1 | RG-003、DOC-C-005 | 核对 LLM 默认状态 | LLM 默认关闭，评估完成不等于已启用 | 通过（2026-07-11，评估类） |
| TC-049 | `docs/research/2026-07-11-tech-env-evaluation-llm.md`、`docs/05-tech-spec.md` §13 | RG-003、RISK-P2-003 | 核对 LLM 启用前风险与降级边界是否已登记 | RISK-P2-003 已评估；新增 RISK-P2-007~010（候选 / 未启用）；降级走规则匹配 + 转人工 | 通过（2026-07-11，评估类） |

#### Sprint-9 RG-003 评估验收记录（2026-07-11）

- 执行范围：RG-003 LLM 专项评估。
- 改动范围：`docs/research/2026-07-11-tech-env-evaluation-llm.md`、`docs/05-tech-spec.md`、`docs/08-dev-plan.md`、`docs/09-verification.md`、`docs/design/knowledge-and-policy.md`。
- 验证结果：TC-047~TC-049 通过（评估类，非实发）。
- RG-003 结论：Conditional Go（评估完成）。LLM 默认仍关闭；真实接入后置 Phase3 或单独授权任务，需先解 DOC-C-005 + 不编造 / 成本 / 兜底 / 隐私四条硬约束 + 安全评审 + 成本授权。
- 边界说明：本次未接真实 LLM API、未安装依赖、未写 API key、未发送真实客户隐私；未改变现有 H5 / Console 默认 Mock 演示链路；本地小模型不作为启用路线。

### 10.14 Sprint-9 验证用例（知识运营强化 / 缺口 accepted 入库 + API-006）

> 2026-07-11 细化。范围：知识缺口 `accepted` 自动入库为 `draft` 知识条目；新增 API-006 `GET/POST /knowledge-items`。不启用 LLM，不接外部系统。默认内存，PG 显式启用且失败回退内存。

| TC-ID | 依据 | 关联 REQ / Gate | 步骤要点 | 通过标准 | 结果 |
|---|---|---|---|---|---|
| TC-050 | `docs/07-api-spec.md` API-006、`docs/06-db-design.md` §4.4 | REQ-004、REQ-011 | `POST /knowledge-items` 新增知识候选，`GET /knowledge-items` 查询 | 新增成功（`draft` 状态、`source_ref` 存在）；GET 可查回；写操作需 admin | 通过（2026-07-11） |
| TC-051 | `docs/design/knowledge-and-policy.md` §5、KP-C-003、`docs/06-db-design.md` §4.4/§4.8 | REQ-011 | `PATCH /knowledge-gaps/{id}` 到 `accepted` | 缺口状态变 `accepted`，且自动生成一条 `draft` 知识条目（`source_ref` 指向缺口），API-006 可查回 | 通过（2026-07-11） |
| TC-052 | `docs/design/knowledge-and-policy.md` §5、ADR-0004 | REQ-011 | `PATCH /knowledge-gaps/{id}` 到 `rejected` | 缺口状态变 `rejected`，不生成知识条目 | 通过（2026-07-11） |

#### Sprint-9 知识运营强化验收记录（2026-07-11）

- 执行范围：`tasks/task-009b-knowledge-items-and-gap-acceptance.md`。
- 改动范围：`backend/app/schemas/console.py`、`backend/app/services/console_service.py`、`backend/app/services/console_store.py`、`backend/app/api/console.py`、`tests/api/test_console.py`、`tests/api/test_console_store.py`。
- 验证结果：TC-050~TC-052 通过；默认全量 `tests/api tests/scenarios tests/acceptance` 48 passed、5 skipped；PG 专项 `test_console_store + test_conversation_store + test_static_data_source` 11 passed。
- 边界说明：缺口 `accepted` 自动生成 `draft` 知识条目（`source_ref = knowledge_gap:{gap_id}`）；`rejected` 不生成；`POST /knowledge-items` 需 admin；LLM 默认关闭未变；不接外部系统；未改前端；未引入新依赖。
- 后置项：知识条目 `draft → active` 转正、`active` 知识进入检索链路、前端知识条目管理页。

### 10.15 Phase2 MVP 验收（M10）

> 2026-07-11 收尾。Phase2 Sprint-7/8/9 全部完成，M10 里程碑验收。

| 维度 | 验收结论 | 证据 |
|---|---|---|
| Sprint-7 试点部署与运营配置 | 通过 | TC-017~020 通过（PR #34）；单实例双场景包、后端角色权限、运营配置入口、本机部署预案 |
| Sprint-8 飞书沙箱 + DB 技术验证 | 通过 | TC-021~046 通过；RG-001 飞书出站通知沙箱 Go、RG-002 PostgreSQL/pgvector Go |
| Sprint-9 LLM 评估 + 知识运营强化 | 通过 | TC-047~052 通过；RG-003 LLM Conditional Go；缺口 accepted 入库 + API-006 |
| Readiness gate | 全部有结论 | RG-001 Go、RG-002 Go、RG-003 Conditional Go |
| 默认全量回归 | 通过 | `tests/api tests/scenarios tests/acceptance` 48 passed、6 skipped |
| PG 专项回归 | 通过 | `test_console_store + test_conversation_store + test_static_data_source` 11 passed |
| Phase2 退出标准 | 达成 | 试点客户主链路可用（H5 问答 / 转人工 / 缺口 / 知识条目 + Console 运营 + 飞书沙箱通知 + DB 可选持久化）；真实 CRM/ERP/OA/工单/LLM 未解锁（后置 Phase3） |

#### Phase2 MVP 验收记录（2026-07-11）

- 验收范围：Phase2 Sprint-7/8/9，M10 里程碑。
- 验收结论：**Phase2 MVP 试点验收通过**。试点客户主链路可用，人工运营流程跑通；技术验证（飞书沙箱、PostgreSQL/pgvector、LLM 评估）均有 gate 结论。
- 退出标准达成：试点客户可用；真实 CRM/ERP/OA/工单/LLM 不在本阶段解锁（DOC-C-003/004/005）。
- 未解锁项（后置 Phase3/4）：真实 CRM/ERP/OA/工单集成（Phase3）、多租户 / 计费 / 监控 / 审计（Phase4）、LLM 自动答复默认启用、飞书事件回调、真实生产群 / 生产组织数据、日报 / 审计日志 PG 化。
- 后置优化（不阻塞验收）：知识条目 `draft → active` 转正、`active` 知识进入检索链路、前端知识条目管理页、`zycs_daily_summaries` / `zycs_audit_logs` PG 持久化。
- Phase 升级：Phase3 需试点客户授权 + 单独 `phase-upgrade` 评估，不在本次验收范围；当前阶段仍为 Phase2。

### 10.16 知识闭环验证用例（task-009c：转正 + active 检索）

> 2026-07-11 细化。范围：知识条目 `draft → active` 转正（`PATCH /knowledge-items/{item_id}`）；`active` 知识进入问答检索链路。不启用 LLM，不接外部系统。

| TC-ID | 依据 | 关联 REQ / Gate | 步骤要点 | 通过标准 | 结果 |
|---|---|---|---|---|---|
| TC-053 | `docs/07-api-spec.md` API-006、`docs/06-db-design.md` §4.4 | REQ-004、REQ-011 | `PATCH /knowledge-items/{item_id}`（admin）把 draft 改 active；viewer 尝试改 | admin 成功改 status；viewer 返回 403 | 通过（2026-07-11） |
| TC-054 | `backend/app/services/message_policy_service.py`、KP-C-001 | REQ-004、REQ-011 | 新增一条 active 知识条目（含可命中关键词），发消息触发检索；对比 draft 同样内容不命中 | active 条目被检索命中（`answer_type=knowledge`、`source_ref` 为该条目来源）；draft 不命中；无 active 时行为不变 | 通过（2026-07-11） |

#### task-009c 知识闭环验收记录（2026-07-11）

- 执行范围：`tasks/task-009c-knowledge-item-active-retrieval.md`。
- 改动范围：`backend/app/services/console_service.py`、`backend/app/services/console_store.py`、`backend/app/api/console.py`、`backend/app/services/message_policy_service.py`、`tests/api/test_console.py`、`tests/api/test_knowledge_retrieval.py`。
- 验证结果：TC-053/054 通过；默认全量 `tests/api tests/scenarios tests/acceptance` 54 passed、6 skipped；PG 专项 `test_console_store + test_conversation_store + test_static_data_source` 11 passed。
- 边界说明：`PATCH /knowledge-items/{item_id}` 需 admin，允许 draft/active/archived 任意合法 status；`active` 知识与 seed 统一评分参与检索，draft/archived 不参与；无 active 时检索行为不变。
- 后置项：前端知识条目管理页（含转正操作 UI）。

### 10.17 前端知识条目管理页验证用例（task-009d）

> 2026-07-11 细化。范围：Console「知识条目」Tab UI（列表 / 转正 / 归档 / 新增），接 API-006。前端 build 通过；UI 交互由人工浏览器验收。

| TC-ID | 依据 | 关联 REQ | 步骤要点 | 通过标准 | 结果 |
|---|---|---|---|---|---|
| TC-055 | `docs/design/web-console.md` §4.4、`frontend/console/src/App.tsx` | REQ-004、REQ-011 | Console 切到「知识条目」Tab：admin 转正 draft→active、归档、表单新增 draft；viewer 只读 | 列表展示 + 状态颜色区分（active 绿 / draft、archived 灰）；admin 可写、viewer 按钮禁用；`npm run build` 通过 | 通过（2026-07-11）；build 通过，人工浏览器验收暂未发现问题 |

- 人工浏览器验收记录（2026-07-11）：本机后端 `8000`、Console `5174`、H5 `5175` 均可访问；用户按 TC-055 路径检查 Console「知识条目」Tab 后反馈“暂时没发现”问题。
