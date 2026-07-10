# task-008b-static-data-postgres

## 目标

让后端静态数据具备 PostgreSQL 读取能力：场景包、知识、规则和 Mock 业务记录可在显式设置环境变量时从 Sprint-8A 数据库读取；默认仍使用 JSON 文件，数据库不可用或未配置时保留 JSON 降级，避免破坏现有 Demo。

## 输入文档

- `docs/05-tech-spec.md`：RG-002 PostgreSQL / pgvector Go、Phase2 新依赖需人工确认。
- `docs/06-db-design.md`：`zycs_scenario_packs`、`zycs_knowledge_items`、`zycs_rule_items`、`zycs_mock_business_records`。
- `docs/08-dev-plan.md`：Sprint-8 DB 技术验证与任务拆分。
- `docs/09-verification.md`：Sprint-8A TC-021~024 与本任务新增验证。
- `tasks/task-008a-db-foundation.md`：DB 地基已完成，容器可 healthy，seed 数据可查。
- `docs/env/postgres-pgvector-runbook.md`：本机 PostgreSQL 启动与连接方式。

## 修改范围

- `backend/requirements.txt`：新增 `psycopg[binary]`。
- `backend/app/services/static_data_source.py`：新增静态数据源环境变量开关。
- `backend/app/services/postgres_static_data_repository.py`：新增 PostgreSQL 静态数据读取仓库。
- `backend/app/services/scenario_pack_service.py`：在 `ZYCS_STATIC_DATA_SOURCE=postgres` 时优先读 PostgreSQL，失败回退 JSON。
- `tests/api/test_static_data_source.py`：覆盖 JSON 默认、PG 缺配置回退、PG seed 读取。
- `docs/env/postgres-pgvector-runbook.md`、`docs/08-dev-plan.md`、`docs/09-verification.md`：补充运行与验收记录。

## 验收标准

- 默认模式不设置环境变量时，后端测试仍通过，静态数据继续从 JSON 读取。
- `ZYCS_STATIC_DATA_SOURCE=postgres` 但未设置 `ZYCS_DATABASE_URL` 时，自动回退 JSON，Demo 不受影响。
- 设置 `ZYCS_TEST_DATABASE_URL=postgresql://zycs:zycs_demo_password@127.0.0.1:5432/zycs` 后，PG 模式测试通过，可读取 seed 场景包、知识和 Mock 业务记录。
- 全量后端测试通过。
- `git diff --check` 通过。

## 禁止事项

- 不迁移会话、消息、转人工、知识缺口、通知、日报到 PostgreSQL。
- 不引入 ORM，不引入 SQLAlchemy，不新增数据库写入业务逻辑。
- 不接真实客户数据，不处理真实订单、真实合同、真实飞书或真实业务系统。
- 不启用向量检索业务能力，不写入 embedding。
- 不改变现有 H5 / Console 默认演示链路。

## 完成记录

- 2026-07-10：已新增 PostgreSQL 静态数据读取能力，默认 JSON，PG 显式启用且失败回退 JSON。
- 验证通过：`tests/api/test_static_data_source.py` 在 PG 模式下 3 passed。
- 验证通过：默认模式全量后端 `tests/api tests/scenarios tests/acceptance`，33 passed、1 skipped（PG 专项在未设置 `ZYCS_TEST_DATABASE_URL` 时跳过）。
- 边界确认：本任务只迁移静态数据读取能力，未做业务写库和会话持久化。
