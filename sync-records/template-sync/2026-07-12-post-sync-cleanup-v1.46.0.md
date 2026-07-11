# v1.46.0 同步后整理审计与迁移计划

## 基本信息

- 项目：zhiyan-digital-cs-platform
- 审计类型：`/run post-sync-cleanup` 完整第一段（同步后整理审计与迁移计划）
- 执行时间：2026-07-12 00:01 +08:00
- 当前分支：`main`
- 当前 HEAD：`ac20622 Merge pull request #37 from emily8421/chore/sync-template-v1.46.0`
- 同步模板版本：`v1.46.0`（见 `TEMPLATE-BASE.md`）
- 同步提交：`ced2c76 sync template v1.46.0 from ai-project-template`
- 边界复核：`powershell -ExecutionPolicy Bypass -File scripts/check-derived-sync.ps1 ced2c76` 通过；Git Bash 启动受本机权限影响失败，PowerShell fallback 成功。

## A. 当前结构审计

### 合规项

- `docs/` 根目录仅保留 `README.md` 与 `00-scenario.md` ~ `09-verification.md` 核心文档。
- 标准子目录已存在：`docs/inputs/`、`docs/vision/`、`docs/design/`、`docs/decisions/`、`docs/research/`、`docs/env/`、`docs/meetings/`、`docs/archive/`。
- `docs/_scaffold/` 不存在；当前规范镜像使用 `ai/doc-standards/00-09`。
- workflow 已符合派生项目边界：仅存在 `.github/workflows/project-check.yml`，未发现 `.github/workflows/template-check.yml`。
- `_proposals/` 仅保留 `_proposals/README.md`；#148 / #160 相关本地提案已归档到 `_archive/proposals/`。

### 需要迁移的文件

无物理迁移项。本轮未发现调研、会议、ADR、详细设计、环境记录或历史归档文件误放在 `docs/` 根目录。

### 不确定项

- 无目录迁移不确定项。
- 存在内容回写项，见 C/D/E/G：README 进度口径、open items 提案状态、运行环境 Docker 口径和 `docs/design/*` 规范兼容差异。

## B. 建议迁移表

| 当前路径 | 建议路径 | 类型 | 理由 | 是否需要人工确认 |
|---|---|---|---|---|
| 无 | 无 | 物理迁移 | docs 分区已合规，无需移动文件 | 否 |

## C. 运行环境约束补齐建议

### 合规项

- `docs/env/local-env.md` 存在，并包含自动采集、人工确认项和服务器资源预案。
- `ai/project-rules.md` 已有 §2.5「运行环境与资源约束」，并引用 `docs/env/local-env.md`。
- `docs/04-architecture.md` 已包含运行拓扑；`docs/05-tech-spec.md` 已包含资源评估、技术风险和 readiness gate；`docs/09-verification.md` 已包含本机资源验证与 RG-002 记录。

### 需回写项

| ID | 位置 | 问题 | 建议 |
|---|---|---|---|
| PSC-ENV-001 | `docs/env/local-env.md:36`、`ai/project-rules.md:76`、`ai/project-rules.md:104` | 仍记录 Docker 当前不可用 / 可用性待修复；但 `docs/research/2026-07-10-tech-env-evaluation-postgres-pgvector.md:17`、`:19`、`:70`、`:78` 已确认 Docker Desktop / PostgreSQL / pgvector 技术验证 Go。 | 下一轮最小修订 `docs/env/local-env.md` 与 `ai/project-rules.md` 的 Docker 摘要，改为“此前不可用；2026-07-10 RG-002 已验证可用；业务启用仍需单独任务”。 |

### 建议先运行的脚本

- 本轮无需重新运行 `scripts/collect-env.ps1`；现有缺口是后续验证结果未回写，不是环境采集缺失。

### 必须人工确认的内容

- 若要更新 `docs/env/local-env.md` 为当前 Docker 可用状态，建议人工确认这是否表示“本机当前仍可用”，还是仅记录“2026-07-10 曾验证可用”。

## D. README 补齐建议

| ID | 位置 | 问题 | 建议 |
|---|---|---|---|
| PSC-README-001 | `README.md:3`、`README.md:7` | README 仍写“Phase2 MVP 试点启动前准备”，但 `ai/project-rules.md:28`、`docs/03-prd.md:8`、`docs/03-prd.md:42` 已记录 Phase2 MVP M10 验收通过。 | 更新当前阶段为“Phase2 MVP 已验收；当前不升 Phase3，进入 Demo Sandbox / Phase3 准备规划”。 |
| PSC-README-002 | `README.md:22`、`README.md:105` | README 仍写 Sprint-1~7 已完成、Sprint-8 可启动、飞书沙箱仍待 RG-001；但 `docs/08-dev-plan.md:29`、`:30`、`docs/09-verification.md:411`、`:428` 记录 Sprint-8/9 完成、RG-001/RG-002 Go、RG-003 Conditional Go。 | 更新开发计划为 Sprint-7/8/9 已完成，后续优先 Demo Sandbox / LLM Sandbox 或 Phase3 准备规划；飞书生产群 / 真实组织数据仍后置。 |
| PSC-README-003 | `README.md:118` | README 验证范围仍写 TC-001~020；但 `docs/09-verification.md:516`、`:522` 已有 TC-060。 | 更新为 TC-001~060，并摘要 Phase2 M10、Demo Sandbox、标准模拟数据包验证。 |

## E. project-rules 补齐建议

### 合规项

- 初始化必填检查已包含 docs 分区规则与 `docs/README.md`。
- §1 Phase 边界、§2 技术栈、§2.5 运行环境、§2.7 UI 原型策略、§3 文档裁剪均存在。
- §3 已明确保留 `docs/06`、`docs/07`、`frontend/`、`backend/`、`tests/`、`scripts/`、`docker/`、`tasks/`。

### 需回写项

- 同 PSC-ENV-001：`ai/project-rules.md:76` 与 `ai/project-rules.md:104` 的 Docker 摘要落后于 RG-002 验证结果。建议与 `docs/env/local-env.md` 同步最小修订。

## F. 风险与注意事项

- 本轮只完成治理闭环审计与报告回写，不修改业务代码，不扩展需求。
- README、open items、project-rules、local-env 的内容修订会改变项目事实文档，应另行确认后按最小变更执行。
- `docs/design/*` 多处存在旧兼容写法，批量重排章节号可能带来大 diff；建议触碰对应文档时最小补齐，或单独开“设计文档结构兼容回梳”任务。
- `check-derived-sync.ps1 ced2c76` 已通过；Git Bash 权限错误由 PowerShell fallback 覆盖，不阻塞派生同步边界结论。

## G. 待人工确认问题

| ID | 来源文档或位置 | 待确认项 | AI 建议 | 建议依据 | 备选方案 | 取舍影响或阻塞关系 |
|---|---|---|---|---|---|---|
| PSC-C-001 | `README.md:3`、`:7`、`:22`、`:105`、`:118` | 是否立即修订 README 当前阶段 / 开发计划 / 验证范围 | 建议下一轮优先修订 | README 是项目入口，当前与 `03/08/09/project-rules` 冲突 | 暂只在同步报告记录 | 不阻塞 A13；会影响新会话理解项目状态 |
| PSC-C-002 | `docs/research/2026-07-09-docs-open-items.md:119`~`:134` | 是否将 DOC-C-006 从 open 改为 closed | 建议下一轮修订并移入已关闭项 | 同步报告已确认 #148 closed 且本地提案归档 | 保留旧状态但由本报告解释 | 不阻塞 A13；影响 open items 总览准确性 |
| PSC-C-003 | `docs/env/local-env.md:36`、`ai/project-rules.md:76`、`:104` | 是否把 Docker 可用性从旧“不可用”回写为 RG-002 已验证可用 | 建议下一轮修订为带时间戳的状态 | PG/pgvector 技术验证报告已 Go | 只在 05/09 保留验证结果 | 不阻塞 A13；影响运行环境权威口径 |
| PSC-C-004 | `docs/design/*` 多文件 | 是否统一补齐设计文档编号 / 元信息兼容差异 | 建议延后到触碰对应文档或单独批量回梳 | DOC-C-007 已标 P2，不阻塞 | 批量重排章节号 | 不阻塞当前；批量改动有误伤风险 |

## H. 模板优化回流建议

- 本轮未发现新的可通用模板缺陷。
- 已有 #148 / #160 均已被模板采纳或决议，并已归档；无需新增 `_proposals/TEMPLATE-UPGRADE-*.md`。

## I. 同步报告回写建议

- 将 `post-sync-cleanup` 状态由“轻量执行”更新为“完整执行”。
- 证据路径：`sync-records/template-sync/2026-07-12-post-sync-cleanup-v1.46.0.md`。
- 已处理项：完成目录、README、project-rules、运行环境、workflow、提案回流状态审计；确认无物理迁移。
- 未处理项：未直接修改 README / open items / project-rules / local-env；这些属于项目事实修订，需另行确认。
- 后续入口：如要消除审计发现，按 `docs` 修订流程最小修改 PSC-C-001~PSC-C-003。
