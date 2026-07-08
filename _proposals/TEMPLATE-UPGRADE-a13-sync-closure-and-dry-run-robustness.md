# TEMPLATE-UPGRADE: A13 同步闭环门禁与 dry-run / PowerShell fallback 鲁棒性

> 来源：zhiyan-digital-cs-platform（emily8421/zhiyan-digital-cs-platform）派生项目回流
> 类型：模板优化提案草稿
> 状态：v1.43.0 同步后复盘起草，待提交模板仓 issue
> 来源记录：`sync-records/template-sync/2026-07-08-sync-template-v1.43.0.md`
> 关联：`template-docs/scenario-guides.md` A13、`ai/commands/sync-methodology.md`、`ai/prompts/maintainers/12-sync-template.md`、`template-docs/derived-sync-report-template.md`、`scripts/sync-template.ps1`、`scripts/check-derived-sync.ps1`
> 已知相关 issue：#102（PowerShell fallback / derived sync check，已关闭但本机仍复现相邻问题）

## 1. 背景与问题

派生项目执行模板同步时，用户说“同步项目模板”已经足以触发 A13「同步模板到派生项目」。A13 的完整闭环要求是：

```text
sync-methodology → post-sync-cleanup → docs-system-audit → 提案回流收口 → 同步报告留痕
```

本次派生项目从 `v1.30.3` 同步到 `v1.43.0`，最终同步提交、边界验证、PR 检查、合并和同步报告都已完成，但复盘发现 AI 执行过程存在可通用于其他派生项目的风险：

1. **A13 场景被降级成单点 `sync-methodology`**：AI 完成同步提交、PR 合并后，容易把“同步主链完成”误说成“A13 完整闭环完成”，而没有严格逐项核对 post-sync-cleanup、docs-system-audit、提案回流收口和同步报告完成判据。
2. **轻量审计与标准命令执行混淆**：AI 可能做了只读抽查并写入同步记录，却把它描述为已执行 `/run post-sync-cleanup` 或 `/run docs-system-audit`，没有标清“轻量执行 / 未生成独立报告 / 未做完整回梳”。
3. **提案回流收口不足**：只查询 issue 是否 `closed` 不足以判断本地 `_proposals/` 是否可归档；仍需区分“已采纳 / 已拒绝 / 已部分采纳 / 需 follow-up / 仍复现”。
4. **PowerShell fallback 仍有参数接收问题**：在 Windows PowerShell 5.1 + Git Bash 不可用时，`scripts/sync-template.ps1 --commit` fallback 仍误走 dry-run，本次只能按 `template-sync.json` 等价手工同步。
5. **大版本 dry-run 可用性不足**：`--dry-run` 在大量文件变更时会逐文件输出 diff stats 和临时目录 LF/CRLF warning，本次两次在 120s / 300s 超时；虽然同步安全可用清单边界核对兜底，但 A13 第 2 步“预览模板有哪些更新、会不会动项目文件”的体验和可审计性不足。

这些问题不是项目业务逻辑，可能影响任何使用 Windows / PowerShell fallback、通过 PR 合并同步分支、或跨大版本同步模板的派生项目。

## 2. 建议改动

### 2.1 A13 完成判据矩阵

在 `ai/prompts/maintainers/12-sync-template.md` 和 / 或 `ai/commands/sync-methodology.md` 中增加硬性收尾要求：

同步任务结束前必须输出 A13 完成判据矩阵，字段建议为：

| A13 步骤 | 证据 | 状态 | 若非完成，原因 | 下一步 |
|---|---|---|---|---|
| 标准闭环计划 | 用户确认记录 / 计划 | 完成 / 未完成 |  |  |
| dry-run 预览 | 命令与输出摘要 | 完成 / 等价替代 / 失败 |  |  |
| commit + 边界验证 | 同步提交 + `check-derived-sync` | 完成 / 等价替代 / 失败 |  |  |
| post-sync-cleanup | 审计摘要 / 报告路径 | 完整执行 / 轻量执行 / 未执行 |  |  |
| docs-system-audit | 审计摘要 / 报告路径 | 完整执行 / 轻量执行 / 未执行 |  |  |
| 提案回流收口 | issue 状态 + 归档建议 | 完成 / 部分完成 / 未执行 |  |  |
| 同步报告留痕 | `sync-records/template-sync/*` | 完成 / 未完成 |  |  |

状态必须区分：

- `完成`：按命令 / prompt 标准流程完整执行。
- `等价替代`：工具异常下采取等价安全动作，必须记录替代依据。
- `轻量执行`：只读抽查或摘要，不等于完整命令执行。
- `未执行`：明确列出原因和下一步。

若仍存在 `轻量执行` / `未执行`，最终回答不得称“A13 完整闭环完成”，只能称“同步主链完成，A13 闭环尚有剩余项”。

### 2.2 同步报告真实性约束

更新 `template-docs/derived-sync-report-template.md`，要求每个关键步骤记录：

- 实际命令。
- 退出结果。
- 是否完整执行。
- 是否为等价替代。
- 是否生成独立报告。
- 若未执行，后续补完路径。

尤其应避免以下模糊写法：

- “已执行 post-sync-cleanup”但实际只是人工只读抽查。
- “已执行 docs-system-audit”但没有说明是否为同步后审计模式、是否输出报告。
- “提案已关闭”但没有判断本地提案归档 / 保留策略。

### 2.3 提案回流收口决策矩阵

在 A13 第 6 步补充一个建议矩阵：

| 本地提案 | 模板 issue / PR | 远端状态 | 关闭原因 / 处理结果 | 本地动作建议 |
|---|---|---|---|---|
| `_proposals/TEMPLATE-UPGRADE-xxx.md` | #123 | open / closed / merged | 已采纳 / 拒绝 / 部分采纳 / 不明 | 归档 / 保留 / 新建 follow-up / 等待 |

仅有 `closed` 不得自动归档；若本机仍复现问题，应保留本地提案并建议补充原 issue 或新建 follow-up。

### 2.4 PowerShell fallback 参数修复

建议继续修复 `scripts/sync-template.ps1` fallback 参数接收，重点覆盖：

- `powershell -ExecutionPolicy Bypass -File scripts/sync-template.ps1 --commit` 在 Windows PowerShell 5.1 下必须进入 commit 分支。
- 避免使用容易与 PowerShell 自动变量 / 调用语义混淆的参数名，例如 helper 函数中的 `$Args`。
- 增加回归测试或模板自检场景：Git Bash 不可用 + `--dry-run`、Git Bash 不可用 + `--commit`、无参数默认 dry-run。
- 若 fallback 识别到 `--commit` 被解析为空或异常，应 fail-fast，不得静默执行 dry-run。

### 2.5 dry-run 大版本同步预览模式

建议为 `scripts/sync-template.*` 增加轻量预览能力，例如：

- `--list-only`：只输出目标版本、同步清单、变更文件名、风险路径命中，不输出逐文件 diff stats。
- `--summary`：按目录聚合新增 / 修改 / 删除数量，例如 `ai/`、`template-docs/`、`scripts/`。
- `--no-stat` 或 `--max-stat-files N`：避免大版本同步时对几十个文件逐个 `git diff --no-index --stat`。
- 抑制临时目录 LF/CRLF warning，或将其汇总成一条非阻塞提示。
- 在 A13 中明确：完整 dry-run 超时后，可以执行“同步清单边界核对模式”作为等价预览，但同步报告必须标记为“dry-run 未完整完成，使用等价边界核对替代”。

## 3. 版本影响

- `scripts/sync-template.ps1` fallback 参数修复适合 patch release。
- A13 完成判据矩阵、同步报告真实性约束和提案收口矩阵适合 minor 或 patch，取决于是否只改 prompt / docs。
- `--list-only` / `--summary` / `--no-stat` 属于脚本功能增强，适合 minor release。

## 4. 影响范围

- 影响 `sync-methodology`、A13 场景执行、派生项目同步报告和 Windows PowerShell fallback。
- 不改变派生项目业务文档、项目事实文档或 `template-sync.json` 同步边界语义。
- 改进后可降低以下风险：
  - 同步 PR 合并后误判 A13 完整完成。
  - 轻量审计被误写成完整审计。
  - issue closed 后本地提案被误归档。
  - Windows 用户 `--commit` fallback 静默变成 dry-run。
  - 大版本同步 dry-run 因输出过多无法完成。

## 5. 验收建议

1. 在派生项目中触发「同步模板」自然语言，AI 输出的计划应按 A13 七步建模，而不是只按 `sync-methodology` 单命令建模。
2. 在同步结束前，AI 必须输出 A13 完成判据矩阵；若 post-sync-cleanup / docs-system-audit 只是轻量执行，最终结论必须明确“未完整闭环”。
3. 在 Windows PowerShell 5.1 且 Git Bash 不可用的环境下，运行 `scripts/sync-template.ps1 --commit`，确认进入 commit 分支，不再误走 dry-run。
4. 构造一个大版本同步场景，运行 `--list-only` / `--summary` / `--no-stat`，确认能快速输出可审计的变更边界。
5. 对一个已关闭 issue 的本地提案执行提案收口，确认输出“归档 / 保留 / follow-up / 等待”的明确建议，而不是仅记录 `closed`。

## 6. 本次派生项目实证

- 同步记录：`sync-records/template-sync/2026-07-08-sync-template-v1.43.0.md`。
- 目标版本：`v1.43.0`。
- dry-run：输出目标版本和同步清单后在 diff stats 阶段超时。
- commit：PowerShell fallback `--commit` 仍误走 dry-run，最终按脚本等价逻辑手工同步。
- check-derived-sync：对同步提交通过。
- A13 复盘：同步主链完成，但 post-sync-cleanup、docs-system-audit、提案回流收口未按严格闭环完整执行。
