# TEMPLATE-UPGRADE：Web 交互型系统代码框架与 Walking Skeleton 门禁

> 来源：zhiyan-digital-cs-platform（emily8421/zhiyan-digital-cs-platform）派生项目回流
> 类型：模板优化提案草稿
> 状态：已提交模板仓 issue，待模板维护者处理
> 模板仓 issue：https://github.com/emily8421/ai-project-template/issues/186
> 关联：`ai/document-lifecycle-rules.md`、`ai/implementation-lifecycle-rules.md`、`ai/doc-standards/frontend-interaction.md`、`ai/prompts/dev/02-run-task.md`、`ai/prompts/review/10-docs-checklist.md`、`template-docs/`

## 1. 背景与问题

Web 后端 + 前端交互界面的系统通常会从本机 Demo 或 MVP 的基本功能开始，按 Sprint / Task 小步实现。该路径能降低单次任务风险，但在缺少代码框架门禁时，容易出现以下问题：

- 初期为了快速跑通，把页面、状态、API 调用、表单、列表、详情和样式集中写入少数入口文件。
- 后续功能逐步增加后，前端单文件持续膨胀，修改字体、布局、表单或 Tab 时都可能触碰同一个大文件。
- 后端服务可能已经分层跑通，但前端交互仍停留在简陋或临时拼装状态，不利于演示和验收。
- 前端交互设计文档可列出页面、状态和组件，但实现阶段没有强制把这些结构落到代码目录。
- AI 后续执行任务时倾向“就近修改现有 App 文件”，而不是先拆分页面、feature、组件和 API 层，导致越改越重。
- Reviewer 难以通过目录职责判断改动是否越界，也难以自动化检查文件膨胀、页面 / 组件 / API / 验收追溯关系。

该问题不限于某个技术栈。只要项目包含 Web 管理台、H5、后台配置页、数据管理页、复杂表单、多 Tab、多角色、多状态或演示依赖点击路径，都可能触发。

## 2. 建议目标

在母模板中新增一个轻量、可选的 **Web App Structure Profile**，并引入 **Walking Skeleton Gate**：

1. 对 Web 交互型项目，编码前必须先有最小代码框架方案。
2. 第一批前端任务应优先建立可运行的 app shell / layout / routing / API client / shared types / 状态组件 / smoke 检查，而不是直接把业务功能堆进入口文件。
3. 后续仍按小任务增量实现功能，但每个任务必须落在既定目录职责内。
4. 当入口文件或样式文件膨胀到阈值时，必须先触发拆分 / 重构门禁，再继续加功能。
5. 该 profile 只规定通用结构和评审规则，不绑定具体业务、UI 组件库、状态库或领域模型。

## 3. 建议改动

### 3.1 新增 Web App Structure Profile

建议新增模板文档，例如：

```text
template-docs/web-app-structure-profile.md
```

建议内容包含：

- 适用条件：独立 Web / H5 / Console / 管理后台 / 多页面 / 多角色 / 多状态 / 复杂表单 / 演示依赖点击路径。
- 编码前输入：`03` Phase、`04/05` 技术边界、`07` API、`docs/design/frontend-interaction.md`、`08/09` 验收目标。
- 输出：前端目录结构草案、页面 / route 清单、feature 边界、shared API / types 位置、状态组件策略、smoke 检查方式。
- 禁止项：不为简单页面强制重型架构；不引入未经确认的新依赖；不把权限只做前端隐藏；不提前实现后续 Phase 功能。

### 3.2 推荐最小前端目录结构

母模板可给“推荐结构”，项目可按技术栈裁剪：

```text
frontend/
  <entry-or-app>/
    src/
      app/              # App shell、provider、router/bootstrap、全局 layout
      pages/            # 页面入口，组合 feature 和 components
      features/         # 业务功能区，含局部组件、hooks、services、state
      components/       # 跨页面通用 UI 组件
      hooks/            # 通用 hooks
      styles/           # tokens、layout、组件样式或样式入口
      main.tsx
  shared/
    api/                # API client / endpoint wrappers
    types/              # 跨入口共享类型
    utils/              # 无业务状态的工具函数
```

对于多入口项目，可保留多个 entry，例如 `customer-h5/`、`console/`，但共享 API、类型和无状态工具应集中到 `frontend/shared/` 或等价位置。

### 3.3 推荐后端目录结构规则

母模板可保留当前通用后端分层建议，并在 Web profile 中明确前后端协作边界：

```text
backend/app/
  api/ or routes/       # HTTP endpoint
  services/             # 业务编排
  schemas/              # request / response / DTO
  repositories/ or data/# 数据访问 / Mock / persistence
  adapters/             # 外部系统 / LLM / notification / integration
  core/                 # config / permissions / common policies
  main.py
```

约束：前端不得直接读取后端数据文件；后端权限必须在 API / service 层执行；外部系统访问必须经 adapter。

### 3.4 Walking Skeleton Gate

建议在 `ai/implementation-lifecycle-rules.md` 或 `ai/prompts/dev/02-run-task.md` 中加入：

触发 Web App Structure Profile 后，第一个前端实现 Sprint / Task 应优先完成 walking skeleton：

- app shell / 基础 layout。
- route / page 占位。
- API client 与共享类型。
- loading / error / empty / disabled / success 状态组件。
- Demo / Mock / 非生产边界提示。
- 至少一个只读 API smoke 或 Mock 数据 smoke。
- 本机演示入口与检查命令。

Walking skeleton 不等于实现全部功能，只保证后续功能有稳定落点、可演示路径和验证入口。

### 3.5 文件膨胀与重构门禁

建议给出默认阈值（可项目覆盖）：

| 触发条件 | 建议动作 |
|---|---|
| 单个 `App.*` 超过 300–400 行 | 后续功能前拆出 pages / features / components |
| 单个样式文件超过 400 行 | 拆分 tokens / layout / components / feature styles |
| 单入口内超过 3 个 route / tab / 主要页面区 | 建立 pages / features 目录 |
| 一个文件同时承担 API、状态、表单、列表、详情、布局 | 拆分 API / hook / component / page 职责 |
| 新任务主要是改布局 / 字体 / 表单但会触碰大入口文件 | 先做局部结构拆分，再做功能变更 |

阈值触发后，AI 应先说明重构计划、影响范围、验证方式，并等待用户确认；不得在大文件上继续叠功能。

### 3.6 前端交互设计到代码结构的追溯

建议扩展 `ai/doc-standards/frontend-interaction.md` 或相关 prompt，要求前端交互设计增加一张“页面 / 组件 / feature / API / 验收”映射表：

| 页面 / 区域 | 代码落点 | Feature | API | 状态 | 验收 |
|---|---|---|---|---|---|
| 页面或 Tab | `pages/...` | `features/...` | API-ID | loading / empty / error 等 | TC-ID |

实现任务应引用该映射，代码偏离时回写设计或任务单。

### 3.7 审查与验证建议

建议在 `docs-checklist` / `project-review` / `sprint-summary` 增加 Web profile 检查项：

- 是否触发 Web App Structure Profile。
- 是否已有 walking skeleton 或明确豁免。
- 新功能是否落在对应 feature / page / API client，而不是继续堆入口文件。
- 是否包含页面 smoke、API proxy smoke 或手工演示路径。
- 是否存在权限只靠前端隐藏的风险。
- 是否需要重构门禁。

## 4. 母模板与领域模板边界

本提案建议先放在母模板，而不是立即派生领域模板。

理由：

- Web / H5 / Console / 管理后台是交付形态，不是单一业务领域。
- 目录职责、walking skeleton、文件膨胀门禁、页面 / API / 验收追溯属于跨项目通用工程约束。
- 母模板可用“可选 profile + checklist”承载，不必下发重型脚手架或业务组件。
- 领域模板机制仍处候选 / 实验阶段，不宜让普通派生项目先承担三层同步复杂度。

但可保留未来迁移条件：当多个同类管理系统持续复用更具体的标准件（例如权限、审批、审计、数据链、功能库、用例库、项目管理等领域模型和页面模式）时，再考虑建立 `management-system-template` / `plm-system-template` 等领域模板。

## 5. 影响面

可能影响：

- `ai/document-lifecycle-rules.md`：补充 Web App Structure Profile 触发条件。
- `ai/implementation-lifecycle-rules.md`：补充 walking skeleton 和文件膨胀门禁。
- `ai/doc-standards/frontend-interaction.md`：补充代码落点映射。
- `ai/prompts/dev/02-run-task.md`：执行前检查目录职责与重构门禁。
- `ai/prompts/review/10-docs-checklist.md` / `03-project-review.md`：补充 Web profile 审查项。
- `template-docs/web-app-structure-profile.md`：新增推荐结构与 checklist。

## 6. 验收建议

模板侧可用以下方式验证：

1. 对一个包含 H5 + Console 的派生项目，检查 AI 是否能在首个前端任务前建议 walking skeleton。
2. 当现有 `App.*` 超过阈值时，AI 是否提示先拆分而不是继续叠功能。
3. 前端交互设计中的页面 / 组件是否能追溯到代码目录和 TC。
4. 新功能 PR 是否能通过目录职责审查：page 组合、feature 局部逻辑、shared API / types 分离。
5. 简单 Lean 项目是否可以写明豁免，不被强制套用复杂目录。

## 7. 待确认项

| ID | 待确认项 | AI 建议 | 建议依据 | 备选方案 | 取舍影响 / 阻塞关系 |
|---|---|---|---|---|---|
| WEB-STRUCT-C-001 | 是否在母模板新增 `Web App Structure Profile`？ | 建议新增为可选 profile。 | Web 交互型项目存在跨项目共性，且不属于单一业务领域。 | 只加强前端交互文档，不新增 profile。 | 不新增 profile 会继续缺少实现层门禁。 |
| WEB-STRUCT-C-002 | 是否规定默认目录结构？ | 建议给推荐结构，不强制文件名完全一致。 | 统一评审和 AI 定位需要共同语言。 | 只给原则不给结构。 | 原则过虚，AI 仍可能就近堆大文件。 |
| WEB-STRUCT-C-003 | 文件膨胀阈值是否写死？ | 建议写默认阈值，并允许项目覆盖。 | 阈值能触发重构门禁，但不同项目复杂度不同。 | 不设阈值，只靠人工判断。 | 无阈值会降低自动审查能力。 |
| WEB-STRUCT-C-004 | 是否现在拆领域模板？ | 不建议现在拆；先在母模板做轻量 profile。 | 领域模板机制尚在候选，Web 结构是通用交付形态。 | 立即启动管理系统领域模板。 | 过早拆领域模板会增加同步复杂度。 |

## 8. 非目标

- 不强制所有项目使用 React / Vite / TypeScript。
- 不强制引入 UI 组件库、路由库、状态管理库或 E2E 框架。
- 不要求简单单页工具套用复杂目录。
- 不把业务领域模型写入母模板。
- 不替代 `docs/design/frontend-interaction.md`，而是补充其到代码结构的落地门禁。
