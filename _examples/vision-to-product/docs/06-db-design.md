# 06 数据库设计

> 本项目存在 SQLite 本地持久化，因此保留本文档。Phase1 表结构写细，后续阶段保留骨架。

## 1. 表清单

| 表名 | 阶段 | 状态 | 用途 | 对应 REQ |
|---|---|---|---|---|
| knowledge_items | [P1] | P1-已设计 | 保存知识条目的标题、正文、摘要和创建时间 | REQ-001~005 |
| item_tags | [P2] | 骨架 | 保存条目与标签关系 | REQ-101 |

## 2. 表结构

### knowledge_items [P1][P1-已设计]

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 条目 ID |
| title | TEXT | NOT NULL | 标题 |
| body | TEXT | NOT NULL | 原文 |
| summary | TEXT | NOT NULL | 摘要 |
| created_at | TEXT | NOT NULL | ISO 8601 创建时间 |
| updated_at | TEXT | NOT NULL | ISO 8601 更新时间 |

### item_tags [P2][骨架]

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| item_id | INTEGER | NOT NULL | 条目 ID |
| tag | TEXT | NOT NULL | 标签名 |

## 3. 索引设计

- `idx_knowledge_items_created_at`：按创建时间倒序列出最近条目。
- `idx_knowledge_items_title`：提升标题关键词查询的基础性能。
- Phase1 不建全文索引；若搜索质量不足，Phase2 再评估 FTS 或语义检索。

## 4. 表间关系

- Phase1 只有 `knowledge_items` 单表，无外键关系。
- Phase2 若启用 `item_tags`，`item_tags.item_id` 逻辑关联 `knowledge_items.id`。
