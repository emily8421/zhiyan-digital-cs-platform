# 05 技术方案

## 1. 技术栈与版本
- Python 3.11
- FastAPI 0.110+（含 uvicorn）
- SQLite（Python 标准库 `sqlite3`，不引入额外 ORM）

## 2. 关键技术决策
- 同步实现即可：单人、低并发，不需要 async 复杂度
- 不引入 ORM：表只有一张、字段简单，直接 `sqlite3` 更轻；Phase2 若扩展再评估
- 无鉴权：Phase1 单人本地，鉴权是 Phase3 的事

## 3. Phase 技术约束
与 `ai/project-rules.md` §1、§2 一致：当前 Phase 允许 FastAPI/SQLite/单人；禁止 PostgreSQL、禁止引入用户/鉴权系统。

## 4. 运行环境与资源评估
- 本机 Demo：FastAPI 单进程 + SQLite 文件可在普通开发机本地运行；派生项目以 `docs/env/local-env.md` 为准确认 Python、端口和磁盘空间。
- 资源瓶颈：Phase1 无大数据、无多用户并发、无独立数据库服务；若端口冲突或依赖不可安装，先调整本机端口或改用最小依赖验证。
- 服务器预案：暂不需要公司服务器；若 Phase2 引入多人协作、独立数据库或公网访问，再评估 CPU、内存、磁盘、端口和部署权限。
## 4. 编码约定
详见 `ai/project-rules.md` §5，本文不重复。
