# task-008c-a-conversation-message-postgres

## 目标

让客户会话与消息具备 PostgreSQL 持久化能力：在显式设置 `ZYCS_CONVERSATION_STORE=postgres` 与 `ZYCS_DATABASE_URL` 时，新建会话、客户消息和助手回答写入 PostgreSQL；默认仍使用内存 Demo，数据库不可用或未配置时保留内存降级。

## 输入文档

- `docs/05-tech-spec.md`：RG-002 PostgreSQL / pgvector Go、Phase2 新依赖边界。
- `docs/06-db-design.md`：`zycs_conversations`、`zycs_messages` 表结构。
- `docs/08-dev-plan.md`：Sprint-8 DB 技术验证与任务拆分。
- `docs/09-verification.md`：Sprint-8A / 8B 验收记录。
- `tasks/task-008a-db-foundation.md`：数据库地基已完成。
- `tasks/task-008b-static-data-postgres.md`：静态数据读库已完成，`psycopg[binary]` 已引入。

## 修改范围

- 新增 `backend/app/services/conversation_store.py`：会话 / 消息 PostgreSQL 存储仓库与环境变量开关。
- 修改 `backend/app/services/conversation_service.py`：在显式启用 PG 时读写 `zycs_conversations` / `zycs_messages`，失败回退内存。
- 新增 `tests/api/test_conversation_store.py`：覆盖默认内存、PG 缺配置回退、PG 会话 / 消息持久化、高风险状态更新。
- 更新 `docs/env/postgres-pgvector-runbook.md`、`docs/08-dev-plan.md`、`docs/09-verification.md`。

## 验收标准

- 默认不设置 `ZYCS_CONVERSATION_STORE` 时，现有后端全量测试通过，仍走内存 Demo。
- 设置 `ZYCS_CONVERSATION_STORE=postgres` 但缺少 `ZYCS_DATABASE_URL` 时，自动回退内存，Demo 不受影响。
- 设置 `ZYCS_CONVERSATION_STORE=postgres` 与 `ZYCS_DATABASE_URL` 后，新建会话写入 `zycs_conversations`。
- 发送消息后，客户消息与助手回答写入 `zycs_messages`。
- 高风险问题将 `zycs_conversations.status` 更新为 `handoff`、`risk_level` 更新为 `high`。
- `git diff --check` 通过。

## 禁止事项

- 不持久化转人工详情、知识缺口、通知、日报、审计日志。
- 不改 H5 / Console 前端。
- 不接真实客户数据、真实订单、真实合同、真实飞书或真实业务系统。
- 不启用向量检索业务能力，不写入 embedding。
- 不引入新依赖；复用 Sprint-8B 已引入的 `psycopg[binary]`。

## 完成记录

- 2026-07-10：已新增会话 / 消息 PostgreSQL 可选持久化能力，默认内存，PG 显式启用且失败回退内存。
- 验证通过：PG 专项 `tests/api/test_conversation_store.py`，4 passed。
- 验证通过：默认模式全量后端 `tests/api tests/scenarios tests/acceptance`，35 passed、3 skipped。
- 边界确认：本任务只持久化会话与消息，未持久化转人工、知识缺口、通知、日报、审计日志。

