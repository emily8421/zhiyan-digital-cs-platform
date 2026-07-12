# task-010b-llm-sandbox-adapter-mock

## 目标

实现 LLM Sandbox 适配器骨架（mock-LLM-first）：在客户消息回答链路中，把"已找到证据的回答"（mock_business / knowledge / rule）交给 LLM 适配器改写成自然语言，返回 `answer_type=llm_sandbox` 并强制透传 `source_ref` 与 evidence；高风险转人工与无依据缺口不进入 LLM。本增量只实现 `mock` 模式（确定性模板改写，零依赖、不联网、不引模型文件），`sandbox` 模式留接口但本增量安全降级到 mock，不接真实 LLM API。

## 输入文档

- `docs/research/2026-07-11-demo-sandbox-readiness-evaluation.md` §3、§5（LLM Sandbox 边界 / 配置 / 验收口径）。
- `docs/research/2026-07-11-tech-env-evaluation-llm.md` §5、§8、§9（RG-003 Conditional Go、ZYCS_LLM_MODE 三态、骨架优先 Mock LLM）。
- `docs/design/integration-adapters.md` §3、§5（disabled / mock / sandbox 模式与错误降级范式）。
- `tasks/task-010a-demo-sandbox-standard-mock-data.md`（标准模拟数据 source_ref / payload 作为证据输入）。
- `backend/app/adapters/feishu_notification_adapter.py`（适配器三态 + 失败降级范本）。
- `backend/app/services/message_policy_service.py`（answer_type 决策点）。

## 修改范围

- `backend/app/adapters/llm_adapter.py`：新建，照飞书适配器三态结构。
- `backend/app/services/message_policy_service.py`：`decide_message_response` 末尾增加 `_maybe_llm_rewrite`，仅对证据型 answer_type 改写；`MessageDecision` 增加可选 `llm` 字段。
- `backend/app/schemas/conversations.py`：`MessageResponseData` 增加可选 `llm` 字段。
- `backend/app/services/conversation_service.py`：`build_demo_message_response` 把 `decision.llm` 透传到响应。
- `tests/api/test_llm_adapter.py`：新建，照 `test_feishu_notification_adapter.py`。
- `tests/api/test_conversations.py`：增加 `ZYCS_LLM_MODE=mock` 下 `llm_sandbox` 用例。
- `tests/scenarios/test_risk_fallback.py`：增加"高风险即使开启 LLM 也转人工"回归（RISK-P2-007）。
- 回写 `docs/07-api-spec.md`、`docs/08-dev-plan.md`、`docs/09-verification.md`。

## 验收标准

- 默认 `ZYCS_LLM_MODE=disabled` 时，现有回答链路与全量测试不受任何影响。
- `ZYCS_LLM_MODE=mock` 下，证据型问题（mock_business / knowledge / rule）返回 `answer_type=llm_sandbox`，`source_ref` 与原证据一致，响应带 evidence。
- 高风险问题在 `ZYCS_LLM_MODE=mock` 下仍返回 `answer_type=handoff`，LLM 不介入（RISK-P2-007）。
- 无依据缺口（gap）不被 LLM 改写，仍返回 `gap`，不编造业务事实（§5.2）。
- `sandbox` 模式缺 provider / key 时安全降级到 mock 并带 `fallback_reason`；本增量不发起真实 LLM 调用、不读 / 写真实 key。
- 全量后端回归通过，新增 LLM 用例通过。

## 禁止事项

- 不接真实 LLM API，不写 / 读真实 API key，不装 LLM SDK，不联网。
- 不改高风险转人工逻辑；不让 LLM 处理高风险或无依据场景。
- 不把 mock / 未实现写成"已启用"或"真实调用"。
- 不引入新依赖、Docker 镜像或外部 SaaS。
- 不改飞书 / PG / 前端（本增量纯后端回答链路）。

## 完成记录

- 2026-07-12：已实现 LLM Sandbox 适配器骨架（mock-first）。
- 新增 `backend/app/adapters/llm_adapter.py`：`ZYCS_LLM_MODE` 三态（disabled 默认 / mock / sandbox）；`generate_llm_answer` 对证据型回答做确定性模板改写，强制透传 `source_ref` / evidence；sandbox 缺 provider/key 或本增量未实现真实调用时安全降级 mock 并带 `fallback_reason`；key 不进结果 / 日志。
- 接入 `message_policy_service.decide_message_response`（新增 `_maybe_llm_rewrite`）：证据型回答（mock_business / knowledge / rule）改写为 `answer_type=llm_sandbox`；高风险 handoff 在入口短路、无依据 gap 不进入 LLM。`MessageDecision` / `MessageResponseData` 各加可选 `llm` 字段。
- 测试：新增 `tests/api/test_llm_adapter.py`（8 用例：模式校验 / mock 改写 / sandbox 降级 / key 不泄露）；`tests/api/test_conversations.py` 加 `llm_sandbox` 端到端用例；`tests/scenarios/test_risk_fallback.py` 加「高风险覆盖 LLM」（RISK-P2-007）与「gap 不改写」回归。
- 验证：默认 disabled 全量 67 passed / 6 skipped；新增 11 用例通过。
- 文档回写：`docs/09-verification.md` §10.24（TC-062）、`docs/08-dev-plan.md` §6 进度行、`docs/07-api-spec.md` API-002（`llm` 字段 + `llm_sandbox` 示例）。
- 边界：不接真实 LLM、不写 / 读 key、不联网、不引依赖；真实调用仍受 RG-003 阻塞。
