# task-010a-demo-sandbox-standard-mock-data

## 目标

为客户演示补齐标准化 Demo Sandbox 模拟业务数据包：在不接真实 CRM / ERP / OA / 工单系统的前提下，让订单、项目、工单等 Mock 数据具备稳定编号、来源追溯、环境标识、规范 payload、进度节点和脱敏边界，可作为后续 LLM Sandbox 的证据输入。

## 输入文档

- `docs/research/2026-07-11-demo-sandbox-readiness-evaluation.md` §4、§5、§7。
- `docs/design/integration-adapters.md` §4、§5、§6。
- `docs/design/mock-integrations.md` §2~§6。
- `docs/07-api-spec.md` API-007 / API-008。

## 修改范围

- `backend/app/data/scenario_packs/*.json`：补标准 Demo Sandbox 记录和字段。
- `backend/app/schemas/`、`backend/app/services/`：兼容返回 `source_ref` / `source_system` / `environment` / `stage` / `payload`。
- `docker/postgres/init/002_seed.sql`：同步 PostgreSQL seed payload。
- `frontend/shared/types.ts`：同步共享类型。
- `tests/api/`、`tests/scenarios/`：补标准编号与字段验证。
- 回写 `docs/07-api-spec.md`、`docs/design/mock-integrations.md`、`docs/08-dev-plan.md`、`docs/09-verification.md`。

## 验收标准

- API-007 可查询 `DEMO-ORDER-202607-001`、`DEMO-PROJ-202607-001`、`DEMO-TICKET-202607-001` 等标准模拟编号。
- API-007 / API-008 响应保留旧字段，并新增 `source_ref`、`source_system`、`environment=demo_sandbox`、`stage`、`payload`。
- 每条标准模拟数据都有 `schema_version=demo_sandbox.v1`、`mock=true`、`redaction_applied=true` 和进度节点。
- H5 消息策略能识别 `DEMO-*` 编号，并返回 `answer_type=mock_business`、来源为标准 `source_ref`。
- 不接真实业务系统，不记录真实凭据，不处理真实客户数据。

## 禁止事项

- 不接真实 CRM / ERP / OA / 工单系统。
- 不启用 LLM Sandbox；本任务只提供结构化模拟证据。
- 不新增外部依赖、Docker 镜像或真实 SaaS 调用。
- 不生成真实客户隐私、合同、报价、联系方式或生产数据。

## 完成记录

- 2026-07-11：已补标准 Demo Sandbox 业务数据包（产品型订单、项目型项目 / 工单），并扩展 API 响应字段和 PG seed payload。
- 关键编号：`DEMO-ORDER-202607-001`、`DEMO-ORDER-202607-002`、`DEMO-PROJ-202607-001`、`DEMO-TICKET-202607-001`。
- 边界：保留旧 `HC-*` / `XS-*` 编号兼容；新增数据均标 `mock=true` 与 `environment=demo_sandbox`。

