# Open Items 总览（知衍数字客服统一平台）

> 本文件为 `docs/research/` 下的待确认事项总览，由 `/run docs-open-items`（A17）产出，只做总览，不替代 `docs/00-09` 事实文档。

## 0. 文档元信息

| 项 | 内容 |
|---|---|
| 定位 | 集中项目的待人工确认事项（open items）；A17 `docs-open-items` 产物 |
| 提出基准日 | 2026-07-09 |
| 方法依据 | `ai/document-lifecycle-rules.md` §6.1 / §6.2、`ai/commands/docs-open-items`（A17） |
| 关联来源 | `docs/research/2026-07-06-phase-upgrade-evaluation.md`（C-001~C-005）、`docs/research/2026-07-09-docs-system-audit-after-v1.43.0.md`（O-001~O-004）、模板仓 issue #148 |
| 落盘约定 | 默认日期戳路径（本文件）；若后续改为长期固定入口 `docs/open-items.md`，须在 `docs/README.md` 说明其定位 |
| 性质 | AI 辅助汇总；所有「AI 建议」均为建议，不等于用户已确认事实 |

## 1. 总览

| ID | 待确认项 | 需确认节点 | 阻塞关系 | 当前状态 |
|---|---|---|---|---|
| DOC-C-001 | 是否接受 Phase1 完成并进入 Phase2 / MVP 试点规划（Conditional Go） | Phase2 启动前 | 阻塞 Phase2 一切边界修订 | 待确认 |
| DOC-C-002 | Phase2 是否以「单个试点客户 MVP」为目标 | Phase2 Sprint 规划前 | 条件阻塞 Phase2 范围 | 待确认 |
| DOC-C-003 | 飞书通知是否进入沙箱 / 试点评估 | Phase2 飞书相关 Sprint 前 | 条件阻塞 | 待确认 |
| DOC-C-004 | PostgreSQL / pgvector 是否作为 Phase2 必做项 | Phase2 存储 / 部署 Sprint 前 | 条件阻塞 | 待确认 |
| DOC-C-005 | LLM 是否进入 Phase2 | Phase2 LLM 评估前 | 条件阻塞 | 待确认 |
| DOC-C-006 | 模板仓 issue #148（A13 同步闭环提案）处理 | 模板维护者侧 | 不阻塞项目 | 待模板仓处理（open） |
| DOC-C-007 | `docs/design/*` 多数未套用 v1.43.0 设计标准元信息 | 触碰对应设计文档时 | 不阻塞（P2） | 可延后 |

## 2. 逐项详情

### DOC-C-001：是否接受 Phase1 完成并进入 Phase2 / MVP 试点规划

| 字段 | 内容 |
|---|---|
| 提出时间 | 2026-07-06 |
| 来源文档 / 位置 | `docs/research/2026-07-06-phase-upgrade-evaluation.md` §3 / §7（原 C-001） |
| 待确认项 | 是否接受 Conditional Go 结论，进入 Phase2 / MVP 试点规划 |
| AI 建议 | 接受 Conditional Go |
| 建议依据 | Phase1 退出标准与 Sprint-6 验收已通过；三端运行、TC-001~TC-016、AC-001~AC-007 均已满足（见 `docs/09-verification.md`） |
| 备选方案 | 暂停升级，继续补 Phase1 体验细节 |
| 取舍影响 | 若不接受，则不修改 Phase 边界、不规划 Phase2 Sprint |
| 需确认节点 | Phase2 启动前 |
| 阻塞关系 | 阻塞 Phase2 一切边界修订（`ai/project-rules.md`、`docs/03-prd.md`、`08`、`09`） |
| 回填位置 | `ai/project-rules.md` §1 Phase 边界、`docs/03-prd.md` §3 Phase2 状态 |
| 当前状态 | 待确认 |
| 关闭依据 | 待人工确认后回填 |

> Conditional Go 保留四条件（接受 Phase2 需同时接受）：① Phase2 先做 MVP 试点，不直接进入 Phase3 真实 CRM/ERP/OA/工单集成；② 真实飞书 / 业务系统 / LLM / PostgreSQL·pgvector 仍需单独技术验证、授权边界与安全评审；③ 任何新依赖、Docker 镜像、外部 SaaS API 或付费服务必须先人工确认；④ Phase2 继续保留 Mock / 降级路径。

### DOC-C-002：Phase2 是否以「单个试点客户 MVP」为目标

| 字段 | 内容 |
|---|---|
| 提出时间 | 2026-07-06 |
| 来源文档 / 位置 | `docs/research/2026-07-06-phase-upgrade-evaluation.md` §7（原 C-002） |
| 待确认项 | Phase2 目标定位：单个试点客户 MVP，还是仅内部增强 |
| AI 建议 | 是（单个试点客户 MVP） |
| 建议依据 | `docs/03-prd.md` Phase2 目标即为 MVP 试点 |
| 备选方案 | 仅做内部增强，不面向试点客户 |
| 取舍影响 | 影响 Phase2 Sprint 范围与验收标准 |
| 需确认节点 | Phase2 Sprint 规划前 |
| 阻塞关系 | 条件阻塞 Phase2 范围 |
| 回填位置 | `docs/03-prd.md` §3 Phase2、`docs/08-dev-plan.md` Phase2 Sprint 草案 |
| 当前状态 | 待确认 |
| 关闭依据 | 待人工确认后回填 |

### DOC-C-003：飞书通知是否进入沙箱 / 试点评估

| 字段 | 内容 |
|---|---|
| 提出时间 | 2026-07-06 |
| 来源文档 / 位置 | `docs/research/2026-07-06-phase-upgrade-evaluation.md` §7（原 C-003） |
| 待确认项 | 飞书通知是否从 Mock payload 推进到沙箱 / 试点联调 |
| AI 建议 | 作为 Phase2 技术验证任务推进 |
| 建议依据 | Phase1 已完成 Mock 通知，Phase2 可强化员工侧触达 |
| 备选方案 | 继续仅 Mock |
| 取舍影响 | 若接入真实组织数据，需权限、安全与回调边界确认 |
| 需确认节点 | Phase2 飞书相关 Sprint 前 |
| 阻塞关系 | 条件阻塞 |
| 回填位置 | `ai/project-rules.md` §1/§2、`docs/05-tech-spec.md`、`docs/07-api-spec.md` 通知契约、`docs/09-verification.md` |
| 当前状态 | 待确认 |
| 关闭依据 | 待人工确认后回填 |

### DOC-C-004：PostgreSQL / pgvector 是否作为 Phase2 必做项

| 字段 | 内容 |
|---|---|
| 提出时间 | 2026-07-06 |
| 来源文档 / 位置 | `docs/research/2026-07-06-phase-upgrade-evaluation.md` §7（原 C-004） |
| 待确认项 | PostgreSQL / pgvector 是否作为 Phase2 必做，还是仅技术验证 |
| AI 建议 | 先做技术验证，不作为全部功能前置 |
| 建议依据 | Docker 当前不可用，Phase1 已按 Mock 降级跑通 |
| 备选方案 | 继续 JSON / 内存 Mock |
| 取舍影响 | 影响部署复杂度与开发节奏 |
| 需确认节点 | Phase2 存储 / 部署 Sprint 前 |
| 阻塞关系 | 条件阻塞 |
| 回填位置 | `ai/project-rules.md` §2.5、`docs/05-tech-spec.md` Risk-ID / readiness gate、`docs/06-db-design.md`、`docs/09-verification.md` |
| 当前状态 | 待确认 |
| 关闭依据 | 待人工确认后回填 |

### DOC-C-005：LLM 是否进入 Phase2

| 字段 | 内容 |
|---|---|
| 提出时间 | 2026-07-06 |
| 来源文档 / 位置 | `docs/research/2026-07-06-phase-upgrade-evaluation.md` §7（原 C-005） |
| 待确认项 | LLM 是否进入 Phase2 |
| AI 建议 | 仅评估，不默认启用自动答复 |
| 建议依据 | 不编造与成本边界未完成专项评估 |
| 备选方案 | 完全延后到 Phase3+ |
| 取舍影响 | 若启用，须先完成证据约束、兜底与成本评估 |
| 需确认节点 | Phase2 LLM 评估前 |
| 阻塞关系 | 条件阻塞 |
| 回填位置 | `ai/project-rules.md` §1/§2、`docs/05-tech-spec.md`、新增 LLM 专项设计 `docs/design/*` |
| 当前状态 | 待确认 |
| 关闭依据 | 待人工确认后回填 |

### DOC-C-006：模板仓 issue #148 处理

| 字段 | 内容 |
|---|---|
| 提出时间 | 2026-07-08 |
| 来源文档 / 位置 | `_proposals/TEMPLATE-UPGRADE-a13-sync-closure-and-dry-run-robustness.md` → https://github.com/emily8421/ai-project-template/issues/148 |
| 待确认项 | 等模板维护者处理 #148（A13 同步闭环门禁矩阵、同步报告真实性约束、提案回流收口矩阵、`sync-template.ps1 --commit` dry-run 误报、大版本 dry-run 超时） |
| AI 建议 | 跟踪至 closed；若长期无响应可补 follow-up |
| 建议依据 | #102 已 closed 但 `sync-template.ps1 --commit` fallback 仍复现，#148 作为 follow-up 单独提交 |
| 备选方案 | 重开 #102 或新建独立 issue |
| 取舍影响 | 不影响本项目业务；仅影响模板同步工具可用性与 A13 闭环门禁 |
| 需确认节点 | 无（模板仓维护者侧） |
| 阻塞关系 | 不阻塞项目 |
| 回填位置 | #148 closed 后归档 `_proposals/TEMPLATE-UPGRADE-a13-sync-closure-and-dry-run-robustness.md` 到 `_archive/proposals/` |
| 当前状态 | 待模板仓处理（open） |
| 关闭依据 | 待 #148 关闭后回填 |

### DOC-C-007：`docs/design/*` v1.43.0 元信息兼容差异

| 字段 | 内容 |
|---|---|
| 提出时间 | 2026-07-09 |
| 来源文档 / 位置 | `docs/research/2026-07-09-docs-system-audit-after-v1.43.0.md` §3 / §5（O-003） |
| 待确认项 | 多数 `docs/design/*` 未显式套用 v1.43.0 设计标准元信息 / 追溯矩阵 / readiness gate |
| AI 建议 | 触碰对应设计文档时最小补齐，不批量重写 |
| 建议依据 | 这些设计文档已支撑 Phase1 Demo 验收；本次不是 Phase2 设计回梳，不阻塞 |
| 备选方案 | 进入 Phase2 时统一补齐 |
| 取舍影响 | 批量补齐工作量大且易引入偏差；按需补更稳 |
| 需确认节点 | 触碰对应 `docs/design/*` 时 |
| 阻塞关系 | 不阻塞（P2） |
| 回填位置 | 各 `docs/design/*.md` 元信息区 |
| 当前状态 | 可延后 |
| 关闭依据 | 各设计文档补齐后逐项标记 |

## 3. 已关闭 / 已解决项（不再 open，仅留痕避免重复决策）

| 原编号 | 内容 | 关闭依据 |
|---|---|---|
| C-B1-001 | `docs/03-prd.md` Phase1 状态回写 | 已修复：`docs/03-prd.md` §3 Phase1 = 已通过验收（2026-07-06，见 `docs/09-verification.md` §6） |
| C-B1-002 | 00-03 是否按 doc-standards 全文重写 | 已决策：2026-07-09 回梳采用「标准项追加矩阵」，不全文重写 |
| C-B1-003 | Batch 1 提案聚焦状态传播 | 已提交模板仓 #111，已 closed |
| O-001 | Phase2 Conditional Go 未集中表达 | 已映射并集中到 DOC-C-001 系列 |
| O-002 | 无集中 open items 总览 | 本文档已补齐 |
| O-004 | 真实集成边界未解锁 | 以 `ai/project-rules.md` §1 与 `docs/03-prd.md` §6 为准，非待确认项 |

## 4. 门禁与回填说明

- 编码前、Phase 升级前、新 Sprint 启动前应检查本表：阻塞项未关闭 / 未转任务 / 未回填权威文档 / 未被明确风险接受时，不得开始对应 Sprint 或直接升级。
- 用户确认某项后：回填对应「回填位置」的权威文档，将该行状态改为「已确认」，并在「关闭依据」记录人工确认时点与回填位置。
- 本表只汇总，不替代 `docs/00-09`；状态变化仍需回写对应事实文档。
