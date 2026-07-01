# 09 验证计划（Verification）

> 本文回答“怎么算对”。本项目有 DB + REST API，因此验证重点是接口契约、SQLite 持久化和 Phase 边界。

## 1. 测试策略

- API 测试：覆盖 POST / GET / PATCH / DELETE 四个接口的成功路径。
- 数据库测试：使用临时 SQLite 文件验证建表、增删改查和重启后数据仍在。
- 错误测试：覆盖不存在 ID、非法入参、空标题。
- 边界审查：确认 Phase1 无鉴权、多用户、前端、ORM、PostgreSQL。
- 人工验收：按 `docs/07-api-spec.md` 的请求 / 响应示例执行接口调用。

## 2. REQ → 用例追溯矩阵

| REQ | 阶段 | 交付物形态 | 状态 | 用例 ID | 验证方式 | 通过标准 |
|---|---|---|---|---|---|---|
| REQ-1 | [P1] | Demo | P1-已设计 | TC-001 | API 测试 + DB 测试 | POST /todos 返回 201，响应含 id/title/done/created_at，数据库新增记录 |
| REQ-2 | [P1] | Demo | P1-已设计 | TC-002 | API 测试 | GET /todos 返回全部待办，按 created_at 倒序 |
| REQ-3 | [P1] | Demo | P1-已设计 | TC-003 | API 测试 + DB 测试 | PATCH /todos/{id} 可更新 done，数据库状态同步变化 |
| REQ-4 | [P1] | Demo | P1-已设计 | TC-004 | API 测试 + DB 测试 | DELETE /todos/{id} 返回 204，再查询不出现该记录 |
| REQ-5 | [P1] | Demo | P1-已设计 | TC-005 | 持久化测试 | 服务 / 连接重启后，已创建待办仍可查询 |

## 3. 错误与边界用例

| 用例 ID | 场景 | 通过标准 |
|---|---|---|
| TC-101 | POST /todos 标题为空 | 返回 422，不写入数据库 |
| TC-102 | PATCH /todos/{id} 指向不存在 ID | 返回 404 |
| TC-103 | DELETE /todos/{id} 指向不存在 ID | 返回 404 |
| TC-104 | 检查 Phase 边界 | 代码中无鉴权、多用户、ORM、PostgreSQL、前端实现 |

## 4. 分阶段验证范围

- Phase1（Demo）：覆盖 REQ-1~REQ-5，以及 TC-101~TC-104。
- Phase2（MVP）：若增加分类标签、到期时间，在原位追加新的 REQ 和用例，不删除 Phase1 用例。

## 5. Sprint 验收对应

- Sprint1：TC-001~TC-005 全部通过；TC-101~TC-104 至少人工审查通过。
## 6. 本机资源验证

- 启动验证：在 `docs/env/local-env.md` 描述的本机环境中启动 FastAPI 服务并执行健康检查或首个接口请求。
- 资源记录：记录启动耗时、端口占用、SQLite 文件大小、测试请求延迟和内存占用。
- 边界验证：确认 Phase1 不依赖 PostgreSQL、Docker、公司服务器或公网访问。
