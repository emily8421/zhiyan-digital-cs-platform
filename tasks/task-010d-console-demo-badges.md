# task-010d-console-demo-badges

## 目标

增强 Web Console 的演示标识：在对外演示时清楚展示 `Demo Sandbox`、`Mock`、`source_ref`、`source_system`、`environment` 和 LLM 默认关闭边界，避免客户误以为已接入真实 CRM / ERP / OA / 工单系统或真实 LLM。

本任务只修改前端展示层和验收文档，不新增后端接口，不改变现有业务逻辑，不接真实系统。

## 输入文档

- `docs/design/frontend-interaction.md`：Console 需展示 Demo / Mock 标识，且 Mock、高风险、错误和成功状态需有文字说明。
- `docs/env/external-demo-script.md`：对外演示需明确当前为 H5 + Web 控制台 + Mock / Sandbox 口径。
- `docs/research/2026-07-13-demo-sandbox-demo-rehearsal.md`：Demo Sandbox 对外演示彩排通过，后续可做展示增强。
- `docs/08-dev-plan.md`、`docs/09-verification.md`：Demo Sandbox TC-060~063 已完成，真实业务系统与真实 LLM 仍未解锁。
- `frontend/console/src/App.tsx`：Console 当前已有 MockBadge 与详情 JSON，但缺少更醒目的演示证据摘要。

## 修改范围

- `frontend/console/src/App.tsx`：新增 Demo Sandbox 边界横幅、详情栏演示证据摘要、Mock 数据卡片 source_ref / source_system / environment 展示。
- `frontend/console/src/styles.css`：新增横幅、证据摘要、标签样式。
- `docs/08-dev-plan.md`：补充 task-010d 进度摘要。
- `docs/09-verification.md`：新增 TC-064 Console 演示标识增强验证记录。
- `.ai/session-handoff.md`：刷新本地续接状态。

## 验收标准

- Console 顶部明确展示 `Demo Sandbox`、`Mock 数据`、`真实系统未接入`、`LLM 默认关闭`。
- 列表和详情不只依赖颜色表达；Mock / Demo / Sandbox 边界有文字说明。
- Mock 业务数据列表展示 `Demo Sandbox`、`source_system`、`source_ref`，便于演示讲解数据来源。
- 详情栏在 JSON 前展示“演示证据摘要”，优先展示 Mock、environment、source_system、source_ref、source_refs、scenario_pack_code 等关键证据。
- `npm run build` 通过。

## 禁止事项

- 不改后端 API，不新增字段，不改数据库 / 持久化逻辑。
- 不接真实 CRM / ERP / OA / 工单系统。
- 不启用真实 LLM，不读取 / 写入 key。
- 不把 Mock / Sandbox 写成生产能力或真实集成。
- 不改 H5 客户页和共享 API client，除非构建类型必须同步。

## 完成记录

- 2026-07-13：已完成 Console 演示标识增强。
- Header 从 `Demo` 升级为 `Demo Sandbox`，并新增 `真实系统未接入`、`LLM 默认关闭` 标签。
- 新增 Demo Sandbox 横幅，说明 Console 仅展示 Mock / Sandbox 证据，真实 CRM / ERP / OA / 工单与真实 LLM 自动答复均未启用。
- Mock 业务数据卡片新增 `environment`、`source_system`、`source_ref` 展示。
- 详情栏 JSON 前新增“演示证据摘要”，提取 Mock、environment、source_system、source_ref、source_refs、场景包和 answer_type 等关键证据。
- 验证：`npm run build` 通过。
- 文档回写：`docs/08-dev-plan.md` §6、`docs/09-verification.md` §10.26。
