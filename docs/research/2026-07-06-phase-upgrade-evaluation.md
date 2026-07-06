# Phase Upgrade Evaluation（Phase1 → Phase2）

## 0. 文档元信息

| 项 | 内容 |
|---|---|
| 项目 | 知衍数字客服统一平台 |
| 评估日期 | 2026-07-06 |
| 当前 Phase | Phase1：本机 Demo |
| 目标 Phase | Phase2：MVP 试点规划 |
| 评估类型 | 只读阶段升级评估 |
| 评估结论 | Conditional Go：建议进入 Phase2 / MVP 试点规划，但不直接解锁真实系统集成或 LLM |
| 关联命令 | `/run phase-upgrade` |

## 1. 评估依据

- `ai/project-rules.md`：当前 Phase1 边界、禁止事项和下一阶段预告。
- `docs/03-prd.md`：Phase 路线图、Phase1 退出标准、Phase2 进入标准和验收标准 AC-001~AC-007。
- `docs/08-dev-plan.md`：Sprint-1~Sprint-6 计划、M7 Demo 验收里程碑。
- `docs/09-verification.md`：Sprint-6 本机验证记录、资源验证、AC 状态和未验证风险。
- `README.md`：Phase1 快速开始、三端启动命令和当前进度。

## 2. 当前 Phase 完成情况核对

| 核对项 | 依据 | 结论 |
|---|---|---|
| Phase1 退出标准 | `docs/03-prd.md` Phase1：H5 + 后端 + Web 控制台 + Mock 数据闭环演示通过 | 已满足 |
| Sprint-6 验收 | `docs/09-verification.md` 2026-07-06 验收记录 | 已通过 |
| 本机三端运行 | 后端 `8000`、H5 `5173`、Console `5174` | 已通过 |
| 自动化 / 场景验证 | 后端 API 测试 `19 passed`；HTTP 场景验证 TC-001~TC-016 全部通过 | 已通过 |
| Phase1 AC | AC-001~AC-006 已通过；AC-007 已回梳并人工接受 | 已满足 |
| 文档与运行说明 | `README.md` 已记录启动命令和限制；`docs/09-verification.md` 已回填验证 | 已完成 |

## 3. 升级结论

结论：**Conditional Go → Phase2 / MVP 试点规划**。

建议接受进入 Phase2 规划，但必须保留以下条件：

1. Phase2 先做 MVP 试点能力，不直接进入 Phase3 的真实 CRM / ERP / OA / 工单系统集成。
2. 真实飞书、真实业务系统、LLM、PostgreSQL / pgvector 仍需单独技术验证、授权边界和安全评审。
3. 任何新依赖、Docker 镜像、外部 SaaS API 或付费服务必须先人工确认。
4. Phase2 应继续保留 Mock / 降级路径，避免试点未就绪时阻塞演示和运营验证。

## 4. 下一 Phase 可解锁清单

| 类别 | Phase2 可解锁内容 | 前置条件 / 约束 |
|---|---|---|
| 知识运营 | 强化知识库、知识缺口审核、知识状态流转 | 不把未确认知识写成事实答案 |
| 运营配置 | 场景包、规则、Mock 数据和基础运营配置 | 保留可追溯配置，不硬编码客户叙事 |
| 基础权限 | 员工侧基础角色 / 可见性 / 操作边界 | 不等同于生产级多租户权限 |
| 飞书通知 | 从 Mock payload 进入试点评估 / 沙箱联调 | 不默认接真实组织数据；需权限与回调边界确认 |
| 试点部署 | 单个试点客户的部署、验收路径、运营流程 | 不处理真实生产数据，或先完成合规边界确认 |
| 技术验证 | PostgreSQL / pgvector、部署脚本、回调服务等 | 作为技术验证任务，不作为 Phase2 默认前置全部完成 |
| LLM 评估 | 有限 LLM 能力可进入评估 | 先补证据约束、不编造、成本、安全和转人工兜底方案 |

## 5. 暂不解锁事项

- 不直接接入真实 CRM / ERP / OA / 工单系统；该类真实业务系统集成仍建议归入 Phase3 或单独授权任务。
- 不处理真实客户隐私、合同、订单、报价、联系方式或生产会话。
- 不启用通用 LLM 自动答复，除非先完成专项评估和人工确认。
- 不把试点能力包装为多租户、计费、监控、审计等产品化平台能力。
- 不绕过人工确认引入新依赖、Docker 镜像、外部 SaaS API 或付费服务。

## 6. `ai/project-rules.md` Phase 边界草稿

> 以下为草稿，等待人工确认后再实际修改 `ai/project-rules.md`、`docs/03-prd.md` 和 `docs/08-dev-plan.md`。

### 当前阶段

Phase2（MVP 试点；在 Phase1 本机 Demo 闭环基础上强化运营可用性）

### 允许

- 在保留 H5 + Web 控制台 + FastAPI 主链路的基础上，强化知识库、知识缺口审核、运营配置和基础权限。
- 将飞书通知从 Mock payload 推进到试点评估 / 沙箱联调，但不得默认接入真实组织数据。
- 以单个试点客户为目标，规划部署、演示数据、运营流程和验收路径。
- 继续保留 Mock 订单 / 项目数据作为默认降级路径。
- 为 PostgreSQL / pgvector、飞书回调、部署脚本等补充技术验证任务。

### 禁止

- 不直接接入真实 CRM / ERP / OA / 工单系统，除非已有接口授权、数据边界和安全评审。
- 不处理真实客户隐私、合同、订单、报价、联系方式或生产会话。
- 不启用通用 LLM 自动答复，除非先完成证据约束、不编造、成本与兜底评估。
- 不把试点能力包装为多租户产品化能力。
- 不绕过人工确认引入新依赖、Docker 镜像、外部 SaaS API 或付费服务。

### 下一阶段预告

- Phase3 可在试点客户授权后接入 CRM / ERP / OA / 飞书项目 / 工单等真实业务系统。
- Phase4 再考虑多租户、计费、监控、审计、插件化场景包和产品化运营。

## 7. 待人工确认项

| ID | 待确认项 | AI 建议 | 建议依据 | 备选方案 | 取舍影响 / 阻塞关系 |
|---|---|---|---|---|---|
| C-001 | 是否接受 Phase1 完成并进入 Phase2 / MVP 试点规划 | 接受 Conditional Go | Phase1 退出标准和 Sprint-6 验收已通过 | 暂停升级，继续补 Phase1 体验细节 | 若不接受，则不修改 Phase 边界，不规划 Phase2 Sprint |
| C-002 | Phase2 是否以“单个试点客户 MVP”为目标 | 建议是 | `docs/03-prd.md` Phase2 目标是 MVP 试点 | 仅做内部增强，不面向试点 | 影响 Phase2 Sprint 范围和验收标准 |
| C-003 | 飞书通知是否进入沙箱 / 试点评估 | 建议作为 Phase2 技术验证任务 | Phase1 已完成 Mock 通知，Phase2 可强化员工侧触达 | 继续仅 Mock | 若接入真实组织数据，需权限、安全和回调边界确认 |
| C-004 | PostgreSQL / pgvector 是否作为 Phase2 必做项 | 建议先做技术验证，不作为全部功能前置 | Docker 当前不可用，Phase1 已按 Mock 降级跑通 | 继续 JSON / 内存 Mock | 影响部署复杂度和开发节奏 |
| C-005 | LLM 是否进入 Phase2 | 建议仅评估，不默认启用自动答复 | 不编造和成本边界未完成专项评估 | 完全延后到 Phase3+ | 若启用，必须先完成证据约束、兜底和成本评估 |

## 8. 建议下一步

1. 人工确认是否接受本报告的 Conditional Go 结论。
2. 若接受，单独启动文档修订任务，更新：
   - `ai/project-rules.md`：Phase 边界。
   - `docs/03-prd.md`：Phase1 状态与 Phase2 细化。
   - `docs/08-dev-plan.md`：新增 Phase2 Sprint 草案。
   - `docs/09-verification.md`：新增 Phase2 验证范围。
3. 若暂不接受，保留本报告作为评估记录，继续针对 Phase1 体验或演示细节开小任务。
