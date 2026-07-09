# 项目专属规则

> 本文件每个新项目都需要重新填写，不参与跨项目同步。
> 判断标准：一条规则换到另一个完全不同的项目上是否还成立——
> 不成立（涉及具体技术栈/具体功能/具体Phase定义）就属于本文件。
>
> 当前内容为 `post-sync-cleanup` 后的项目草稿，依据 `docs/meetings/2026-07-01-input-review.md`、
> `docs/inputs/platform-vision-brief.md`、`docs/inputs/agent-delivery-modes.md` 与
> `docs/env/local-env.md` 起草；Phase1 关键口径已于 2026-07-04 人工确认；Phase2 Conditional Go 已于 2026-07-09 人工确认（见 `docs/research/2026-07-06-phase-upgrade-evaluation.md`、`docs/research/2026-07-09-docs-open-items.md` DOC-C-001~C-005）。

## 初始化必填检查（生成 docs/03-09 前）

- `项目名称` 与 `代号/缩写`：已确认，缩写为 `zycs`，数据库表前缀为 `zycs_`。
- `§1 Phase边界`：已确认 Phase2 MVP 试点边界（2026-07-09；Phase1 本机 Demo 已通过验收）。
- `§2 技术栈约束`：已确认 React + Vite + TypeScript、Python + FastAPI；Docker / PostgreSQL 不强制纳入 Phase1。
- `§2.5 运行环境与资源约束`：已生成 `docs/env/local-env.md`，Phase1 默认本机 Demo，不使用公司服务器。
- `§3 项目形态与文档裁剪`：已起草保留 `docs/06`、`docs/07` 与主要代码目录。
- 新增项目文档必须继续遵守 `docs/README.md` 分区规则，不得直接堆到 `docs/` 根目录。

## 0. 项目标识

项目名称：知衍数字客服统一平台（zy-digital-cs）

代号/缩写：zycs；数据库表前缀：`zycs_`。

## 1. Phase边界

当前阶段：Phase2（MVP 试点；在 Phase1 本机 Demo 闭环基础上强化运营可用性，面向单个试点客户）

> Phase1 已通过本机 Demo 验收（2026-07-06，见 `docs/09-verification.md` §6）；Phase2 Conditional Go 已人工确认（2026-07-09，DOC-C-001~C-005 全按 AI 推荐）。

允许：
- 在保留 H5 + Web 控制台 + FastAPI 主链路的基础上，强化知识库、知识缺口审核、运营配置和基础权限。
- 将飞书通知从 Mock payload 推进到试点评估 / 沙箱联调，但不得默认接入真实组织数据（DOC-C-003）。
- 以单个试点客户为目标，规划部署、演示数据、运营流程和验收路径（DOC-C-002）。
- 继续保留 Mock 订单 / 项目数据作为默认降级路径。
- 为 PostgreSQL / pgvector、飞书回调、部署脚本等补充技术验证任务（DOC-C-004：先技术验证，不作全部功能前置）。

禁止：
- 不直接接入真实 CRM / ERP / OA / 工单系统，除非已有接口授权、数据边界和安全评审（Phase3 范围）。
- 不处理真实客户隐私、合同、订单、报价、联系方式或生产会话。
- 不启用通用 LLM 自动答复，除非先完成证据约束、不编造、成本与兜底评估（DOC-C-005：Phase2 仅评估，不默认启用）。
- 不把试点能力包装为多租户、计费、监控、审计等产品化平台能力（Phase4 范围）。
- 不绕过人工确认引入新依赖、Docker 镜像、外部 SaaS API 或付费服务。
- AI 不做售后高风险裁决；高风险场景必须转人工或规则化引导。
- 无外部数据或数据不足时不得编造订单、项目进度、库存、报价、合同等业务事实。

下一阶段预告：
- Phase3 可在试点客户授权后接入 CRM / ERP / OA / 飞书项目 / 工单等真实业务系统。
- Phase4 再考虑多租户、计费、监控、审计、插件化场景包和产品化运营。

Conditional Go 保留条件（Phase2 全程有效）：

1. Phase2 先做 MVP 试点，不直接进入 Phase3 真实集成。
2. 真实飞书 / 业务系统 / LLM / PostgreSQL·pgvector 仍需单独技术验证、授权边界与安全评审。
3. 任何新依赖、Docker 镜像、外部 SaaS API 或付费服务必须先人工确认。
4. Phase2 继续保留 Mock / 降级路径。

## 2. 技术栈约束

- 客户侧前端：H5 对话页，React + Vite + TypeScript。
- 员工侧前端：Web 控制台，React + Vite + TypeScript。
- 员工通知入口：飞书机器人；仅用于 Demo 通知 / 转交，不替代完整工单系统。
- 后端：Python + FastAPI。
- 数据库：PostgreSQL + pgvector 为计划方向；Phase1 不强制运行，优先 JSON / SQLite / 内存 Mock 降级。
- 向量 / Embedding：Docker TEI 方案作为候选；Phase1 默认关闭，使用关键词 / 规则匹配降级。
- 外部业务数据：Phase1 使用 Mock 数据，不接真实订单、项目、CRM、ERP 或工单系统。
- LLM：Demo 阶段默认不启用；如后续启用，必须先补充不编造、可追溯、转人工兜底与成本边界。
- 新依赖：任何新依赖、Docker 镜像或外部 API 调用必须先人工确认。

## 2.5 运行环境与资源约束

> 本节用于约束架构与技术方案选择。Demo / MVP 阶段优先保证本机可运行；若本机资源不足，必须在 `docs/05-tech-spec.md` 中明确降级策略或服务器资源预案。

- 本机环境文档：`docs/env/local-env.md`（已由 `scripts/collect-env.ps1` 生成，Phase1 关键资源口径已确认）
- 当前本机概要：Windows 10 / PowerShell 5.1 / 约 31.73 GB 内存 / Python 3.14.3 / Node.js 22.17.1 / Docker 已安装但当前不可用 / 未检测到 GPU 信息。
- Demo 阶段必须能在本机运行的部分：H5 对话页、FastAPI 后端、Web 控制台、Mock 数据、基础手工验证；数据库与向量服务不作为 Phase1 前置。
- 允许降级 / Mock / 远程运行的部分：订单 / 项目进度等外部业务系统、Embedding / 向量检索、飞书通知；LLM 默认关闭。
- 禁止在本机运行的重资源部分：本地大模型推理、模型训练、生产规模向量索引、真实生产数据处理。
- 是否允许使用公司服务器：Phase1 默认不使用公司服务器。
- 若需服务器，资源申请口径：仅当本机无法支撑 Demo 时另行确认触发条件、CPU / 内存 / GPU / 端口 / 成本 / 安全边界。

## 2.7 UI 原型策略

> 依据 `ai/global-rules.md` §5.3 / `ai/document-lifecycle-rules.md` §5.3。本项目为 UI 型（H5 客户对话页 + Web 控制台），记录 UI 原型策略以闭合规范要求。

- **主策略：代码原型（engineering-driven）**。H5 与 Console 直接用真实技术栈（React + Vite + TypeScript）实现可运行原型，配合 Mock 数据验证交互；不引入 Figma / Penpot 等独立设计稿工具（当前无专职设计协作角色）。
- **补充：需求探索原型（按需）**。在需求阶段或新阶段 UX 不确定时，用低保真原型（ASCII 草图 + 自包含 HTML 静态页）与用户确认需求、页面结构、状态与文案，状态标为「探索 / 待确认」；产物落 `docs/research/YYYY-MM-DD-ui-prototype-exploration.md` + `docs/research/prototypes/*.html`，确认后回填 `00-03`，不替代需求 / 设计 / 验收。
- **前端交互权威**：页面信息架构、状态、文案、接口依赖、验收路径以 `docs/design/frontend-interaction.md` 为准；原型不替代它。
- **边界**：原型不锁定架构 / 技术栈 / 接口 / DB；不作为验收通过证据；不新增未授权需求。

## 3. 项目形态与文档裁剪

- 是否有持久化存储：有，计划使用 PostgreSQL + pgvector；Demo 可在必要时降级为 Mock / 本地临时数据。
- 是否有对外接口：有，至少包括 H5 / Web 调用后端的 REST API，以及飞书机器人通知 / 回调契约。
- 演示形态：独立 Web 页面（H5 对话页 + Web 控制台）+ 飞书机器人通知；不采用消息通道内交互作为客户侧主入口。
- docs/06-db-design.md：保留。
- docs/07-api-spec.md：保留。
- 需要保留的代码目录：`frontend/`、`backend/`、`tests/`、`scripts/`、`docker/`、`tasks/`。

按项目形态裁剪说明：
- `frontend/` 保留，用于 H5 对话页与 Web 控制台。
- `backend/` 保留，用于 FastAPI 服务、知识 / 场景 / Mock 数据 / 集成层。
- `docker/` 保留，用于 PostgreSQL / pgvector / TEI 等本地服务编排；当前 Docker 可用性待修复确认。
- `tests/` 保留，用于接口、规则、场景包与验收用例。
- `docs/design/` 后续用于拆分 H5、Web 控制台、后端服务、知识库、场景包、Mock 集成层等详细设计。
- `docs/decisions/` 后续用于记录入口选择、企微客户群自动回复证伪、高风险转人工、不编造等决策。

## 4. 目录规范的项目特例

- 无，整体遵循 `ai/global-rules.md` 通用目录标准。
- `_archive/`、`_examples/` 如后续确认无项目用途，可单独开清理任务；本次不删除。
- `template-docs/`、`ai/doc-standards/` 属于模板方法论 / 规范镜像区域，不直接写入项目事实。

## 5. 编码约定与禁区

> Phase 级功能禁止见 §1，技术栈替代品禁止见 §2，本节只管代码层。

### 5.1 既有约定（新代码必须向其看齐）
- 命名：后端 Python 使用 `snake_case`；前端变量 / 函数使用 `camelCase`，组件使用 `PascalCase`；数据库表使用 `zycs_` 前缀。
- 分层与目录：后端至少区分 API 层、服务层、数据 / Mock 层、集成适配层；前端至少区分客户 H5、员工 Web 控制台、共享组件 / API 客户端。
- 场景包：产品型与项目型客户场景应以可追溯配置或数据文件表达，不得把客户叙事硬编码散落在业务逻辑中。
- 外部系统：所有订单、项目进度、CRM、ERP、工单等外部系统访问必须走适配层；Phase1 仅实现 Mock 适配。
- 错误处理 / 日志：不得在日志中输出真实隐私数据、访问 token、客户联系方式或敏感业务数据；Demo 阶段如使用样例数据，必须标明 Mock。

### 5.2 禁区（未经人工确认不得触碰）
- 不得擅改 `ai/` 中模板同步文件、`template-docs/`、`ai/doc-standards/`；通用改进走 `_proposals/`。
- 不得擅自引入新依赖、Docker 镜像、外部 SaaS API、LLM API 或付费服务。
- 不得接入真实企业微信会话存档、真实飞书组织数据、真实 CRM / ERP / 工单系统。
- 不得处理真实客户隐私数据、合同、订单、报价、联系方式或生产会话。
- 不得把 `docs/inputs/` 原始设想直接当作已批准实现范围；阶段归属以 `docs/03-prd.md` 路线图为准，编码以 §1 当前阶段为准。
- 不得在 `docs/00-09` 未补齐并人工确认前启动功能编码。

## 6. AI修改确认规则

- AI在进行任何文件新增、修改、删除、重命名、格式化、批量替换前，必须先说明计划、影响范围与预期变更文件，并等待用户明确确认后再执行。
- AI在运行任何可能写入文件、安装依赖、生成构建产物、修改配置或改变项目状态的命令前，必须先询问用户确认。
- 只读分析操作（如读取文件、搜索代码、查看 Git 状态）无需逐次确认，但不得借只读分析之名修改项目内容。
- 用户在单次消息中明确要求“直接修改”“执行修复”“不必确认”等同类授权时，仅对该次明确任务生效；后续新任务仍默认先确认再修改。
