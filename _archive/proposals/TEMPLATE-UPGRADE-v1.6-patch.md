# TEMPLATE-UPGRADE-v1.6 —— 实际改动 Patch（给 ai-project-template PR 用）

> 本文件是 `TEMPLATE-UPGRADE-v1.6.md` 的落地 patch：到【ai-project-template】开分支按此改即可开 PR。

## 改动 1：新增 `_proposals/README.md`（提案收件箱说明）

在模板仓库根新建 `_proposals/README.md`：
```markdown
# _proposals/ —— 模板优化提案收件箱

本目录收集各派生项目回流的本模板优化提案（`TEMPLATE-UPGRADE-vX.Y.md` + 可选 `-patch.md`），供模板维护者 AI 统一读取、汇总分析后辅助修改模板。

## 流程
1. 派生项目在本项目根起草 `TEMPLATE-UPGRADE-vX.Y.md`（提案：动机/拟改/版本/影响）+ 可选 `-patch.md`（具体 old→new）。
2. 开 PR 把提案文件**加到本目录**（`_proposals/TEMPLATE-UPGRADE-vX.Y.md`）。
3. 模板维护者用 `INIT-PROMPT.md`「模板优化汇总」prompt 读本目录全部提案 → 去重/冲突/依赖 → 优化计划（合并 vs 分阶段）→ 辅助改 global-rules 等文件（人审）。
4. PR 评审合并后，**清空本目录**（已处理的提案移除；变更事实改由「模板版本 vX.Y + git log」承载）。

## 命名
`TEMPLATE-UPGRADE-vX.Y.md`（X.Y = 提议的目标模板版本）；`TEMPLATE-UPGRADE-vX.Y-patch.md` 为配套 patch。

> 本目录是**模板仓库专属**，派生项目不复制（`new-project.sh` 已排除）。
```

## 改动 2：`scripts/new-project.sh` 排除 `_proposals/`

在复制模板到派生项目时，排除 `_proposals/`（与 `_archive/`、`_examples/` 同处理——模板仓库专属、派生不需要）。
> 落地：在 new-project.sh 的复制逻辑里，把 `_proposals/` 加入排除清单（若脚本用 rsync `--exclude`，加 `_proposals/`；若是手动 cp，注明跳过）。

## 改动 3：`INIT-PROMPT.md` 新增「模板优化汇总」节

新增一节（建议放在文末，或专门 `TEMPLATE-PROMPT.md`）：
```text
## 模板优化汇总（供模板维护者）

读取 _proposals/ 下所有 TEMPLATE-UPGRADE-*.md（提案）与 -patch.md（具体改动）：
1. 去重 / 冲突 / 依赖梳理（多提案是否改同一文件、是否冲突、是否有依赖）；
2. 优化计划：本次合并改（一次版本递增）还是 分阶段（v1.X 改一批、v1.Y 改一批，因依赖/风险），给理由；
3. 把各 patch 的 old→new 合并为模板文件的实际 diff（解决冲突/重叠）；
4. 辅助改 ai/global-rules.md / INIT-PROMPT.md 等文件（人审 diff，不直接 push）。
输出：一份「优化计划文档」（合并/分阶段 + 理由 + 合并后的文件 diff 清单）。
```

## 改动 4：`CONTRIBUTING.md`（§4 AI 辅助 + 双向闭环总览 + §5 措辞澄清）

### 4a. §4「上行流程 B」升级（人工改 → AI 辅助汇总）
把第 2-3 步从「人到模板仓库按 patch 手动改」升级为：
```
2. 派生项目开 PR，把提案加到模板仓库 _proposals/（临时）。
3. 模板维护者用 INIT-PROMPT「模板优化汇总」prompt 读 _proposals/ 全部提案 →
   去重/冲突/依赖 → 优化计划（合并 vs 分阶段）→ AI 辅助改模板文件（人审 diff）→ PR。
4. 合并后清空 _proposals/。
```

### 4b. 新增「双向闭环总览」（放 §2 后、§3 前）
明确上行 + 下行是闭环的两半（缺一不可），避免把 sync 误读为「派生改模板」：
```
## 模板 ↔ 派生：双向闭环
模板方法论在「模板仓库」与「派生项目」间双向流动，两方向互补、构成闭环：
- 【上行·改进】派生发现优化 → 写 _proposals/TEMPLATE-UPGRADE-*.md（§4）→ 模板 PR 合并 → 模板演进（vX.Y）。
- 【下行·对齐】派生执行 sync-template.sh（§5）→ 拉模板最新到派生 → 删 _proposals/ 提案 → 重新对齐。
> 只有上行没下行：模板改了派生拿不到（停留旧版）；只有下行没上行：模板不演进（没人反馈）。两者缺一不可。
```

### 4c. §5「下行同步」措辞澄清
§5 补一句，明确 sync 是「下行获取」、派生是接收方（非派生改模板）：
```
> 注：sync-template.sh 是**下行获取**（派生拉模板最新方法论覆盖本地），派生是接收方、不修改模板；模板的改进只在上行（§3/§4 PR 合并）产生。
```

## 改动 5：`ai/global-rules.md`（模板维护者 AI 汇总职责）

在 global-rules（模板仓库视角）注明：模板维护者 AI 读 `_proposals/` → 优化计划 → 辅助改（人审）；递增版本号 v1.5 → v1.6。

## 落地步骤
1. `git clone ai-project-template && git checkout -b feat/template-v1.6-proposal-inbox`
2. 按改动 1-5 修改（新增 `_proposals/README.md`、改 `new-project.sh` / `INIT-PROMPT.md` / `CONTRIBUTING.md` / `global-rules.md`）
3. `git commit -m "feat(template): v1.6 提案收件箱 _proposals/ + AI 汇总工作流"`
4. 开 PR，body 引用 `TEMPLATE-UPGRADE-v1.6.md`
5. 合并后下行同步 + 删除本提案与 patch
