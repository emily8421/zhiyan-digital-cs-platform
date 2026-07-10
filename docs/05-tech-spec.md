# 05 Tech Spec（技术方案）

## 0. 文档元信息

| 项 | 内容 |
|---|---|
| 上游输入 | `docs/04-architecture.md`、`docs/env/local-env.md`、`ai/project-rules.md` |
| 当前状态 | Phase1 已通过验收；Phase2 Conditional Go 已确认（2026-07-09）；RG-001（飞书沙箱）Conditional Go、RG-002（PostgreSQL/pgvector）技术验证 Go（2026-07-10，见 §14） |
| 最后更新 | 2026-07-10 |
| 当前阶段 | Phase2：MVP 试点 |
| 覆盖架构组件 | COMP-001~012（见 `docs/04-architecture.md` §3） |

## 1. 技术栈

| 层 | 技术 | 状态 | 说明 |
|---|---|---|---|
| 客户 H5 | React + Vite + TypeScript | Phase1 确认 | 独立 Web 页面，快速演示交互。 |
| Web 控制台 | React + Vite + TypeScript | Phase1 确认 | 可与 H5 共享 API client 和类型。 |
| 后端 | Python + FastAPI | 已列入项目规则草稿 | REST API、服务层、适配层。 |
| 数据库 | PostgreSQL + pgvector | 计划方向，Phase1 可降级 | Docker 不可用时先 Mock / 本地临时数据。 |
| 向量检索 | pgvector / TEI | 预留，默认关闭 | Phase1 不强制向量服务。 |
| 通知 | 飞书机器人适配 | 预留，Phase1 Mock | 默认不真实发送。 |
| 外部业务系统 | CRM / ERP / OA / 工单适配 | 预留，Phase3 | Phase1 仅 Mock。 |
| LLM | Phase1 不启用 | 默认关闭 | 启用前需补成本、不编造、兜底、审计。 |

## 2. 本机环境约束

依据 `docs/env/local-env.md`：当前本机为 Windows 10 / PowerShell 5.1，约 31.73 GB 内存，Python 3.14.3，Node.js 22.17.1，Docker 已安装但当前不可用，未检测到 GPU。

Phase1 必须能本机运行：

- H5 对话页。
- FastAPI 后端。
- Web 控制台。
- Mock 数据与基础手工验证。

允许降级 / Mock：

- PostgreSQL / pgvector。
- Embedding / 向量检索。
- 飞书通知。
- 订单 / 项目 / 售后等外部业务系统。
- LLM 能力。

禁止本机运行：本地大模型推理、模型训练、生产规模向量索引、真实生产数据处理。

## 3. 关键技术决策

| TDR-ID | 决策 | 当前口径 | 原因 | 风险 | 验证状态 |
|---|---|---|---|---|---|
| TDR-001 | 前端单仓多入口 | `frontend/customer-h5` 与 `frontend/console` 分目录 | H5 与控制台职责不同，但共享类型和 API client | 前端框架已按 Phase1 确认为 React + Vite + TypeScript | 已验证（Phase1 build 通过） |
| TDR-002 | 后端分层 | API / Service / Adapter / Data / Schema / Core | 避免外部系统与业务逻辑耦合 | 初期目录较多 | 已验证（Phase1 API 测试通过） |
| TDR-003 | 场景包配置化 | 使用数据文件表达产品型 / 项目型场景 | 支持复用与追溯 | 需要设计校验规则 | 已验证（Phase1 场景包加载通过） |
| TDR-004 | Mock 优先 | Phase1 所有外部系统走 Mock | 保证本机可跑与安全 | 与真实系统差异需标明 | 已启用（Phase1）；Phase2 部分转沙箱 |
| TDR-005 | 不编造策略 | 无依据 / 高风险转人工 | 保护售后和承诺风险 | 演示时可能不够“智能” | 已启用（ADR-0004） |
| TDR-006 | 数据库目标设计保留 | `docs/06` 写 PostgreSQL 目标结构 | 为后续 MVP / 集成铺路 | Phase1 实现可能降级 | 已验证（目标结构）；Phase1 降级运行 |

## 3.1 依赖与配置（P1 补强，2026-07-09）

> 对应 `ai/doc-standards/05-tech-spec.md` §3。Phase1 依赖最小；Phase2 新增依赖需按 `ai/project-rules.md` §6 逐次确认。

| 类型 | 名称 / 路径 | 用途 | 启用阶段 | 当前状态 | 配置来源 | 密钥 / 敏感性 | 验证方式 |
|---|---|---|---|---|---|---|---|
| Python 包 | `backend/requirements.txt`（FastAPI / Pydantic / uvicorn 等） | 后端运行 | Phase1 | 已启用 | requirements.txt | 无 | `pytest tests/api` 通过 |
| Node 包 | `frontend/customer-h5/package.json`、`frontend/console/package.json` | 前端构建 | Phase1 | 已启用 | package.json | 无 | `npm run build` 通过 |
| 数据库 | PostgreSQL 16 + pgvector 0.8.0 | 持久化 / 向量 | Phase2 技术验证 | 已验证可用（RG-002 Go） | docker-compose（待 Sprint-8 实现） | 连接串（secret） | 已验证（2026-07-10，见 `docs/research/2026-07-10-tech-env-evaluation-postgres-pgvector.md`） |
| 通知 | 飞书机器人 webhook | 员工通知 | Phase2 沙箱 | Conditional Go（默认 Mock，真实发送待凭据） | `.env.local` / 环境变量 | webhook URL / secret（secret） | 已完成启动前评估；待沙箱实发（RG-001，见 `docs/research/2026-07-10-tech-env-evaluation-feishu-sandbox.md`） |
| LLM | 外部 LLM API | 自动答复 | Phase2 评估 | 默认关闭 | .env（待） | API key（secret） | 待专项评估（RG-003） |

## 4. 后端技术方案

- 使用 FastAPI 提供 REST API。
- 使用 Pydantic 模型定义请求 / 响应 / 内部 DTO。
- 服务层包含 `conversation_service`、`intent_router`、`knowledge_service`、`handoff_service`、`gap_service`、`summary_service`。
- 适配层包含 `mock_business_adapter`、`notification_adapter`，未来新增 `crm_adapter`、`erp_adapter`、`oa_adapter`。
- 数据层 Phase1 可先加载 JSON / YAML / Python seed 数据；若 PostgreSQL 可用则按 `docs/06-db-design.md` 实现。
- 日志必须脱敏，禁止输出 token、真实联系方式、真实订单或合同信息。

## 5. 前端技术方案

前端交互细节、页面状态、边界文案、接口依赖和验收路径统一见 `docs/design/frontend-interaction.md`。

### 5.1 H5 对话页

- 核心页面：会话入口、消息列表、输入框、依据 / Mock 标识、转人工提示。
- 核心状态：`conversationId`、`messages`、`scenarioPackId`、`loading`、`error`。
- 样式目标：手机浏览器可读、演示屏幕可展示。

### 5.2 Web 控制台

- 核心页面：概览、会话列表、待跟进、知识缺口、通知记录、场景包 / Mock 数据查看。
- 控制台 Phase1 不做复杂权限；仅用于本机 Demo。
- 所有外部数据必须标明 Mock。

## 6. 数据与存储方案

| 数据 | Phase1 默认 | 目标结构 |
|---|---|---|
| 会话 / 消息 | 本地临时存储或 PostgreSQL | `zycs_conversations`、`zycs_messages` |
| 知识 / 规则 | JSON / seed 数据 | `zycs_knowledge_items`、`zycs_rule_items` |
| 场景包 | JSON / YAML | `zycs_scenario_packs` |
| Mock 业务数据 | JSON / seed 数据 | `zycs_mock_business_records` |
| 转人工 / 缺口 | 本地临时存储或 PostgreSQL | `zycs_human_handoffs`、`zycs_knowledge_gaps` |
| 通知 / 摘要 / 审计 | 本地临时存储或 PostgreSQL | `zycs_notifications`、`zycs_daily_summaries`、`zycs_audit_logs` |

数据库表前缀已确认为 `zycs_`。

## 7. 接口方案

- REST API 前缀：`/api/v1`。
- 响应统一包含 `request_id`，错误响应包含 `code`、`message`、`details`。
- H5 和 Web 控制台均只调用后端 API，不直接读取本地数据文件。
- 外部通知 API 默认不真实发送，只记录 payload。
- API 契约见 `docs/07-api-spec.md`。

## 8. 安全与合规

- 不保存真实客户隐私数据；样例数据必须标明 Mock。
- 不把 token、密钥、账号密码写入日志、文档或测试数据。
- 不自动承诺价格、交期、赔付、合同、法律责任或售后结论。
- 默认不访问外部网络和付费服务。
- 如后续启用 LLM，必须新增安全评审：提示词边界、检索证据、成本上限、失败兜底、人工复核。

## 9. 资源评估与降级策略

| 项 | 正常方案 | 降级方案 | 触发条件 |
|---|---|---|---|
| PostgreSQL | Docker 启动本地数据库 | JSON / SQLite / 内存 Mock | Docker 不可用或 Phase1 未要求启用数据库 |
| pgvector | PostgreSQL 扩展 | 关键词 / 规则匹配 | 向量服务不可用 |
| TEI / Embedding | 远程或容器服务 | 不启用 | Phase1 默认关闭；无 GPU / 无服务器 / 成本未纳入 Phase1 |
| 飞书通知 | 真实机器人 webhook | Mock payload + 日志 | Phase1 不授权外部联网 / 不配置真实凭据 |
| LLM | 受控 API 调用 | 不启用 | Phase1 默认关闭；后续需另行确认成本、安全、准确性 |

## 10. 编码约定

- Python 使用 `snake_case`，前端变量 / 函数使用 `camelCase`，组件使用 `PascalCase`。
- 外部系统访问必须走适配层，不得在服务逻辑中直接调用外部 API。
- 场景包、Mock 数据和客户叙事必须以可追溯配置或数据文件表达。
- 错误处理不得吞掉高风险状态；高风险问题要显式进入转人工。

## 11. 人工确认记录与待确认项

### 11.1 已确认记录

1. Phase1 存储降级策略已确认优先 JSON / SQLite / 内存 Mock，不强制 PostgreSQL。
2. 允许安装 Sprint 必需依赖，但每次安装前需说明包名、用途和影响范围；Docker 镜像 Phase1 默认不新增。
3. 真实飞书机器人通知不纳入 Phase1，仅记录 Mock payload。
4. Phase1 默认不使用公司服务器；若后续需要，需另行确认 CPU / 内存 / GPU / 端口 / 成本 / 安全边界。

### 11.2 待确认项（§6.1 结构）

> 集中在 `docs/research/2026-07-09-docs-open-items.md`：

| 引用 ID | 待确认项 | AI 建议 | 建议依据 | 取舍影响 / 阻塞关系 |
|---|---|---|---|---|
| DOC-C-003 | 飞书通知沙箱 / 试点评估 | Phase2 技术验证任务 | Phase1 已 Mock | 条件阻塞 Sprint-8（RG-001） |
| DOC-C-004 | PostgreSQL / pgvector Phase2 必做性 | 先技术验证，不作前置 | Docker 不可用 | 条件阻塞 Sprint-8（RG-002） |
| DOC-C-005 | LLM 是否进入 Phase2 | 仅评估，不默认启用 | 不编造/成本边界未评估 | 条件阻塞 Sprint-9（RG-003） |
| IN-C-005 | Channel Adapter Layer 设计 | Phase2 readiness gate 再补 | Phase1 仅 H5 | 条件阻塞 Phase2 全渠道入口 |
| ARCH-C-001 | 04/05 doc-standards 合规改进 | 本次 P1 执行 | 评估报告 | 不阻塞 |

## 12. Phase2 技术约束（P0 补强，2026-07-09）

> 对应 `ai/doc-standards/05-tech-spec.md` §5（Phase 技术约束）。本文件保留实际章节号 §12，全文未做章节重排，对齐方式见 §15 章节映射说明。

| Phase | 允许 | 禁止 | Mock / 降级 | 技术状态说明 | 权威源 |
|---|---|---|---|---|---|
| Phase2 | 强化知识库 / 缺口流转 / 权限 / 运营配置；飞书沙箱联调；PostgreSQL/pgvector 技术验证；单个试点客户部署 | 真实 CRM/ERP/OA/工单（Phase3）；多租户 / 计费（Phase4）；LLM 默认启用；真实客户隐私 / 生产会话 | 飞书沙箱不接真实组织数据；DB 验证不作功能前置；Mock / 降级路径保留 | Conditional Go（2026-07-09） | `ai/project-rules.md` §1、`docs/03-prd.md` §3 |

## 13. 技术风险与验证计划（P0 补强，2026-07-09）

> 对应 `ai/doc-standards/05-tech-spec.md` §8（技术风险）。Risk-ID 使用 RISK-P2-* 前缀。

| Risk-ID | 风险 | 触发条件 | 影响 | 当前状态 | 验证方式 | 对应用例 / 任务 | 解锁条件 |
|---|---|---|---|---|---|---|---|
| RISK-P2-001 | Docker 不可用阻塞 PostgreSQL/pgvector | Sprint-8 需 DB 技术验证 | 影响 DB 验证节奏 | 已解除（2026-07-10） | Docker 修复 + 技术环境评估 | Sprint-8 / RG-002 | Docker 可用或确认降级可接受（已解除：Docker Desktop 4.76.0 可用） |
| RISK-P2-005 | ivfflat 索引小数据低召回 | pgvector 向量检索 | 影响检索召回 | 已知，不阻塞 | 数据量足后评估 HNSW | Sprint-9 / 知识运营 | 数据量足或改 HNSW |
| RISK-P2-006 | embedding 维度 / 方案未定 | 向量字段启用 | 向量检索暂不可用 | 待 embedding 方案（Phase2 默认关闭） | 关键词 / 规则匹配降级 | Sprint-9 / Phase3 | embedding 方案确定 |
| RISK-P2-002 | 飞书真实通知权限 / 回调边界未定 | Sprint-8 沙箱联调 | 影响员工侧触达 | Conditional Go（凭据清单 / 出站通知 / 回调边界已定义，实发待凭据） | 沙箱联调 + 权限确认 | Sprint-8 / RG-001 | 人工提供沙箱 webhook URL / secret 后完成实发验证；回调另拆任务 |
| RISK-P2-003 | LLM 不编造 / 成本 / 兜底边界未评估 | Sprint-9 LLM 评估 | 阻塞 LLM 启用决策 | 待评估 | LLM 专项评估 | Sprint-9 / RG-003 | 评估结论 Go |
| RISK-P2-004 | 沙箱内 Vite `spawn EPERM` | 前端 build / dev | 沙箱内构建失败 | 已接受 | 非沙箱本机运行 | TC-015 | 非沙箱环境 |

## 14. Readiness Gate（P0 补强，2026-07-09）

> 对应 `ai/doc-standards/05-tech-spec.md` §9（Readiness Gate）。Phase2 涉及真实运行依赖（飞书 / DB / LLM），进入相关 Sprint 前必须给出 gate 结论。

| Gate | 适用对象 | 进入标准 | 必需证据 | 状态 | 阻塞项 / 下一步 |
|---|---|---|---|---|---|
| RG-001 | 飞书真实通知 | 沙箱联调通过 + 权限 / 回调边界确认 | `docs/research/2026-07-10-tech-env-evaluation-feishu-sandbox.md` | Conditional Go（2026-07-10） | 可进入默认 Mock / 显式 sandbox 的适配器设计；真实实发需人工提供 webhook URL / secret；事件回调另拆任务 |
| RG-002 | PostgreSQL/pgvector | 技术验证 Go / Conditional Go | `docs/research/2026-07-10-tech-env-evaluation-postgres-pgvector.md` | Go（2026-07-10） | 已通过，可进 Sprint-8 DB 实现 |
| RG-003 | LLM | 证据约束 / 不编造 / 成本 / 兜底评估完成 | LLM 专项评估报告 | 待评估 | Sprint-9 前补 LLM 专项评估 |

Conditional Go 保留：上述 gate 在对应 Sprint 前必须由「待评估」推进到 Go / Conditional Go；No-Go 阻止相关 Sprint。详见 `docs/09-verification.md` §10.2。

## 15. 与 doc-standards 章节映射说明（P1 合规，2026-07-09）

> 本文件未做全文章节号重排（§4 后端 / §6 数据 / §7 接口在 doc-standards 05 无对应归属，整文件重写风险高），采用映射说明对齐 `ai/doc-standards/05-tech-spec.md`。追溯链用 TDR-ID / Risk-ID / RG-ID 串联，不依赖章节号。

| doc-standards 章节 | 本文件实际章节 | 说明 |
|---|---|---|
| §2 关键技术决策 | §3 | TDR-001~006 |
| §3 依赖与配置 | §3.1 | 新增（P1） |
| §4 运行环境与资源评估 | §2 + §9 | 本机环境 + 资源降级 |
| §5 Phase 技术约束 | §12 | Phase2 约束（P0） |
| §6 编码约定 | §10 | — |
| §7 安全隐私合规 | §8 | — |
| §8 技术风险与验证 | §13 | RISK-P2-*（P0） |
| §9 Readiness Gate | §14 | RG-001~003（P0） |
| §10 待确认项 | §11.2 | 引用 open items（§6.1 结构） |
| §4 后端 / §6 数据 / §7 接口（DS 无对应） | §4 / §6 / §7 | 保留为技术实现口径（非 DB/API 字段细节） |
