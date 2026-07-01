# TEMPLATE-UPGRADE: sync/check PowerShell 原生 fallback（Git Bash/MSYS 启动失败时）

> 类型：派生项目起草的模板优化提案（去项目化）。
> 状态：已落地于 v1.21.3（2026-07-01）；从 `_proposals/` 归档到 `_archive/proposals/`。
> 来源：派生项目同步 `v1.21.0` 的真实运行记录；详见本项目 `docs/archive/template-sync/2026-06-30-sync-template-v1.21.0.md`。

## 1. 动机

派生项目在 Windows / PowerShell 环境执行 `scripts/sync-template.ps1 --dry-run`、`scripts/check-derived-sync.ps1` 时，遇到 Git Bash / MSYS 启动失败：

```text
fatal error - couldn't create signal pipe, Win32 error 5
```

当前 `.ps1` 入口只负责定位并启动 Git Bash；一旦 Git Bash/MSYS 被本机权限、终端宿主或安全软件阻断，流程会直接失败。派生项目仍可用 Git 原生命令与 PowerShell 等价完成同步 / 校验，但该 fallback 未模板化，容易导致：

- 用户误以为模板同步失败，而不是本机 Git Bash 运行环境问题。
- AI 需要临场手写等价同步逻辑，增加误写空文件、漏同步或混入项目事实改动的风险。
- `check-derived-sync` 无法在没有 Git Bash 的 Windows 环境下提供边界检查结果。

## 2. 拟改

建议为 Windows PowerShell 入口增加原生 fallback 或独立脚本：

- `scripts/sync-template.ps1`：当 Git Bash 启动探测失败时，提供明确选项或自动转入 PowerShell 原生 dry-run / commit 流程。
- `scripts/check-derived-sync.ps1`：当 Git Bash 不可用时，用 PowerShell 原生逻辑检查：工作区状态、同步清单、最近提交标题、变更文件是否在 `template-sync.json` 或允许镜像路径内。
- `git-guide.md` / `template-docs/env-setup.md`：补充“Git Bash 失败时可使用 PowerShell fallback；若 fallback 不可用，才要求修复 Git Bash/MSYS 环境”。
- `template-docs/derived-sync-report-template.md`：在“遇到的问题”中提示记录是否走了 fallback。

## 3. PowerShell fallback 最小能力

### sync dry-run

- `git fetch --no-tags --depth=1 <template-remote> main`
- 读取远端 `template-sync.json`
- 对比本地文件与 `FETCH_HEAD:<file>`
- 对比模板 `docs/00-09` 与本地 `ai/doc-standards/00-09`
- 输出差异清单，不修改工作区、不 stage

### sync commit

- 仅在用户明确确认后执行
- 从 `FETCH_HEAD` 恢复 `template-sync.json` 清单内文件
- 镜像模板 `docs/00-09` 到 `ai/doc-standards/00-09`
- 不覆盖派生项目 `docs/00-09`
- 自动提交或输出待提交清单（行为与 Bash 脚本保持一致）

### check-derived-sync

- 读取 `template-sync.json`
- 允许 `ai/doc-standards/*`（以及迁移期旧 `docs/_scaffold/*`）
- 拦截 `README.md`、`ai/project-rules.md`、项目事实 `docs/00-09`、业务代码目录等同步提交越界
- 输出与 Bash 版本一致的通过 / 失败摘要

## 4. 版本影响

建议作为补丁或小版本增强（例如 v1.21.x / v1.22.0）。不改变模板方法论，只增强 Windows 同步可用性与安全性。

## 5. 影响面

- `scripts/sync-template.ps1`
- `scripts/check-derived-sync.ps1`
- `git-guide.md`
- `template-docs/env-setup.md`
- `template-docs/derived-sync-report-template.md`
- 可选：`scripts/check-template.ps1` 若同样依赖 Git Bash，也可沿用 fallback 模式

## 6. 验收口径

- 在 Git Bash 正常的 Windows 环境，现有行为不回退、不破坏。
- 在 Git Bash 无法启动但 Git CLI 可用的 Windows 环境，`sync-template.ps1 --dry-run` 能输出只读差异预览。
- `sync-template.ps1 --commit` 不覆盖派生项目 `docs/00-09`，只同步清单文件与 `ai/doc-standards/00-09`。
- `check-derived-sync.ps1` 能在无 Git Bash 环境下完成边界检查。
- 文档明确说明 fallback 的适用边界，不把所有 Git Bash/MSYS 问题都包装成模板 bug。

## 7. 风险

- PowerShell 与 Bash 双实现可能漂移：建议抽取共享同步清单读取规则，并在模板自检中加入关键断言。
- 自动 fallback 若过于静默，可能掩盖本机 Git Bash 问题：建议在输出中明确标注“使用 PowerShell fallback”。
- `--commit` fallback 涉及写文件和提交，必须保留干净工作区检查与同步边界保护。
