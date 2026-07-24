# 已处理模板优化提案归档

本目录保存已经处理完成、但仍需保留审计记录的模板优化提案。

归档原则：

- `_proposals/` 是待处理 / 汇总中的提案收件箱。
- `_archive/proposals/` 是已处理提案的历史记录。
- 提案归档后，模板变更事实仍以根目录 `VERSION`、README 版本记录和 Git 历史为准。
- 归档内容不得作为当前待办事项重复执行；若要再次调整，应创建新的 `TEMPLATE-UPGRADE-*.md` 提案。

## 2026-07-11 同步 v1.46.0 归档

- `TEMPLATE-UPGRADE-a13-sync-closure-and-dry-run-robustness.md`：模板 issue #148 已关闭；A13 门禁、fallback 参数修复、dry-run 轻量预览已在模板 v1.44.x / v1.45.x / v1.46.0 链路中落地，本地归档。
- `TEMPLATE-UPGRADE-demo-runbook-trigger.md`：模板 issue #160 已关闭；`show-demo` 命令与 `demo-runbook-template` 已在模板 v1.45.0+ 落地，本地归档。

## 2026-07-15 同步 v1.52.4 归档

- `TEMPLATE-UPGRADE-demo-port-identity-check.md`：模板 issue #184 已关闭；Demo 页面身份与端口漂移检查已在模板 v1.47.3 落地，并随本次 v1.52.4 同步下行。
- `TEMPLATE-UPGRADE-web-app-structure-profile.md`：模板 issue #186 已关闭；Web App Structure Profile 与 Walking Skeleton Gate 已在模板 v1.51.0 落地，并随本次 v1.52.4 同步下行。
- `TEMPLATE-UPGRADE-codex-sandbox-remote-ops.md`：模板 issue #195 已关闭；Codex Checkpoint Mode 与远端操作 SOP 已在模板 v1.52.1 落地，并随本次 v1.52.4 同步下行。

## 2026-07-24 同步 v1.56.13 归档

- `TEMPLATE-UPGRADE-sync-powershell-fallback-commit-pathspec.md`：模板 issue #217 已关闭；PowerShell fallback commit 避免超长 pathspec 的修复已在模板 v1.52.5 落地，并随本次 v1.56.13 同步下行。
- `TEMPLATE-UPGRADE-derived-version-governance.md`：模板 issue #221 已关闭；派生项目版本机制默认启用、存量检测与整理引导已在模板 v1.56.13 相关脚本和 Prompt 中落地，并随本次同步下行。
