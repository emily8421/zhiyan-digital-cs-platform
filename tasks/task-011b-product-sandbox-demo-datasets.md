# task-011b-product-sandbox-demo-datasets

## 目标

为启用场景包补齐独立 Demo Dataset 与虚拟客户资料包，支撑 Product Sandbox 完整产品试用语境。

## 输入文档

- `docs/02-srs.md`：REQ-018、REQ-020、REQ-022
- `docs/03-prd.md`：F-013、AC-008、AC-014
- `docs/06-db-design.md`：Product Sandbox 表占位
- `docs/design/scenario-packs.md`
- `docs/09-verification.md`：TC-067、TC-069、TC-071

## 修改范围

- `backend/app/data/`
- `backend/app/services/`
- `backend/app/schemas/`
- `tests/`
- 必要时更新 `docs/env/external-demo-script.md`

## 验收标准

- 每个启用场景包有独立模拟知识、业务记录、历史会话、缺口、转人工、通知、摘要和虚拟客户资料。
- 切换场景包不会串用 Demo Dataset 或运行态。
- H5 / Console 可展示虚拟客户语境并标识为模拟数据。

## 禁止事项

- 不复制真实客户资料、真实订单、合同、报价或生产会话。
- 不把模拟数据写入真实数据空间。
