# task-010c-demo-sandbox-demo-rehearsal

## 目标

完成 Demo Sandbox 对外演示彩排收口：按现有演示 SOP 启动后端、H5 客户页和 Web 控制台，验证三端可访问、前端代理链路、标准模拟数据、四类演示主路径和移动端 / Console 联动证据，形成对外演示前的最小完成包。

本任务只做演示彩排与验收留痕，不新增产品能力，不接真实业务系统，不启用真实 LLM。

## 输入文档

- `docs/env/local-demo-runbook.md`：本机 Demo 启动、检查、二维码和关闭服务方式。
- `docs/env/external-demo-script.md`：对外演示路径、推荐话术、标准 Demo Sandbox 问题和边界口径。
- `docs/research/2026-07-11-demo-sandbox-readiness-evaluation.md`：Demo Sandbox Conditional Go、标准模拟数据 / 飞书测试群 / LLM Sandbox 边界。
- `tasks/task-010a-demo-sandbox-standard-mock-data.md`：标准模拟业务数据包已完成。
- `tasks/task-010b-llm-sandbox-adapter-mock.md`：LLM Sandbox mock-first 适配器骨架已完成。
- `docs/research/2026-07-13-demo-manual-acceptance.md`：同日手机 H5 与 Console 联动人工复核已通过。
- `docs/08-dev-plan.md`、`docs/09-verification.md`：当前 Phase2 / Demo Sandbox 进度与验证记录。

## 修改范围

- 新增 `docs/research/2026-07-13-demo-sandbox-demo-rehearsal.md`：记录本轮对外演示彩排证据、边界和残留。
- 更新 `docs/08-dev-plan.md`：补充 task-010c 进度摘要与后续口径。
- 更新 `docs/09-verification.md`：新增 TC-063 Demo Sandbox 对外演示彩排验收记录。
- 更新 `.ai/session-handoff.md`：刷新本地续接状态。
- 新增 `ai-records/token-hotspots/2026-07-13-task-010c-demo-rehearsal.md`：记录本轮 token hotspot。

## 验收标准

- 官方启动脚本可启动 Demo 三端，H5 / Console / Backend 使用 `8021` / `5195` / `5196` 端口。
- `scripts/check-local-demo.ps1 -BackendPort 8021 -H5Port 5195 -ConsolePort 5196` 返回 `6 / 6 reachable`。
- 聚焦 API 回归通过：`tests/api/test_mock_business.py`、`tests/api/test_conversations.py`、`tests/api/test_scenario_packs.py`。
- 运行中后端 HTTP 抽样覆盖知识回答、标准 Demo 订单进度、高风险转人工和未知问题缺口四类主路径，结果类型符合边界。
- 手机扫码 / 移动端 H5 / Console 联动有同日人工验收记录可追溯；若网络或 IP 变化，需重新人工复核。
- 验收完成后关闭本轮 Demo 服务，确认目标端口无监听，避免占用。

## 禁止事项

- 不接真实 CRM / ERP / OA / 工单系统，不处理真实客户数据。
- 不启用真实 LLM 自动答复，不读取或写入真实 API key。
- 不把 Mock / Demo / Sandbox 写成生产能力或真实集成已启用。
- 不提交二维码、运行日志、runtime JSON 等本地运行产物。
- 不借演示彩排修改业务逻辑、接口契约或新增功能。

## 完成记录

- 2026-07-13：Demo Sandbox 对外演示彩排完成。
- 启动：`scripts/start-local-demo.ps1 -BackendPort 8021 -H5Port 5195 -ConsolePort 5196`。CLI sandbox 内前端 Vite 曾因 `spawn EPERM` 无法启动；按授权在 sandbox 外重跑官方脚本后启动成功。
- 健康检查：`scripts/check-local-demo.ps1 -BackendPort 8021 -H5Port 5195 -ConsolePort 5196` 通过，`6 / 6 reachable`。
- 聚焦回归：`$env:PYTHONPATH='backend'; python -m pytest -p no:cacheprovider tests/api/test_mock_business.py tests/api/test_conversations.py tests/api/test_scenario_packs.py` 通过，`17 passed, 1 warning`。
- HTTP 抽样：知识回答返回 `answer_type=knowledge` / `SRC-SP-PRODUCT-001`；标准 Demo 订单返回 `answer_type=mock_business` / `demo_erp:order:DEMO-ORDER-202607-001`；高风险投诉返回 `answer_type=handoff`；未知问题返回 `answer_type=gap`。
- 移动端证据：复用同日 `docs/research/2026-07-13-demo-manual-acceptance.md`，手机 H5 打开、发送并收到回答、Console 联动数据均已人工确认通过。
- 清理：验收后目标端口 `8021` / `5195` / `5196` 无监听。
- 文档回写：`docs/research/2026-07-13-demo-sandbox-demo-rehearsal.md`、`docs/08-dev-plan.md`、`docs/09-verification.md` 已补充。
