# v1.52.4 同步后整理审计与迁移计划

## 基本信息

- 项目：zhiyan-digital-cs-platform
- 审计类型：`/run post-sync-cleanup` 同步后整理审计与迁移计划
- 执行时间：2026-07-15 16:31 +08:00
- 当前分支：`chore/sync-template-v1.52.4`
- 当前同步提交：`727dc4f sync template v1.52.4 from ai-project-template`
- 同步模板版本：`v1.52.4`
- 边界复核：`powershell -ExecutionPolicy Bypass -File scripts/check-derived-sync.ps1 727dc4f` 通过；Git Bash 启动失败，由 PowerShell fallback 完成检查。

## A. 当前结构审计

### 合规项

- `docs/` 根目录仅保留 `README.md` 与 `00-scenario.md` ~ `09-verification.md` 核心文档。
- 标准子目录已存在：`archive/`、`decisions/`、`design/`、`env/`、`inputs/`、`meetings/`、`research/`、`vision/`。
- `docs/_scaffold/` 不存在；当前规范镜像使用 `ai/doc-standards/`。
- workflow 仍符合派生项目边界：仅发现 `.github/workflows/project-check.yml`，未发现 `.github/workflows/template-check.yml`。
- 根 `README.md`、`docs/env/local-env.md`、`ai/project-rules.md` 与 `docs/research/2026-07-09-docs-open-items.md` 已吸收上次 v1.46.0 审计的 P1 状态传播项：Phase2 M10、Sprint-8/9、RG-001/002/003、TC-060/061、DOC-C-006 已关闭。

### 需要迁移的文件

无物理迁移项。本轮未发现调研、会议、ADR、详细设计、环境记录或归档文件误放在 `docs/` 根目录。

## B. v1.52.4 新方法论影响

| 新增 / 强化项 | 当前项目状态 | 整理建议 | 是否立即修改项目事实 |
|---|---|---|---|
| Web Fullstack Profile + Walking Skeleton Gate | 项目已具备 `frontend/customer-h5`、`frontend/console`、`frontend/shared`，后端已有 `api/services/schemas/adapters/data` 分层，测试目录已存在 | 下一次前端 / 全栈 Sprint 前，把 WSG-001~006 映射到对应任务输入和验收，不建议本轮机械重构 | 否 |
| Frontend Experience Brief | 已有 `docs/design/frontend-interaction.md`、UI 原型策略与需求探索原型记录 | 若 Phase3 前需要重新确认视觉 / 信息密度 / 演示首屏，再用 brief 作为探索记录；不替代现有设计 | 否 |
| UI Brief Intake | 当前 README、交互设计和 Demo runbook 已能支撑现有演示；无需补原始 UI brief | 新增重大页面或演示体验方向变化时，先补 `docs/inputs/ui-brief.md` 或 `docs/research/YYYY-MM-DD-ui-brief-intake.md` | 否 |
| Capability Packages / Remote CI SOP | 本轮已遇到 Git Bash / PowerShell fallback 与远端 issue 查询认证问题 | 后续 push / PR / issue / CI 操作前按 Remote / CI SOP 做 checkpoint 与权限预检 | 否 |

## C. 运行环境与资源约束

- `docs/env/local-env.md` 存在，且已记录 Docker 自动采集时不可用、2026-07-10 RG-002 复测 Go、后续运行前仍以实时检查为准。
- `ai/project-rules.md` 已记录 Docker / PostgreSQL / pgvector 技术验证 Go，但生产或客户侧启用仍需单独任务和人工确认。
- 本轮无需重新运行 `scripts/collect-env.ps1`；此次是方法论同步，不改变本机运行事实。

## D. README 与项目事实入口

- 根 `README.md` 当前阶段、开发计划、验证方式已与 Phase2 M10 / Demo Sandbox 状态一致。
- `docs/README.md` 本轮随模板同步更新，仍作为 docs 分区规则入口。
- 本轮不建议修改项目事实文档；若后续采用 Web Fullstack Profile，应在具体 Sprint / 文档修订任务中最小回写。

## E. 提案归档整理

本轮确认 3 个待处理提案已在模板仓关闭并被当前同步版本覆盖，已移动到 `_archive/proposals/` 并更新 `_archive/proposals/README.md`：

- `TEMPLATE-UPGRADE-demo-port-identity-check.md`：issue #184，已在模板 v1.47.3 落地。
- `TEMPLATE-UPGRADE-web-app-structure-profile.md`：issue #186，已在模板 v1.51.0 落地。
- `TEMPLATE-UPGRADE-codex-sandbox-remote-ops.md`：issue #195，已在模板 v1.52.1 落地。

## F. 新发现可回流优化点

本轮 `scripts/sync-template.ps1 --commit --preserve-project-version` 在 PowerShell fallback 下已成功覆盖并 stage 同步文件，但内部 `git commit ... -- <大量路径>` 失败。已用等价安全动作手动提交同步文件，并新增提案：

- `_proposals/TEMPLATE-UPGRADE-sync-powershell-fallback-commit-pathspec.md`

## G. 待确认事项

| ID | 待确认项 | AI 建议 | 建议依据 | 备选方案 | 取舍影响 / 阻塞关系 |
|---|---|---|---|---|---|
| PSC-1524-C-001 | 是否在下一次前端 / 全栈 Sprint 前显式采用 Web Fullstack Profile | 建议采用轻量映射，不做目录级重构 | 项目已是 H5 + Console + FastAPI 多入口 Web 项目 | 继续沿用现有文档，不显式记录 WSG | 不阻塞本次同步；影响后续前端任务结构审查 |
| PSC-1524-C-002 | 是否提交新的 fallback commit pathspec 提案到模板仓 issue | 建议提交 | 本轮复现真实脚本失败，具备跨项目通用性 | 暂留本地 `_proposals/` | 不阻塞同步；影响后续 Windows fallback 稳定性 |

## H. 同步报告回写建议

- 将本轮 post-sync-cleanup 状态记录为“轻量执行”：完成只读结构审计、状态传播复核、提案归档和新提案识别；未执行项目事实文档迁移。
- 将 “Web Fullstack Profile / UI Brief / Capability Packages” 作为后续任务建议，不作为本轮必须整改项。
