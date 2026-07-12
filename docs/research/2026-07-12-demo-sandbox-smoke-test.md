# Demo Sandbox 演示可用性 Smoke Test（2026-07-12）

## 0. 文档元信息

| 字段 | 内容 |
|---|---|
| 日期 | 2026-07-12 |
| 类型 | Demo Sandbox 演示可用性收口记录 |
| 范围 | 本机三端启动、端口 / 身份误判防护、标准 Demo Sandbox 数据包、H5 主链路 API 场景 |
| 依据 | `docs/env/local-demo-runbook.md`、`docs/env/external-demo-script.md`、`docs/09-verification.md` §10.22 |
| 边界 | 不接真实 CRM / ERP / OA / 工单系统；不处理真实客户数据；不启用真实 LLM；不提交 `.ai/local-demo-h5-qr.svg` |

## 1. 执行命令

| 步骤 | 命令 / 动作 | 结果 |
|---|---|---|
| 初始检查 | `powershell -ExecutionPolicy Bypass -File scripts/check-local-demo.ps1` | 发现 5173 返回 200 但不是本项目 H5（lumen 知识库测试页占用），旧版检查存在误判风险 |
| 防误判修复 | 为 H5 / Console 增加 `zycs-demo-app` identity marker；`check-local-demo.ps1` 校验 marker；`start-local-demo.ps1` 增加端口占用预检、Vite `--strictPort` 和 `.ai/local-demo-runtime.json` | 已实现 |
| 端口预检复测 | `powershell -ExecutionPolicy Bypass -File scripts/start-local-demo.ps1` | 默认端口已有服务时启动失败，提示对应端口已占用；避免继续打开新窗口造成误判 |
| 误判复测 | `powershell -ExecutionPolicy Bypass -File scripts/check-local-demo.ps1` | 默认端口检查失败：H5 5173 HTTP 200 但缺少 `customer-h5` marker，脚本提示可能被其他本地应用占用 |
| 备用端口启动 | `powershell -ExecutionPolicy Bypass -File scripts/start-local-demo.ps1 -BackendPort 8001 -H5Port 5175 -ConsolePort 5176` | 已打开后端、H5、Console 三个本地服务窗口；生成 `.ai/local-demo-h5-qr.svg` 与 `.ai/local-demo-runtime.json` |
| 健康检查 | `powershell -ExecutionPolicy Bypass -File scripts/check-local-demo.ps1 -BackendPort 8001 -H5Port 5175 -ConsolePort 5176` | 4 / 4 reachable：Backend health、Backend docs、H5、Console 均 200 且 identity marker 通过 |
| 聚焦测试 | `$env:PYTHONPATH='backend'; python -m pytest tests/api/test_mock_business.py tests/api/test_conversations.py tests/api/test_scenario_packs.py` | 16 passed；有 2 条非阻塞 warning（StarletteDeprecationWarning、pytest cache path warning） |
| 本地 HTTP smoke | `Invoke-RestMethod` 调用 `http://127.0.0.1:8001` 的 `/health`、API-007、创建会话、发送 H5 消息、场景包详情 | 全部通过；返回 `demo_sandbox`、`mock_business`、`source_ref` 等预期字段 |

## 2. 三端可访问性

| 入口 | 结果 | 说明 |
|---|---|---|
| Backend health | 通过 | `http://127.0.0.1:8001/health` 返回 200，`status=ok` |
| Backend docs | 通过 | `http://127.0.0.1:8001/docs` 返回 200 |
| H5 客户页 | 通过 | `http://127.0.0.1:5175` 返回 200，且 HTML 包含 `name="zycs-demo-app" content="customer-h5"` |
| Web Console | 通过 | `http://127.0.0.1:5176` 返回 200，且 HTML 包含 `name="zycs-demo-app" content="console"` |
| 手机扫码 | 待人工复核 | 启动脚本已生成 `.ai/local-demo-h5-qr.svg`；手机需与电脑同 Wi-Fi / LAN，未在本轮自动验证手机端 |

## 3. 标准 Demo Sandbox 数据验证

| 项目 | 结果 |
|---|---|
| 标准订单编号 | `DEMO-ORDER-202607-001` |
| API | `/api/v1/mock-business/order/DEMO-ORDER-202607-001` |
| 关键字段 | `environment=demo_sandbox`、`source_ref=demo_erp:order:DEMO-ORDER-202607-001`、`payload.schema_version=demo_sandbox.v1` |
| 边界 | `mock=true`，不调用真实业务系统 |

## 4. H5 主链路场景验证

| 场景 | 输入 | 结果 | 关键字段 |
|---|---|---|---|
| 产品知识 | `灯带有什么规格？` | 通过 | `answer_type=knowledge`、`source_ref=SRC-SP-PRODUCT-001` |
| 标准进度查询 | `我想查一下 DEMO-ORDER-202607-001 的生产进度` | 通过 | `answer_type=mock_business`、`intent=order_progress`、`source_ref=demo_erp:order:DEMO-ORDER-202607-001` |
| 高风险转人工 | `如果客户投诉并要求赔偿，你们能保证赔多少钱？` | 通过 | `answer_type=handoff`、`source_ref=rule:high_risk_handoff`、`handoff=true` |
| 未知问题缺口 | `请说明火星基地联调验收流程` | 通过 | `answer_type=gap`、`source_ref=policy:knowledge_gap`、`knowledge_gap=true` |

## 5. 结论

- Demo Sandbox 本机三端可启动并可访问。
- 旧版“仅检查 HTTP 200”的方式会把其他本地页面误判为 H5；本轮已补端口预检、strict port、identity marker 与 runtime 状态文件，并用默认端口被占用场景验证启动脚本 / 检查脚本会失败告警。
- 标准 Demo Sandbox 模拟数据包可通过 API 与 H5 主链路触发。
- 演示脚本已改用标准 `DEMO-*` 编号，降低旧 `HC-*` / `XS-*` 编号与新 Demo Sandbox 口径混用风险。
- 本轮 smoke test 不等于生产验收；真实系统、生产飞书、真实客户数据和生产 LLM 自动答复仍为 No-Go。

## 6. 后续建议

| ID | 建议 | 优先级 | 说明 |
|---|---|---|---|
| DEMO-C-001 | 人工用手机扫描 `.ai/local-demo-h5-qr.svg` 复核移动端访问 | P1 | 自动脚本无法替代真实手机网络 / 防火墙验证 |
| DEMO-C-002 | 若要对客户演示，先按 `docs/env/external-demo-script.md` 做一次人工彩排 | P1 | 确认话术、Mock 标识和边界说明都能讲清楚 |
| DEMO-C-003 | LLM Sandbox 适配器另开任务 | P2 | 必须限定模拟数据 + 证据约束，不接真实 key / 真实客户数据 |
| DEMO-C-004 | 将 demo 端口 / identity marker 检查机制回流模板 | P2 | 已起草 `_proposals/TEMPLATE-UPGRADE-demo-port-identity-check.md`，避免其他派生项目复现误判 |
