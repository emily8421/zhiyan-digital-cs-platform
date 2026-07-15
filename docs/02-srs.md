# 02 SRS（Software Requirements Specification）

## 0. 文档元信息

| 项 | 内容 |
|---|---|
| 上游输入 | `docs/01-user-requirements.md` |
| 当前状态 | Phase2 MVP 已验收；Phase2.5 / Phase3A Product Sandbox 系统需求与下游文档已同步（2026-07-15） |
| 最后更新 | 2026-07-15 |
| 当前阶段 | Phase2.5 / Phase3A Product Sandbox 可试用版 |

## 1. 系统范围

知衍数字客服统一平台在 Phase1/Phase2 已提供一条可本机演示和 MVP 验收的数字客服闭环：客户从 H5 进入会话，系统识别意图，基于场景包、知识库、规则和 Mock 数据给出有依据的回答；遇到高风险、无依据或需人工判断的问题时转人工；员工侧 Web 控制台展示会话、缺口、待跟进、Mock 通知和摘要。

Phase2.5 / Phase3A 需要在不依赖真实客户数据的情况下，把上述闭环扩展为 Product Sandbox 可试用版：系统可按场景包选择数据源模式，默认使用独立模拟数据集跑通客户问答、进度查询、转人工、缺口流转、Console 看板、通知记录、日报摘要和演示重置；真实数据模式仅作为只读预留，启用前必须满足授权、字段映射、安全评审和只读验证。

系统不直接接入真实企业微信客户群、真实飞书组织、真实 CRM/ERP/OA/工单系统，不处理真实客户隐私或生产数据。

## 2. 功能性需求

| REQ-ID | 系统需求 | 阶段 | 验收要点 | 来源 U-ID |
|---|---|---|---|---|
| REQ-001 | 系统应提供 H5 客户对话入口，支持用户输入文本问题并展示回复、转人工状态和 Mock 标识。 | [P1] Demo | H5 页面可发起对话并展示响应。 | U-001 |
| REQ-002 | 系统应维护会话状态，包括会话 ID、客户入口、当前场景包、消息列表和待跟进状态。 | [P1] Demo | 刷新或切换查询时能按会话 ID 读取状态。 | U-001 |
| REQ-003 | 系统应识别售前、售中、售后、资料、投诉、高风险、未知等意图，并路由到对应处理流程。 | [P1] Demo | 典型样例能进入正确流程，未知问题不误答。 | U-002 |
| REQ-004 | 系统应基于知识条目、规则条目、场景包配置或 Mock 数据生成回复。 | [P1] Demo | 每条自动回复都有来源类型。 | U-002、U-003 |
| REQ-005 | 系统应实现不编造保护：无来源、置信不足或高风险内容不得自动承诺。 | [P1] Demo | 无依据问题触发转人工或缺口记录。 | U-003、U-011 |
| REQ-006 | 系统应支持转人工流程，记录转人工原因、建议负责人、客户问题摘要和处理状态。 | [P1] Demo | 高风险 / 无依据问题生成待跟进记录。 | U-004 |
| REQ-007 | 系统应支持产品型客户和项目型客户场景包，以配置或数据文件表达意图、知识、规则和 Mock 数据。 | [P1] Demo | 可在两个场景包间切换演示。 | U-005、U-009 |
| REQ-008 | 系统应提供订单 / 项目 / 售后进度 Mock 查询能力，并明确标记为 Mock 数据。 | [P1] Mock，[P3B] 集成 | 输入样例编号返回 Mock 进度，不连接真实系统。 | U-006 |
| REQ-009 | 系统应提供通知适配层，Phase1 支持 Mock / 日志形式记录飞书通知内容。 | [P1] Mock，[P2] MVP | 转人工和缺口能生成通知 payload。 | U-004、U-008、U-010 |
| REQ-010 | 系统应提供 Web 控制台，展示会话、待跟进、风险、缺口、场景包和 Mock 摘要。 | [P1] Demo | 员工侧能查看核心运营列表。 | U-008、U-009 |
| REQ-011 | 系统应支持知识缺口生命周期：发现、记录、人工确认、入库候选、关闭。 | [P1] Demo，[P2] 强化 | 答不上问题进入缺口列表。 | U-004、U-007、U-009 |
| REQ-012 | 系统应生成可审计日志和日终摘要，避免记录真实敏感信息。 | [P1] Demo | 摘要包含会话数、转人工数、缺口数、未结案。 | U-003、U-008、U-011、U-012 |
| REQ-013 | 系统应提供 REST API 供 H5、Web 控制台和通知适配层调用。 | [P1] Demo | API 契约见 `docs/07-api-spec.md`。 | U-001、U-010 |
| REQ-014 | 系统应提供可替换的 Mock 数据与配置加载机制，避免把客户叙事硬编码到业务逻辑。 | [P1] Demo | 场景包数据可独立修改。 | U-005、U-006、U-007、U-009 |
| REQ-015 | 系统应提供本机运行与验证路径，覆盖 H5、后端、Web 控制台和 Mock 数据。 | [P1] Demo | 验证项见 `docs/09-verification.md`。 | U-012 |
| REQ-016 | 系统应实现隐私与安全基础约束，包括 Mock 标识、日志脱敏、禁止真实凭据和外部调用默认关闭。 | [P1] Demo | 日志不含 token、手机号、真实客户资料。 | U-011、U-012 |
| REQ-017 | 系统应支持场景包级数据源模式配置，至少区分 `demo_sandbox` 与 `customer_sandbox_readonly` 预留。 | [P2.5] Product Sandbox | 场景包可显示并读取当前数据模式；未配置真实数据时显示 Not configured / No-Go。 | U-013、U-016 |
| REQ-018 | 系统应按场景包隔离模拟知识、模拟业务记录、历史会话、缺口、转人工记录和摘要。 | [P2.5] Product Sandbox | 切换场景包不会串用另一套模拟数据或运行态。 | U-014、U-015 |
| REQ-019 | 系统应提供 Demo Sandbox 初始化 / 重置能力。 | [P2.5] Product Sandbox | 重置后会话、缺口、转人工、通知和摘要恢复到演示初始态，且不影响其他场景包。 | U-015、U-018 |
| REQ-020 | 系统应提供虚拟客户资料包加载机制。 | [P2.5] Product Sandbox | H5 / Console 可基于公司背景、产品目录、FAQ、订单、项目、售后、人员角色和历史会话展示完整演示语境。 | U-014、U-019 |
| REQ-021 | 真实数据模式启用前必须检查客户授权、字段映射、安全评审和只读配置。 | [P3B] 真实集成 | 未满足门禁时不调用真实系统，只显示 No-Go / Not configured。 | U-013、U-017 |
| REQ-022 | 所有回答、通知、摘要、日志和 API 响应应带数据来源标识。 | [P2.5] Product Sandbox | UI / API 可看到 `source_mode`、`scenario_pack`、`source_ref` 与 `mock` / `real` 标识。 | U-013、U-015、U-016 |

## 3. 非功能需求

| NFR-ID | 需求 | 阶段 | 说明 |
|---|---|---|---|
| NFR-001 | 本机可运行 | [P1] | Windows + PowerShell 环境下可运行 Demo；Docker 不可用时允许降级。 |
| NFR-002 | 可追溯 | [P1] | 回复、转人工、缺口、通知都需保留来源和状态。 |
| NFR-003 | 可配置 | [P1] | 场景包、知识条目、Mock 业务数据与规则独立于业务逻辑。 |
| NFR-004 | 安全默认关闭 | [P1] | 外部 API、LLM、飞书真实通知、真实业务系统接入默认关闭。 |
| NFR-005 | 可测试 | [P1] | 每个 REQ 至少有一条手工或接口验证用例。 |
| NFR-006 | 可演示 | [P1] | Demo 流程不依赖真实生产数据和公司服务器。 |
| NFR-007 | 数据模式透明 | [P2.5] | H5、Console、API、日志和摘要均需显示当前数据源模式与来源。 |
| NFR-008 | 数据隔离可重置 | [P2.5] | 不同场景包、模拟数据、演示运行态和真实数据空间必须隔离；演示数据可重置。 |
| NFR-009 | 产品级逼真试用 | [P2.5] | 模拟数据应覆盖完整客户旅程、业务记录和运营后台，支撑销售演示、试用和培训。 |

### 3.1 质量需求映射（Q-ID → NFR-ID → REQ-ID / TC-ID）

> 质量需求（Q-ID）定义见 `docs/01-user-requirements.md` §2，非功能需求（NFR-ID）见本文件 §3，REQ / TC 追溯见 §6。

| Q-ID | 质量需求 | NFR-ID | REQ-ID | TC-ID |
|---|---|---|---|---|
| Q-001 | 响应可解释 | NFR-002 可追溯 | REQ-004、REQ-005 | TC-004、TC-005 |
| Q-002 | 入口简单 | NFR-006 可演示 | REQ-001 | TC-001 |
| Q-003 | 风险可控 | NFR-002 可追溯 | REQ-005、REQ-006 | TC-005、TC-006 |
| Q-004 | 数据可替换 | NFR-003 可配置 | REQ-007、REQ-014 | TC-007、TC-014 |
| Q-005 | 本机可跑 | NFR-001 本机可运行 | REQ-015 | TC-015 |
| Q-006 | 隐私最小化 | NFR-004 安全默认关闭 | REQ-016 | TC-016 |
| Q-007 | 产品级逼真试用 | NFR-009 产品级逼真试用 | REQ-018、REQ-020 | TC-018、TC-020 |
| Q-008 | 数据模式透明 | NFR-007 数据模式透明 | REQ-017、REQ-022 | TC-017、TC-022 |
| Q-009 | 数据隔离可重置 | NFR-008 数据隔离可重置 | REQ-018、REQ-019、REQ-021 | TC-018、TC-019、TC-021 |

- NFR-005（可测试）为横切需求：每个 REQ 至少一条手工或接口验证用例，覆盖全部 TC-001~TC-022，不单独绑定某个 Q-ID。
- Q-002（入口简单）主要由 REQ-001 驱动；NFR-006 体现「不依赖真实生产数据 / 公司服务器即可演示」的可达性。

## 4. 数据与接口需求

- 数据对象至少包括：会话、消息、意图结果、知识条目、规则条目、场景包、Mock 订单 / 项目 / 售后记录、转人工记录、知识缺口、通知记录、日报摘要。
- Product Sandbox 新增或显式化数据对象：`DataSourceMode`、`DemoDataset`、`VirtualCustomerProfile`、`DemoRuntimeState`、`SourceRef`。
- Phase1 可使用 PostgreSQL + pgvector 设计作为目标结构，但实现可先用内存、JSON 或轻量本地存储降级；降级不得改变 API 契约。
- H5 与 Web 控制台统一调用后端 REST API；飞书机器人真实调用默认关闭，仅保留适配层契约。
- `demo_sandbox` 为默认允许模式；`customer_sandbox_readonly`、`production_readonly`、`production_writeback` 仅作后续模式预留，未满足门禁前不得调用真实系统。

## 5. 边界与异常

| 场景 | 系统行为 |
|---|---|
| 无匹配知识 | 不编造答案，生成知识缺口并建议转人工。 |
| 高风险售后 / 投诉 | 不承诺赔付、价格、交期或法律责任，生成转人工记录。 |
| Mock 数据不存在 | 明确说明未查到 Mock 记录，提示人工确认。 |
| 外部通知未启用 | 记录通知 payload 和日志，不实际发送。 |
| 用户输入敏感信息 | Demo 不保存真实敏感值，必要时做脱敏提示。 |
| 真实数据模式未授权 | 不调用真实系统，显示 `Not configured / No-Go`，并保留门禁失败原因。 |
| 真实数据不可用 | 不编造业务结果；允许降级到 `demo_sandbox`，但 UI / API 必须明确标识当前为模拟数据。 |
| 场景包数据源切换失败 | 保持原数据源模式，不混用数据，提示运营人员重试或转人工确认。 |
| Demo 重置失败 | 不删除真实配置；保留失败日志并提示人工处理。 |

## 6. 需求追溯矩阵

| REQ-ID | 主要模块 | 数据对象 | API | 验证用例 |
|---|---|---|---|---|
| REQ-001 | H5 对话页、会话 API | `Conversation`、`Message` | API-001、API-002 | TC-001 |
| REQ-002 | 会话服务 | `Conversation`、`Message` | API-002、API-003 | TC-002 |
| REQ-003 | 意图路由服务 | `IntentResult` | API-002 | TC-003 |
| REQ-004 | 知识与规则服务 | `KnowledgeItem`、`RuleItem` | API-002、API-006 | TC-004 |
| REQ-005 | 安全回答策略 | `AuditLog`、`HumanHandoff` | API-002、API-004 | TC-005 |
| REQ-006 | 转人工服务 | `HumanHandoff`、`Notification` | API-004、API-009 | TC-006 |
| REQ-007 | 场景包服务 | `ScenarioPack` | API-010、API-011 | TC-007 |
| REQ-008 | Mock 业务适配层 | `MockBusinessRecord` | API-007、API-008 | TC-008 |
| REQ-009 | 通知适配层 | `Notification` | API-009 | TC-009 |
| REQ-010 | Web 控制台 | 多对象聚合 | API-003、API-004、API-005、API-012 | TC-010 |
| REQ-011 | 知识缺口服务 | `KnowledgeGap` | API-005、API-006 | TC-011 |
| REQ-012 | 摘要与审计服务 | `DailySummary`、`AuditLog` | API-012 | TC-012 |
| REQ-013 | API 层 | 全部 | API-001~API-012 | TC-013 |
| REQ-014 | 配置与 Mock 数据层 | `ScenarioPack`、`MockBusinessRecord` | API-007、API-010 | TC-014 |
| REQ-015 | 本机运行方案 | 不适用 | 不适用 | TC-015 |
| REQ-016 | 安全与隐私控制 | `AuditLog` | 全部 | TC-016 |
| REQ-017 | 数据源模式服务、场景包服务 | `DataSourceMode`、`ScenarioPack` | 待设计 | TC-017 |
| REQ-018 | Demo 数据集服务、配置与 Mock 数据层 | `DemoDataset`、`ScenarioPack`、`DemoRuntimeState` | 待设计 | TC-018 |
| REQ-019 | Demo 初始化 / 重置服务 | `DemoRuntimeState`、`AuditLog` | 待设计 | TC-019 |
| REQ-020 | 虚拟客户资料包服务 | `VirtualCustomerProfile`、`DemoDataset` | 待设计 | TC-020 |
| REQ-021 | 真实数据门禁、集成适配层 | `DataSourceMode`、`SourceRef`、`AuditLog` | 待设计 | TC-021 |
| REQ-022 | 来源标识与审计服务 | `SourceRef`、`AuditLog` | 全部相关 API | TC-022 |

## 7. 人工确认记录

- Phase1 前端默认方案已确认采用 React + Vite + TypeScript。
- Phase1 数据存储已确认优先使用 JSON / SQLite / 内存 Mock，不强制 PostgreSQL。
- 飞书真实通知不纳入 Phase1，仅记录 Mock payload。
- Phase1 不启用 LLM；如后续启用，需另补安全、成本、不编造和审计边界。
- 2026-07-15 已确认 Phase2.5 / Phase3A Product Sandbox 需求方向：默认使用场景包独立模拟数据，真实数据模式仅预留并需授权 / 安全评审后启用。
