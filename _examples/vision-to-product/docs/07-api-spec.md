# 07 API设计（CLI 契约）

> 本项目 Phase1 对外接口是 CLI 命令，不提供 HTTP API。本文描述命令、参数、输出和错误契约。

## 1. 统一约定

- 命令前缀：`kc`
- 输出格式：默认人类可读文本；`--json` 可输出 JSON（P1 可选）
- 成功退出码：`0`
- 参数错误退出码：`2`
- 运行时错误退出码：`1`
- 数据库路径：默认本地文件，可通过 `--db-path` 覆盖

## 2. 接口清单

| 命令 | 阶段 | 状态 | 用途 | 对应功能 |
|---|---|---|---|---|
| `kc add --title <title> --body <text>` | [P1] | P1-已设计 | 新增知识条目并生成摘要 | F-001/F-002/F-005 |
| `kc search <keyword>` | [P1] | P1-已设计 | 按关键词搜索条目 | F-003 |
| `kc show <id>` | [P1] | P1-已设计 | 查看单条知识详情 | F-004 |
| `kc tag ...` | [P2] | 骨架 | 标签管理 | F-101 |

## 3. 请求 / 响应示例

### `kc add --title <title> --body <text>`

输入：

```bash
kc add --title "AI 编程原则" --body "先写需求和边界，再让 AI 编码。"
```

输出：

```text
created item 1
summary: 先写需求和边界，再让 AI 编码。
```

### `kc search <keyword>`

输入：

```bash
kc search "边界"
```

输出：

```text
1  AI 编程原则  先写需求和边界，再让 AI 编码。
```

### `kc show <id>`

输入：

```bash
kc show 1
```

输出：

```text
ID: 1
Title: AI 编程原则
Summary: 先写需求和边界，再让 AI 编码。
Body: 先写需求和边界，再让 AI 编码。
Created: 2026-06-21T00:00:00
```

### 错误示例

```text
error: title and body are required
```
