# TEMPLATE-UPGRADE: 模板可维护性审计与去个人化优化

> 类型：模板仓库内直接发起（去项目化）。
> 状态：已落地于 v1.18.3（2026-06-28）；随 PR #40 合并，从 `_proposals/` 归档到 `_archive/proposals/`。
> 关联：v1.18.2 后对 `ai-project-template` 进行只读评估时发现的维护性、隐私边界与自检覆盖优化点。

## 1. 现状与问题

当前模板已经具备较完整的文档驱动链路、下行同步机制、`docs/_scaffold` 规范镜像、`16-docs-system-audit` 审计闭环以及 PR/CI 保护。后续优化重点不再是补齐单点能力，而是降低模板继续演进时的维护成本，并减少派生项目误用或带入个人信息的风险。

本次审计发现以下问题：

- **[H1] Bash 自检版本断言仍有硬编码**：`scripts/check-template.sh` 仍用固定字符串断言 `CHANGELOG.md` 包含 `v1.9.0`，而当前模板版本已是 `v1.18.2`。这会让“CHANGELOG 是否包含当前 VERSION”的检查失真。PowerShell 入口已经动态读取 `VERSION`，Bash 入口应对齐。
- **[H2] 同步文件中存在个人账号 / 邮箱 / Token 类型经验**：`git-guide.md` 会随 `template-sync.json` 下行同步，但其账号体系章节包含具体 GitHub 账号、邮箱和 PAT 类型说明。模板公开复用时，应保留通用多账号操作方法，把个人账户事实移出同步文档。
- **[H3] CHANGELOG 顺序缺少机器保护**：`CHANGELOG.md` 中历史记录曾出现同一日期版本排序不严格降序的情况。当前没有断言防止新增版本插入位置错误。
- **[M1] `check-template.sh` 体积过大且多职责耦合**：脚本同时负责结构断言、同步 dry-run、新项目烟测、`_scaffold` 镜像验证和文档滞后断言，后续继续追加规则会越来越难维护。
- **[M2] README 命令入口混合模板维护者与派生项目使用者**：`README.md` 常用命令块同时列出新建项目、环境准备、远端建仓、模板自检和派生同步。新手容易混淆哪些命令在模板仓库跑，哪些命令在派生项目跑。
- **[M3] Windows / Git Bash 边界需要矩阵化表达**：当前 README 已有边界说明，但 `check-template.ps1`、`sync-template.ps1`、`check-derived-sync.ps1` 的 Git Bash 依赖和 fallback 行为不同，适合用矩阵统一说明。
- **[M4] 派生项目初始化占位仍容易漏填**：`ai/project-rules.md` 中多个关键项仍是占位或 `待确认`，虽然规则要求生成 docs/03-09 前必须填好，但可以通过 `new-project.sh` 生成更明确的最小填表示例或首次任务 checklist 降低漏填概率。
- **[L1] 同步清单可读性依赖 JSON 与脚本断言**：`template-sync.json` 是权威源，但人读文档只概述原则。维护者常需要打开 JSON 才知道具体同步项，可考虑生成或维护一份同步清单摘要。
- **[L2] 关键机制的多入口引用断言可以通用化**：v1.18.2 已对 `_scaffold` / 16 审计闭环补了防文档滞后断言。未来新增关键机制时，应复用类似模式，要求脚本、Prompt、README / SOP / MAINTAINERS / git-guide 等入口同步引用。
- **[L3] 本地续接文件模式可提供示例**：`NEXT-STEPS.md` 已被 `.gitignore` 忽略，适合作为本地会话续接文件。可以提供 `NEXT-STEPS.example.md` 或在 README / SOP 中简述用法，帮助新维护者建立不入库的续接习惯。

## 2. 拟改

建议拆成一个小版本落地，范围控制为“维护性与安全边界增强”，不改变模板方法论主流程：

1. **动态化 Bash 版本断言**
   - 修改 `scripts/check-template.sh`，读取根目录 `VERSION` 并断言 `CHANGELOG.md` 包含该版本。
   - 保持 `scripts/check-template.ps1` 现有动态行为不变。

2. **去个人化 `git-guide.md`**
   - 把具体账号、邮箱、PAT 类型描述改成通用占位示例。
   - 保留多账号切换、提交身份、权限不足排查等通用操作。
   - 如需保留本仓库维护者本地账号备忘，放入被忽略的本地续接文件，不进入同步清单。

3. **增加 CHANGELOG 排序自检**
   - 在 `scripts/check-template.sh` 增加轻量断言：从 `CHANGELOG.md` 提取 `## vMAJOR.MINOR.PATCH` 标题，确保首个版本等于 `VERSION`，并尽量保证版本标题按语义版本降序排列。
   - PowerShell 入口可选择同步增强，或先保持结构检查入口轻量，作为后续补齐项。

4. **拆分 README 常用命令**
   - 将 `README.md` 的常用命令分为“派生项目使用者”和“模板维护者”两组。
   - 明确模板自检只在模板仓库跑；派生项目同步后跑 `check-derived-sync`，不跑完整 `check-template`。

5. **补 Windows 命令选择矩阵**
   - 在 `README.md` 或 `template-docs/env-setup.md` 增加简短矩阵：脚本入口、运行目录、是否依赖 Git Bash、失败时优先排查方向。
   - 与 `git-guide.md` / `SOP.md` 保持引用一致。

6. **增强派生项目首次填表指引**
   - 在 `scripts/new-project.sh` 生成的 README 或初始化提示中，增加 `ai/project-rules.md` 首次必填 checklist。
   - 可选：在 `ai/project-rules.md` 中把“模板占位”与“派生项目必须替换内容”标得更醒目。

7. **维护者同步清单摘要**
   - 在 `MAINTAINERS.md` 增补“同步清单摘要维护规则”：`template-sync.json` 是权威，文档只写分组摘要，不重复完整清单。
   - 如新增自动生成脚本，需避免引入额外依赖。

8. **沉淀通用防滞后断言模式**
   - 在 `MAINTAINERS.md` 自检章节补一条：新增关键机制时，需要同时考虑脚本 / Prompt / 人读文档入口的引用断言。
   - 不绑定长文案，优先断言稳定关键词。

9. **补本地续接文件说明**
   - 在 `CONTRIBUTING.md` 或 `SOP.md` 简述 `NEXT-STEPS.md`：本地可建、可更新、不可提交。
   - 可选新增 `NEXT-STEPS.example.md`；若新增，需决定是否纳入同步清单。

## 3. 版本影响

建议版本：**PATCH，v1.18.2 → v1.18.3**。

理由：主要是自检增强、文档去个人化、入口说明重排与维护流程提醒；不改变文档生命周期、编号体系、同步机制或派生项目运行时行为。

如落地时决定拆分脚本模块或新增 `NEXT-STEPS.example.md` 并纳入同步清单，可视实际影响评估是否仍保持 PATCH。

## 4. 影响面

预计修改文件：

- `scripts/check-template.sh`
- `git-guide.md`
- `README.md`
- `MAINTAINERS.md`
- `SOP.md` 或 `CONTRIBUTING.md`（用于 `NEXT-STEPS.md` / 操作入口说明，二选一或都少量更新）
- `scripts/new-project.sh`（如增强派生项目首次填表指引）
- `VERSION`
- `CHANGELOG.md`

可选修改文件：

- `scripts/check-template.ps1`（如同步增加 CHANGELOG 排序自检）
- `template-docs/env-setup.md`（如 Windows 命令矩阵放在环境手册）
- `NEXT-STEPS.example.md`（如决定提供本地续接示例）
- `template-sync.json`（仅当新增同步文件时需要）

## 5. 验收

- `bash scripts/check-template.sh` 通过。
- `powershell -ExecutionPolicy Bypass -File scripts/check-template.ps1` 通过或至少保持现有结构检查通过。
- `git-guide.md` 不再包含具体个人 GitHub 账号、个人邮箱或 PAT 类型事实。
- `CHANGELOG.md` 首个版本与 `VERSION` 一致，且排序自检可捕获明显乱序。
- README 能清晰区分模板维护命令与派生项目使用命令。
- Windows 脚本入口的 Git Bash 依赖 / fallback 行为在一个权威位置可查。
- 若增强 `new-project.sh`，本地 smoke 新建项目后 README / 初始化提示包含 `ai/project-rules.md` 首次必填 checklist。

## 6. 风险

- 去个人化 `git-guide.md` 时，需避免删掉真正通用的多账号 / 权限排查经验。
- CHANGELOG 语义版本排序断言需处理历史版本如 `v1.5`、`v1.6` 这种两段式旧记录；建议只对三段式标题做强校验，对旧历史记录放行或先规范化历史标题。
- 拆分 `check-template.sh` 可能触及 CI 入口，若本轮只做低风险修复，可先不拆脚本，只新增“后续模块化”待办。
- `NEXT-STEPS.example.md` 若纳入同步清单，可能被派生项目误认为必须维护；若不纳入同步清单，则只作为模板维护者参考。
