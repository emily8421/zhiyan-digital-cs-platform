# 正式演示前全链路彩排记录

> 定位：本文件记录正式对外演示前的本机全链路彩排结果，补充 `docs/env/external-demo-script.md`、`docs/research/2026-07-13-demo-sandbox-demo-rehearsal.md` 与 `docs/09-verification.md`。本记录不代表生产环境、真实业务系统或真实 LLM 已启用。

## 1. 彩排信息

| 项 | 内容 |
|---|---|
| 日期 | 2026-07-13 |
| 彩排类型 | 正式演示前全链路彩排 |
| Backend | `http://127.0.0.1:8021` |
| H5 客户页 | `http://127.0.0.1:5195` |
| H5 手机地址 | `http://192.168.8.196:5195` |
| H5 二维码 | `.ai/local-demo-h5-qr.svg`（本地运行产物，不提交） |
| Console | `http://127.0.0.1:5196` |
| 结论 | 通过：电脑端全链路通过；手机 H5 与 Console 联动本轮人工复核通过 |

## 2. 启动与健康检查

| 项 | 命令 / 结果 |
|---|---|
| 启动命令 | `powershell -ExecutionPolicy Bypass -File scripts/start-local-demo.ps1 -BackendPort 8021 -H5Port 5195 -ConsolePort 5196` |
| 启动说明 | Vite 在 CLI sandbox 内已知可能触发 `spawn EPERM`；本轮按授权在 sandbox 外启动官方脚本。 |
| 检查命令 | `powershell -ExecutionPolicy Bypass -File scripts/check-local-demo.ps1 -BackendPort 8021 -H5Port 5195 -ConsolePort 5196` |
| 检查结果 | 通过，`6 / 6 reachable`：Backend health、Backend docs、H5、Console、H5 proxy API、Console proxy API 均 200。 |

## 3. H5 代理主路径抽样

> 本轮通过 H5 代理路径 `http://127.0.0.1:5195/api/v1` 发起会话和消息请求，验证前端代理到后端的主链路。

| 场景 | 场景包 | 示例问题 | 结果摘要 |
|---|---|---|---|
| 产品知识 | `product_business` | `灯带有什么规格？` | `answer_type=knowledge`，`source_ref=SRC-SP-PRODUCT-001`，未转人工、未建缺口。 |
| 标准 Demo 订单进度 | `product_business` | `我想查一下 DEMO-ORDER-202607-001 的生产进度` | `answer_type=mock_business`，`source_ref=demo_erp:order:DEMO-ORDER-202607-001`，未转人工、未建缺口。 |
| 高风险投诉 | `product_business` | `我要投诉并索赔十万元` | `answer_type=handoff`，`source_ref=rule:high_risk_handoff`，触发转人工。 |
| 未知问题缺口 | `project_business` | `你们能不能安排火星基地施工？` | `answer_type=gap`，`source_ref=policy:knowledge_gap`，创建知识缺口。 |

## 4. Console 演示标识检查

- Console 可访问：`http://127.0.0.1:5196`。
- Console 代理 API 可访问：`http://127.0.0.1:5196/api/v1/summaries/daily`。
- Mock 业务数据 API 返回标准 Demo Sandbox 字段：`environment=demo_sandbox`、`source_system`、`source_ref`、`mock=true`。
- 代码与构建依据：task-010d 已完成并推送，Console 顶部包含 `Demo Sandbox`、`真实系统未接入`、`LLM 默认关闭`，详情栏包含“演示证据摘要”；`npm run build` 已通过（见 `docs/09-verification.md` §10.26）。

## 5. 手机扫码复核

- 本轮手机地址：`http://192.168.8.196:5195`。
- 二维码位置：`.ai/local-demo-h5-qr.svg`。
- 当前状态：通过（用户人工反馈：手机 H5 可打开、可发送问题并收到回答，Console 可看到联动数据）。
- 既有证据：同日 `docs/research/2026-07-13-demo-manual-acceptance.md` 已确认手机 H5 可打开、可发送并收到回答、Console 可看到联动数据。
- 建议：正式演示当天或网络 / IP / 端口变化后，应重新扫码确认。

## 6. 边界

- 当前仍为本机 Mock / Demo Sandbox。
- 不接真实 CRM / ERP / OA / 工单系统。
- 不处理真实客户隐私、合同、订单、报价、联系方式或生产会话。
- 不启用真实 LLM 自动答复。
- 真实业务系统、生产飞书、真实客户数据和真实 LLM 自动答复仍需 Phase3 授权、安全评审、接口字段和验收场景。

## 7. 后续处理

1. 本轮正式演示前全链路彩排已通过。
2. 正式演示当天若网络、IP、端口或防火墙状态变化，仍需重新执行手机扫码确认。
