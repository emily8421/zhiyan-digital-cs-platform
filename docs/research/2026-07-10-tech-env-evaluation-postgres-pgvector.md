# 技术环境评估：PostgreSQL + pgvector（Sprint-8 前置 / RG-002）

> 本文件为技术环境评估留痕（`ai/prompts/review/20-tech-env-evaluation.md`），属 `docs/research/`。不替代 `docs/env/local-env.md`、`docs/05-tech-spec.md` 或 `docs/09-verification.md`。

## 0. 文档元信息

| 项 | 内容 |
|---|---|
| 范围 | PostgreSQL 16 + pgvector 0.8.0 本机 Docker 可行性（RG-002） |
| 评估日期 | 2026-07-10 |
| 结论 | **Go** |
| 关联 | `docs/05-tech-spec.md` §13 RISK-P2-001 / §14 RG-002、`docs/06-db-design.md`、`docs/09-verification.md` §10.2 |

## 1. 评估摘要

- 范围：验证 PostgreSQL 16 + pgvector 在本机 Docker 是否可跑，作为 Sprint-8 DB 技术验证前置与 RG-002 证据。
- 结论：**Go**。容器可起、扩展可装、`zycs_` 表可建（含向量字段）、向量检索可用、资源占用极低。
- 不阻塞 Sprint-8 DB 实现。
- 最关键理由：① pgvector 0.8.0 扩展安装成功；② ivfflat 索引 + cosine 距离检索排序正确；③ 空闲态仅 48.67 MiB；④ Docker Desktop 4.76.0 现已可用（RISK-P2-001 解除）。

## 2. 评估范围与依据

- 读取：`docs/06-db-design.md`（11 张 `zycs_` 表 + `embedding` 字段）、`docs/05-tech-spec.md` §13/§14、`docs/09-verification.md` §10、`ai/project-rules.md` §2/§2.5、`docs/env/local-env.md`（Docker 此前记录"不可用"）。
- 实跑验证命令见 §6。

## 3. 本机环境事实

- Docker Desktop 4.76.0（Engine 29.5.2，Compose v5.1.4）—— 本次实测可用（与 `local-env` 旧记录"不可用"不一致，已更新）。
- 本机约 31.73 GB 内存；容器内存上限 15.48 GiB（Docker 默认）。
- 端口 5432 可用。

## 4. 技术路线候选与决策

| 方案 | 说明 | 决策 |
|---|---|---|
| `pgvector/pgvector:0.8.0-pg16`（官方） | PG16 + pgvector 0.8.0 一体镜像 | ✓ 采用 |
| `ankane/pgvector` | 已 deprecated | 不采用 |
| 自建 PG + 手动装 pgvector | 维护成本高 | 不采用 |

依据：官方 pgvector 镜像，版本明确（0.8.0-pg16），与 `06` 设计一致。

## 5. 依赖与工具支撑矩阵

| 名称 | 目标版本 | 启用阶段 | 当前状态 | 验证方式 | 验证状态 |
|---|---|---|---|---|---|
| PostgreSQL | 16（pgvector 镜像） | Phase2 技术验证 | 已验证可用 | `docker run` + `pg_isready` | ✅ 通过 |
| pgvector | 0.8.0 | Phase2 技术验证 | 已验证可用 | `CREATE EXTENSION vector` | ✅ 通过 |
| ivfflat 索引 | 内置 | Phase2 技术验证 | 已验证可用（小数据低召回提示） | `CREATE INDEX` + 检索 | ✅ 通过（P2：数据量足后评估 HNSW） |

## 6. 安装 / 运行验证（已执行）

- `docker pull pgvector/pgvector:0.8.0-pg16` → 成功。
- `docker run -d --name zycs-pg-test -e POSTGRES_PASSWORD=demo -e POSTGRES_DB=zycs -p 5432:5432 ...` → 容器启动，`pg_isready` 2s 就绪。
- `CREATE EXTENSION vector` → 成功，`extversion=0.8.0`。
- `CREATE TABLE zycs_knowledge_items(... embedding vector(3) ...)` → 成功。
- `CREATE INDEX ... ivfflat (embedding vector_cosine_ops)` → 成功（小数据低召回提示，预期）。
- `INSERT` 2 行向量 + `ORDER BY embedding <=> query` → 排序正确（k001=0.0026，k002=0.1443）。
- `docker stats` → **48.67 MiB / 15.48 GiB**，CPU 0.04%。

## 7. 资源 / 网络 / 权限

- 资源：空闲 48 MiB，远低于本机 31 GB；生产规模需按数据量复评。
- 网络：拉镜像需访问 Docker Hub（技术验证必要下载，属依赖安装范畴）；容器运行不需外网。
- 权限：本机 Docker Desktop，无额外管理员权限需求。

## 8. 风险与降级

| Risk-ID | 风险 | 状态 | 降级 |
|---|---|---|---|
| RISK-P2-001 | Docker 不可用阻塞 PG/pgvector | **已解除**（4.76.0 可用） | 若再不可用，回退 JSON/Mock |
| RISK-P2-005（新） | ivfflat 小数据低召回 | 已知，不阻塞 | 数据量足后评估 HNSW；Phase2 embedding 默认关闭 |
| RISK-P2-006（新） | embedding 维度 / 方案未定 | 待 embedding 方案（Phase2 默认关闭） | 向量字段先空，关键词 / 规则匹配降级 |

## 9. Readiness gate

| Gate | 适用对象 | 进入标准 | 证据 | 状态 |
|---|---|---|---|---|
| RG-002 | PostgreSQL/pgvector | 技术验证 Go / Conditional Go | 本报告 §6 | **Go** |

## 10. 结论

**Go**。Sprint-8 DB 技术验证前置满足，可进入 Sprint-8 数据库实现（docker compose 编排 + 迁移脚本 + Mock→PG 切换）；实现范围需单独方案确认。

## 11. 对 docs/05、docs/09、docs/08 的修改建议

- `05 §0`：日期→2026-07-10；状态补 RG-002 Go。
- `05 §3.1`：PG 依赖"候选（默认关闭）"→"已验证可用（RG-002 Go）"。
- `05 §13`：RISK-P2-001 状态"待验证"→"已解除"；新增 RISK-P2-005/006。
- `05 §14`：RG-002 状态"待评估"→"Go"。
- `09 §0`：状态补 RG-002 Go；`§10.2` RG-002 状态"待验证"→"Go"。
- `08`：Sprint-8 前置 RG-002 满足；Sprint-8 实现范围待方案确认。

## 12. 待人工确认项

| ID | 待确认项 | AI 建议 | 依据 | 阻塞 |
|---|---|---|---|---|
| DB-C-001 | Sprint-8 DB 实现是否立即启动（compose + 迁移 + Mock→PG） | 评估通过后单独起 Sprint-8 DB 实现方案确认 | RG-002 Go | 不阻塞评估落盘 |
| DB-C-002 | pgvector 索引 ivfflat vs HNSW | 数据量足后再定，当前 ivfflat | 小数据低召回提示 | 不阻塞 |
| DB-C-003 | embedding 维度与方案 | Phase2 默认关闭，待 TEI / 方案 | `project-rules` §2 | 不阻塞 DB 存储 |

## 13. 报告落盘

- 路径：`docs/research/2026-07-10-tech-env-evaluation-postgres-pgvector.md`（本文件）。
- 不替代 `docs/env/local-env.md`、`docs/05-tech-spec.md`、`docs/09-verification.md`。
