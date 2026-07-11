# task-008e-feishu-notification-adapter

## 目标

实现 Feishu 通知适配器骨架：默认保持 Mock；只有显式设置 `ZYCS_FEISHU_NOTIFY_MODE=sandbox` 且本机提供 webhook URL / secret 时才尝试真实发送；缺配置或发送失败时自动降级为 Mock / failed，不阻塞主链路。本任务不提交真实凭据、不启用事件回调、不接真实组织数据。

## 输入文档

- `docs/research/2026-07-10-tech-env-evaluation-feishu-sandbox.md`：RG-001 Conditional Go、凭据 / 出站通知 / 回调边界。
- `tasks/task-008d-feishu-sandbox-readiness.md`：飞书沙箱启动前评估完成记录。
- `docs/05-tech-spec.md`：RG-001、RISK-P2-002、依赖与配置表。
- `docs/design/mock-integrations.md`：Mock 通知 payload 与真实集成升级条件。
- `docs/07-api-spec.md`：API-009 Mock 通知接口。

## 修改范围

- 新增 `backend/app/adapters/feishu_notification_adapter.py`：Feishu 通知模式、签名、文本消息构造、sandbox 发送与降级结果。
- 新增 `backend/app/adapters/__init__.py`：后端适配器包入口。
- 修改 `backend/app/services/console_service.py`：通知创建路径调用 Feishu 适配器，保留默认 Mock。
- 新增 `tests/api/test_feishu_notification_adapter.py`：覆盖默认 Mock、签名、不泄露 secret、sandbox 缺配置降级、消息最小化。
- 修改 `tests/api/test_console.py`：覆盖 API 通知路径在 sandbox 缺 secret 时降级 Mock。
- 更新 `docs/env/postgres-pgvector-runbook.md`、`docs/08-dev-plan.md`、`docs/09-verification.md`。

## 验收标准

- 默认不设置 `ZYCS_FEISHU_NOTIFY_MODE` 时，API-009 仍返回 `send_status=mocked`、`mock=true`。
- 设置 `ZYCS_FEISHU_NOTIFY_MODE=sandbox` 但缺少 webhook URL / secret 时，通知创建不报错，降级为 Mock，payload 不泄露 webhook / secret。
- Feishu 签名函数按时间戳 + secret 生成 HMAC-SHA256 + Base64 结果，且请求体不暴露 secret。
- 沙箱消息内容只包含事件类型、关联 ID、风险 / 缺口摘要和 sandbox 说明，不包含真实客户隐私或生产数据。
- 不启用事件回调；不新增依赖；`git diff --check` 通过。

## 禁止事项

- 不写入真实 webhook、token、secret、用户 ID、组织 ID 或生产数据。
- 不联网调用真实飞书 API 做实发验收；TC-039 仍待人工凭据。
- 不启用事件回调，不暴露公网回调地址。
- 不改变现有 H5 / Console 默认 Mock 演示链路。

## 完成记录

- 2026-07-10：已新增 Feishu 通知适配器骨架，默认 Mock，显式 sandbox，失败降级。
- 验证通过：`tests/api/test_feishu_notification_adapter.py tests/api/test_console.py`，18 passed。
- 验证通过：默认模式全量后端 `tests/api tests/scenarios tests/acceptance`，43 passed、4 skipped。
- 验证通过：TC-039 沙箱实发（2026-07-11），用户本机配置沙箱 webhook URL / secret 后触发 API-009，接口返回 `send_status=sent`、`mock=False`、`notify_mode=sandbox`，且飞书测试群收到通知。
- 边界确认：本任务未提交任何密钥，未启用事件回调，未接真实生产群 / 生产组织数据。
