# 派生项目模板同步运行记录：zhiyan-digital-cs-platform → v1.64.0

## 基本信息

- 项目：zhiyan-digital-cs-platform（普通派生项目）
- 同步日期：2026-08-18
- 同步前模板版本：v1.61.4（2026-08-13，PR #55）
- 目标模板版本：v1.64.0
- 项目自身版本（`VERSION`）：v0.3.0（保留不变）
- 继承版本记录（`TEMPLATE-BASE.md`）：存在；Lineage type: ordinary derived project；本次同步到 v1.64.0
- 同步分支：`chore/sync-template-v1.64.0`
- 实际同步提交：`d47f548`（bootstrap）+ `e04c520`（sync template v1.64.0 from ai-project-template，44 文件）
- 操作入口：`/run sync-methodology`（模板仓发起模式，registry 路由）
- AI 工具 / CLI：Claude Code（GLM）

## 执行命令

- dry-run：`powershell -ExecutionPolicy Bypass -File scripts/sync-template.ps1 --dry-run`（首次 EXIT=1 提示 bootstrap；bootstrap 后 EXIT=0）
- bootstrap：`git checkout FETCH_HEAD -- scripts/sync-template.sh` → commit `d47f548`（+6 行）
- commit：`powershell -ExecutionPolicy Bypass -File scripts/sync-template.ps1 --commit --preserve-project-version`（EXIT=0）
- 版本保留标志：`--preserve-project-version`（普通派生）
- check-derived-sync：`powershell -ExecutionPolicy Bypass -File scripts/check-derived-sync.ps1`（HEAD 即同步提交链）→ ✅ 通过
- post-sync-cleanup：轻量执行（见下）
- docs-system-audit（同步后审计）：轻量执行（见下）
- 项目验证建议：CI project-check + 人工抽查 docs/README 新分区说明

### 命令真实性记录

| 步骤 | 实际命令 / 动作 | 退出结果 | 是否完整执行 | 是否等价替代 | 是否生成独立报告 | 备注 |
|---|---|---|---|---|---|---|
| 预检 A（身份安全） | git status / log / stash / VERSION / TEMPLATE-BASE | pass（1 个 untracked research 文档，非阻塞） | 完整 | 否 | 否 | stash 有 1 条历史 wip（token hotspot rollup），未动 |
| 预检 B（同步能力） | test -f 精确查询 5 项 | 全 pass | 完整 | 否 | 否 | — |
| fetch + 目标版本 | git fetch --depth=1 → git show FETCH_HEAD:VERSION | v1.64.0 | 完整 | 否 | 否 | — |
| dry-run | sync-template.ps1 --dry-run → sync.log | 首次 EXIT=1（bootstrap 提示），bootstrap 后 EXIT=0 | 完整 | 否 | 否 | log 已清理，未入库 |
| dry-run 误触检查 | grep 项目专属文件模式 | 无误触（docs/README.md 在 template-sync.json 清单内，非项目专属） | 完整 | 否 | 否 | — |
| sync commit | sync-template.ps1 --commit --preserve-project-version | EXIT=0，44 文件 +1418/-139 | 完整 | 否 | 否 | — |
| 边界验证 | check-derived-sync.ps1 | ✅ 通过 | 完整 | 否 | 否 | — |

## 同步内容摘要（v1.61.4 → v1.64.0，跨 v1.62.x/v1.63.x）

- v1.62.0/v1.62.1：Web UI 设计知识核心层（`template-docs/ui-knowledge/` 4 文件）+ 参考分析模板 + 质量基线
- v1.63.0（Batch A）：OO 建模 overlay（用例图 / 领域模型 / 类图 / 状态图 / ERD 图 ID）+ `docs/diagrams` / `docs/tables` 生成式镜像 + references 参考区约定 + 02/04 引用式概述骨架
- v1.64.0（Batch B+C）：`--shape` 形态裁剪 + 根目录三层地图（beginner-guide）+ pitfall 存量触发 + 场景手册指引（scenario-guides §8）+ capability-packages 重构 + extract-diagrams.mjs 脚本样例
- 新增：`template-docs/examples/extract-diagrams.mjs`、`template-docs/frontend-ui-reference-analysis-template.md`、`template-docs/ui-knowledge/`（4 文件）
- 更新：check-template.sh/ps1、new-project.sh、sync-template.sh、template-sync.json、upstream/CHANGELOG*

## 脚本提示与既知事项

- 根 `CHANGELOG-PLAIN.md` 顶部版本警告：结构为「项目版本（v0.3.0）+ 模板继承历史（v1.56.13 起，审计参考）」双段式，项目版本段在最顶部——脚本启发式取到继承历史段的 v1.56.13，实际无冲突；post-sync-cleanup 不需要处理。
- 工作区 untracked：`docs/research/2026-08-13-frontend-ui-reference-analysis.md`（Batch 0 试点② UI 参考分析，本地文档，不入本次同步提交；处置待用户后续决定——提交 / 移动 / 保留本地）。
- stash@{0}（wip: token hotspot rollup docs）：历史遗留，未动。

## post-sync-cleanup（轻量执行）

- 只读抽查：`ai/project-rules.md` 无需人工迁移新骨架项（本次同步无 project-rules 结构变更）；`docs/env/local-env.md` 已存在；无旧 `docs/_scaffold/` 残留。
- CHANGELOG-PLAIN 警告核实为误报（见上），无需整理动作。
- 未做完整审计（等价于只读抽查 + 摘要），标为轻量执行。

## docs-system-audit（同步后审计，轻量执行）

- 对照同步范围抽查：本次未新增 `ai/doc-standards/` 文件（00-09 标准文件此前已在位），新增的是 `template-docs/ui-knowledge/` 与 examples 脚本，属模板资产而非项目文档规范。
- `docs/README.md` 随同步更新（分区规则新版），项目 `docs/` 实际分区无需即时迁移；若后续要采用 references 参考区约定（v1.63.0），另开任务。
- 标为轻量执行（未做全量 00-09 对照审计）。

## 提案回流收口决策矩阵

| 本地提案 | 模板 issue 或 PR | 远端状态 | 关闭原因或处理结果 | 本地动作建议 |
|---|---|---|---|---|
| `_proposals/` 仅 README.md，无待处理提案 | 无 | — | — | 无归档动作 |

（zhiyan 历史回流提案已在此前同步轮次归档完毕，本轮 `_proposals/` 收件箱为空。）

## 项目验证建议

1. CI：PR 合并前 project-check workflow 绿。
2. 人工抽查：`docs/README.md` 新分区说明与项目实际 docs 结构无冲突；`template-docs/beginner-guide.md` 根目录三层地图可读性。
3. 项目业务验证：本轮无业务代码改动，无需跑业务测试。

## 可回流优化点（本次无模板回流提案）

- 无：bootstrap 提示 → 执行 → 通过的标准流程；CHANGELOG-PLAIN 警告启发式已有既有结论，未产生新的可通用问题。

## 后续动作

- PR 合并 → main 对齐 → 删分支 → 模板仓 registry 更新（zhiyan 行 → v1.64.0 / Last sync 2026-08-18）。
