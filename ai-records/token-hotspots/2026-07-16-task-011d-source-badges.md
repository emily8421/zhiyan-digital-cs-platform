# Token Hotspot 观察记录：task-011d 来源徽章 + API-016

> 本文件为 AI 协作观察记录，不替代 `.ai/session-handoff.md`、`docs/08-dev-plan.md` 或 `docs/09-verification.md`。
> 本记录不包含 token、密钥、完整对话、客户敏感数据或隐私事实。

## 元数据

- 日期：2026-07-16
- 任务：执行 `task-011d-product-sandbox-source-badges`，前端来源徽章 + API-016 来源标识查询。
- 触发原因：从快速续接进入分析 / 写入任务后，按规则完整读取 `ai/index.md` 及其规则清单；随后做代码现状探查、编码、多级验证、文档回写与 PR 闭环。
- 状态：已记录

## Hotspot 来源

1. **快速续接升级为执行任务**
   - 本轮先按快速续接读取 handoff（fresh），用户确认继续执行推荐方案。
   - 按 `ai/session-rules.md` §3.2，进入执行任务必须回到 `ai/index.md` 规则路由，完整读取编码任务规则包。

2. **规则路由必读文件较多（标准门禁，难以压缩）**
   - `ai/rules-core.md`、`ai/global-rules.md`、`ai/implementation-lifecycle-rules.md`、`ai/project-rules.md`、`ai/commands/run-dev-task.md`、`ai/prompts/dev/02-run-task.md` 一次性读入。
   - 这些是编码任务前置门禁，本轮属首次进入该层，无法复用已加载规则。

3. **代码现状探查跨多文件**
   - 后端模板：`backend/app/services/demo_dataset_service.py`、`api/demo_dataset.py`、`schemas/demo_dataset.py`、`services/scenario_pack_service.py`、`services/source_mode_service.py`、`schemas/scenario_packs.py`、`schemas/common.py`、`main.py`。
   - 前端：`frontend/shared/types.ts`、`apiClient.ts`、`frontend/customer-h5/src/App.tsx`（全文）、`frontend/console/src/App.tsx`（分段 1-200 / 200-320 / 455-549）、`frontend/console/src/styles.css`（全文）。
   - handoff 已有探查结论且可信，但代码即将写入，仍逐项核实缺口（H5/Console 缺 source_mode / scenario_pack）。

4. **文档按锚点检索（已优化）**
   - `docs/07-api-spec.md` §API-016、`docs/08-dev-plan.md` Sprint-10、`docs/09-verification.md` §10.28 均先 grep 定位行号再读对应窗口，未读全文。
   - 这是本轮相对 011b/011c 的改进点。

5. **多级验证与多轮编辑**
   - 后端 pytest（含一次断言设计修正后重跑）、Console build、H5 build、git add / commit / push / gh pr create，命令轮次多但均必要。

## 质量影响

- 正面：完整规则读取确保不越 Phase2.5 / Phase3A 边界、不改 API-002 message 契约、来源标识统一为 demo_sandbox / mock、未把未验证的 TC 写成通过。
- 成本：规则补读 + 多文件现状探查 + 文档锚点检索 + 多轮验证命令，累计上下文与轮次较高。
- 风险：首轮 `test_source_refs.py` 的 `isdisjoint` 断言失败——误以为不同场景包 source_ref 必不重叠，实际资料来源（如 `SRC-PRD-001`）跨包复用属正常。说明现状探查未深入数据语义，导致一次测试返工。

## 优化建议

1. **现状探查「先 grep 缺口再读全文」**
   - 对「补徽章 / 补字段」类任务，前端现状先用定向 grep 确认目标字段是否已存在（如 `source_mode|scenario_pack`），命中行号后再决定是否整文件读入，减少整文件加载。
   - 本轮 H5 / Console 已部分采用该方式；可在后续前端任务固化为默认第一步。

2. **测试断言与数据语义先对齐**
   - 写跨实体断言（隔离 / 不重叠 / 计数差异）前，先确认字段语义：场景包级「数据不串用」≠「source_ref 字符串全局唯一」。
   - 演示数据共享资料来源（同一产品手册 / PRD）属正常来源引用，不应作为隔离失败依据。

3. **规则路由读取分层复用**
   - 编码任务标准门禁（5 个规则文件 + 命令 prompt）在首次进入该层时不可避免；建议在同一未中断会话内连续执行同链任务（011d → 011e），复用已加载规则，避免每个子任务重读。
   - 长文档（`docs/07/08/09`）持续按 grep 锚点 + 窗口读取，不读全文。

4. **Console 抽样区样式口径**
   - `hint-badge` 在现有 `styles.css` 中未定义（全局无样式），抽样区复用它保持现状一致；如后续 011e 彩排发现视觉突兀，可统一补 `.hint-badge` 样式（小任务，不阻塞）。

## 本轮关键结果摘要

- 后端 API-016：`backend/app/schemas/source_ref.py`、`services/source_ref_service.py`、`api/source_refs.py` + `main.py` 注册。
- 前端徽章：`frontend/customer-h5/src/App.tsx`、`frontend/console/src/App.tsx`、`frontend/console/src/styles.css`、`frontend/shared/types.ts`、`frontend/shared/apiClient.ts`。
- 测试：`tests/api/test_source_refs.py`；全量 `PYTHONPATH=backend python -m pytest tests/` → 87 passed / 6 skipped。
- 前端构建：`frontend/console` & `frontend/customer-h5` `npm run build`（tsc + vite）均通过。
- 文档回写：`docs/09-verification.md` §10.28 补 task-011d 证据 + TC-069 / TC-071 推进。
- PR：#49（feat/task-011d-product-sandbox-source-badges，commit `fd5bd0c`，CI project-check pass），待 review merge。
- 残留：TC-069 完整虚拟客户资料展示、TC-071 全链路人工彩排待 task-011e；版本 bump 待 M11 完成。
