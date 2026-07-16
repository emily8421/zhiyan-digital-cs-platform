# Token Hotspot 观察记录：task-011e 端到端彩排 + M11 验收 + PR #49 合并

> 本文件为 AI 协作观察记录，不替代 `.ai/session-handoff.md`、`docs/08-dev-plan.md` 或 `docs/09-verification.md`。
> 本记录不包含 token、密钥、完整对话、客户敏感数据或隐私事实。

## 元数据

- 日期：2026-07-16
- 任务：合并 PR #49（task-011d）→ 执行 task-011e 端到端彩排 → M11 验收 + v0.3.0 bump。
- 触发原因：从快速续接进入 PR/CI 收尾（合并 PR #49）再连续进入 Sprint 执行（task-011e 彩排），跨越两类任务规则路由；彩排涉及启动三端、API 全链路验证、前端人工验收、多文件文档回写与版本发布。
- 状态：已记录

## Hotspot 来源

1. **跨任务类型规则路由（PR 收尾 + Sprint 执行）**
   - 合并 PR #49：读 `ai/index.md`、`rules-core.md`、`implementation-lifecycle-rules.md`、`project-rules.md`、`commands/README.md`、`git-guide.md`（PR/CI/Git 收尾包）。
   - task-011e：追加 `global-rules.md`、`commands/run-dev-task.md`、`prompts/dev/02-run-task.md`（编码/Sprint 执行包）。
   - 两类任务在同一连续会话，规则有部分重叠但不可全复用（PR 收尾 vs 编码执行层不同）。

2. **彩排 SOP 大文档**
   - `docs/env/local-demo-runbook.md`（183 行）、`docs/env/external-demo-script.md`（221 行）整文件读入，为启动三端 + 演示主线 + 边界话术。
   - task-011e 任务单 + `docs/09` §10.28（TC-066~071 验收口径）按锚点读。

3. **API 全链路验证返工（curl 中文编码）**
   - 首轮用 curl 发中文 message body → FastAPI HTTP 400 "error parsing the body"（Windows Git Bash curl 中文编码不可靠）。
   - 误判为 message 响应字段名错误，多轮探查结构（conversation_id vs id、handoff_id、gap_id）后才定位根因。
   - 改用 python urllib（写临时脚本 `.ai/task-011e-rehearse.py`）一次性跑通 9 步闭环。

4. **seed 数据 vs 运行时数据混淆**
   - 首轮 curl 失败时，GET /handoffs、/knowledge-gaps 返回的 handoff_001 / gap_001（conv_demo_*，2026-07-05）是 seed 预置，非新产生；一度误读为"产生了 2 个 handoff"。
   - record 主键命名不统一（conversation_id / handoff_id / gap_id，非通用 id）也消耗探查轮次。

5. **多文件文档回写 + 版本发布**
   - 阶段 3：`docs/09` §10.28（TC-069/071 → ✅ + task-011e 证据段）、`docs/08`（Sprint-10 完成 + §6 + §7）、新建 `docs/research` 彩排记录、VERSION + CHANGELOG v0.3.0、handoff，共 6 处写入。

## 质量影响

- 正面：彩排严格按 TC-066~071 逐项验，TC-069/071 未硬凑通过（前端人工确认 ABCD 全正常才标 ✅）；发现 CI 只跑 diff-check 不跑 pytest，补跑全量 87 passed 确认合并无回归；VERSION/CHANGELOG bump 一次通过 CI 校验。
- 成本：curl 中文编码返工 + seed/运行时数据混淆探查 + 跨任务规则读取 + 彩排 SOP 大文档，累计上下文与轮次高（本会话从快速续接到 M11 发布跨多任务）。
- 风险：curl 中文 body 400 初次误判为字段名问题，浪费 2 轮探查；若未定位编码根因可能误报 message 接口缺陷。

## 优化建议

1. **Windows 下 API 验证默认用 python，不用 curl 中文 body**
   - Git Bash curl 发中文 JSON body 不可靠（HTTP 400 parsing body）；API 全链路验证默认 python urllib / httpx，或项目提供 `scripts/` 验证脚本。
   - 本轮 `.ai/task-011e-rehearse.py` 可提升到 `scripts/rehearse-product-sandbox.py` 作为可复用彩排验证脚本（去硬编码、参数化场景包）。

2. **彩排验证区分 seed 数据 vs 运行时数据**
   - GET /handoffs、/knowledge-gaps 返回 seed 预置（conv_demo_*、2026-07-05）+ 运行时新产生；验证"产生了 X 个"前先按 conversation_id 过滤本次会话产生的，避免把 seed 计入。

3. **record 字段名约定**
   - 本项目 record 主键命名不统一（conversation_id / handoff_id / gap_id，非通用 id）；API 验证脚本与文档可注明各 record 的主键字段，减少探查。

4. **规则路由跨任务复用**
   - 合并 PR（PR/CI 收尾包）+ 紧接 Sprint 执行（编码包）的连续任务，重叠规则（rules-core / project-rules / implementation-lifecycle）可标注复用，避免重读；命令 prompt（git-guide vs run-dev-task）按任务类型分别读。

## 本轮关键结果摘要

- PR #49 合并：merge commit `5f3227e`，main 同步，分支清理。
- task-011e 彩排：三端 6/6 reachable、pytest 87 passed / 6 skipped、API 9 步闭环 http=200、前端 ABCD 全正常。
- TC-066~071 全过 → M11 Product Sandbox 可试用版验收通过（2026-07-16）。
- 版本：v0.2.0 → v0.3.0（VERSION + CHANGELOG），commit `72a09df`，CI project-check pass。
- 文档：`docs/09` §10.28、`docs/08`、`docs/research/2026-07-16-task-011e-product-sandbox-rehearsal.md`、handoff。
- 残留：project-rules §1 Phase 口径（Phase2 + M11 记录，dev-plan Phase2.5/3A 标签口径待统一）；`.ai/task-011e-rehearse.py` 加 .gitignore。
