# TEMPLATE-UPGRADE: Prompt Library 拆分与 INIT-PROMPT 瘦身

> 类型：模板仓库内直接发起的模板优化提案。
> 状态：随本次模板 PR 落地后归档。

## 1. 动机

`INIT-PROMPT.md` 已增长到 800+ 行，混合普通项目初始化、日常开发、文档审查、模板同步、维护者治理等多类场景。普通使用者难以快速找到需要复制的 Prompt，维护者也难以单独演进某一类 Prompt。

## 2. 拟改

- 新增 `ai/prompts/`，按场景拆分 `INIT-PROMPT.md` 中的 §0-§15。
- 保留 `INIT-PROMPT.md` 作为轻量索引，提供场景到 Prompt 文件的映射。
- 新增 `ai/prompts/README.md` 说明 Prompt Library 使用方式。
- 更新 `template-sync.json`，将新增 prompt 文件纳入下行同步。
- 更新 `scripts/check-template.sh`，自检 prompt 文件存在、关键内容保留、索引可用。

## 3. 版本影响

建议升级为 `v1.9.0`：新增一组同步方法论文件与 Prompt 管理能力，属于 MINOR。

## 4. 验证方式

- `git diff --check`
- `powershell -ExecutionPolicy Bypass -File scripts/check-template.ps1`
- 人工检查 `INIT-PROMPT.md` 是否只保留索引，且每个拆分文件可独立复制使用。

## 5. 归档计划

本提案落地完成后移动到 `_archive/proposals/`。
