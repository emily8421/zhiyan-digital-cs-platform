# TEMPLATE-UPGRADE: 08-09 开发计划、进度回写与验证证据规范

> 来源：zhiyan-digital-cs-platform（emily8421/zhiyan-digital-cs-platform）派生项目回流
> 类型：模板优化提案草稿
> 状态：Batch 4 开发计划与验证证据审计后起草，待后续模板维护者评估
> 来源 Batch：`docs/research/2026-07-06-docs-evaluation-batch-4-plan-verification-08-09.md`
> 关联：`ai/doc-standards/08-dev-plan.md`、`ai/doc-standards/09-verification.md`、`ai/implementation-lifecycle-rules.md`、`ai/session-rules.md`、`ai/prompts/dev/09-sprint-summary.md`

## 1. 背景与问题

派生项目完成多个 Sprint 或一个 Phase 后，常见问题不是“没有计划或验证”，而是“计划、验证、README、PRD、project-rules 的状态不同步”：

- `09` 已记录验收通过，README 已写当前能力完成，但 `08` 当前进度仍停留在早期 Sprint。
- `03` Phase 状态仍是“待实现”，但 `09` 已有验收记录。
- Sprint 计划写了目标、输入和验收标准，但完成后没有回写 Sprint 完成包。
- 验证记录写了“已通过”，但缺少命令、环境、执行人、失败项、残留风险和回归范围。
- 长任务跨 AI 会话时，`.ai/session-handoff.md` 记录了进度，但正式 `08/09` 未同步，导致本地续接状态与项目事实文档脱节。

因此建议强化 `08-09` 的完成后回写规范和验证证据最低结构。

## 2. 设计目标

1. **计划可反映当前事实**：Sprint 完成后，`08` 不能长期停留在待执行状态。
2. **证据可复现**：`09` 的验收记录应记录命令、环境、结果、失败项和残留风险。
3. **状态跨文档一致**：完成 Sprint / Phase 后必须检查 `08/09/README/03/project-rules`。
4. **支持长任务续接**：本地 handoff 只能辅助恢复，长期事实必须回写正式文档。
5. **不过度增加负担**：小项目可用最小完成包，复杂项目再拆任务和回归记录。

## 3. 建议新增规范

### 3.1 Sprint 总览状态列

建议 `ai/doc-standards/08-dev-plan.md` 的 Sprint 总览保持或强化以下字段：

| Sprint | 目标 | 覆盖 REQ / 功能 | 修改范围 | 验证包 | 验收方式 | 状态 | 完成证据 |
|---|---|---|---|---|---|---|---|
| Sprint-1 |  | REQ-001 | 1-3 个模块 | TC-001 / 命令 | 自动 / 手工 | 待开始 / 进行中 / 已完成 / 已验收 | `docs/09-verification.md` §验收记录 |

说明：

- `状态` 不应只在聊天或 handoff 中维护。
- `完成证据` 应引用 `09`、PR、测试日志或验收记录。
- 若 Sprint 被拆成 task，应引用 task 文件或 task 验收记录。

### 3.2 Sprint 完成包最低结构

建议每个 Sprint 完成后在 `08` 或 `09` 形成最小完成包：

| 字段 | 说明 |
|---|---|
| Sprint / Task | 稳定编号 |
| 关联 REQ / 功能 | 对应需求或功能 |
| 改动文件 / 模块 | 实际新增 / 修改 / 删除范围 |
| 验证命令 / 人工步骤 | 可复现命令或步骤 |
| 验证结果 | 通过 / 未通过 / 部分通过 |
| 验收记录位置 | `docs/09-verification.md` 或其他正式记录 |
| 残留风险 | 未验证项、降级、依赖、后续任务 |
| 下一步 | 后续 Sprint、回归、文档回写或 Phase 升级 |

### 3.3 验证证据最低字段

建议 `09` 的验收记录至少包含：

| 字段 | 说明 |
|---|---|
| 日期 | 验证日期 |
| 范围 | Sprint / Phase / Task / TC |
| 执行人 / 工具 | 人工、AI、CI、脚本或测试框架 |
| 环境 | 本机 / CI / 服务器；关键版本和端口 |
| 命令 / 步骤 | 可复现命令或手工步骤 |
| 结果 | 通过 / 未通过 / 部分通过 |
| 证据 | 日志摘要、测试数、截图路径、报告路径 |
| 失败项 / 残留风险 | 未通过项、未验证风险和后续动作 |

### 3.4 完成后跨文档状态回写清单

建议 `sprint-summary`、`docs-evaluation`、`phase-upgrade` 或实现生命周期规则中增加完成后检查：

| 触发事件 | 必查文档 | 检查内容 |
|---|---|---|
| Sprint 完成 | `docs/08-dev-plan.md`、`docs/09-verification.md` | Sprint 状态、完成包、验收记录是否回写 |
| Phase 验收完成 | `docs/03-prd.md`、`docs/08-dev-plan.md`、`docs/09-verification.md`、README | Phase 状态、退出标准、验证证据和当前进度是否一致 |
| Phase 升级评估 | `ai/project-rules.md`、`docs/03-prd.md`、`docs/08-dev-plan.md`、`docs/09-verification.md` | 当前阶段指针、下一阶段范围、验证计划是否待确认 |
| 长任务中断 / 续接 | `.ai/session-handoff.md`、Git 状态、正式 docs | handoff 是否只记录临时状态；长期事实是否已回写 docs |

### 3.5 缺陷与回归记录触发条件

建议 `09` 明确以下情况必须记录缺陷 / 回归：

- 修复已验收功能的 bug。
- 修改公共 API、数据模型、状态枚举、权限、安全策略。
- 引入真实外部服务、数据库、LLM、部署脚本或新依赖。
- Phase 升级后继续依赖上一 Phase 的 Demo 能力。

回归记录建议字段：

| 缺陷 / 变更 ID | 来源 / 现象 | 修复 Task | 回归范围 | 回归命令 / 步骤 | 回归结果 | 后续动作 |
|---|---|---|---|---|---|---|

## 4. 拟改范围

### 4.1 文档标准

建议评估是否修改：

- `ai/doc-standards/08-dev-plan.md`：强化 Sprint 状态、完成证据、完成包字段。
- `ai/doc-standards/09-verification.md`：强化验收记录证据字段、Sprint 验收包和缺陷 / 回归记录触发条件。

### 4.2 实现生命周期规则

建议评估是否修改：

- `ai/implementation-lifecycle-rules.md`：在 Sprint 完成和 Phase 验收后增加跨文档状态回写清单。
- `ai/session-rules.md`：强调 handoff 不能替代正式 `08/09` 进度和验收记录。

### 4.3 Prompt / 命令

建议评估是否修改：

- `ai/prompts/dev/09-sprint-summary.md`：要求输出并回写 Sprint 完成包。
- `ai/prompts/planning/08-phase-upgrade.md`：Phase 升级评估后检查 `03/08/09/project-rules/README` 是否需同步。
- `ai/commands/sprint-summary.md`：明确何时写 `09` 验收记录和 `08` 进度。

## 5. 不覆盖范围

本提案不直接要求：

- 每个小改动都产生冗长验收报告。
- Lean 小工具必须建立完整测试平台。
- 本地 handoff 纳入正式提交。
- 未经人工确认自动修改 Phase 边界或进入下一阶段。

## 6. 版本影响

建议版本影响：MINOR。

理由：该提案增强实现生命周期闭环和文档标准，影响 `08/09`、Sprint 总结和 Phase 升级流程；不破坏已有文档，允许项目按最小完成包渐进补齐。

## 7. 影响面

| 影响对象 | 影响 |
|---|---|
| 派生项目 `docs/08-09` | Sprint 完成状态和验证证据更可追溯 |
| `sprint-summary` | 输出从总结文本升级为可回写完成包 |
| `phase-upgrade` | 更容易发现 Phase 状态和验证事实未同步 |
| 多 AI 续接 | handoff 与正式文档职责更清晰 |
| 模板维护者 | 可减少派生项目反复出现“验证已过但计划未回写”的问题 |

## 8. 验收口径

模板维护者可用以下方式验收：

1. `08` 标准包含 Sprint 状态、验证包、完成证据或完成包字段。
2. `09` 标准包含可复现验证证据最低字段。
3. Sprint 总结 Prompt 能提示回写 `08` 和 `09`。
4. Phase 升级 Prompt 能提示检查 `03/08/09/README/project-rules` 状态一致性。
5. `session-rules` 明确 handoff 不是正式进度 / 验收记录替代品。

## 9. 风险与缓解

| 风险 | 缓解 |
|---|---|
| 文档维护成本增加 | 提供最小完成包；复杂项目再扩展证据字段 |
| AI 自动改 Phase 状态 | 要求人工确认 Phase 升级和正式文档修订 |
| 与现有 08 / 09 标准重复 | 本提案聚焦完成后回写和证据最低字段，不重复基础章节 |
| 本地 handoff 与正式 docs 混淆 | 明确 handoff 只做续接，长期事实写 `08/09` |

## 10. 待人工确认项

| ID | 待确认项 | AI 建议 | 建议依据 | 备选方案 | 取舍影响 / 阻塞关系 |
|---|---|---|---|---|---|
| C-B4-P-001 | Sprint 完成包应写在 `08` 还是 `09` | 建议 `08` 记录进度摘要，`09` 记录验证证据 | `08` 管计划，`09` 管验证，职责分离 | 全部写 `09` | 集中验收证据但计划状态仍可能滞后 |
| C-B4-P-002 | 是否强制每次 Sprint 完成都检查 README | 建议当 README 声明当前进度或运行方式时检查 | README 是开发入口，容易与真实进度不一致 | 只在 Phase 完成时检查 | 减少小改成本，但进度入口可能滞后 |
| C-B4-P-003 | 是否要求 handoff 中的长期状态回写正式 docs | 建议要求 | handoff 本地忽略提交，不可作为项目事实 | handoff 保留即可 | 跨工具续接方便，但正式文档仍不可信 |

## 11. 后续动作

- 若本提案成熟，按 `/run submit-proposal` 回流到模板仓库 issue。
- Batch 5 将继续审计 `docs/design/*`，避免把详细设计结构问题混入本计划 / 验证提案。
