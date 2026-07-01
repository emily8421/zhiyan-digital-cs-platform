# TEMPLATE-UPGRADE-v1.6：模板优化汇总工作流（`_proposals/` 收件箱 + AI 汇总）

> **模板优化提案（去项目化）**。按 `CONTRIBUTING.md` §4：派生项目起草 → 模板仓库 PR 落实 → 合并同步后删除。
>
> - 起草项目：`digital-cs-demo`。
> - 提议版本：**v1.5 → v1.6**（假设 v1.5 已合；若与 v1.5 并行 PR，可合并为一次 v1.5 递增）。
> - 与 v1.5 配合：v1.5 让**派生项目 AI** 知道「写提案」；v1.6 让**模板仓库 AI** 知道「读提案汇总分析」。两者一写一读，闭环。

## 1. 动机

当前 `CONTRIBUTING.md` §4「上行流程 B」：派生项目起草提案 → **人**到模板仓库按 patch **手动改文件** → PR。痛点：

- **人工改文件**：按 patch 逐文件改，易错、慢；
- **分散**：多个派生项目各自提案，无统一收集，模板仓库无法整体看（去重 / 冲突 / 分阶段）；
- **无汇总分析**：哪些提案合并改、哪些分阶段、冲突如何，全靠人判断。

**升级**：模板仓库 `_proposals/` 收件箱 + **AI 读全部提案汇总分析**（去重 / 冲突 / 依赖 → 优化计划：合并 vs 分阶段）+ AI 辅助改文件（人审）。

## 2. 拟改（去项目化，落在模板仓库）

### 2.1 新增 `_proposals/` 文件夹 + README（提案收件箱）
- 位置：`ai-project-template/_proposals/`（与 `_archive/`、`_examples/` 同级，模板仓库专属）。
- `_proposals/README.md`：说明这是派生提案**收件箱**——命名（`TEMPLATE-UPGRADE-vX.Y.md` + 可选 `-patch.md`）、回流方式（派生项目开 PR 把提案文件加到此处）、AI 汇总流程（模板维护者 AI 读全部 → 计划 → 辅助改）、合并后清空。

### 2.2 `scripts/new-project.sh` 排除 `_proposals/`
复制模板到派生项目时排除 `_proposals/`（同 `_archive/`、`_examples/`），派生项目不需要别人的提案收件箱。

### 2.3 AI 汇总 prompt（`INIT-PROMPT.md` 新增一节「模板优化汇总」，或专门 `TEMPLATE-PROMPT.md`）
```text
读取 _proposals/ 下所有 TEMPLATE-UPGRADE-*.md（提案）与 -patch.md（具体改动）：
1. 去重 / 冲突 / 依赖梳理（多提案是否改同一文件、是否冲突、是否有依赖）；
2. 优化计划：本次合并改（一次版本递增）还是分阶段（v1.X 改一批、v1.Y 改一批，因依赖/风险），给出理由；
3. 把各 patch 的 old→new 合并为模板文件的实际 diff（解决冲突/重叠）；
4. 辅助改 global-rules / INIT-PROMPT 等文件（人审 diff）。
输出：一份「优化计划文档」（合并/分阶段 + 理由 + 合并后的文件 diff 清单）。
```

### 2.4 `CONTRIBUTING.md` §4 升级
- **回流方式**：派生项目开 PR 把提案文件**加到模板 `_proposals/`**（提案作为文件进模板仓库，临时）；
- **新增「AI 汇总」步骤**：模板维护者用 §2.3 prompt 读 `_proposals/` 汇总 → 输出优化计划 → 辅助改文件 → PR；
- 合并后**清空 `_proposals/`**（已处理的提案）。

### 2.5 `ai/global-rules.md`（模板仓库视角）
注明模板维护者 AI 的汇总职责：读 `_proposals/` → 优化计划 → 辅助改（人审）。

## 3. 版本号
`global-rules.md` 改动（模板维护者 AI 汇总职责）→ 递增 v1.5 → **v1.6**（假设 v1.5 已合）；若与 v1.5 并行，可合并为一次 v1.5 递增（两者都改 global-rules）。

## 4. 影响面
- **模板仓库**：新增 `_proposals/` + AI 汇总 prompt + CONTRIBUTING §4 升级（人工改 → AI 辅助）。
- **派生项目**：不复制 `_proposals/`；提案回流方式从「人按 patch 改」升级为「PR 加提案到 `_proposals/` + 模板 AI 汇总」。
- **向后兼容**：不改变既有 `docs/` 骨架，新增汇总工作流。

## 5. 落地流程
1. 本提案在 `digital-cs-demo` 起草（本文件 + patch）。
2. 到 ai-project-template 开分支 `feat/template-v1.6-proposal-inbox`，落实 §2（新增 `_proposals/` + README、new-project.sh 排除、INIT-PROMPT 汇总节、CONTRIBUTING §4 升级、global-rules 维护者职责）。
3. PR 评审合并 → 下行同步 → 删除本提案。
