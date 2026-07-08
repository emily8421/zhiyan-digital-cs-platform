# TEMPLATE-UPGRADE: A13 场景完整闭环说法补充

> 来源：zhiyan-digital-cs-platform（emily8421/zhiyan-digital-cs-platform）派生项目回流
> 类型：模板优化提案草稿
> 状态：A13 同步模板场景使用后起草，待后续模板维护者评估
> 影响版本：v1.30.3+
> 关联：`template-docs/scenario-guides.md` A13 场景

## 1. 背景与问题

派生项目在执行「同步模板到派生项目」（A13 场景）时，常见以下问题：

- 用户容易只执行 `sync-methodology`，遗漏后续的 `post-sync-cleanup`、`docs-system-audit`、提案回流和同步报告留痕
- 场景描述中缺少明确的"完整闭环"说法，导致 AI 无法给用户一句话说明整个流程
- 2026-07-06 派生项目 `zhiyan-digital-cs-platform` 完成同步后，AI 需要在续接文件中手动补充完整闭环流程，表明该流程应在场景描述中显式声明

因此建议在 A13 场景描述中补充"完整闭环说法"，让用户和 AI 能快速识别完整流程范围。

## 2. 设计目标

1. **一句话概括完整闭环**：让用户和 AI 能快速识别 A13 的完整执行范围
2. **减少遗漏步骤**：明确列出所有必需步骤，避免遗漏 `post-sync-cleanup` 或 `docs-system-audit`
3. **符合现有格式**：在现有场景描述结构中自然插入，不破坏现有章节

## 3. 建议新增内容

在 `template-docs/scenario-guides.md` 的 A13 场景描述中，在「触发」行后新增一行「完整闭环说法」：

```markdown
#### A13 同步模板到派生项目
- **说明**：把模板方法论的更新拉到你的派生项目（不回传），并完成同步后的边界验证、整理、文档审计、项目验证建议和同步报告留痕；若已完成同步提交但旧流程未跑后续，则进入"同步后续接模式"，跳过 dry-run / commit，从边界验证开始补完闭环。
- **触发**：「同步模板」「更新方法论」「sync template」「已同步但没做后续」「补完同步后流程」「同步后续接」
- **完整闭环说法**：「模板新版已发布，请按 A13 执行完整闭环：sync-methodology → post-sync-cleanup → docs-system-audit → 提案回流收口 → 同步报告留痕。」
- **cwd·前置**：在派生项目；若缺少 `scripts/sync-template.ps1`、`template-sync.json`，或 `VERSION` 低于 `v1.6.8` / 无法判断脚本是否为新版，仍属于本场景，先按 `git-guide.md` §5.2 走旧派生项目首次同步 bootstrap，再继续完整 A13 闭环。
```

## 4. 修改影响

- **影响文件**：`template-docs/scenario-guides.md`
- **影响范围**：A13 场景描述，新增一行
- **向后兼容**：是，仅新增内容，不修改现有结构
- **用户可见性**：当用户说「同步模板」或触发 A13 时，AI 可引用该行给用户一句话说明

## 5. Patch 建议（old → new）

```diff
#### A13 同步模板到派生项目
- **说明**：把模板方法论的更新拉到你的派生项目（不回传），并完成同步后的边界验证、整理、文档审计、项目验证建议和同步报告留痕；若已完成同步提交但旧流程未跑后续，则进入"同步后续接模式"，跳过 dry-run / commit，从边界验证开始补完闭环。
- **触发**：「同步模板」「更新方法论」「sync template」「已同步但没做后续」「补完同步后流程」「同步后续接」
+- **完整闭环说法**：「模板新版已发布，请按 A13 执行完整闭环：sync-methodology → post-sync-cleanup → docs-system-audit → 提案回流收口 → 同步报告留痕。」
- **cwd·前置**：在派生项目；若缺少 `scripts/sync-template.ps1`、`template-sync.json`，或 `VERSION` 低于 `v1.6.8` / 无法判断脚本是否为新版，仍属于本场景，先按 `git-guide.md` §5.2 走旧派生项目首次同步 bootstrap，再继续完整 A13 闭环。
```

## 6. 待确认项

- 是否将「完整闭环说法」也纳入其他场景（如 A9 新建派生项目、A15 执行 Sprint）？
- 该行是否需要纳入 `ai/commands/README.md` 的 `/run sync-methodology` 描述？