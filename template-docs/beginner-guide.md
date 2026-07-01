# BEGINNER-GUIDE

> Sync notice: This file is maintained by `ai-project-template` and may be overwritten when a derived project syncs template methodology.
> Do not edit it directly in derived projects; propose reusable changes in `_proposals/` and upstream them to the template repository.

本手册面向第一次使用 `ai-project-template` 的人。它回答“先做什么、每一步产物是什么、卡住时去哪看”；规则正文仍以 `ai/` 和 `docs/` 里的活文件为准。

如果你是从 `README.md` 跳到这里，不需要再回 README 找下一步；按本手册继续操作即可。

## 1. 这份手册适合谁

- 第一次使用这套模板的新手。
- 会开发，但还不熟悉 AI 协作开发流程的人。
- 想先跑通一遍最小路径，再逐步理解完整体系的人。

## 2. 先建立正确预期

- 这不是“给 AI 一个想法，然后直接生成整个项目”的模板。
- 这是一套“确认机器可用 -> 准备输入材料 -> 采集本机环境 -> 生成或补齐文档体系 -> 按 Sprint 小步开发”的模板。
- AI 不能替代项目边界、需求来源和验收标准；这些要先由人提供或确认。
- 新手最容易卡住的不是文档编号，而是机器还没有准备好就直接运行 `new-project.sh` 或让 AI 开始写代码。

## 3. 先判断你处在哪种状态

| 你的状态 | 先做什么 | 下一步 |
|---|---|---|
| 不确定这台机器能不能跑模板 | 运行 `scripts/check-prereqs.ps1` | 缺必备工具时看 `template-docs/env-setup.md` |
| 机器缺 Git Bash / Node.js / Python 等基础工具 | 运行 `scripts/bootstrap-dev-env.ps1` 或手工安装 | 重开终端后再跑一次 `check-prereqs.ps1` |
| 只想验证新手链路是否通 | 按 `template-docs/smoke-test.md` 执行 | 用 `template-docs/smoke-test-report-template.md` 留痕 |
| 基础环境已通过检查 | 运行 `scripts/new-project.sh` 新建项目 | 进入项目后运行 `scripts/collect-env.ps1` |
| 已有派生项目，但还没环境记录 | 在项目根目录运行 `scripts/collect-env.ps1` | 补齐 `docs/env/local-env.md` 人工确认项 |
| 准备真正让 AI CLI 执行任务 | 至少安装并登录一种 AI CLI | 安装顺序看 `template-docs/ai-cli-setup.md` |

## 4. 照着做：从零开始的最小路径

优先推荐“AI CLI 引导模式”：新手只负责确认边界、输入和授权，具体命令由 AI 解释后辅助执行。若 AI CLI 尚未安装，先按本节的手动命令走到能安装 / 打开 AI CLI 为止。

### 路径 A：推荐，AI CLI 引导模式

> Keyword for template checks: newbie AI CLI onboarding path.

先确保两件事：

1. 基础环境检查能运行：`powershell -ExecutionPolicy Bypass -File scripts/check-prereqs.ps1`。
2. 至少一种 AI CLI 已安装并能打开：`Claude CLI` 或 `Codex CLI`；安装说明见 `template-docs/ai-cli-setup.md`。

然后在模板仓库或派生项目根目录打开 AI CLI，对它说：

```text
我是第一次使用这个 ai-project-template。请先读取 ai/index.md 和相关规则，
然后按新手 AI CLI 引导路径带我完成：
1. 检查基础环境
2. 判断是否需要安装/补齐工具
3. 新建本地项目
4. 采集本机环境
5. 准备上游输入
6. 评审输入材料
7. 生成文档体系

每一步执行命令前先说明目的和影响范围，需要我确认后再运行。
```

接下来你主要做三件事：

- 确认 AI 计划是否合理。
- 在需要写文件、安装依赖、运行会改变状态的命令前明确授权。
- 补充 AI 无法替你决定的信息，例如产品愿景、阶段边界、是否允许联网、是否允许 Mock、是否需要服务器。

### 路径 B：兜底，手动命令模式

#### 第一步：检查机器是否具备基础环境

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check-prereqs.ps1
```

看输出里的 `Summary` 和 `Suggested next steps`：

- 如果缺少必备项，先看 `template-docs/env-setup.md`，按需运行 `scripts/bootstrap-dev-env.ps1`。
- 如果只缺 `gh`，但你只做本地烟测或本地起步，可以先继续；远端建仓前再补 `gh auth login`。
- 如果 PowerShell 找不到 `bash`，但 Git Bash 已安装，可按 `template-docs/env-setup.md` 里的完整路径方式运行 Bash 脚本。

#### 第二步：新建本地项目

```bash
bash scripts/new-project.sh my-demo --local --no-remote
cd my-demo
```

#### 第三步：采集本机运行环境

```powershell
powershell -ExecutionPolicy Bypass -File scripts/collect-env.ps1
```

然后打开 `docs/env/local-env.md`，补齐“人工确认项”：本机必须跑通什么、哪些可以 Mock / 远程运行、是否允许联网、是否需要服务器预案。

#### 第四步：准备上游输入

至少准备一种可审计输入：

- 产品愿景：写入 `docs/vision/product-vision.md`。
- 小工具 brief / 客户 PRD / SRS / 现有系统说明：先放入 `docs/inputs/`。
- 明确任务单：确认已有 docs 是否足够支撑任务，不足时先补需求链路。

#### 第五步：让 AI 先评审，再生成文档体系

1. 初填 `ai/project-rules.md` 的 `§1`、`§2`、`§2.5`、`§3`，先把阶段边界、技术栈倾向、运行环境约束和项目形态写清楚。
2. 在 AI CLI 中说“评审输入材料”（或 `/run review-inputs`），让 AI 先确认入口模式、文档剖面、缺口和待确认项。
3. 评审通过后，再说“生成文档体系”（或 `/run generate-docs`），生成或补齐 `docs/00-09`。
4. 人工确认 `docs/03-prd.md`、`docs/05-tech-spec.md`、`docs/08-dev-plan.md` 后，再说“执行当前 Sprint”（或 `/run run-dev-task`）。

> 纯本地烟测可以暂时不安装 AI CLI；真正开始 AI 协作开发前，建议至少完成 `Claude CLI` 或 `Codex CLI` 其中一种的安装与登录。

## 5. 开工前你需要准备什么

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

## 6. 遇到这些情况再离开本手册

| 情况 | 去哪里 | 回到哪里继续 |
|---|---|---|
| 环境检查失败，或者不知道缺什么工具 | `template-docs/env-setup.md` | 本手册 §4 第一步 |
| 想验证新手链路是否真的可跑通 | `template-docs/smoke-test.md` | 本手册 §4 第二步 |
| 想记录一次烟测结果 | `template-docs/smoke-test-report-template.md` | 本手册 §4 第一步 |
| 要安装或登录 `Claude CLI` / `Codex CLI` | `template-docs/ai-cli-setup.md` | 本手册 §4 路径 A |
| 已经知道任务意图，但不知道对应命令或 Prompt | `SOP.md` 或 `ai/commands/README.md` | 对应命令执行完回到当前 Sprint |
| 想理解模板为什么这样设计 | `template-docs/template-methodology.md` | 不影响本手册最小路径 |

## 7. `docs/` 核心文档怎么理解

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

## 8. `docs/` 子目录怎么理解

- `docs/vision/`：愿景、叙事、业务背景等输入。
- `docs/inputs/`：尚未归类的原始输入包。
- `docs/design/`：项目子系统详细设计，不是模板方法论文档。
- `docs/decisions/`：ADR 和关键取舍。
- `docs/research/`：调研、实验和可行性结论。
- `docs/env/`：本机环境、资源约束、服务器预案。
- `docs/meetings/`：会议纪要、访谈、评审记录。
- `docs/archive/`：已废弃但需要留痕的项目文档。

## 9. `ai/` 目录怎么理解

- `ai/index.md`：路由表，决定 AI 要先读哪些规则。
- `ai/global-rules.md`：跨项目通用规则。
- `ai/document-lifecycle-rules.md`：文档怎么生成、追溯、传播和裁剪。
- `ai/project-rules.md`：本项目自己的边界和禁区。

## 10. 第一次生成文档体系怎么做

- 输入材料不确定时，先评审，不要直接让 AI 生成一整套文档。
- 先判断入口模式：Vision-first、PRD-first、Task-first、Existing-system 等。
- 再判断文档剖面：Full、Standard、Lean、Existing-system。
- 生成后重点检查四件事：范围是否越界、`docs/06` / `docs/07` 是否裁剪正确、Demo 是否真能在本机跑、`docs/08` 是否已经拆成可执行 Sprint。

## 11. 第一次执行任务怎么做

- 一次只执行一个 Sprint 或一个 task。
- 执行前先读相关 `docs/03-09` 和 `ai/index.md` 指向的规则文件。
- 修改范围尽量限制在 1 到 3 个文件或模块。
- 完成后把验证结果记到 `docs/09-verification.md` 或当前 Sprint 的验收记录。

## 12. 什么时候用 `SOP`、命令和 Prompt

- `SOP.md`：当你已经知道要做什么，但不知道该找哪个流程入口时再看。
- `ai/commands/README.md`：当你想用 `/run ...` 或自然语言触发常见任务时再看。
- `INIT-PROMPT.md` 和 `ai/prompts/`：当命令路由不够细，需要复制完整操作模板给 AI 时再看。
- Prompt 不是需求本身；输入不足时，先补输入，不要让 AI 猜。

## 13. 常见错误

- 只有一句想法，没有上游输入材料，就直接让 AI 生成代码。
- 没先跑环境检查，就直接执行 `new-project.sh`，结果把 Git Bash / PowerShell / PATH 问题误判成模板问题。
- 没填 `ai/project-rules.md`，就开始生成设计文档。
- 把愿景功能直接当当前阶段需求。
- 把模板自身文档和派生项目过程文档混在一起。
- 一次让 AI 改太多文件，最后无法验收。
- 没有验证记录，就认为任务已经完成。

## 14. 常见问题

- 什么时候省略 `docs/06` 和 `docs/07`：看 `ai/project-rules.md` §3 和 `docs/README.md` 的裁剪决策表。
- 什么时候需要 `tasks/`：当 `docs/08-dev-plan.md` 里的某个 Sprint 已经复杂到需要拆成多个独立任务。
- 什么时候需要 `docs/design/`：当某个子系统已经非平凡，光靠 `docs/04` / `docs/05` 不够表达内部逻辑。
- 什么时候需要服务器预案：当本机资源不能支撑当前阶段 Demo / MVP，且不能通过降级或 Mock 解决时。
- 切换 AI 工具怎么办：规则不变，先记录当前进度，再让新工具从 `ai/index.md` 和当前 Sprint 继续。

## 15. 后续查找入口

- 环境准备卡住：看 `template-docs/env-setup.md`，再回到本手册 §4。
- 想验证一遍新手链路：按 `template-docs/smoke-test.md` 执行。
- 想记录一遍烟测结果：使用 `template-docs/smoke-test-report-template.md`。
- 想单独安装 `Claude CLI` / `Codex CLI`：看 `template-docs/ai-cli-setup.md`。
- 生成文档体系前：先确认 `ai/project-rules.md`、`docs/env/local-env.md` 和上游输入材料。
- 执行第一个 Sprint 前：先确认 `docs/08-dev-plan.md` 和 `docs/09-verification.md`。
- 想理解模板为什么这么设计：看 `template-docs/template-methodology.md`。
