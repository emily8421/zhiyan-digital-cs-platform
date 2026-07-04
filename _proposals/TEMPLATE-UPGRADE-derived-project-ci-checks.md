# TEMPLATE-UPGRADE: 区分模板仓与派生项目的 CI 检查入口

> 类型：派生项目中发现的模板优化提案。
> 状态：待评估 / 待回流。
> 关联：`.github/workflows/template-check.yml`、`scripts/check-template.sh`、`scripts/check-derived-sync.sh`、`scripts/check-derived-sync.ps1`、`scripts/new-project.sh`、`scripts/sync-template.*`、`template-sync.json`。

## 1. 背景与问题

模板仓与派生项目当前已经在文档和脚本层区分了两类检查：

- 模板仓完整性自检：`scripts/check-template.sh` / `scripts/check-template.ps1`。
- 派生项目同步边界检查：`scripts/check-derived-sync.sh` / `scripts/check-derived-sync.ps1`。

现有说明已多次强调：派生项目同步验收不应运行模板仓自检。但在实际派生项目中，如果 `.github/workflows/template-check.yml` 保留模板仓逻辑，普通 PR 仍会运行 `scripts/check-template.sh`，导致派生项目被模板仓规则误拦截。

典型失败表现包括：

- 要求派生项目 README 保留模板仓 SOP / beginner guide / template guide 入口。
- 要求派生项目 `docs/00-09` 保留模板文档占位结构。
- 要求 `_proposals/README.md` 是模板仓“提案收件箱”口径。
- 要求 Product Vision 保留派生初始化替换提示。

这些检查对模板仓是正确的，但对已经项目化的派生项目是错误的。它会误导 AI 或维护者去修复本不该修复的项目事实文档。

## 2. 根因分析

该问题不是单个派生项目配置错误，而是模板方法论缺少“CI 入口派生化”规则：

- 模板仓 workflow 适合模板仓自身，不适合派生项目。
- 派生项目需要保留 `git diff --check` 等通用质量检查，但不应对普通业务 / 文档 PR 跑 `check-template`。
- `check-derived-sync` 只适合模板同步提交，不适合所有普通 PR。
- 新项目生成、同步清单和自检断言未形成闭环，导致派生项目容易继承或保留模板仓 workflow。

## 3. 设计目标

- 明确区分模板仓 CI 与派生项目 CI。
- 防止派生项目普通 PR 被模板仓完整性自检误拦截。
- 保留模板同步提交的边界检查能力。
- 保留通用空白检查，避免降低基础质量门槛。
- 在新项目生成和模板同步流程中固化正确默认值，减少人工事后修复。

## 4. 建议方案

### 4.1 模板仓 CI

模板仓自身继续保留完整自检：

```yaml
- name: Run template self-check
  run: bash scripts/check-template.sh
```

适用范围：`ai-project-template` 模板仓。

### 4.2 派生项目 CI

派生项目默认 workflow 建议采用以下逻辑：

```yaml
name: Project Check

on:
  pull_request:
    branches:
      - main
  push:
    branches:
      - main

jobs:
  project-check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Check whitespace
        shell: bash
        run: |
          if [[ "${{ github.event_name }}" == "pull_request" ]]; then
            git diff --check "${{ github.event.pull_request.base.sha }}" "${{ github.event.pull_request.head.sha }}"
          elif [[ "${{ github.event.before }}" =~ ^0+$ ]]; then
            git diff-tree --check --no-commit-id --root -r "${{ github.sha }}"
          else
            git diff --check "${{ github.event.before }}" "${{ github.sha }}"
          fi

      - name: Check derived sync boundary
        shell: bash
        run: |
          subject="$(git log -1 --format=%s)"
          if [[ "$subject" =~ ^sync[[:space:]]template[[:space:]]v[0-9]+\.[0-9]+\.[0-9]+[[:space:]]from[[:space:]]ai-project-template$ ]]; then
            bash scripts/check-derived-sync.sh HEAD
          else
            echo "Not a template sync commit; skip derived sync boundary check."
          fi
```

适用范围：由模板生成或同步的派生项目。

### 4.3 同步策略

建议模板明确以下规则：

- `.github/workflows/template-check.yml` 不应直接作为派生项目同步文件下发。
- `scripts/new-project.sh` 应生成派生项目版 workflow，而不是复制模板仓自检 workflow。
- 如模板同步流程检测到派生项目存在旧版 `template-check.yml`，应提示迁移为 `Project Check` 或提供自动迁移选项。
- `check-template.sh` 应增加 smoke test，确保新生成派生项目不会默认运行 `scripts/check-template.sh`。

## 5. 拟改范围

### 模板规则 / 文档

- `ai/global-rules.md`：补充模板仓检查与派生项目检查边界。
- `ai/session-rules.md` 或维护流程文档：提醒 AI 遇到派生项目 CI 跑模板自检时，应先判断 CI 配置是否错误，而不是修改项目事实文档。
- `git-guide.md`：在 PR / CI 章节补充派生项目 workflow 推荐配置。

### 脚本

- `scripts/new-project.sh`：生成派生项目版 `.github/workflows/project-check.yml` 或等价 workflow。
- `scripts/sync-template.sh` / `scripts/sync-template.ps1`：检测旧版派生 workflow 并提示迁移。
- `scripts/check-template.sh`：保留模板仓自检断言，同时增加派生项目 smoke test，确保新项目 workflow 不跑 `check-template`。

### 同步清单

- `template-sync.json`：确认是否应同步 workflow 文件。
  - 若不同步 workflow，应在新项目生成脚本中负责创建派生 workflow。
  - 若同步 workflow，应区分模板仓版与派生项目版，避免同一路径承载两种语义。

### 提示词 / 命令

- `ai/prompts/maintainers/12-sync-template.md`：补充同步后检查派生 workflow 的步骤。
- `ai/commands/sync-methodology.md`：补充不要用模板仓自检阻塞派生普通 PR 的说明。
- `ai/prompts/maintainers/15-post-sync-cleanup.md`：将旧 workflow 迁移列入 post-sync cleanup 检查项。

## 6. 版本影响

建议作为后续 minor 版本落地。

理由：该变更会影响新项目生成、派生项目 CI 默认行为、模板同步后检查流程和维护者判断口径；属于可见的方法论增强，但不改变项目事实文档体系。

## 7. 验收口径

- 模板仓 PR 仍运行 `scripts/check-template.sh`。
- 新生成派生项目的普通 PR 不运行 `scripts/check-template.sh`。
- 新生成派生项目的普通 PR 仍运行 `git diff --check`。
- 新生成派生项目的模板同步提交会运行 `scripts/check-derived-sync.sh HEAD` 或 PowerShell 等价入口。
- `scripts/check-template.sh` 的新项目 smoke test 能发现派生 workflow 误跑模板自检的问题。
- 文档明确说明：派生项目普通 PR 如果因模板占位 / 模板 README / Product Vision 初始化提示失败，应优先检查 workflow 是否误用模板自检。

## 8. 风险与缓解

- **派生项目质量门槛降低**：保留 `git diff --check`；项目自己的测试 / lint 应由项目后续补充，不由模板自检替代。
- **模板同步提交漏检**：仅对匹配 `sync template vX.Y.Z from ai-project-template` 的提交运行 `check-derived-sync`，保留同步边界检查。
- **workflow 文件双重语义混乱**：建议模板仓版和派生项目版分离命名，或由新项目脚本生成派生版。
- **老派生项目仍保留旧 workflow**：同步脚本或 post-sync cleanup 提示迁移，避免静默保留错误配置。
- **Windows / Git Bash 兼容性**：派生项目本地可继续使用 `check-derived-sync.ps1` fallback；GitHub Actions Ubuntu 环境可直接使用 Bash 入口。
