# task-008a-db-foundation

## 目标

为 Phase2 Sprint-8A 搭建 PostgreSQL + pgvector 本机数据库地基：提供可启动的 Docker Compose 编排、数据库表结构初始化、Demo 种子数据和运行手册。当前任务只验证“数据库仓库与货架可用”，不把后端业务逻辑切到数据库。

## 输入文档

- `docs/03-prd.md`：Phase2 MVP 试点边界。
- `docs/05-tech-spec.md`：RG-002 PostgreSQL / pgvector Go、RISK-P2-005 / RISK-P2-006。
- `docs/06-db-design.md`：11 张 `zycs_` 表、索引与种子数据要求。
- `docs/08-dev-plan.md`：Sprint-8 飞书沙箱联调 + DB 技术验证。
- `docs/09-verification.md`：RG-002 与 Phase2 验证边界。
- `docs/research/2026-07-10-tech-env-evaluation-postgres-pgvector.md`：本机 Docker + pgvector 技术验证 Go。

## 修改范围

- 新增 `docker/docker-compose.pgvector.yml`：本机 PostgreSQL 16 + pgvector 0.8.0 编排。
- 新增 `docker/postgres/init/001_schema.sql`：创建 `docs/06-db-design.md` 对应的 11 张 `zycs_` 表与基础索引。
- 新增 `docker/postgres/init/002_seed.sql`：写入产品型 / 项目型场景包、知识、规则、Mock 业务记录和 Mock 通知样例。
- 新增 `docs/env/postgres-pgvector-runbook.md`：启动、检查、重置、关闭和边界说明。

## 验收标准

- `docker compose -f docker/docker-compose.pgvector.yml config` 通过。
- `docker compose -f docker/docker-compose.pgvector.yml up -d` 后 PostgreSQL 健康检查通过。
- 容器内 `psql` 可查询到 pgvector 扩展、11 张 `zycs_` 表和种子数据。
- `git diff --check` 通过。

## 禁止事项

- 不改后端服务层，不把内存 / JSON / Mock 存储切到 PostgreSQL。
- 不新增 Python DB driver、ORM 或应用运行依赖。
- 不接真实客户数据、真实订单、真实合同、真实飞书或真实业务系统。
- 不启用向量检索业务能力；`embedding` 字段仅作为空字段保留。
- 不处理飞书 RG-001、不启用 LLM、不改变现有 H5 / Console 演示链路。

## 完成记录

- 2026-07-10：已新增 PostgreSQL + pgvector Docker Compose 编排、11 张 `zycs_` 表初始化脚本、Demo seed 数据和运行手册。
- 验证通过：`docker compose -f docker/docker-compose.pgvector.yml config`。
- 验证通过：`docker compose -f docker/docker-compose.pgvector.yml up -d` 后容器 health = `healthy`。
- 验证通过：pgvector 扩展版本 `0.8.0`，`zycs_` 表数量 = 11，seed 场景包 = 2，Mock 业务记录 = 5。
- 边界确认：本任务未改后端业务逻辑，H5 / Console 仍默认使用现有 Mock / 本地临时数据链路。
