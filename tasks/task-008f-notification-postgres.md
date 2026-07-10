# task-008f-notification-postgres

## 目标

让控制台通知记录具备 PostgreSQL 持久化能力：在显式设置 `ZYCS_CONVERSATION_STORE=postgres` 与 `ZYCS_DATABASE_URL` 时，API-009 创建的通知记录写入 `zycs_notifications`，通知列表优先从 PostgreSQL 读取；默认仍使用内存 Mock，数据库不可用或未配置时保留内存降级。

## 输入文档

- `docs/06-db-design.md`：`zycs_notifications` 表结构。
- `docs/07-api-spec.md`：API-009 Mock 通知接口。
- `docs/research/2026-07-10-tech-env-evaluation-feishu-sandbox.md`：Feishu 出站通知边界。
- `tasks/task-008e-feishu-notification-adapter.md`：Feishu 通知适配器骨架已完成。
- `docs/08-dev-plan.md`、`docs/09-verification.md`：Sprint-8 验收与追溯记录。

## 修改范围

- 修改 `backend/app/services/console_store.py`：新增 `zycs_notifications` 写入和列表读取。
- 修改 `backend/app/services/console_service.py`：通知创建成功后在 PG 模式写入，通知列表在 PG 模式优先读取 PostgreSQL。
- 修改 `tests/api/test_console_store.py`：覆盖 PG 模式下通知写入、列表读取、payload / send_status 持久化。
- 更新 `docs/env/postgres-pgvector-runbook.md`、`docs/08-dev-plan.md`、`docs/09-verification.md`。

## 验收标准

- 默认不设置 `ZYCS_CONVERSATION_STORE` 时，API-009 仍走内存 Mock，现有测试通过。
- 设置 `ZYCS_CONVERSATION_STORE=postgres` 但缺少 `ZYCS_DATABASE_URL` 时，自动回退内存，Demo 不受影响。
- 设置 `ZYCS_CONVERSATION_STORE=postgres` 与 `ZYCS_DATABASE_URL` 后，API-009 创建通知写入 `zycs_notifications`。
- PG 模式下，`GET /api/v1/notifications/mock?event_type=...&send_status=...` 可从 PostgreSQL 查回通知记录。
- `payload`、`send_status`、`is_mock` 持久化正确，且不包含真实 webhook / secret。
- `git diff --check` 通过。

## 禁止事项

- 不持久化日报、审计日志。
- 不执行 TC-039 飞书沙箱实发，不提交真实 webhook / secret。
- 不启用事件回调，不接真实组织数据。
- 不改 H5 / Console 前端。
- 不引入新依赖。

## 完成记录

- 2026-07-10：已新增 `zycs_notifications` 可选持久化能力，默认内存，PG 显式启用且失败回退内存。
- 验证通过：PG 专项 `tests/api/test_console_store.py tests/api/test_conversation_store.py tests/api/test_static_data_source.py`，10 passed。
- 验证通过：默认模式全量后端 `tests/api tests/scenarios tests/acceptance`，43 passed、5 skipped。
- 边界确认：本任务只持久化通知记录，未持久化日报 / 审计日志，未执行飞书实发。
