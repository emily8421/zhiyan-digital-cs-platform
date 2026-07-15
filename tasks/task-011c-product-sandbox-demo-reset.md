# task-011c-product-sandbox-demo-reset

## 目标

实现 Demo Sandbox 初始化 / 重置能力，仅重置当前场景包演示运行态。

## 输入文档

- `docs/02-srs.md`：REQ-019
- `docs/03-prd.md`：F-014、AC-010
- `docs/04-architecture.md`：Flow-005
- `docs/07-api-spec.md`：API-015
- `docs/design/web-console.md`、`docs/design/backend-service.md`
- `docs/09-verification.md`：TC-068

## 修改范围

- `backend/app/api/`
- `backend/app/services/`
- `backend/app/data/` 或持久化仓库
- `frontend/console/`
- `tests/`

## 验收标准

- reset 前有明确作用域提示。
- reset 后当前场景包会话、缺口、转人工、通知和摘要恢复到初始演示态。
- 其他场景包和真实数据配置不受影响。

## 禁止事项

- 不删除真实配置或真实来源引用。
- 不做全局清库式 reset。
