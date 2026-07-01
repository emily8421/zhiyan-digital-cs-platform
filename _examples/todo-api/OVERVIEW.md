# Todo API（DB + API 完整参考）

本样例展示：**当项目有数据库和对外 API 时，如何保留 `docs/06`、`docs/07`，并用 `docs/09` 建立验证闭环**。

## 样例项目

- 项目名：MiniTodo
- 形态：FastAPI + SQLite 的单人本地待办 API
- Phase1：创建、查询、更新完成状态、删除待办项，并持久化到 SQLite
- 文档裁剪：有持久化、有 REST API，因此保留 `docs/06-db-design.md` 与 `docs/07-api-spec.md`

## 阅读重点

1. `docs/02-srs.md`：每个 REQ 都是可验证的 API / 持久化行为。
2. `docs/06-db-design.md`：`todos` 表如何承接 REQ-1~REQ-5。
3. `docs/07-api-spec.md`：四个 REST 接口如何承接 REQ-1~REQ-4。
4. `docs/09-verification.md`：如何把 REQ 映射到 API 测试、持久化测试和边界测试。

## 与主样例的区别

- `vision-to-product/` 展示从愿景到产品文档的完整生成流程。
- `todo-api/` 更像查阅型参考，用于学习 DB/API 项目的文档闭环。

## Phase 边界

Phase1 只做单人本地 CRUD，不做鉴权、多用户、前端、云部署或 ORM 抽象。
