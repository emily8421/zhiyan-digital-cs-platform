# TEMPLATE-UPGRADE-v1.5：模板易用性——演示决策前置 + 反馈机制可见性 + README 项目化

> **模板优化提案（去项目化）**。按 `CONTRIBUTING.md` §4「上行流程 B」：本文件在派生项目起草 → 到【ai-project-template】仓库开 PR 落成实际改动 → 合并下行同步后**从派生项目删除**（改由「模板版本 vX.Y + git log」作变更事实来源）。
>
> - 起草项目：`digital-cs-demo`。
> - 提议版本：模板 **v1.4 → v1.5**（`global-rules.md` 改动触发版本号；含三处 global-rules 改动 + `new-project.sh`/`INIT-PROMPT.md` 的 README 项目化机制，合并一次递增）。

## 1. 动机（三点）

### 1.1 演示决策缺口
Demo / 原型项目核心目的是**可演示**。当前 `project-rules.md §3` 只显式决策「持久化 / 对外接口」，**未决策演示形态 / 前端** → `frontend/` 启用被归为「按需」（`global-rules §5`），创建时易遗漏。
**实例**：`digital-cs-demo` P1 全后端、无演示 UI，演示靠 Swagger / 脚本，需 P1 收官后**事后补** `demo-ui`（本可前置的决策被推迟）。愿景含界面交互词时更易矛盾、埋返工。

### 1.2 反馈机制不可见
「发现模板可优化 → 写 `TEMPLATE-UPGRADE-*.md`」的标准流程**只在 `CONTRIBUTING.md` §4**（治理文档）。但 AI 进派生项目时按 `ai/index.md` **只读 `global-rules.md` + `project-rules.md`（必读规则层）**，不主动读 `CONTRIBUTING` → 发现可通用优化时**不知标准做法**，可能直接改派生项目里的 `global-rules.md`（正是 §4 明确禁止的版本漂移）。**机制存在但不可见，等于没机制。**

### 1.3 README 未项目化
模板的根 `README.md`（讲模板本身：`# ai-project-template` + 模板说明 + 方法论同步）被复制到派生项目后**沿袭模板内容**，没有自动项目化机制。
**实例**：`digital-cs-demo` 根 README 一直停在 `# ai-project-template`（讲模板怎么用），而非项目说明，直到 P1 收官后才发现并项目化（PR #12）。新项目复制模板时应**提示 / 自动项目化 README**。
> 注：`scripts/sync-template.sh` 的 `SYNC_FILES` 已**不含 README**（仅 global-rules/CONTRIBUTING/git-guide/scripts），即 README 是项目件、下行同步不覆盖——项目化是安全的，缺的只是「创建时项目化」的机制。

## 2. 拟改（去项目化，落在模板通用层）

### 2.1 `ai/project-rules.md` §3 模板骨架
新增「演示形态」**必填裁剪项**，与「持久化 / 对外接口」并列：消息通道内交互 / 独立 Web / 移动端 / CLI / 不需演示；决定 `frontend/` 启用、`docs/04-05` 是否体现前端。

### 2.2 `INIT-PROMPT.md`
- **§0**：据 `project-rules §3` 演示决策推导 `frontend`；解析愿景界面交互词，矛盾时警告。
- **§1**：读取清单含「演示形态」。

### 2.3 `ai/global-rules.md` §5 目录标准
`frontend/` 启用从「按需」改为「按 §3 演示决策」；补演示形态维度说明。

### 2.4 `ai/global-rules.md` 新增「模板优化反馈」指示（对应动机 1.2）
AI 必读层加一条：本仓 `global-rules.md` 是复用件不得直接改；**每次任务收尾时顺带审视本次是否暴露模板可优化点**（规则不清/决策缺失/流程别扭）；发现可通用优化写 `TEMPLATE-UPGRADE-*.md` **提案**（可附 `-patch.md` 具体改动清单），**放本仓 `_proposals/`**（派生提案起草区，与模板仓库 `_proposals/` 收件箱对称），按 `CONTRIBUTING.md` §4 到模板仓库 PR。

### 2.5（可选）`_examples/`
补「消息通道内交互、`frontend` 不启用」样例，与 `md-notes-frontend` 对照。

### 2.6 README 项目化机制（对应动机 1.3）
- **`scripts/new-project.sh`**：创建项目时把根 `README.md` 从模板说明**替换为项目 README 骨架**（或显式提示「需项目化 README」），不让模板 README 原样留存。
- **`INIT-PROMPT.md`**：初始化流程加一步「项目化 README」——据 00-02 / 愿景生成项目说明（简介/能力/快速开始/文档指针/模板关系/进度），替换模板 README。
- **`ai/global-rules.md`（或 README 说明）**：注明根 README 是**项目件**（不在 `sync-template.sh` 同步清单，已确认），各项目各自维护。

## 3. 版本号
`global-rules.md` 内容变更（§5 目录标准 + 「模板优化反馈」+ §2.6「README 是项目件」说明）→ 递增 **v1.4 → v1.5**（按 `CONTRIBUTING.md` §7，仅 global-rules 内容变更触发版本号）；`new-project.sh` / `INIT-PROMPT.md` 改动（README 项目化机制）不单独触发版本号，随 v1.5 登记到 README 版本记录。

## 4. 影响面
- **新项目**：创建时 `project-rules §3` 多一项演示决策；`INIT-PROMPT §0/§1` 据此推导前端；`global-rules` 反馈指示让 AI 知反馈机制；**README 在 new-project 时即项目化**（不再沿袭模板版）。
- **现有派生项目**：不受影响（除非主动同步 v1.5）；同步后获得新决策位 + 反馈指示 + README 项目化指引。
- **向后兼容**：不改变既有 `docs/` 骨架编号 / 结构，只新增决策维度 + 规则 + README 机制。

## 5. 落地流程（CONTRIBUTING.md §4）
1. 本提案在 `digital-cs-demo` 起草（本文件）。
2. 到【ai-project-template】仓库开分支 `feat/template-v1.5`，落实 §2 的实际改动（**落成真实文件改动，不是把提案丢进模板**）。
3. 走 PR 评审、合并（`global-rules.md` 递增 v1.5 + README 版本记录登记）。
4. 下行同步回 `digital-cs-demo`（及其他派生项目）：`bash scripts/sync-template.sh --commit`。
5. **删除本提案文档**（`TEMPLATE-UPGRADE-v1.5.md`），改由「模板版本 v1.5 + git log」作为变更事实来源。

---

> 参考：`CONTRIBUTING.md` §4 示例——LUMEN 的 `TEMPLATE-UPGRADE-v1.4.md` 即按此回流（起草 → PR 合入模板 → 同步后从 LUMEN 移除）。
