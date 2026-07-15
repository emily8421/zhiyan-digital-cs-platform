# task-011e-product-sandbox-end-to-end-rehearsal

## 目标

完成 Product Sandbox 可试用版端到端彩排，验证 M11 验收口径。

## 输入文档

- `docs/03-prd.md`：AC-008~AC-014
- `docs/08-dev-plan.md`：Sprint-10 / M11
- `docs/09-verification.md`：TC-066~TC-071
- `docs/design/frontend-interaction.md`、`docs/design/h5-dialog.md`、`docs/design/web-console.md`
- `docs/env/local-demo-runbook.md`
- `docs/env/external-demo-script.md`

## 修改范围

- `docs/research/`（彩排记录）
- `docs/09-verification.md`（验收记录）
- 必要时补 `scripts/` 验证辅助，不新增外部依赖

## 验收标准

- TC-066~TC-071 全部通过或记录明确阻塞项。
- 完整跑通：客户问答 → 订单 / 项目 / 售后进度查询 → 高风险转人工 → 缺口生成 → 知识入库 → Console 看板 → 通知记录 → 日报摘要 → Demo reset。
- 彩排记录明确真实数据、真实业务系统、生产飞书和生产 LLM 均未解锁。

## 禁止事项

- 不接真实生产系统。
- 不使用真实客户数据做演示。
- 不把彩排通过等同于生产上线。
