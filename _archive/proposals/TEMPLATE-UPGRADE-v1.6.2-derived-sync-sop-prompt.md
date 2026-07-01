# TEMPLATE-UPGRADE-v1.6.2：派生项目新建 / 同步 SOP Prompt 固化

## 状态

- 状态：已随本次模板改动落地，归档留痕
- 目标版本：v1.6.2
- 提案来源：派生项目新建与同步流程标准化需求

## 背景

模板 v1.6.1 已增强 `scripts/sync-template.sh` 的自身更新保护，并要求派生项目同步前先 bootstrap 最新同步脚本。但目前“派生项目同步 SOP”主要散落在 `git-guide.md` 和 `INIT-PROMPT.md` §12 的执行要求中，用户希望将标准流程沉淀成可直接复制给 AI 的 Prompt 模板，便于两个或更多派生项目重复执行。

同时，新建项目流程虽然在 `git-guide.md` 中有简要说明，但仍保留“手动复制模板”的旧表述，容易让用户误解为要先人工复制文件夹再运行 `new-project.sh`。需要明确：正式新项目应优先通过 `scripts/new-project.sh` 从 GitHub `main` 派生，并把该 SOP 也沉淀为 Prompt。

## 目标

1. 在 `INIT-PROMPT.md` 中补充“派生项目同步模板标准 SOP”的完整 Prompt 模板。
2. 明确目标版本必须运行时读取模板仓库 `VERSION`，不能在 Prompt 中固定写死；同时覆盖 bootstrap 最新脚本、dry-run 审查、commit、check-template、自检、提案归档与 PR 创建步骤。
3. 在 `git-guide.md` 中明确新建项目 SOP：推荐 `scripts/new-project.sh`，不推荐手工复制模板目录。
4. 在 `INIT-PROMPT.md` 中新增“从模板新建派生项目”的可复制 Prompt。
5. 保留停止条件，防止覆盖项目专属文件、在工作区不干净时继续执行，或在模板本地副本不可信时创建正式项目。
6. 版本升级为 `v1.6.2`，作为 Prompt / 文档层补丁。

## 拟改范围

- `VERSION`：升级到 `v1.6.2`。
- `README.md`：新增 `v1.6.2` 版本记录。
- `INIT-PROMPT.md`：在 §12 内补充可复制的派生项目同步 SOP Prompt；新增 §14“从模板新建派生项目”。
- `git-guide.md`：将 §2 改为新建派生项目 SOP 权威文档。
- `scripts/check-template.sh`：检查 SOP Prompt 关键语句存在。
- `_archive/proposals/TEMPLATE-UPGRADE-v1.6.2-derived-sync-sop-prompt.md`：本提案归档。

## 版本影响

- 版本类型：PATCH。
- 理由：不改变模板核心机制，仅将已有派生项目同步流程固化为 Prompt 模板。

## 验证方式

- 运行 `git diff --check`。
- 运行 `bash scripts/check-template.sh`。
