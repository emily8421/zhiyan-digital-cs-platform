# BEGINNER-GUIDE

> Sync notice: This file is maintained by `ai-project-template` and may be overwritten when a derived project syncs template methodology.
> Do not edit it directly in derived projects; propose reusable changes in `_proposals/` and upstream them to the template repository.

本手册面向第一次使用 `ai-project-template` 的人。它回答"先做什么、每一步产物是什么、卡住时去哪看"；规则正文仍以 `ai/` 和 `docs/` 里的活文件为准。

如果你是第一次用，先看 `README.md`（它能做什么 + 快速开始），再把本手册当「理解模板设计 + 心智模型 + 常见错误」的参考。具体操作走 `template-docs/scenario-guides.md` 场景引导。

## 1. 这份手册适合谁 + 先建立正确预期

适合：

- 第一次使用这套模板的新手。
- 会开发，但还不熟悉 AI 协作开发流程的人。
- 想先跑通一遍最小路径，再逐步理解完整体系的人。

先建立正确预期：

- 这不是"给 AI 一个想法，然后直接生成整个项目"的模板。
- 这是一套"确认机器可用 → 准备输入材料 → 采集本机环境 → 生成或补齐文档体系 → 按 Sprint 小步开发"的模板。
- AI 不能替代项目边界、需求来源和验收标准；这些要先由人提供或确认。
- 新手最容易卡住的不是文档编号，而是机器还没准备好就直接运行 `new-project.sh` 或让 AI 开始写代码。

## 2. 怎么起步

> Keyword for template checks: newbie AI CLI onboarding path.

**起步走场景引导**：在项目根目录打开 AI CLI（`Claude CLI` / `Codex CLI`），说一个具体场景或 `/run scenario`，AI 会按 `template-docs/scenario-guides.md` 给「做什么 + 为什么」引导计划，确认后逐步执行——不用记具体步骤。

开工前只需确认这些（命令与排障见 scenario-guides A1）：

1. 基础环境：`scripts/check-prereqs.ps1`；缺工具按 `template-docs/env-setup.md` 运行 `scripts/bootstrap-dev-env.ps1`。
2. AI CLI：官方文档安装并登录 `Claude CLI` 或 `Codex CLI`（见 `template-docs/ai-cli-setup.md`）。
3.（可选）验证新手链路：`template-docs/smoke-test.md` + `template-docs/smoke-test-report-template.md`。
4.（公司环境）中转站 / LeMesh / CC-Switch 见内网手册（`lemesh_ai_model`），不替代 CLI 官方安装。

> 没装 AI CLI？先按 `template-docs/ai-cli-setup.md` 安装；纯本地烟测可暂不装。

## 3. 开工前你需要准备什么

- 愿景文档、客户 PRD、SRS、任务说明、现有系统说明，至少要有一种明确输入。
- 本机环境和资源信息，尤其是 Python / Node / Docker / 数据库等是否可用。
- 必备基础工具：Git for Windows、Git Bash、PowerShell。
- 至少一种 AI CLI 工具：`Claude CLI` 或 `Codex CLI`。
- 当前阶段的允许项、禁止项、下一阶段预告。
- 技术栈倾向和禁区，不要让 AI 猜。
- 项目形态裁剪：是否需要 `docs/06`、`docs/07`、`frontend/`、`backend/`、`tests/`、`docker/`。

如果公司要求通过内部中转站访问模型，先看：

- `http://192.168.30.51:50088/994_wiki/?term=lemesh_ai_model`

这份内网手册更适合用来处理 LeMesh / CC-Switch / 公司中转站代理配置，不应直接当作 `Claude CLI` 或 `Codex CLI` 的官方安装文档。

推荐顺序：

1. 先按官方文档安装并登录 `Claude CLI` 或 `Codex CLI`。
2. 再按这份内网手册处理公司中转站、密钥和代理接入。
3. 具体代理、地址、鉴权或环境变量配置，以这份内网手册为准。

## 4. 文档与目录怎么理解

### docs/ 核心文档（项目事实）

| 文件 | 作用 |
|---|---|
| `docs/00-scenario.md` | 工程想定、背景和典型场景 |
| `docs/01-user-requirements.md` | 用户需求全集与来源 |
| `docs/02-srs.md` | 系统需求规格和 REQ |
| `docs/03-prd.md` | 当前阶段功能范围和路线图 |
| `docs/04-architecture.md` | 总体模块、边界和运行拓扑 |
| `docs/05-tech-spec.md` | 技术选型、依赖、降级与资源策略 |
| `docs/06-db-design.md` | 数据模型与存储设计；无持久化可省略 |
| `docs/07-api-spec.md` | 接口或命令契约；无对外接口可省略 |
| `docs/08-dev-plan.md` | Sprint / task 拆分、验收标准和禁止事项 |
| `docs/09-verification.md` | 验证矩阵、验收与资源验证口径 |

### docs/ 子目录

- `docs/vision/`：愿景、叙事、业务背景等输入。
- `docs/inputs/`：尚未归类的原始输入包。
- `docs/design/`：项目子系统详细设计，不是模板方法论文档。
- `docs/decisions/`：ADR 和关键取舍。
- `docs/research/`：调研、实验和可行性结论。
- `docs/env/`：本机环境、资源约束、服务器预案。
- `docs/meetings/`：会议纪要、访谈、评审记录。
- `docs/archive/`：已废弃但需要留痕的项目文档。

### ai/ 目录（AI 行为规范）

- `ai/index.md`：路由表，决定 AI 要先读哪些规则。
- `ai/global-rules.md`：跨项目通用规则。
- `ai/document-lifecycle-rules.md`：文档怎么生成、追溯、传播和裁剪。
- `ai/project-rules.md`：本项目自己的边界和禁区。

> 操作（生成文档、执行任务、用命令等）不在本手册重复——走 `template-docs/scenario-guides.md` 场景引导；命令速查看 `SOP.md`。

## 5. 常见错误与常见问题

### 常见错误

- 只有一句想法，没有上游输入材料，就直接让 AI 生成代码。
- 没先跑环境检查，就直接执行 `new-project.sh`，结果把 Git Bash / PowerShell / PATH 问题误判成模板问题。
- 没填 `ai/project-rules.md`，就开始生成设计文档。
- 把愿景功能直接当当前阶段需求。
- 把模板自身文档和派生项目过程文档混在一起。
- 一次让 AI 改太多文件，最后无法验收。
- 没有验证记录，就认为任务已经完成。

### 常见问题

- 什么时候省略 `docs/06` 和 `docs/07`：看 `ai/project-rules.md` §3 和 `docs/README.md` 的裁剪决策表。
- 什么时候需要 `tasks/`：当 `docs/08-dev-plan.md` 里的某个 Sprint 已经复杂到需要拆成多个独立任务。
- 什么时候需要 `docs/design/`：当某个子系统已经非平凡，光靠 `docs/04` / `docs/05` 不够表达内部逻辑。
- 什么时候需要服务器预案：当本机资源不能支撑当前阶段 Demo / MVP，且不能通过降级或 Mock 解决时。
- 切换 AI 工具怎么办：规则不变，先记录当前进度，再让新工具从 `ai/index.md` 和当前 Sprint 继续。
