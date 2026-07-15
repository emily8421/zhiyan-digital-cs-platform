# task-011d-product-sandbox-source-badges

## 目标

在 H5、Console、API 响应和日志中统一展示 Product Sandbox 来源标识。

## 输入文档

- `docs/02-srs.md`：REQ-016、REQ-022
- `docs/03-prd.md`：F-016、AC-009、AC-012
- `docs/07-api-spec.md`：统一响应 meta、API-016
- `docs/design/frontend-interaction.md`
- `docs/09-verification.md`：TC-071

## 修改范围

- `backend/app/schemas/`
- `backend/app/services/`
- `frontend/customer-h5/`
- `frontend/console/`
- `frontend/shared/`
- `tests/`

## 验收标准

- H5 回复、Console 列表 / 详情、通知、摘要和 API 响应均展示 `source_mode`、`scenario_pack`、`source_ref`、`mock` / `real`。
- 降级到模拟数据时界面明确提示当前为 `demo_sandbox`。
- 来源缺失不能通过 Product Sandbox 验收。

## 禁止事项

- 不在日志或 UI 中展示 token、真实联系方式或敏感业务数据。
- 不静默降级。
