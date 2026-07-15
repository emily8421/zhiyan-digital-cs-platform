# task-011a-product-sandbox-data-source-mode

## 目标

实现 Product Sandbox 的场景包级数据源模式门禁，默认 `demo_sandbox`，真实数据模式仅显示 `Not configured / No-Go`。

## 输入文档

- `docs/02-srs.md`：REQ-017、REQ-021、REQ-022
- `docs/03-prd.md`：F-012、F-015、F-016
- `docs/04-architecture.md`：COMP-013、Flow-005
- `docs/07-api-spec.md`：API-013、API-016
- `docs/design/frontend-interaction.md`、`docs/design/web-console.md`、`docs/design/integration-adapters.md`
- `docs/09-verification.md`：TC-066、TC-070、TC-071

## 修改范围

- `backend/app/api/`
- `backend/app/services/`
- `backend/app/schemas/`
- `frontend/shared/`
- `frontend/console/`
- `tests/`

## 验收标准

- API 可查询当前场景包 `source_mode`、`scenario_pack`、`source_ref` 和门禁状态。
- 未授权真实数据模式返回 `Not configured / No-Go`，不调用真实系统。
- Console 显示当前数据源模式和真实数据门禁状态。

## 禁止事项

- 不接真实 CRM / ERP / OA / 工单系统。
- 不写入真实凭据、token 或客户隐私数据。
- 不把 `demo_sandbox` 展示为真实数据。
