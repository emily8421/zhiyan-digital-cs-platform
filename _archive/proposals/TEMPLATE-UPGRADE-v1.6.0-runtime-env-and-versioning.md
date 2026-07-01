# TEMPLATE-UPGRADE-v1.6.0：运行环境资源约束与三段式模板版本治理

## 状态

- 状态：已随本次模板改动落地，归档留痕
- 目标版本：v1.6.0
- 提案来源：模板维护过程中的初始化流程优化

## 背景

在生成系统架构、技术方案和 Demo / MVP 实现方案时，AI 容易默认选择“理论可行但本机跑不动”的方案，例如本地大模型、向量数据库、多服务 Docker Compose、GPU 推理或重型数据库组合。

模板此前缺少统一的本机环境采集入口，也缺少“本机 Demo 可行性 / 服务器资源预案”的固定文档位置，导致技术方案无法稳定受项目机器资源约束。

同时，模板此前只在 `ai/global-rules.md` 顶部使用两段式版本 `vX.Y`，且只在修改 `global-rules` 时递增版本。若新增脚本、Prompt、文档骨架、自检或同步清单，即使下游项目需要同步，版本号也不会变化，不利于审计与下行同步判断。

## 目标

1. 在模板中新增“运行环境与资源约束”机制，使 AI 在生成架构和技术方案前先读取本机环境信息。
2. 提供可运行的 PowerShell 脚本，自动采集大部分本机硬件 / 软件信息，减少人工填写。
3. 保留人工确认项，覆盖 Demo 资源边界、联网权限、公司服务器权限、敏感数据和服务器资源预案。
4. 将资源约束纳入 `project-rules`、架构、技术方案、验证计划、初始化 Prompt、README、自检与参考样例。
5. 将模板版本策略升级为三段式 `vMAJOR.MINOR.PATCH`，以根目录 `VERSION` 作为整个模板版本的单一审计入口。
6. 明确任何模板修改都必须先有提案记录，完成后归档到 `_archive/proposals/`。

## 拟改范围

### 新增

- `VERSION`：记录整个模板版本，当前为 `v1.6.0`。
- `scripts/collect-env.ps1`：采集本机运行环境，生成 `docs/env/local-env.md`。
- `docs/env/README.md`：说明环境文档生成方式、使用要求和脱敏提醒。
- `_archive/proposals/TEMPLATE-UPGRADE-v1.6.0-runtime-env-and-versioning.md`：本提案归档。

### 修改

- `ai/project-rules.md`：新增 `§2.5 运行环境与资源约束`，并纳入初始化必填检查。
- `docs/04-architecture.md`：新增部署 / 运行拓扑约束。
- `docs/05-tech-spec.md`：新增运行环境与资源评估。
- `docs/09-verification.md`：新增本机资源验证。
- `INIT-PROMPT.md`：新增环境采集 Prompt，初始化和 checklist 读取环境约束。
- `README.md`：更新快速开始、轻量路径、同步清单和版本策略。
- `CONTRIBUTING.md`：新增提案先行、归档和三段式版本规则。
- `_proposals/README.md`、`_archive/proposals/README.md`：更新提案命名与归档要求。
- `scripts/sync-template.sh`：改为从 `VERSION` 读取模板版本，并同步 `VERSION` 与环境采集脚本。
- `scripts/check-template.sh`：检查 `VERSION`、环境采集入口、文档资源章节、提案归档规则。
- `scripts/new-project.sh`：派生项目 README 提醒先采集本机环境。
- `.github/pull_request_template.md`、`.github/ISSUE_TEMPLATE/template-change.md`：更新提案先行和三段式版本检查。
- `_examples/`：三个参考样例补资源约束章节，保持模板示例一致。

## 版本策略

采用三段式版本：`vMAJOR.MINOR.PATCH`。

- `MAJOR`：文档编号体系、核心流程、同步机制发生不兼容变化。
- `MINOR`：新增模板能力、初始化流程新增必填项、新增同步文件、文档骨架新增章节。
- `PATCH`：文案修正、Prompt 小修、自检增强、兼容性脚本修复。

本次改动新增运行环境资源约束机制、环境采集脚本、资源评估文档骨架、Prompt 和同步清单，属于模板能力级增强，版本定为 `v1.6.0`。

## 提案先行规则

任何需要修改项目模板的工作，都必须先形成 `TEMPLATE-UPGRADE-*.md` 提案，说明动机、拟改、版本影响、影响面和验证方式。

- 派生项目中发现的通用优化：先在派生项目 `_proposals/` 起草，再回流模板仓库。
- 模板仓库内直接发现的优化：也必须先新增提案，可在同一 PR 中落地并归档。
- 已完成的提案移动到 `_archive/proposals/`，作为审计记录。
- `_proposals/` 仅保留待处理或正在汇总的提案。

## 验证方式

- 运行 `powershell -ExecutionPolicy Bypass -File scripts/collect-env.ps1 -OutputPath docs/env/local-env.test.md`，确认可生成环境文档。
- 运行 `git diff --check`，确认无空白错误。
- 运行 `bash scripts/check-template.sh`，确认入口、文档骨架、版本号、同步清单和样例自洽。

## 影响面

- 下游项目同步后会获得新的环境采集脚本、Prompt、自检和版本策略。
- 下游项目需运行 `scripts/collect-env.ps1` 生成 `docs/env/local-env.md`，并人工补齐资源边界。
- 已有项目若未迁移 `ai/project-rules.md` §2.5，可在同步后人工补充。

