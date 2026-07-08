# 派生项目模板同步运行记录：v1.43.0

## 基本信息

- 项目：zhiyan-digital-cs-platform
- 同步日期：2026-07-08
- 同步前模板版本：v1.30.3
- 目标模板版本：v1.43.0
- 同步分支：chore/sync-template-20260708
- 实际同步提交（非 PR merge commit）：`00e7f6c sync template v1.43.0 from ai-project-template`
- Bootstrap 提交：`3c0fbf0 chore: bootstrap latest sync script`
- 操作入口：`/run sync-methodology`（用户说法：同步项目模板）
- AI 工具 / CLI：Codex CLI

## 执行命令

- dry-run：`powershell -ExecutionPolicy Bypass -File scripts/sync-template.ps1 --dry-run`；因输出 diff 统计较多，两次在 120s / 300s 超时，但已输出目标版本、同步清单和边界信息；未修改工作区。
- commit：先按脚本提示执行 `git checkout FETCH_HEAD -- scripts/sync-template.sh scripts/sync-template.ps1` 并提交 `3c0fbf0`；随后因 PowerShell fallback 仍将 `--commit` 误判为 `--dry-run`，按 `scripts/sync-template.ps1` 等价逻辑手工执行 `template-sync.json` 清单 checkout、`ai/doc-standards/00-09` 镜像刷新、`git diff --cached --check` 和提交 `00e7f6c`。
- check-derived-sync：`powershell -ExecutionPolicy Bypass -File scripts/check-derived-sync.ps1`，通过。
- 是否触发 PowerShell fallback（sync / check）：sync 与 check 均触发；本机 Git Bash 报 `Win32 error 5`。
- post-sync-cleanup：已执行只读整理审计；未修改项目事实文档。
- docs-system-audit（同步后审计）：已执行轻量只读审计；未启动文档回梳。
- 项目验证建议 / 已执行验证：已执行 `git diff --check main...HEAD` 和 `check-derived-sync`；未运行业务测试 / 前端构建。

## 同步结果

- 是否成功：成功，同步到 v1.43.0。
- 新增 / 修改的方法论文件：同步提交 `00e7f6c` 涉及 90 个模板方法论文件，包含 `ai/commands/resume.md`、`ai/commands/docs-open-items.md`、`ai/commands/ui-prototype-exploration.md`、`ai/doc-standards/design-doc.md`、`ai/doc-standards/frontend-interaction.md`、`ai/doc-standards/ui-prototype-strategy.md`、`template-docs/docs-scaffold/*`、`template-docs/glossary.md` 等。
- 项目专属文件是否被误改：否；`check-derived-sync` 通过，未改 `docs/00-09`、`frontend/`、`backend/`、`tests/`、`docker/`、`ai/project-rules.md` 或根 `README.md`。
- 是否新增 / 刷新 `ai/doc-standards/00-09`：已刷新，并新增设计类文档标准。
- 是否残留旧 `docs/_scaffold/`：未发现需要迁移的旧 scaffold。

## 同步后整理摘要

- 是否执行 `/run post-sync-cleanup`：是，只读执行。
- README / `ai/project-rules.md` / docs 分区是否需整理：当前基本合规；`docs/` 根目录仅保留 `README.md` 与 `00-09` 核心文档，细分文档位于 `docs/design/`、`docs/decisions/`、`docs/env/`、`docs/inputs/`、`docs/meetings/`、`docs/research/`、`docs/vision/`。
- 已处理项：模板同步到 v1.43.0；派生项目 workflow 仅保留 `.github/workflows/project-check.yml`；边界检查通过。
- 待确认项：v1.43.0 新增 `docs-open-items` 与 UI 原型探索方法论，当前项目尚无 `docs/research/docs-open-items.md`，可在后续 Phase2 文档整理时决定是否创建待确认事项总览。
- 建议回写 / 后续迁移任务：当前不建议立即改项目事实文档；若接受 Phase2 Conditional Go，再同时补 Phase2 规划与 open items 总览。

## 文档体系审计摘要

- 是否执行 `/run docs-system-audit` 同步后审计模式：是，轻量只读执行。
- 规范基线缺口：`docs/00-09` 均存在且均有 `## 0. 文档元信息`；`docs/design/*` 已覆盖后端、H5、Web 控制台、前端交互、知识策略、Mock 集成与场景包。
- 可接受兼容差异：项目文档已完成 Phase1 验收回填，但未逐字套用 v1.43.0 的新 scaffold；这是旧项目兼容差异，暂不要求重写。
- 项目事实风险：Phase2 仍待人工确认；确认前不应解锁真实飞书、真实业务系统、PostgreSQL / pgvector 必做项或 LLM 自动答复。
- 回梳计划摘要：无阻塞回梳；建议在 Phase2 启动前用新 `docs-open-items` 方法整理 C-001~C-005 等待确认项。

## 项目验证建议

- 建议运行的测试 / lint / 文档检查 / 人工验收：本次同步建议以 `check-derived-sync`、`git diff --check`、PR 检查为主；业务测试可在合并前按需抽跑。
- 已执行验证与结果：`powershell -ExecutionPolicy Bypass -File scripts/check-derived-sync.ps1` 通过；`git diff --check main...HEAD` 通过。
- 未验证项与原因：未运行后端 pytest、H5 build、Console build；本次仅同步模板方法论，不改业务代码或项目事实文档。

## 遇到的问题

- Git / gh / Git Bash / PowerShell / 网络问题：Git Bash 仍报 `fatal error - couldn't create signal pipe, Win32 error 5`，同步和边界检查均走 PowerShell fallback。
- `gh issue create` / `submit-proposal` 问题：未创建新 issue；只读查询模板仓 issue 状态时，普通沙箱网络失败，提权只读查询成功。
- 同步脚本问题：v1.43.0 的 `scripts/sync-template.ps1` fallback 仍使用 `Invoke-NativeTemplateSync` 的 `Args` 参数名，本机 PowerShell 5.1 下 `--commit` 仍被误判为 dry-run；本次通过等价手工同步绕过。
- Prompt / 快捷命令理解问题：无。
- 文档说明不清：`--commit` fallback 问题已在既有 issue #102 范围内，但 issue 已关闭而本机仍复现，建议后续重新反馈或补充复现。
- 派生项目专属冲突：无。

## 可优化点归纳

| 问题 | 是否项目专属 | 是否建议回流模板 | 建议提案 |
|---|---|---|---|
| `scripts/sync-template.ps1` fallback 在 Windows PowerShell 5.1 下仍无法正确接收 `--commit`，实际执行 dry-run | 否 | 是 | 复用 / 补充 issue #102；若需新提案，起草 follow-up |
| dry-run diff 统计在大版本同步时输出过多并超时 | 否 | 可选 | 可建议增加 `--list-only` 或跳过 diff stats 的快速预览参数 |

## 已生成的回流提案

- 已存在 `_proposals/TEMPLATE-UPGRADE-derived-sync-powershell-fallback.md`，对应 issue #102：https://github.com/emily8421/ai-project-template/issues/102。
- 本次未新增提案文件；先在本运行记录中登记复现，避免重复提案。

## 提案回流收口

- 扫描范围：`_proposals/`、`_archive/proposals/`、`.ai/session-handoff.md`、模板仓 issue 链接。
- 已确认 issue 当前状态：#102、#111、#112、#113、#114、#115、#116、#117、#118 均为 closed。
- 已确认被模板采纳或已有决议的提案：Batch 0~6 与 A13 对应 issue #111~#118 已关闭，v1.43.0 已吸收其中多项文档治理能力。
- 已归档到 `_archive/proposals/` 的本地提案：本次未移动文件。
- 仍需保留在 `_proposals/` 的提案：本次暂保留全部现有提案，等待单独归档任务确认；尤其 #102 虽 closed 但本机仍复现相关问题。
- 无法判断是否已处理的 issue / 提案与待确认项：各 issue 关闭原因未逐条读取评论，当前仅记录 GitHub API issue state。

## 后续动作

- 是否需要 `/run post-sync-cleanup`：已完成轻量只读审计；无需立即再跑。
- 是否需要 `/run docs-system-audit`：已完成轻量只读审计；若进入 Phase2，再按新规范做专题回梳。
- 是否需要按审计结果回梳 `docs/00-09` / `docs/design` / `docs/env`：当前不需要；Phase2 启动时再改。
- 是否需要补项目验证入口：当前不需要；PR 检查可覆盖同步边界。
- 是否需要人工清理旧目录：建议后续单独确认是否归档 `_proposals/` 中已关闭 issue 对应提案。
- 是否需要同步回模板仓库：建议针对 `sync-template.ps1 --commit` fallback 仍复现的问题，决定是补充 issue #102 还是新建 follow-up。
