# zy-digital-cs

> 本项目由 `ai-project-template` 派生。请在初始化阶段把本文件改写为项目说明，而不是保留模板仓库说明。

## 项目简介

（用 2-3 句话说明本项目要解决的问题、目标用户与当前阶段范围。）

## 当前阶段

- 当前阶段：Phase1（待确认）
- 交付物形态：Demo / MVP / 产品（待确认；Phase1 不默认等于 MVP）
- 阶段目标：（说明当前阶段要演示、上线或生产化到什么程度）
- 非目标：（说明当前阶段明确不做什么）

## 当前能力

- （列出当前 Phase 已确认要实现的核心能力）

## 快速开始

1. 若尚未确认机器环境，先看 `template-docs/env-setup.md`，运行 `powershell -ExecutionPolicy Bypass -File scripts/check-prereqs.ps1`；缺必备工具时再执行 `scripts/bootstrap-dev-env.ps1` 或手工安装。
2. 运行 `powershell -ExecutionPolicy Bypass -File scripts/collect-env.ps1` 生成 `docs/env/local-env.md`，补齐本机必须跑通的功能、允许降级 / Mock 项与服务器预案。
3. 准备可审计上游输入：可先把产品愿景写入 `docs/vision/product-vision.md`，或把尚未归类的小工具 brief、PRD / SRS、任务单、现有系统说明放入 `docs/inputs/`。
4. 初填 `ai/project-rules.md` 的项目名称、Phase1 目标、技术栈倾向、运行环境约束与项目形态裁剪；不确定项标“待确认”。
5. 在 AI CLI 中说“评审输入材料”（或 `/run review-inputs`），让 AI 读取 `ai/commands/` 路由并评审输入材料；评审通过后说“生成文档体系”（或 `/run generate-docs`），多入口生成 / 补齐 `docs/00-09`、必要的 `docs/design/` 详细设计、项目 README 与 Sprint1；底层 Prompt 见 `ai/prompts/docs/00-generate-or-complete-docs.md`。
6. 人工确认 `docs/03-prd.md` §3 阶段路线图、交付物形态和 `docs/05-tech-spec.md` 的本机 Demo 可行性；确认后再说“执行当前 Sprint”（或 `/run run-dev-task`）。

> 纯本地烟测可以暂时不安装 AI CLI；真正开始 AI 协作开发前，至少准备并登录一种 AI CLI，安装顺序见 `template-docs/ai-cli-setup.md`。

### 推荐：打开 AI CLI 后让 AI 带你继续

> Keyword for template checks: newbie AI CLI onboarding path.

如果已经安装并登录 `Claude CLI` 或 `Codex CLI`，在本项目根目录打开 AI CLI，然后说：

```text
我是第一次使用这个 ai-project-template。请先读取 ai/index.md 和相关规则，
然后按新手 AI CLI 引导路径带我完成当前项目初始化：
1. 检查基础环境
2. 确认当前项目目录和 Git 状态
3. 采集本机环境
4. 准备上游输入
5. 评审输入材料
6. 生成文档体系

每一步执行命令前先说明目的和影响范围，需要我确认后再运行。
```

### `ai/project-rules.md` 首次必填 checklist

生成 `docs/03-09` 前，至少确认以下项目不再保留模板占位：

- 项目名称与代号 / 缩写。
- Phase1 允许事项、禁止事项与 Phase2 预告。
- 已确定或待确认的前端 / 后端 / 数据库 / AI 模型等技术栈。
- 本机 Demo 必须运行的部分、允许降级 / Mock 的部分、是否需要服务器。
- 是否有持久化存储、是否有对外接口、演示形态。
- `docs/06-db-design.md` 与 `docs/07-api-spec.md` 的保留 / 省略决策。
- 需要保留的代码目录；不用的目录后续再删除，不要先删再补依据。

## 文档入口

- `docs/00-scenario.md`：场景
- `docs/vision/product-vision.md`：产品愿景叙事源文档
- `docs/inputs/`：尚未归类、尚未转成 00-09 的原始输入包
- `docs/01-user-requirements.md`：用户需求
- `docs/02-srs.md`：软件需求规格
- `docs/03-prd.md`：产品需求与阶段路线图
- `docs/README.md`：文档分区规则，新增文档前先看这里
- `docs/env/local-env.md`：本机运行环境与资源约束
- `docs/design/`：子系统 / 模块详细设计
- `docs/08-dev-plan.md`：开发计划
- `docs/09-verification.md`：验证计划

## 运行环境

- 本机环境记录：`docs/env/local-env.md`
- 本机 Demo 可行性：（待确认）
- 降级 / Mock 策略：（待确认）

## 开发计划

- 当前 Sprint：见 `docs/08-dev-plan.md`
- 执行单个任务时使用 `ai/prompts/dev/02-run-task.md`

## 验证方式

- 验证计划：见 `docs/09-verification.md`
- 本机资源验证：见 `docs/09-verification.md` 的资源验证项

## 模板关系

- 通用方法论来自 `ai-project-template`。
- 当前同步到的模板版本记录在 `VERSION`。
- 文档生成、追溯链、变更传播与多入口规则见 `ai/document-lifecycle-rules.md`；可复制 Prompt 见 `INIT-PROMPT.md` 索引与 `ai/prompts/`。
- 根 `README.md` 是项目专属文档，不参与模板下行同步。
- 模板方法论文件由 `template-sync.json` 定义，执行 `scripts/sync-template.*` 时可能被覆盖。
- 项目专属规则写在 `ai/project-rules.md`。
- 项目事实文档写在 `docs/`，但新增文档必须遵守 `docs/README.md` 的分区规则，不要直接堆到 `docs/` 根目录。
- 如发现可通用的模板优化，先在 `_proposals/` 起草提案，再回流到模板仓库。
