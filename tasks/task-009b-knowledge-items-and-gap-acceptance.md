# task-009b-knowledge-items-and-gap-acceptance

## 目标

补齐 Sprint-9 知识运营强化：知识缺口审核通过（`accepted`）时自动生成 `draft` 知识条目入库（`zycs_knowledge_items`），并实现 API-006 `GET/POST /knowledge-items` 知识条目管理；默认内存 Mock，显式启用 PostgreSQL 时持久化并保留内存降级。LLM 保持关闭，不接外部系统。

## 输入文档

- `docs/06-db-design.md`：`zycs_knowledge_items`（§4.4）、`zycs_knowledge_gaps`（§4.8）。
- `docs/07-api-spec.md`：API-006 知识条目。
- `docs/design/knowledge-and-policy.md`：§5 缺口生命周期（`accepted → active_knowledge`）、KP-C-003。
- `docs/decisions/ADR-0004-no-fabrication-and-human-handoff.md`。
- `docs/08-dev-plan.md`、`docs/09-verification.md`：Sprint-9 验收与追溯。

## 修改范围

- 修改 `backend/app/schemas/console.py`：新增 `KnowledgeItemRecord`、`KnowledgeItemCreateRequest`。
- 修改 `backend/app/services/console_service.py`：新增知识条目内存存储 + `list_knowledge_items` / `create_knowledge_item`；`update_knowledge_gap_status` 在 `accepted` 时自动生成 `draft` 知识条目。
- 修改 `backend/app/services/console_store.py`：新增 `zycs_knowledge_items` 写入和列表读取（`scenario_pack_code ↔ id` 映射）。
- 修改 `backend/app/api/console.py`：新增 `GET / POST /knowledge-items` 路由。
- 修改 `tests/api/test_console.py`：覆盖 API-006、缺口 accepted 入库、rejected 不入库、权限。
- 更新 `docs/08-dev-plan.md`、`docs/09-verification.md`。

## 验收标准

- 默认不设置 `ZYCS_CONVERSATION_STORE` 时，API-006 走内存，现有测试通过。
- 设置 `ZYCS_CONVERSATION_STORE=postgres` 但缺少 `ZYCS_DATABASE_URL` 时，自动回退内存。
- 设置 `ZYCS_CONVERSATION_STORE=postgres` 与 `ZYCS_DATABASE_URL` 后，知识条目写入 `zycs_knowledge_items`，列表可从 PG 查回。
- `PATCH /knowledge-gaps/{id}` 到 `accepted` 时，自动生成 `draft` 知识条目（`source_ref` 指向缺口），API-006 可查回。
- `PATCH` 到 `rejected` 时不生成知识条目。
- `POST /knowledge-items` 需 admin 角色。
- `git diff --check` 通过。

## 禁止事项

- 不启用 LLM，不接外部系统。
- 不改 H5 / Console 前端。
- 不引入新依赖。
- 不把 `draft` 知识条目写成 `active`（运营后续确认）。

## 完成记录

- 2026-07-11：已新增知识缺口 `accepted` 自动入库为 `draft` 知识条目（`zycs_knowledge_items`）+ API-006 `GET/POST /knowledge-items`；内存默认，PG 显式启用且失败回退内存。
- 改动文件：`backend/app/schemas/console.py`、`backend/app/services/console_service.py`、`backend/app/services/console_store.py`、`backend/app/api/console.py`、`tests/api/test_console.py`、`tests/api/test_console_store.py`。
- 验证通过：默认全量 `tests/api tests/scenarios tests/acceptance`，48 passed、5 skipped。
- 验证通过：PG 专项 `test_console_store + test_conversation_store + test_static_data_source`，11 passed。
- 边界确认：缺口 `accepted` 生成 `draft`（不直接 `active`）；`rejected` 不生成；`POST /knowledge-items` 需 admin；LLM 默认关闭未变；未改前端；未引入新依赖。
- 后置项：知识条目 `draft → active` 转正、`active` 知识进入检索链路、前端知识条目管理页。
