# zhiyan 模板同步运行记录：v1.46.0

## 基本信息

- 项目：zhiyan-digital-cs-platform
- 同步日期：2026-07-11
- 同步前模板版本：v1.43.0（旧语义下 `VERSION` 记录继承模板版本）
- 目标模板版本：v1.46.0
- 项目自身版本（`VERSION`）：v0.1.0（同步后重新定义项目自有版本基线，不沿用旧 `v1.43.0`）
- 继承版本记录（`TEMPLATE-BASE.md`）：新增；当前同步到 v1.46.0
- 同步分支：`chore/sync-template-v1.46.0`
- Bootstrap 提交：`840811e chore: bootstrap latest sync script`
- 实际同步提交（非 PR merge commit）：`ced2c76 sync template v1.46.0 from ai-project-template`
- 操作入口：`/run sync-methodology`（用户自然语言触发“小规模同步试点”）
- AI 工具 / CLI：Codex CLI

## 执行命令

- 预检：`git status --short --branch` → 干净，位于 `main...origin/main`
- 拉取模板：`git fetch --no-tags --depth=1 https://github.com/emily8421/ai-project-template.git main` → 目标版本 `v1.46.0`
- 新建分支：`git switch -c chore/sync-template-v1.46.0`
- Bootstrap：`git checkout FETCH_HEAD -- scripts/sync-template.sh scripts/sync-template.ps1` + `git commit -m "chore: bootstrap latest sync script"`
- dry-run：`powershell -ExecutionPolicy Bypass -File scripts/sync-template.ps1 --dry-run --no-stat --preserve-project-version`
- commit：`powershell -ExecutionPolicy Bypass -File scripts/sync-template.ps1 --commit --preserve-project-version`
- check-derived-sync：`powershell -ExecutionPolicy Bypass -File scripts/check-derived-sync.ps1 HEAD`
- 是否使用 `--preserve-project-version`：是
- 是否触发 PowerShell fallback（sync / check）：否，PowerShell 入口可用；脚本自行拉取模板远端
- post-sync-cleanup：轻量执行，只读检查 workflow / 受保护文件 / docs 分区，不做迁移
- docs-system-audit（同步后审计）：轻量执行，只确认规范镜像刷新与项目事实文档未被同步改动，不做完整 PLM 审计
- 项目验证建议 / 已执行验证：已执行 `check-derived-sync`；未运行应用测试 / lint（本次不改业务代码）

### 命令真实性记录

| 步骤 | 实际命令 / 动作 | 退出结果 | 是否完整执行 | 是否等价替代 | 是否生成独立报告 | 备注 |
|---|---|---|---|---|---|---|
| dry-run 预览 | `scripts/sync-template.ps1 --dry-run --no-stat --preserve-project-version` | 退出 0 | 是 | 否 | 不适用 | 预览模板清单变更，允许 `TEMPLATE-BASE.md`，未发现受保护项目文件 |
| commit / 同步 | `scripts/sync-template.ps1 --commit --preserve-project-version` | 退出 0，提交 `ced2c76` | 是 | 否 | 不适用 | `VERSION` / `CHANGELOG.md` 保留，新增 `TEMPLATE-BASE.md` |
| check-derived-sync | `scripts/check-derived-sync.ps1 HEAD` | 退出 0 | 是 | 否 | 不适用 | 同步边界检查通过 |
| post-sync-cleanup | 只读轻量检查 | 完成 | 轻量执行 | 否 | 否 | 未修改 README / `ai/project-rules.md` / 项目事实文档 |
| docs-system-audit | 只读轻量检查 | 完成 | 轻量执行 | 否 | 否 | 未做完整 00-09 / design PLM 审计 |
| 项目验证 | `check-derived-sync` + Git 状态检查 | 通过 | 是 | 否 | 不适用 | 应用级测试未运行，记录为未验证 |

## A13 完成判据矩阵

| A13 步骤 | 证据 | 状态 | 若非完成，原因 | 下一步 |
|---|---|---|---|---|
| 标准闭环计划 | 本轮执行前已说明同步分支、双版本模式、预期文件与验证方式 | 完成 |  |  |
| dry-run 预览 | `--dry-run --no-stat --preserve-project-version` 退出 0 | 完成 |  |  |
| commit + 边界验证 | `ced2c76` + `check-derived-sync` 通过 | 完成 |  |  |
| post-sync-cleanup | workflow / 受保护文件 / 分区轻量检查 | 轻量执行 | 未按 `15-post-sync-cleanup` 完整生成迁移计划 | 如需严格闭环，单独执行 `/run post-sync-cleanup` 完整审计 |
| docs-system-audit | 规范镜像刷新与项目事实文档未被同步改动的轻量检查 | 轻量执行 | 未按 `16-docs-system-audit` 完整审计 00-09 / design / env | 如需严格闭环，单独执行 `/run docs-system-audit` 同步后审计 |
| 提案回流收口 | #148、#160 远端 CLOSED；模板 changelog 已记录回流落地；本地提案已归档 | 完成 |  |  |
| 同步报告留痕 | `sync-records/template-sync/2026-07-11-sync-template-v1.46.0.md` | 完成 |  |  |

> 结论：同步主链完成；因 post-sync-cleanup 与 docs-system-audit 为轻量执行，本轮不称“A13 完整闭环完成”。

## 同步结果

- 是否成功：成功
- 新增 / 修改的方法论文件：见同步提交 `ced2c76`
- `VERSION` / `CHANGELOG.md` 是否保持项目自身版本：是；同步提交先保留旧值，随后本分支将项目自有版本基线重定义为 `v0.1.0`，并将 `CHANGELOG.md` 改为项目变更记录
- `TEMPLATE-BASE.md` 是否新增 / 更新继承模板版本：是，新增并记录当前同步模板版本 `v1.46.0`
- 项目专属文件是否被误改：否；同步提交未包含根 `README.md`、`ai/project-rules.md`、`docs/00-09`、`frontend/`、`backend/`、`tests/`、`docker/`
- 是否新增 / 刷新 `ai/doc-standards/00-09`：是，已刷新
- 是否残留旧 `docs/_scaffold/`：本轮未处理；如存在，后续完整 docs-system-audit 再判断

## 双版本试点观察

- `--preserve-project-version` 可在普通派生项目中保留 `VERSION` / `CHANGELOG.md`。
- 新增 `TEMPLATE-BASE.md` 字段完整：模板仓、Base template version、Current synced template version、Synced at、Project version file、Project version at sync time。
- `check-derived-sync` 在双版本模式下跳过 README ↔ `VERSION` 模板版本一致性检查，并改为校验 `TEMPLATE-BASE.md` 当前同步模板版本。
- 迁移结论：`zhiyan` 旧语义下的 `VERSION=v1.43.0` 原本是继承模板版本，不作为项目版本基线；本轮将项目自有版本基线重定义为 `v0.1.0`。

## 同步后整理摘要

- 是否执行 `/run post-sync-cleanup`：轻量执行，不做迁移
- README / `ai/project-rules.md` / docs 分区是否需整理：本次未发现同步误改；完整整理需另开任务
- workflow：仅存在 `.github/workflows/project-check.yml`，未发现模板仓 `template-check.yml`
- 已处理项：无项目事实文档迁移
- 待确认项：无；用户已确认不沿用旧 `VERSION=v1.43.0`
- 建议回写 / 后续迁移任务：后续模板同步继续使用 `--preserve-project-version`

## 文档体系审计摘要

- 是否执行 `/run docs-system-audit` 同步后审计模式：轻量执行
- 规范基线缺口：未做完整审计
- 可接受兼容差异：旧项目不要求机械重写 `docs/00-09`
- 项目事实风险：本次同步未修改项目事实文档；仍需完整审计时另开任务
- 回梳计划摘要：暂无，本轮仅验证同步机制

## 项目验证建议

- 建议运行的测试 / lint / 文档检查 / 人工验收：如本分支进入 PR，可运行 `git diff --check`、项目既有前后端测试 / lint（若审查者要求）
- 已执行验证与结果：`check-derived-sync` 通过；`git status --short --branch` 干净
- 未验证项与原因：未运行应用测试 / lint，因为本次只同步方法论与模板规范镜像，不修改业务代码

## 遇到的问题

- Git / gh / Git Bash / PowerShell / 网络问题：无阻塞；同步过程中出现 `TEMPLATE-BASE.md` LF→CRLF 工作区提示，不影响提交与边界检查
- `gh issue create` / `submit-proposal` 问题：未创建新 issue
- 同步脚本问题：旧 `zhiyan` 同步脚本不支持 `--preserve-project-version`，已先 bootstrap 最新同步脚本
- Prompt / 快捷命令理解问题：无新增
- 文档说明不清：已处理，项目版本基线改为 `v0.1.0`
- 派生项目专属冲突：无

## 可优化点归纳

| 问题 | 是否项目专属 | 是否建议回流模板 | 建议提案 |
|---|---|---|---|
| 旧派生项目从“继承模板 VERSION”迁移到“双版本”时，项目自身版本基线可能需要人工确认 | 否 | 暂不新增；本项目已采用 `v0.1.0` 作为基线 | 如多项目复现，再补迁移提示提案 |

## 已生成的回流提案

- 无

## 提案回流收口

- 扫描范围：`_proposals/`、最近同步记录、模板仓 issue 链接
- 已确认被模板采纳或已有决议的提案：`TEMPLATE-UPGRADE-a13-sync-closure-and-dry-run-robustness.md`（#148）、`TEMPLATE-UPGRADE-demo-runbook-trigger.md`（#160）
- 已归档到 `_archive/proposals/` 的本地提案：上述两项
- 仍需保留在 `_proposals/` 的提案：无（除 `_proposals/README.md`）
- 无法判断是否已处理的 issue / 提案与待确认项：无

| 本地提案 | 模板 issue / PR | 远端状态 | 关闭原因 / 处理结果 | 本地动作建议 |
|---|---|---|---|---|
| `TEMPLATE-UPGRADE-a13-sync-closure-and-dry-run-robustness.md` | #148 | closed | 已分批落地到 A13 门禁、fallback 参数修复、dry-run 轻量预览；模板 changelog 记录回流 | 归档 |
| `TEMPLATE-UPGRADE-demo-runbook-trigger.md` | #160 | closed | 已落地 `show-demo` 命令与 `demo-runbook-template`；模板 changelog 记录回流 | 归档 |

## 后续动作

- 是否需要 `/run post-sync-cleanup`：可选；若要严格 A13 完整闭环，需完整执行
- 是否需要 `/run docs-system-audit`：可选；若要严格 A13 完整闭环，需完整执行
- 是否需要按审计结果回梳 `docs/00-09` / `docs/design` / `docs/env`：本轮未发现必须项
- 是否需要补项目验证入口：本轮不需要
- 是否需要人工清理旧目录：未判断
- 是否需要同步回模板仓库：暂不需要；本次无新回流提案
