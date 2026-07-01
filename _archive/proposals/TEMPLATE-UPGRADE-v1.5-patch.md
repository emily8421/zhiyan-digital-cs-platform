# TEMPLATE-UPGRADE-v1.5 —— 实际改动 Patch（给 ai-project-template PR 用）

> 本文件是 `TEMPLATE-UPGRADE-v1.5.md` 的**落地 patch**：到【ai-project-template】仓库开分支 `feat/template-v1.5-demo-and-feedback`，按下述改动各文件，即可开 PR。
> old 片段取自模板 v1.4（与各派生项目的 `ai/global-rules.md`/`INIT-PROMPT.md` 逐字一致；`project-rules.md` 为骨架，按实际骨架措辞对齐）。

## 改动 1：`ai/global-rules.md`

### 1a. 版本号（第 6 行）
```diff
-> **模板版本：v1.4（2026-06-19）**。下游项目比对这一行即可判断本文件是否过期；
+> **模板版本：v1.5（2026-06-21）**。下游项目比对这一行即可判断本文件是否过期；
```

### 1b. §5 目录标准 —— frontend 启用绑定演示决策
```diff
 ├─ frontend/ backend/ tests/ scripts/ docker/   # 按项目技术栈创建，不必全有
+├─ frontend/   # 启用由 project-rules §3「演示形态」决定（消息通道内交互→通常不启用；Web/移动端→启用）
```
并在 §5 末尾补一句：
```
`frontend/` 是否启用取决于 `project-rules.md §3` 的「演示形态」决策（消息通道内交互 / Web / 移动端 / CLI / 不需演示），不再笼统「按需」。
```

### 1c. 新增 §9 模板优化反馈（对应「反馈机制可见性」动机，置于文末）
```markdown
## 9. 模板优化反馈

本仓库派生自 `ai-project-template`，`ai/global-rules.md` 是模板复用件、**不得在本仓直接改**（会版本漂移、无法审计）。
**每次任务收尾时，顺带审视本次是否暴露模板可优化点**（规则不清/决策缺失/流程别扭等）；发现可通用优化时，写 `TEMPLATE-UPGRADE-*.md` **提案**（去项目化：动机 / 拟改 / 版本 / 影响；**可附 `-patch.md`**：具体 old→new 改动清单，给执行者），按 `CONTRIBUTING.md` §4 到【ai-project-template】仓库开 PR 落实；合并后下行同步、删除提案与 patch 文档。
```

## 改动 2：`INIT-PROMPT.md`

### 2a. §0 —— 生成 docs 时推导前端 + 解析愿景交互词
在 §0「【硬约束】」列表中新增一条：
```
8. 演示形态：据 ai/project-rules.md §3「演示形态」推导 frontend 是否启用、docs/04-05 是否体现前端；解析愿景文档，若含「页面/界面/点击/手机/打开」等界面交互词且 §3 标「无前端」，需警告并提示人工复核（防与愿景矛盾）。
```

### 2b. §1 —— 读取清单显式含演示形态
在 §1 读取清单中，把：
```
- ai/project-rules.md（§1 Phase边界、§2 技术栈、§3 项目形态与文档裁剪——生成前已由人工填好，作为约束）
```
改为：
```
- ai/project-rules.md（§1 Phase边界、§2 技术栈、§3 项目形态与文档裁剪含「演示形态」——生成前已由人工填好，作为约束）
```

## 改动 3：`ai/project-rules.md`（骨架）

在 §3「项目形态与文档裁剪」中，「是否有对外接口」项之后新增「演示形态」裁剪项：
```
- 演示形态：[消息通道内交互 / 独立 Web 页面 / 移动端 / CLI / 不需演示]（决定 frontend/ 是否启用、docs/04-05 是否体现前端架构）
```
> 注：本文件是「骨架」（新项目复制后填），落地时对齐模板仓库 `project-rules.md` §3 的实际占位措辞，把此项插入「对外接口」与「06/07 裁剪」之间。

## 改动 4：`README.md`（版本记录）

在「方法论同步 / 版本记录」段新增一行：
```
- v1.5（2026-06-21）：global-rules §5 frontend 绑定 §3「演示形态」+ 新增「模板优化反馈」指示 + 注明 README 是项目件；INIT-PROMPT §0/§1 推导前端 + 项目化 README；project-rules §3 加「演示形态」；new-project.sh 创建时项目化 README。提议来自 digital-cs-demo（TEMPLATE-UPGRADE-v1.5）。
```

## 改动 5：README 项目化机制（对应动机 1.3）

### 5a. `scripts/new-project.sh`
创建项目（复制模板）后：① 把根 `README.md` 替换为项目 README 骨架（占位：`# <项目名>` + 简介/能力/快速开始/文档指针/模板关系/进度，待填）或提示项目化；② **创建空 `_proposals/`**（派生提案起草区，放 `TEMPLATE-UPGRADE-*.md`；与模板仓库 `_proposals/` 收件箱对称，见 v1.6）。

### 5b. `INIT-PROMPT.md`
初始化流程（§0/§1）加一步「项目化 README」：据 00-02 / 愿景生成项目说明，替换模板 README。

### 5c. `ai/global-rules.md`（随改动 1 的 §5 / 改动 2 反馈节一并改）
注明根 `README.md` 是**项目件**（项目说明），不在 `sync-template.sh` 同步清单（已确认 SYNC_FILES 不含 README），各项目各自维护。

## 改动 6：`CONTRIBUTING.md` §4（补「提案 vs patch」区分约定）

在 §4「上行流程 B」补一句区分约定，让派生项目的 AI/人不仅知道「要写提案」，还知道「提案与 patch 各是什么、何时附 patch」：
- **提案 `TEMPLATE-UPGRADE-*.md`** = WHY/WHAT（去项目化：动机 / 拟改 / 版本 / 影响），给评审者决策；
- **patch `-patch.md`（可选但推荐）** = HOW（具体 old→new 改动，绑定模板当前版本），给执行者照改。

## 落地步骤
1. `git clone ai-project-template && git checkout -b feat/template-v1.5-demo-and-feedback`
2. 按上述改动 1-4 修改 4 个文件
3. `git commit -m "feat(template): v1.5 演示决策前置 + 反馈机制可见性"`
4. 开 PR，body 引用 `TEMPLATE-UPGRADE-v1.5.md`（动机/影响面）
5. 评审合并后：`sync-template.sh` 下行同步到各派生项目 → 删除派生项目里的 `TEMPLATE-UPGRADE-v1.5.md` 与本 patch 文件
