# 派生项目模板同步运行记录：v1.30.0

## 基本信息

- 项目：zy-digital-cs
- 同步日期：2026-07-05
- 同步前模板版本：v1.26.0
- 目标模板版本：v1.30.0
- 同步分支：chore/sync-template-v1.30.0
- 操作入口：自然语言“同步模版” / `sync-methodology` 等价流程
- AI 工具 / CLI：Codex CLI

## 执行命令

- dry-run：`powershell -ExecutionPolicy Bypass -File scripts/sync-template.ps1 --dry-run`，首次因本地同步脚本过旧停止。
- bootstrap：`git checkout FETCH_HEAD -- scripts/sync-template.ps1 scripts/sync-template.sh scripts/check-derived-sync.ps1 scripts/check-derived-sync.sh`，提交 `5679666 chore: bootstrap template sync script`。
- dry-run 复跑：使用 `powershell -ExecutionPolicy Bypass -Command "... & './scripts/sync-template.ps1' --dry-run"` 成功预览 v1.30.0 同步范围。
- commit：因本机 Git Bash `Win32 error 5` 与 PowerShell fallback `--commit` 参数识别问题，最终按 `template-sync.json` 清单等价执行 `git checkout FETCH_HEAD -- <sync files>`，并刷新 `ai/doc-standards/00-09` 规范镜像；提交 `1c51583 sync template v1.30.0 from ai-project-template`。
- check-derived-sync：使用 UTF-8 临时副本执行 `check-derived-sync.ps1 HEAD`，结果通过。
- 是否触发 PowerShell fallback（sync / check）：sync 与 check 均触发；Git Bash 在本机无法启动。
- post-sync-cleanup：未执行，建议同步 PR 合并后另开任务。
- docs-system-audit（同步后审计）：未执行，建议同步 PR 合并后另开任务。
- 项目验证建议 / 已执行验证：本次为方法论同步，已执行 `git diff --cached --check` 与 `check-derived-sync`；业务测试建议在同步 PR 合并后按需回归。

## 同步结果

- 是否成功：成功生成同步提交，待 PR 合并。
- 新增 / 修改的方法论文件：以 `template-sync.json` 清单和同步提交文件列表为准；`VERSION` 更新到 v1.30.0。
- 项目专属文件是否被误改：未发现；变更集中在模板方法论文件、脚本、`template-docs/`、`ai/doc-standards/`、`docs/README.md` 与 `docs/inputs/README.md`。
- 是否新增 / 刷新 `ai/doc-standards/00-09`：是。
- 是否残留旧 `docs/_scaffold/`：未发现。

## 同步后整理摘要

- 是否执行 `/run post-sync-cleanup`：否。
- README / `ai/project-rules.md` / docs 分区是否需整理：同步脚本提示当前存在 `.github/workflows/template-check.yml`，该项应在同步后整理中评估是否迁移为派生项目 `project-check.yml`。
- 已处理项：同步脚本 bootstrap；方法论文件更新到 v1.30.0；派生同步边界检查通过。
- 待确认项：是否对 `.github/workflows/template-check.yml` 做派生项目 CI 迁移；是否把 PowerShell 兼容问题整理成模板回流提案。
- 建议回写 / 后续迁移任务：另开 `post-sync-cleanup` 任务，只读审计后再确认修改范围。

## 文档体系审计摘要

- 是否执行 `/run docs-system-audit` 同步后审计模式：否。
- 规范基线缺口：待审计。
- 可接受兼容差异：待审计。
- 项目事实风险：待审计。
- 回梳计划摘要：建议在同步 PR 合并后执行 docs-system-audit，只读输出报告后再决定是否回梳。

## 项目验证建议

- 建议运行的测试 / lint / 文档检查 / 人工验收：`git diff --check`、`scripts/check-derived-sync.ps1 HEAD`、后端 API / 场景 / 验收测试、H5 与 Console build。
- 已执行验证与结果：`git diff --cached --check` 通过；`check-derived-sync` 通过。
- 未验证项与原因：未运行业务测试和前端 build；本次仅同步方法论，避免扩大同步提交范围。

## 遇到的问题

- Git / gh / Git Bash / PowerShell / 网络问题：Git Bash 多次报 `fatal error - couldn't create signal pipe, Win32 error 5`，导致同步脚本和检查脚本均进入 PowerShell fallback。
- 同步脚本问题：`powershell -ExecutionPolicy Bypass -File scripts/sync-template.ps1 --commit` 在本机失败；`-Command` 调用虽可执行 dry-run，但 fallback 中 `--commit` 未进入 commit 分支，疑似参数名 `Args` 与 PowerShell 自动变量冲突或调用兼容问题。
- Prompt / 快捷命令理解问题：无。
- 文档说明不清：本次模板已将同步记录推荐路径改为 `sync-records/template-sync/`，但本项目历史记录仍位于 `docs/archive/template-sync/`；本次沿用项目既有路径，后续可在 cleanup 中决定是否迁移。
- 派生项目专属冲突：未发现。

## 可优化点归纳

| 问题 | 是否项目专属 | 是否建议回流模板 | 建议提案 |
|---|---|---|---|
| PowerShell fallback 中 `sync-template.ps1 --commit` 未进入 commit 分支 | 否 | 是 | 可提案：避免参数名 `Args`，增加 fallback mode 自测与 commit e2e |
| PowerShell 5.1 直接执行 UTF-8 无 BOM 中文脚本会解析失败 | 否 | 是 | 可提案：脚本发布为 BOM 或避免中文单引号正则 / 增加编码自检 |
| Git Bash `Win32 error 5` 导致 Bash 入口不可用 | 偏本机环境 | 否 | 记录为本机 Git for Windows / 权限问题 |
| 同步记录推荐路径从 `docs/archive/template-sync/` 演进为 `sync-records/template-sync/` | 否 | 视情况 | cleanup 中评估迁移策略，不混入本次同步 |

## 已生成的回流提案

- 本次未生成 `_proposals/TEMPLATE-UPGRADE-*.md`；建议在同步 PR 合并后单独确认是否回流 PowerShell 兼容性提案。

## 后续动作

- 是否需要 `/run post-sync-cleanup`：需要；建议同步 PR 合并后另开分支。
- 是否需要 `/run docs-system-audit`：需要；建议 post-sync-cleanup 后执行只读审计。
- 是否需要按审计结果回梳 `docs/00-09` / `docs/design` / `docs/env`：待审计结论。
- 是否需要补项目验证入口：待 cleanup 评估，尤其关注 `.github/workflows/template-check.yml`。
- 是否需要人工清理旧目录：待 cleanup 评估。
- 是否需要同步回模板仓库：可能需要；仅限 PowerShell 兼容性等去项目化问题，需单独提案确认。
