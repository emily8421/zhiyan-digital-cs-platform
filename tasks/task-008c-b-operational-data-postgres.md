# task-008c-b-operational-data-postgres

## 目标

让控制台运营数据中的转人工记录与知识缺口具备 PostgreSQL 持久化能力：在显式设置 `ZYCS_CONVERSATION_STORE=postgres` 与 `ZYCS_DATABASE_URL` 时，客户消息触发的转人工 / 知识缺口写入 PostgreSQL，控制台列表和状态更新优先读取 / 写入 PostgreSQL；默认仍使用内存 Demo，数据库不可用或未配置时保留内存降级。

## 输入文档

- `docs/05-tech-spec.md`：RG-002 PostgreSQL / pgvector Go、Phase2 新依赖边界。
- `docs/06-db-design.md`：`zycs_human_handoffs`、`zycs_knowledge_gaps` 表结构。
- `docs/07-api-spec.md`：API-004 查询 / 更新转人工、API-005 查询 / 更新知识缺口。
- `docs/08-dev-plan.md`：Sprint-8 DB 技术验证与任务拆分。
- `docs/09-verification.md`：Sprint-8A / 8B / 8C-A 验收记录。
- `tasks/task-008c-a-conversation-message-postgres.md`：会话 / 消息持久化已完成，PG 开关与降级模式已建立。

## 修改范围

- 新增 `backend/app/services/console_store.py`：转人工 / 知识缺口 PostgreSQL 存储仓库。
- 修改 `backend/app/services/console_service.py`：在显式启用 PG 时读写 `zycs_human_handoffs` / `zycs_knowledge_gaps`，失败回退内存。
- 新增 `tests/api/test_console_store.py`：覆盖 PG 缺配置回退、PG 转人工 / 知识缺口持久化、控制台状态更新。
- 更新 `docs/env/postgres-pgvector-runbook.md`、`docs/08-dev-plan.md`、`docs/09-verification.md`。

## 验收标准

- 默认不设置 `ZYCS_CONVERSATION_STORE` 时，现有控制台与会话测试通过，仍走内存 Demo。
- 设置 `ZYCS_CONVERSATION_STORE=postgres` 但缺少 `ZYCS_DATABASE_URL` 时，自动回退内存，Demo 不受影响。
- 设置 `ZYCS_CONVERSATION_STORE=postgres` 与 `ZYCS_DATABASE_URL` 后，高风险消息生成的转人工写入 `zycs_human_handoffs`。
- PG 模式下，无依据消息生成的知识缺口写入 `zycs_knowledge_gaps`，并保留 `suggested_tags`。
- PG 模式下，控制台转人工 / 知识缺口列表可查回新增记录，状态更新写回 PostgreSQL。
- `git diff --check` 通过。

## 禁止事项

- 不持久化通知、日报、审计日志。
- 不改 H5 / Console 前端。
- 不接真实客户数据、真实订单、真实合同、真实飞书或真实业务系统。
- 不启用向量检索业务能力，不写入 embedding。
- 不引入新依赖；复用 Sprint-8B 已引入的 `psycopg[binary]`。

## 完成记录

- 2026-07-10：已新增转人工 / 知识缺口 PostgreSQL 可选持久化能力，默认内存，PG 显式启用且失败回退内存。
- 验证通过：PG 专项 `tests/api/test_console_store.py tests/api/test_conversation_store.py`，6 passed。
- 验证通过：默认模式控制台 / 会话相关测试 `tests/api/test_console_store.py tests/api/test_console.py tests/api/test_conversation_store.py`，14 passed、3 skipped。
- 验证通过：默认模式全量后端 `tests/api tests/scenarios tests/acceptance`，36 passed、4 skipped。
- 边界确认：本任务只持久化转人工与知识缺口，未持久化通知、日报、审计日志。
- 残留风险：`zycs_human_handoffs` 当前表结构无 `summary` / `resolution_note` 字段，PG 列表中的 `summary` 临时沿用 `reason`，转人工处理说明不写入 PG；如需完整运营工单字段，应另拆 schema 演进任务。
