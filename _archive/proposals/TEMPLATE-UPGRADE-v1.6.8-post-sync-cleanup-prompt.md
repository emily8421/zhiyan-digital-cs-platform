# TEMPLATE-UPGRADE-v1.6.8：新增同步后项目整理 Prompt

## 状态

- 状态：已随本次模板改动落地，归档留痕
- 目标版本：v1.6.8
- 提案来源：派生项目同步方法论后仍需整理项目专属内容的流程缺口

## 背景

`scripts/sync-template.*` 只负责同步模板方法论文件，不会自动修改派生项目的项目事实文档。v1.6.6 / v1.6.7 引入了 docs 分区、派生 README 标准版块和同步边界说明后，已有派生项目仍可能保留旧结构，例如：

- 文档直接堆在 `docs/` 根目录。
- 根 `README.md` 缺少当前阶段、运行环境、验证方式和模板关系说明。
- `ai/project-rules.md` 缺少 §2.5 运行环境与资源约束。
- 缺少 `docs/env/local-env.md`，或 04 / 05 / 09 中没有运行拓扑、资源评估、本机资源验证。

这些内容是项目专属事实，不能由模板同步脚本直接覆盖，需要一套“同步后整理”的 AI Prompt：先审计、给迁移计划、人工确认后再执行。

## 目标

1. 在 `INIT-PROMPT.md` 新增 §15「同步后项目整理」。
2. §15 覆盖 docs 分区整理、根 README 补齐、`ai/project-rules.md` 补齐和环境约束补齐。
3. 明确检查 / 生成 `docs/env/local-env.md`，并补齐 `ai/project-rules.md` §2.5、`docs/04`、`docs/05`、`docs/09` 的环境约束相关章节。
4. 要求先输出迁移计划，等待人工确认后再移动 / 修改文件。
5. 更新 `SOP.md`，在派生项目同步模板后指向 §15。
6. 更新自检，确保 Prompt 和 SOP 场景存在。

## 拟改范围

- `VERSION`：升级到 `v1.6.8`。
- `CHANGELOG.md`：新增 v1.6.8 记录。
- `INIT-PROMPT.md`：新增 §15「同步后项目整理」。
- `SOP.md`：新增“同步后项目整理”场景，并在同步模板常见选择中提示使用 §15。
- `scripts/check-template.sh`：检查 §15、环境约束关键词和 SOP 场景。
- `_archive/proposals/TEMPLATE-UPGRADE-v1.6.8-post-sync-cleanup-prompt.md`：本提案归档。

## 版本影响

- 版本类型：PATCH。
- 理由：新增 Prompt 和 SOP 导航，指导派生项目整理项目专属内容，不改变同步机制或核心文档编号。

## 验证方式

- 运行 `git diff --check`。
- 运行 `powershell -ExecutionPolicy Bypass -File scripts/check-template.ps1`。
