# 08 开发计划

> 当前阶段拆 Sprint；每个 Sprint 限制范围，避免一次实现整个系统。

## Sprint1：知识条目持久化闭环

### 目标

实现新增知识条目、生成摘要、SQLite 持久化与详情查看，覆盖 REQ-001、REQ-002、REQ-004、REQ-005 的最小闭环。

### 输入文档

- `docs/02-srs.md`：REQ-001、REQ-002、REQ-004、REQ-005
- `docs/03-prd.md`：F-001、F-002、F-004、F-005
- `docs/04-architecture.md`：CLI 入口、业务服务层、摘要模块、数据访问层
- `docs/05-tech-spec.md`：标准库、SQLite、规则摘要约束
- `docs/06-db-design.md`：`knowledge_items` 表
- `docs/07-api-spec.md`：`kc add`、`kc show`
- `docs/09-verification.md`：TC-001、TC-002、TC-004、TC-005

### 修改范围

- `backend/db.py`
- `backend/repository.py`
- `backend/summarizer.py`
- `backend/service.py`
- `backend/cli.py`
- `tests/test_knowledge_items.py`

### 验收标准

- `kc add` 可新增条目并返回 ID 与摘要。
- `kc show <id>` 可查看标题、摘要、正文、创建时间。
- 重启后仍可查看已新增条目。
- 摘要字段非空且长度不超过 120 字。

### 禁止事项

- 不实现搜索以外的 Phase2 能力。
- 不接入真实在线模型。
- 不引入 ORM、Web 框架或向量数据库。

## Sprint2：关键词搜索

### 目标

实现 `kc search <keyword>`，覆盖 REQ-003。

### 输入文档

- `docs/02-srs.md`：REQ-003
- `docs/03-prd.md`：F-003
- `docs/07-api-spec.md`：`kc search`
- `docs/09-verification.md`：TC-003

### 修改范围

- `backend/repository.py`
- `backend/service.py`
- `backend/cli.py`
- `tests/test_search.py`

### 验收标准

- 搜索标题、摘要、正文中任一字段命中关键词时返回对应条目。
- 无匹配时返回空结果提示，不报错。

### 禁止事项

- 不引入全文索引、向量检索或标签过滤。
- 不改变 Sprint1 的表结构，除非先更新 `docs/06-db-design.md` 并人工确认。
