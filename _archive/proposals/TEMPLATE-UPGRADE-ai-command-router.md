# TEMPLATE-UPGRADE: AI 快捷命令与 Prompt 路由机制

> 类型：模板仓库内直接发起的模板优化提案。
> 状态：待评估 / 待落地。
> 关联：`SOP.md` 标准操作入口、`ai/prompts/` Prompt Library、`INIT-PROMPT.md` 轻量索引、`git-guide.md` 派生项目同步流程。

## 1. 背景与问题

当前模板已经提供较多操作说明与提示词模板，例如：

- `git-guide.md`：Git / GitHub / 派生项目同步流程。
- `SOP.md`：标准操作流程索引。
- `INIT-PROMPT.md`：初始化入口。
- `ai/prompts/`：按 dev / docs / review / maintainers / setup / git 等场景拆分的 Prompt Library。

这些文件解决了“标准流程和提示词在哪里定义”的问题，但实际使用时仍有入口成本：用户想做某类工作（如“派生项目更新方法论”“文档体系审核”“同步后项目整理”“模板提案汇总”）时，需要人工找到对应 prompt 文件，打开、复制提示词，再粘贴到 AI CLI 对话窗口。

AI CLI 本身可以直接读取仓库文件，因此继续依赖“人工复制 prompt”并不必要。更合适的方式是增加一层“快捷命令 / 命令路由”：用户用短命令或自然语言表达意图，AI 根据命令索引自动读取相关规则、SOP、prompt 与脚本说明，并按对应流程执行。

## 2. 设计目标

- 降低使用成本：用户无需记忆 prompt 文件路径，也无需复制粘贴长提示词。
- 保留权威来源：命令文件只做路由，不复制大段 prompt，避免 prompt 与命令内容双写漂移。
- 支持自然语言：用户说“更新方法论”“做文档体系审核”等，AI 能映射到标准命令。
- 明确执行边界：每个命令声明是否只读、是否可能写文件、是否必须先确认。
- 兼容现有结构：不替代 `SOP.md` / `ai/prompts/`，而是在其上增加更易用的入口层。
- 可自检防滞后：关键 prompt 应有命令入口，命令入口应指向真实存在的 prompt 和文档。

## 3. 建议方案

新增命令路由目录：

```text
ai/commands/
```

建议文件：

```text
ai/commands/README.md
ai/commands/sync-methodology.md
ai/commands/docs-system-audit.md
ai/commands/post-sync-cleanup.md
ai/commands/template-proposal-summary.md
ai/commands/run-dev-task.md
ai/commands/fix-bug.md
ai/commands/generate-docs.md
ai/commands/docs-checklist.md
ai/commands/collect-env.md
```

命令文件定位：**轻量路由器**，不重复完整 prompt，只声明用户说法、适用场景、必读文件、执行流程、写入风险和确认节点。

## 4. 命令触发方式

建议同时支持两类触发：

### 显式命令

```text
/run sync-methodology
/run docs-system-audit
/run post-sync-cleanup
```

### 自然语言别名

```text
更新方法论
同步模板方法论
做文档体系审核
同步后整理项目
汇总模板优化提案
执行当前 Sprint
```

AI 收到类似请求后，应先读取 `ai/commands/README.md` 或对应命令文件，确认命令含义，再按命令指定的权威文档与 prompt 执行。

## 5. 命令文件建议结构

示例：

```markdown
# Command: sync-methodology

## 用户说法

- 更新方法论
- 同步模板方法论
- sync methodology
- /run sync-methodology

## 适用场景

派生项目需要同步 `ai-project-template` 的最新方法论文件。

## 必读文件

- ai/index.md
- git-guide.md
- ai/prompts/maintainers/12-sync-template.md
- scripts/check-derived-sync.ps1

## 执行流程

1. 判断当前仓库是否为派生项目。
2. 检查 git 状态与当前模板版本。
3. 读取同步提示词与 git-guide 对应章节。
4. 输出同步计划与风险点。
5. 用户确认后执行 dry-run / commit。
6. 运行派生项目同步边界检查。
7. 输出同步后整理建议。

## 写入风险

会修改模板同步文件；执行前必须确认。
```

## 6. 首批命令建议

| 命令 | 用户意图 | 路由到 |
|---|---|---|
| `sync-methodology` | 派生项目更新 / 同步模板方法论 | `git-guide.md` §5 + `ai/prompts/maintainers/12-sync-template.md` |
| `post-sync-cleanup` | 同步后整理项目文档与规则 | `ai/prompts/maintainers/15-post-sync-cleanup.md` |
| `docs-system-audit` | 文档体系全链路审核 | `ai/prompts/review/16-docs-system-audit.md` |
| `template-proposal-summary` | 汇总模板优化提案 | `ai/prompts/maintainers/11-template-proposal-summary.md` |
| `generate-docs` | 生成 / 补齐 00-09 文档体系 | `ai/prompts/docs/00-generate-or-complete-docs.md` |
| `review-inputs` | 审查输入材料能否生成文档 | `ai/prompts/docs/01-review-inputs.md` |
| `docs-checklist` | 开发前文档检查 | `ai/prompts/review/10-docs-checklist.md` |
| `run-dev-task` | 执行当前 Sprint / 单任务 | `ai/prompts/dev/02-run-task.md` |
| `fix-bug` | 修复缺陷 | `ai/prompts/dev/05-fix-bug.md` |
| `sprint-summary` | Sprint 完成总结 | `ai/prompts/dev/09-sprint-summary.md` |
| `collect-env` | 收集本机环境 | `ai/prompts/setup/13-collect-env.md` + `scripts/collect-env.ps1` |
| `new-project` | 初始化派生项目 | `ai/prompts/setup/14-new-project.md` + `scripts/new-project.sh` |
| `commit-message` | 生成提交信息 | `ai/prompts/git/06-commit-message.md` |

## 7. 与现有文档的关系

- `ai/prompts/`：继续作为详细执行 prompt 的权威来源。
- `SOP.md`：继续作为人读流程总索引，可新增“快捷命令”列。
- `README.md`：面向新手展示常用命令入口，减少直接复制 prompt 的说明。
- `INIT-PROMPT.md`：可改为提示用户优先使用命令入口，再按需读取完整 prompt。
- `git-guide.md`：仍是 Git / 同步细节权威；命令只负责路由到对应章节。

## 8. 与会话续接机制的关系

本提案与 `TEMPLATE-UPGRADE-session-handoff.md` 互补：

- 命令开始执行后，应把命令名、任务目标、执行计划写入续接文件。
- 命令完成一个阶段后，应刷新“已完成 / 下一步 / 待确认项”。
- 新窗口恢复时，如果续接文件记录了正在执行的命令，应优先读取对应 `ai/commands/*.md` 继续。

因此两个提案可以同批落地，也可以先落地命令路由，再增强续接落盘。

## 9. 拟改范围

### 新增目录与文件

- `ai/commands/README.md`：命令索引、触发规则、命令文件格式、只读 / 写入确认规则。
- `ai/commands/*.md`：首批常用命令路由文件。

### 规则与入口

- `ai/index.md`：新增命令路由规则文件或索引入口，确保 AI 启动后知道可用命令。
- `ai/global-rules.md`：补充“用户提出常见操作意图时，优先查 `ai/commands/` 路由”的规则。
- `SOP.md`：在标准操作流程表中增加快捷命令列。
- `README.md`：新增“常用 AI 快捷命令”小节。
- `INIT-PROMPT.md`：提示优先使用快捷命令，不再强调复制长 prompt。

### 同步与自检

- `template-sync.json`：将 `ai/commands/README.md` 与首批命令文件加入下行同步清单。
- `scripts/check-template.sh`：增加断言，确保关键 prompt 有命令入口，命令入口引用的 prompt 文件存在。
- `MAINTAINERS.md`：新增维护要求：新增关键 prompt 或 SOP 时，应评估是否需要新增 / 更新命令入口。
- `CONTRIBUTING.md`：说明命令文件只做路由，不应复制大段 prompt，避免双写漂移。

## 10. 版本影响

建议作为 `v1.19.0` 或后续 minor 版本落地。

理由：该机制新增模板方法论入口层，改变用户与 AI 交互方式，并影响同步清单、SOP、README、规则文件与自检逻辑。

若与会话续接机制同批落地，可形成一组“AI CLI 使用体验增强”版本；若担心范围过大，可先落地命令路由，再单独落地续接自动写入。

## 11. 验收口径

- 用户输入 `/run sync-methodology` 或“更新方法论”时，AI 能定位到对应命令文件，并读取 `12-sync-template` 与 `git-guide.md` 后执行。
- 用户输入“做文档体系审核”时，AI 能定位到 `docs-system-audit`，读取 `16-docs-system-audit.md`，先出报告不改文件。
- 首批命令文件不复制大段 prompt，只保留路由信息与确认边界。
- `SOP.md` / `README.md` 能引导用户优先使用快捷命令。
- `template-sync.json` 包含命令入口文件，派生项目同步后也能使用快捷命令。
- `check-template.sh` 能检查命令入口与关键 prompt 的基本一致性，防止新增 prompt 后入口滞后。

## 12. 风险与缓解

- **命令与 prompt 双写漂移**：命令文件只写路由和确认边界，不复制完整 prompt；自检要求命令引用真实 prompt。
- **自然语言误触发**：AI 识别到可能命令但不确定时，应先复述将执行的命令并请求确认。
- **写入操作误执行**：命令文件必须声明写入风险；涉及修改、同步、安装、提交等操作前必须确认。
- **命令数量膨胀**：首批只覆盖高频场景；新增命令需满足“可复用、路径稳定、能降低入口成本”。
- **与 SOP 重叠**：SOP 保持人读流程索引，命令层作为 AI 执行路由，两者互补而非替代。
