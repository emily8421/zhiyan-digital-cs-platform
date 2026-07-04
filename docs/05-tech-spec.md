# 05 Tech Spec（技术方案）

## 0. 文档元信息

| 项 | 内容 |
|---|---|
| 上游输入 | `docs/04-architecture.md`、`docs/env/local-env.md`、`ai/project-rules.md` |
| 当前状态 | Phase1 关键口径已确认 |
| 最后更新 | 2026-07-03 |
| 当前阶段 | Phase1 本机 Demo |

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

| 决策 | 当前口径 | 原因 | 风险 |
|---|---|---|---|
| 前端单仓多入口 | `frontend/customer-h5` 与 `frontend/console` 分目录 | H5 与控制台职责不同，但共享类型和 API client | 前端框架已按 Phase1 确认为 React + Vite + TypeScript |
| 后端分层 | API / Service / Adapter / Data / Schema / Core | 避免外部系统与业务逻辑耦合 | 初期目录较多 |
| 场景包配置化 | 使用数据文件表达产品型 / 项目型场景 | 支持复用与追溯 | 需要设计校验规则 |
| Mock 优先 | Phase1 所有外部系统走 Mock | 保证本机可跑与安全 | 与真实系统差异需标明 |
| 不编造策略 | 无依据 / 高风险转人工 | 保护售后和承诺风险 | 演示时可能不够“智能” |
| 数据库目标设计保留 | `docs/06` 写 PostgreSQL 目标结构 | 为后续 MVP / 集成铺路 | Phase1 实现可能降级 |

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

## 11. 人工确认记录与延后项

1. Phase1 存储降级策略已确认优先 JSON / SQLite / 内存 Mock，不强制 PostgreSQL。
2. 允许安装 Sprint 必需依赖，但每次安装前需说明包名、用途和影响范围；Docker 镜像 Phase1 默认不新增。
3. 真实飞书机器人通知不纳入 Phase1，仅记录 Mock payload。
4. Phase1 默认不使用公司服务器；若后续需要，需另行确认 CPU / 内存 / GPU / 端口 / 成本 / 安全边界。
