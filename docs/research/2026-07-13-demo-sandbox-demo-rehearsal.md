# Demo Sandbox 对外演示彩排记录

> 定位：本文件记录 Demo Sandbox 对外演示前的本机彩排证据，补充 `docs/env/local-demo-runbook.md`、`docs/env/external-demo-script.md` 与 `docs/09-verification.md`。本记录不代表生产环境、真实业务系统或真实 LLM 已启用。

## 1. 彩排信息

| 项 | 内容 |
|---|---|
| 日期 | 2026-07-13 |
| 任务 | `task-010c-demo-sandbox-demo-rehearsal` |
| 彩排范围 | Backend `8021`、H5 `5195`、Console `5196`、标准 Demo Sandbox 数据、四类主路径问题 |
| 依据 | `docs/env/external-demo-script.md`、`docs/research/2026-07-11-demo-sandbox-readiness-evaluation.md`、`tasks/task-010a-demo-sandbox-standard-mock-data.md`、`tasks/task-010b-llm-sandbox-adapter-mock.md` |
| 移动端证据 | `docs/research/2026-07-13-demo-manual-acceptance.md` |
| 结论 | 通过；可作为对外演示前本机彩排证据 |

## 2. 启动与健康检查

| 项 | 命令 / 结果 |
|---|---|
| 启动命令 | `powershell -ExecutionPolicy Bypass -File scripts/start-local-demo.ps1 -BackendPort 8021 -H5Port 5195 -ConsolePort 5196` |
| 运行说明 | CLI sandbox 内前端 Vite 曾因 `spawn EPERM` 无法启动；按授权在 sandbox 外重跑官方启动脚本后成功。 |
| H5 手机地址 | `http://192.168.8.196:5195` |
| H5 二维码 | `.ai/local-demo-h5-qr.svg`（本地运行产物，不提交） |
| 检查命令 | `powershell -ExecutionPolicy Bypass -File scripts/check-local-demo.ps1 -BackendPort 8021 -H5Port 5195 -ConsolePort 5196` |
| 检查结果 | 通过，`6 / 6 reachable`：Backend health、Backend docs、H5、Console、H5 proxy API、Console proxy API 均 200。 |

## 3. 聚焦回归

| 项 | 内容 |
|---|---|
| 命令 | `$env:PYTHONPATH='backend'; python -m pytest -p no:cacheprovider tests/api/test_mock_business.py tests/api/test_conversations.py tests/api/test_scenario_packs.py` |
| 结果 | 通过，`17 passed, 1 warning`。 |
| 说明 | 初次直接运行 `pytest` 时本机 PATH 不含 `pytest`；改用 `python -m pytest` 后需补 `PYTHONPATH=backend`，最终命令如上。禁用 cacheprovider 是为了避免 `.pytest_cache` 权限噪声。 |

## 4. HTTP 演示主路径抽样

| 场景 | 场景包 | 示例问题 | 结果摘要 |
|---|---|---|---|
| 产品知识 | `product_business` | `灯带有什么规格？` | `answer_type=knowledge`，`source_ref=SRC-SP-PRODUCT-001`，未转人工、未建缺口。 |
| 标准 Demo 订单进度 | `product_business` | `我想查一下 DEMO-ORDER-202607-001 的生产进度` | `answer_type=mock_business`，`source_ref=demo_erp:order:DEMO-ORDER-202607-001`，未转人工、未建缺口。 |
| 高风险投诉 | `product_business` | `我要投诉并索赔十万元` | `answer_type=handoff`，`source_ref=rule:high_risk_handoff`，触发转人工。 |
| 未知问题缺口 | `project_business` | `你们能不能安排火星基地施工？` | `answer_type=gap`，`source_ref=policy:knowledge_gap`，创建知识缺口。 |

## 5. 手机与 Console 联动

- 同日人工复核记录见 `docs/research/2026-07-13-demo-manual-acceptance.md`。
- 已确认手机浏览器同 Wi-Fi 可打开 H5、H5 可发送并收到回答、Console 可看到联动数据。
- 若正式演示前电脑 IP、Wi-Fi 或端口变化，需按 `docs/env/local-demo-runbook.md` 重新生成二维码并请用户再次人工复核。

## 6. 清理与端口状态

- 彩排完成后检查目标端口 `8021` / `5195` / `5196`：无监听。
- `.ai/local-demo-h5-qr.svg`、`.ai/local-demo-runtime.json` 和临时日志均为本地运行产物，不纳入正式提交。

## 7. 结论与边界

- 结论：Demo Sandbox 对外演示本机彩排通过，可按 `docs/env/external-demo-script.md` 进行人工讲解和客户演示准备。
- 当前仍为本机 Mock / Sandbox Demo，不接真实 CRM / ERP / OA / 工单系统。
- 不处理真实客户隐私、合同、订单、报价、联系方式或生产会话。
- LLM Sandbox 当前仍是 mock-first / 默认关闭口径；真实 LLM 调用仍受 RG-003、DOC-C-005、安全评审和成本授权约束。
- Phase3 真实集成实施仍为 No-Go；客户 / IT / 安全负责人补齐接口、授权、沙箱账号、字段映射和验收场景前，不进入真实接入。
