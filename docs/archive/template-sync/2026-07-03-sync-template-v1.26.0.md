# 派生项目模板同步运行记录：v1.26.0

## 基本信息

- 项目：zy-digital-cs
- 同步日期：2026-07-03
- 同步前模板版本：v1.22.4
- 目标模板版本：v1.26.0
- 同步分支：chore/sync-template-v1.26.0
- 操作入口：自然语言“更新方法论” / `sync-methodology` 等价流程
- AI 工具 / CLI：Codex CLI

## 执行命令

- dry-run：`powershell -ExecutionPolicy Bypass -File scripts/sync-template.ps1 --dry-run`
- bootstrap：`git checkout FETCH_HEAD -- scripts/sync-template.sh scripts/sync-template.ps1`，提交 `73cbb32 chore: bootstrap latest sync script`
- commit：因本机 PowerShell 参数 / 编码问题，最终按 `template-sync.json` 清单等价执行 checkout + commit，提交 `f7782cd sync template v1.26.0 from ai-project-template`；拆分 PR 后对应提交为 `818e44a sync template v1.26.0 from ai-project-template`
- check-derived-sync：官方 `scripts/check-derived-sync.ps1` 在本机 Windows PowerShell 5 下解析失败；已执行等价边界校验
- 是否触发 PowerShell fallback（sync / check）：sync 触发 fallback；check 因 Git Bash 不可用转 fallback，但 fallback 脚本解析失败
- post-sync-cleanup：本记录由 `post-sync-cleanup` 第一批整理生成

## 同步结果

- 是否成功：成功；PR #1 已合并
- 方法论同步 PR：https://github.com/emily8421/zhiyan-digital-cs-platform/pull/1
- 输入文档 PR：https://github.com/emily8421/zhiyan-digital-cs-platform/pull/2
- 新增 / 修改的方法论文件：以 `template-sync.json` 清单和 PR #1 文件列表为准，目标版本 `VERSION` 已更新到 v1.26.0
- 项目专属文件是否被误改：未发现；PR #1 已拆分为纯方法论同步，项目输入材料位于 PR #2
- 是否新增 / 刷新 `ai/doc-standards/00-09`：是，方法论同步中保留规范镜像
- 是否残留旧 `docs/_scaffold/`：未发现

## 遇到的问题

- Git / gh / Git Bash / PowerShell / 网络问题：
  - Git Bash / sh 在本机多次报 `fatal error - couldn't create signal pipe, Win32 error 5`，导致脚本进入 PowerShell fallback 或 Git 凭据提示失败。
  - 沙箱内 `gh auth status` 多次显示 token 无效或 GraphQL 401；沙箱外 `git push` 与 `gh pr create` 可使用本机凭据成功执行。
  - Windows PowerShell 5 运行新版 `scripts/check-derived-sync.ps1` 时，对 UTF-8 无 BOM 中文字符串解析失败。
- 同步脚本问题：`powershell -ExecutionPolicy Bypass -File scripts/sync-template.ps1 --commit` 在本机没有正确进入 commit 模式，表现为仍执行 dry-run；已记录为可复核问题。
- Prompt / 快捷命令理解问题：无。
- 文档说明不清：无明显项目专属问题。
- 派生项目专属冲突：初始 PR 混入输入文档提交，已拆分为 PR #1（方法论）和 PR #2（输入文档）。

## 可优化点归纳

| 问题 | 是否项目专属 | 是否建议回流模板 | 建议提案 |
|---|---|---|---|
| Windows PowerShell 5 对 UTF-8 无 BOM 中文脚本解析失败，影响 `check-derived-sync.ps1` fallback | 否 | 是 | 可提案：PowerShell 脚本避免单引号中文正则或保存为兼容编码 / 增加 PS 版本检测 |
| `sync-template.ps1 --commit` 在本机 PowerShell 调用下被识别为 dry-run | 不确定 | 是 | 可提案：增强参数解析兼容性，增加实际 mode 输出和自测 |
| Git Bash / sh `Win32 error 5` 导致 GitHub 凭据提示失败 | 偏本机环境 | 否 | 记录在本项目环境问题中，优先本机修复 Git for Windows / 权限 |
| 沙箱内 `gh` token 不可用但沙箱外可用 | 偏工具运行环境 | 否 | 记录为本次执行限制 |

## 已生成的回流提案

- 本次未生成 `_proposals/TEMPLATE-UPGRADE-*.md`；建议先人工确认是否将 PowerShell 兼容问题去项目化后回流模板。

## 后续动作

- 是否需要 `/run post-sync-cleanup`：已开始；下一步补齐项目规则、环境约束与文档体系。
- 是否需要 `/run docs-system-audit`：需要；待 `docs/00-09` 从输入材料生成/补齐后执行。
- 是否需要人工清理旧目录：暂未发现旧 `docs/_scaffold/`；是否删除未用代码目录需待 `ai/project-rules.md` §3 决策。
- 是否需要同步回模板仓库：可能需要；仅限 PowerShell 兼容性等去项目化问题，需单独提案确认。
