# PostgreSQL + pgvector 本机运行手册

> 定位：本文件是 Phase2 Sprint-8A「DB 持久化基础设施」的本机运行手册，归属 `docs/env/`。它说明如何启动、检查、重置和关闭 PostgreSQL + pgvector 本机容器；不表示后端业务已经切换到数据库，也不替代 `docs/06-db-design.md` 的数据库设计或 `docs/09-verification.md` 的验收记录。

## 0. 当前口径

| 项 | 内容 |
|---|---|
| 阶段 | Phase2 MVP 试点 / Sprint-8A DB 地基 |
| 技术栈 | PostgreSQL 16 + pgvector 0.8.0 |
| 镜像 | `pgvector/pgvector:0.8.0-pg16` |
| Compose 文件 | `docker/docker-compose.pgvector.yml` |
| 初始化脚本 | `docker/postgres/init/001_schema.sql`、`docker/postgres/init/002_seed.sql` |
| 本机端口 | `5432` |
| 数据库 | `zycs` |
| 用户 | `zycs` |
| Demo 密码 | `zycs_demo_password` |

## 1. 重要边界

- 本手册只搭建数据库地基，不改 H5、Console 或 FastAPI 业务逻辑。
- 当前 Demo 仍默认使用内存 / JSON / Mock 数据，不从 PostgreSQL 读写业务数据。
- `zycs_knowledge_items.embedding` 仅保留空字段；embedding 维度、模型和向量检索业务能力仍未启用。
- 不接真实客户数据、真实订单、真实合同、真实报价、真实联系方式或生产会话。
- 不接真实飞书、CRM / ERP / OA / 工单系统，不启用 LLM。
- `zycs_demo_password` 只用于本机 Demo，不得用于任何生产或共享环境。

## 2. 启动前检查

确认 Docker 可用：

```powershell
docker --version
docker compose version
```

确认 `5432` 未被其他 PostgreSQL 占用：

```powershell
netstat -ano | Select-String ':5432'
```

如端口已占用，先停止旧 PostgreSQL，或临时修改 `docker/docker-compose.pgvector.yml` 的端口映射。

## 3. 启动数据库

先检查 Compose 配置：

```powershell
docker compose -f docker/docker-compose.pgvector.yml config
```

启动：

```powershell
docker compose -f docker/docker-compose.pgvector.yml up -d
```

查看状态：

```powershell
docker compose -f docker/docker-compose.pgvector.yml ps
```

期望看到 `zycs-postgres-pgvector` 为 healthy。

## 4. 验证数据库地基

### 4.1 验证 pgvector 扩展

```powershell
docker compose -f docker/docker-compose.pgvector.yml exec postgres psql -U zycs -d zycs -c "SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';"
```

期望返回 `vector`。

### 4.2 验证 11 张 `zycs_` 表

```powershell
docker compose -f docker/docker-compose.pgvector.yml exec postgres psql -U zycs -d zycs -c "SELECT COUNT(*) AS table_count FROM information_schema.tables WHERE table_schema = 'public' AND table_name LIKE 'zycs_%';"
```

期望 `table_count = 11`。

### 4.3 验证种子数据

```powershell
docker compose -f docker/docker-compose.pgvector.yml exec postgres psql -U zycs -d zycs -c "SELECT code, name FROM zycs_scenario_packs ORDER BY code;"
docker compose -f docker/docker-compose.pgvector.yml exec postgres psql -U zycs -d zycs -c "SELECT record_type, external_ref, status FROM zycs_mock_business_records ORDER BY external_ref;"
```

期望包含：

- `product_business`
- `project_business`
- `HC-ORDER-001`
- `HC-ORDER-002`
- `XS-PROJ-001`
- `XS-PROJ-002`
- `XS-TICKET-001`

## 5. 关闭数据库

只停止容器，保留数据卷：

```powershell
docker compose -f docker/docker-compose.pgvector.yml down
```

清空数据卷并重跑初始化脚本：

```powershell
docker compose -f docker/docker-compose.pgvector.yml down -v
docker compose -f docker/docker-compose.pgvector.yml up -d
```

## 6. 常见问题

| 现象 | 处理 |
|---|---|
| `5432` 端口冲突 | 停止旧 PostgreSQL，或改 Compose 端口映射为 `15432:5432`。 |
| 容器不是 healthy | 先看日志：`docker compose -f docker/docker-compose.pgvector.yml logs postgres`。 |
| 修改 SQL 后没生效 | PostgreSQL 初始化脚本只在空数据卷首次启动时执行；需要 `down -v` 后重启。 |
| H5 / Console 仍使用 Mock | 这是预期行为。本任务只搭 DB 地基，不改后端业务读写。 |
| 想连接数据库客户端 | 使用 host `127.0.0.1`、port `5432`、database `zycs`、user `zycs`、password `zycs_demo_password`。 |

## 7. 后续建议

下一步可拆为两个独立任务：

1. **Sprint-8B：静态数据读库**——让场景包、知识、规则、Mock 业务记录可从 PostgreSQL 读取，同时保留 JSON 降级。
2. **Sprint-8C：会话持久化**——让会话、消息、转人工、知识缺口、通知和日报写入 PostgreSQL，同时保留 Mock / 内存降级。

飞书沙箱（RG-001）和 LLM 评估（RG-003）继续单独处理，不与 DB 切换混在同一任务。

