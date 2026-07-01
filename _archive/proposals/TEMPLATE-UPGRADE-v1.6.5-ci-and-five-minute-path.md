# TEMPLATE-UPGRADE-v1.6.5：新增 CI 自检、5 分钟最小路径与同步可维护性改进

## 状态

- 状态：已随本次模板改动落地，归档留痕
- 目标版本：v1.6.5
- 提案来源：模板评估 P0 / P1 / P2 改进项

## 背景

模板已有 `scripts/check-template.sh` 本地自检，但 PR 合并前仍依赖人工记得运行；同时 README 的快速开始偏标准流程，对第一次使用者来说仍需理解较多上下文。

评估后确定一组高优先级改进：

1. 将模板自检接入 GitHub Actions，让 PR 自动运行 `git diff --check` 与 `bash scripts/check-template.sh`。
2. 在 README 顶部补一个“5 分钟最小路径”，帮助新项目从产品愿景起步，优先采集本机环境，再让 AI 生成完整文档体系。
3. 降低 Windows 环境中直接调用 Bash 的摩擦，提供 PowerShell 包装入口。
4. 将下行同步清单抽成机器可读文件，避免 README、脚本和自检三处手动漂移。
5. 增加派生项目本地烟测，确保 `new-project.sh --local --no-remote --no-examples` 可用。
6. 增加裁剪决策表，降低初始化时是否保留 `docs/06`、`docs/07`、`frontend/`、`backend/`、`tests/`、`docker/` 的判断成本。

## 目标

1. 新增 `.github/workflows/template-check.yml`，覆盖 PR / main push 的基础自检。
2. 在 README 快速开始处新增“5 分钟最小路径（愿景 → 本机 Demo）”。
3. 最小路径以 `docs/vision/product-vision.md` 为输入，而不是手写 00-02。
4. 最小路径要求先生成 `docs/env/local-env.md`，确保 04 架构、05 技术方案、09 验证计划受本机环境约束。
5. 更新 `scripts/new-project.sh` 生成的派生项目 README，使新项目默认按愿景 + 环境约束启动。
6. 更新 `scripts/check-template.sh`，检查 CI workflow 与最小路径入口存在。
7. 新增 `template-sync.json`，作为下行同步清单事实来源。
8. 新增 `scripts/check-template.ps1` 与 `scripts/sync-template.ps1`，作为 Windows / PowerShell 入口。
9. 在自检中加入 `new-project` 本地-only 烟测。
10. 在 README 增加裁剪决策表。

## 拟改范围

- `VERSION`：升级到 `v1.6.5`。
- `README.md`：新增 5 分钟最小路径与版本记录。
- `.github/workflows/template-check.yml`：新增 PR / main push 自检。
- `scripts/new-project.sh`：更新派生项目 README 快速开始。
- `template-sync.json`：新增同步清单事实来源。
- `scripts/sync-template.sh`：优先读取 `template-sync.json`。
- `scripts/check-template.sh`：新增 CI、最小路径、同步清单和新项目烟测断言。
- `scripts/check-template.ps1`：新增 Windows 自检入口。
- `scripts/sync-template.ps1`：新增 Windows 下行同步入口。
- `_archive/proposals/TEMPLATE-UPGRADE-v1.6.5-ci-and-five-minute-path.md`：本提案归档。

## 版本影响

- 版本类型：PATCH。
- 理由：增强模板入口与治理自动化，不改变核心文档编号、AI 行为原则或同步机制。

## 验证方式

- 运行 `git diff --check`。
- 运行 `bash scripts/check-template.sh`。
