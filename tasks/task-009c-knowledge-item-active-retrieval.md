# task-009c-knowledge-item-active-retrieval

## 目标

补齐知识闭环最后一环：知识条目 `draft → active` 转正（`PATCH /knowledge-items/{item_id}`），并让 `active` 知识条目（含缺口入库的）进入问答检索链路——运营补的知识下次能被自动答中。默认内存，PG 可选持久化。LLM 保持关闭。

## 输入文档

- `docs/06-db-design.md`：`zycs_knowledge_items`（§4.4，status: draft/active/archived）。
- `docs/07-api-spec.md`：API-006 知识条目。
- `docs/design/knowledge-and-policy.md`：§5（`accepted → active_knowledge`）、KP-C-001。
- `docs/decisions/ADR-0004-no-fabrication-and-human-handoff.md`：active 知识必须有 `source_ref`。
- `backend/app/services/message_policy_service.py`：现有检索链路（`_match_knowledge_or_rule`）。

## 修改范围

- `backend/app/services/console_service.py`：新增 `update_knowledge_item_status`。
- `backend/app/services/console_store.py`：新增 `update_knowledge_item_status_in_postgres`。
- `backend/app/api/console.py`：新增 `PATCH /knowledge-items/{item_id}`（需 admin，允许任意合法 status）。
- `backend/app/services/message_policy_service.py`：`_match_knowledge_or_rule` 合并 active 知识条目 + seed 知识统一评分。
- `tests/api/test_console.py`：PATCH 转正测试。
- `tests/api/test_knowledge_retrieval.py`（新增）：active 命中 / draft 不命中 / 无 active 行为不变。
- 更新 `docs/08-dev-plan.md`、`docs/09-verification.md`。

## 验收标准

- `PATCH /knowledge-items/{item_id}` 可改 status（draft/active/archived），需 admin；viewer 返回 403。
- `active` 知识条目（运行时新增或缺口入库后转正）能被问答检索命中（`answer_type=knowledge`、`source_ref` 为该条目的来源）。
- `draft` / `archived` 知识不参与检索。
- **无 active 知识时检索行为不变**（不破坏现有场景测试）。
- 默认全量 + PG 专项回归通过；`git diff --check` 通过。

## 禁止事项

- 不启用 LLM，不接外部系统。
- 不改 H5 / Console 前端。
- 不引入新依赖。
- 不改高风险转人工 / Mock / 通知逻辑。

## 完成记录

- 2026-07-11：已新增 `PATCH /knowledge-items/{item_id}`（draft→active→archived，需 admin）；`active` 知识进入问答检索链路（`message_policy_service._match_knowledge_or_rule` 合并 active + seed 统一评分，只 active 参与）。
- 改动文件：`backend/app/services/console_service.py`、`backend/app/services/console_store.py`、`backend/app/api/console.py`、`backend/app/services/message_policy_service.py`、`tests/api/test_console.py`、`tests/api/test_knowledge_retrieval.py`。
- 验证通过：默认全量 `tests/api tests/scenarios tests/acceptance`，54 passed、6 skipped。
- 验证通过：PG 专项 `test_console_store + test_conversation_store + test_static_data_source`，11 passed。
- 边界确认：无 active 知识时检索行为不变（不破坏现有场景）；draft/archived 不参与检索；PATCH 需 admin；LLM 默认关闭未变；未改前端；未引入新依赖。
- 后置项：前端知识条目管理页（含转正操作 UI）。
