# TEMPLATE-UPGRADE: 派生项目同步运行记录与回流观察机制

> 类型：模板仓库内直接发起的模板优化提案。
> 状态：待评估 / 待落地。
> 关联：`/run sync-methodology`、`ai/prompts/maintainers/12-sync-template.md`、`/run post-sync-cleanup`、`_proposals/` 模板优化回流流程。

## 1. 背景与问题

模板已具备下行同步能力：派生项目可以通过 `sync-template` 将 `ai-project-template` 的方法论文件同步到本地，并通过 `check-derived-sync` 检查同步边界。

但真实派生项目同步过程本身目前缺少结构化记录：

- 同步是否顺利、哪些命令成功 / 失败，往往只停留在当前 CLI 会话中。
- 遇到的 Git Bash / PowerShell / gh / 网络 / 权限 / dry-run 解释问题，容易随会话结束丢失。
- 同步后发现的模板说明不清、Prompt 路由不顺、脚本边界不准等可通用问题，缺少从“运行观察”到 `_proposals/TEMPLATE-UPGRADE-*.md` 的固定转写步骤。
- 派生项目里的同步事实与模板仓库的改进闭环之间仍依赖人工记忆。

因此建议为派生项目模板同步增加“同步运行记录 / 同步观察报告”机制，并在必要时自动归纳可回流模板优化提案。

## 2. 设计目标

- 每次真实派生项目同步后，能留下可复盘的同步运行记录。
- 把同步中的问题分为项目专属问题、环境问题、模板方法论问题。
- 对可通用于多个项目的问题，生成去项目化的 `_proposals/TEMPLATE-UPGRADE-*.md` 建议。
- 不把派生项目运行记录直接提交到模板仓库；模板仓库只接收去项目化提案。
- 与 `sync-methodology` / `post-sync-cleanup` / `docs-system-audit` 命令形成闭环。

## 3. 建议方案

新增一份同步运行记录模板：

```text
template-docs/derived-sync-report-template.md
```

派生项目同步完成后，建议将实际运行记录写到：

```text
docs/archive/template-sync/YYYY-MM-DD-sync-template-vX.Y.Z.md
```

如果只是短期续接，可先写入：

```text
.ai/session-handoff.md
```

如果发现可回流模板优化，再生成：

```text
_proposals/TEMPLATE-UPGRADE-<topic>.md
```

## 4. 运行记录建议结构

```markdown
# 派生项目模板同步运行记录

## 基本信息

- 项目：
- 同步日期：
- 同步前模板版本：
- 目标模板版本：
- 同步分支：
- 操作入口：`/run sync-methodology` / 手动命令
- AI 工具 / CLI：

## 执行命令

- dry-run：
- commit：
- check-derived-sync：
- post-sync-cleanup：

## 同步结果

- 是否成功：
- 新增 / 修改的方法论文件：
- 项目专属文件是否被误改：
- 是否新增 / 刷新 `ai/doc-standards/00-09`：
- 是否残留旧 `docs/_scaffold/`：

## 遇到的问题

- Git / gh / Git Bash / PowerShell / 网络问题：
- 同步脚本问题：
- Prompt / 快捷命令理解问题：
- 文档说明不清：
- 派生项目专属冲突：

## 可优化点归纳

| 问题 | 是否项目专属 | 是否建议回流模板 | 建议提案 |
|---|---|---|---|

## 已生成的回流提案

- `_proposals/TEMPLATE-UPGRADE-xxx.md`

## 后续动作

- 是否需要 `/run post-sync-cleanup`：
- 是否需要 `/run docs-system-audit`：
- 是否需要人工清理旧目录：
- 是否需要同步回模板仓库：
```

## 5. 拟改范围

### 新增模板文档

- `template-docs/derived-sync-report-template.md`：派生项目同步运行记录模板。

### 命令与 Prompt

- `ai/commands/sync-methodology.md`：同步流程末尾增加“生成同步运行记录”步骤。
- `ai/prompts/maintainers/12-sync-template.md`：`check-derived-sync` 后增加运行记录与模板优化回流判断。
- `ai/commands/post-sync-cleanup.md`：把同步运行记录作为可选输入。
- `ai/prompts/maintainers/15-post-sync-cleanup.md`：补充“从运行记录中提炼模板优化提案”。
- `ai/commands/template-proposal-summary.md`：说明可读取派生项目回流的同步观察提案。

### 人读入口

- `SOP.md`：新增“派生同步运行记录”场景或在“派生项目同步模板”备注中补充。
- `README.md`：派生项目同步说明中提示同步后可生成观察记录。
- `MAINTAINERS.md`：维护规则中要求真实派生同步问题优先沉淀为运行记录，再提炼为去项目化提案。
- `CONTRIBUTING.md`：强调运行记录可包含项目事实，回流提案必须去项目化。

### 同步与自检

- `template-sync.json`：纳入 `template-docs/derived-sync-report-template.md`。
- `scripts/sync-template.sh` 兜底清单：纳入运行记录模板。
- `scripts/check-template.sh`：增加断言，确保同步 Prompt / 命令 / SOP / 同步清单引用运行记录模板。

## 6. 版本影响

建议作为 `v1.21.0` 落地。

理由：该机制新增派生项目同步后的观察记录能力和回流闭环，影响同步命令、Prompt、人读文档、同步清单和自检逻辑，属于可见的方法论能力增强。

## 7. 验收口径

- `/run sync-methodology` 或 `12-sync-template` 的流程末尾明确要求生成同步运行记录。
- 运行记录模板存在且进入 `template-sync.json`。
- 同步运行记录清晰区分项目事实、环境问题、模板方法论问题。
- 若发现可通用优化，Prompt 指引生成去项目化 `_proposals/TEMPLATE-UPGRADE-*.md`。
- `SOP.md` / `README.md` 能让用户知道“真实同步后可留观察记录”。
- `check-template.sh` 对运行记录入口有防滞后断言。

## 8. 风险与缓解

- **记录过重影响同步体验**：运行记录可以先作为同步完成后的建议步骤；只有真实派生同步或遇到问题时要求完整填写。
- **项目敏感信息进入模板提案**：运行记录留在派生项目；回流提案必须去项目化，删除客户、账号、路径、业务细节。
- **重复记录会话续接内容**：`.ai/session-handoff.md` 只记录当前任务断点，运行记录用于长期复盘；两者职责不同。
- **目录选择不清**：推荐长期记录放 `docs/archive/template-sync/`，临时记录放 `.ai/session-handoff.md`。
