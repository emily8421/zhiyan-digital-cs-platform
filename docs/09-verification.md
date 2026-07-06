# 09 Verification（验证计划）

## 0. 文档元信息

| 项 | 内容 |
|---|---|
| 上游输入 | `docs/02-srs.md`、`docs/03-prd.md`、`docs/08-dev-plan.md` |
| 当前状态 | Phase1 关键口径已确认 |
| 最后更新 | 2026-07-03 |
| 当前 Phase | Phase1 本机 Demo |

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
