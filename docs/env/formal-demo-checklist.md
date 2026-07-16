# 正式演示当天 5 分钟检查清单

> 适用范围：正式对外演示前的本机 Demo 快速检查。本文只服务 Demo Sandbox 演示，不代表生产环境、真实业务系统或真实 LLM 已启用。

## 1. 演示边界口径

演示开始前先确认并对外说明：

- 当前是本机 `Demo Sandbox`，使用标准模拟业务数据和 Mock / Sandbox 口径。
- 不接真实 CRM / ERP / OA / 工单系统。
- 不处理真实客户隐私、合同、订单、报价、联系方式或生产会话。
- 真实 LLM 自动答复未启用；Console 会展示 `LLM 默认关闭` / `真实系统未接入` 标识。
- 若客户问“什么时候接真实系统”，回答：需要客户授权、接口说明、沙箱账号、字段映射、安全评审和单独 Phase3 评估。

## 2. 启动前检查

| 检查项 | 通过标准 |
|---|---|
| 电脑网络 | 电脑连接演示 Wi-Fi / 局域网。 |
| 手机网络 | 手机与电脑在同一 Wi-Fi / 局域网。 |
| 端口 | `8021` / `5195` / `5196` 未被其他服务占用；如占用，关闭旧窗口或换端口。 |
| 浏览器 | 电脑浏览器可访问本机地址；手机浏览器可访问局域网地址。 |
| 敏感信息 | 不打开真实客户资料、真实订单、真实合同、真实凭据或真实系统后台。 |

## 3. 启动命令

默认演示端口：

```powershell
cd "D:/2-Project/0-Product/4-DigitalCustomerService/zhiyan-digital-cs-platform"
powershell -ExecutionPolicy Bypass -File scripts/start-local-demo.ps1 -BackendPort 8021 -H5Port 5195 -ConsolePort 5196
```

启动脚本输出后，以脚本实际输出的 URL 为准；不要复述过期端口。

## 4. 健康检查

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check-local-demo.ps1 -BackendPort 8021 -H5Port 5195 -ConsolePort 5196
```

通过标准：输出 `6 / 6 reachable`，覆盖：

- Backend health
- Backend docs
- H5 customer page
- Web console
- H5 proxy API
- Console proxy API

若失败：先看端口占用、前端 identity marker、前端代理目标和启动窗口日志；不要继续演示。

## 5. 演示入口

| 入口 | 默认地址 |
|---|---|
| H5 客户页（电脑） | `http://127.0.0.1:5195` |
| H5 客户页（手机） | 以启动脚本输出的 `H5 phone scan` 为准，通常为 `http://<电脑局域网IP>:5195` |
| H5 二维码 | `.ai/local-demo-h5-qr.svg` |
| Web Console | `http://127.0.0.1:5196` |
| 后端 API 文档 | `http://127.0.0.1:8021/docs` |

## 6. 手机扫码复核

正式演示当天必须做一次：

1. 手机扫码或打开启动脚本输出的 H5 局域网地址。
2. 确认手机 H5 页面可打开。
3. 用手机发送一个问题并确认收到回答。
4. 在电脑 Console 确认能看到联动数据。

若手机打不开：检查同 Wi-Fi、电脑局域网 IP、Windows 防火墙、H5 是否以 `--host 0.0.0.0` 启动。

## 7. 推荐演示问题

| 场景 | 场景包 | 示例问题 | 预期结果 |
|---|---|---|---|
| 产品知识 | 产品型客户场景包 | `灯带有什么规格？` | 返回知识回答，带来源依据。 |
| 标准 Demo 订单 | 产品型客户场景包 | `我想查一下 DEMO-ORDER-202607-001 的生产进度` | 返回标准 Demo Sandbox Mock 订单进度。 |
| 项目进度 | 项目型客户场景包 | `DEMO-PROJ-202607-001 到哪个阶段了？` | 返回标准 Demo Sandbox Mock 项目进度。 |
| 高风险转人工 | 任一场景包 | `我要投诉并索赔十万元` | 不承诺处理结果，转人工。 |
| 知识缺口 | 任一场景包 | `你们能不能安排火星基地施工？` | 不编造，生成知识缺口。 |

## 8. Console 必看点

- 顶部应显示 `Demo Sandbox`、`Mock 数据`、`真实系统未接入`、`LLM 默认关闭`。
- Mock 数据列表应显示 `environment`、`source_system`、`source_ref`。
- 右侧详情栏应显示“演示证据摘要”，再展示原始 JSON。
- 待跟进、知识缺口、通知、日报摘要都属于 Demo / Mock 运营数据。
- 角色切换是 Demo 级权限演示，不是生产账号体系。
- **（M11 新增）虚拟客户资料**：切到产品型 / 项目型场景包，应能看到该虚拟客户的完整画像（公司背景、产品目录 / FAQ、订单 / 项目 / 售后、历史会话），全程标识为模拟数据。
- **（M11 新增）来源标识全链路**：Console「来源标识抽样（API-016）」专区应列出知识 / 规则 / Mock 业务 / Demo Dataset 来源，全部 `demo_sandbox` / `mock=true`；H5 回复气泡底部应有「来源模式：Demo Sandbox」+「来源：{source_ref}」徽章。
- **（M11 新增）数据源模式门禁**：顶部 banner 显示 `Demo Sandbox`；admin 试切真实模式应回显 `Not configured / No-Go` + 门禁原因（不偷偷接真实数据）。
- **（M11 新增）一键重置**：Console sandbox 区「重置演示运行态」按钮（admin）可重置当前场景包运行态，演示前 / 后使用，只影响当前场景包。

## 9. 收尾检查

演示结束后关闭 3 个服务窗口，或在各窗口按 `Ctrl+C`。

可选检查端口是否释放：

```powershell
powershell -Command "foreach($port in 8021,5195,5196){ $count=@(Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue).Count; \"port $port listeners=$count\" }"
```

通过标准：`8021` / `5195` / `5196` 均无监听，避免影响下一次演示或开发。

## 10. 参考记录

- 本机 Demo runbook：`docs/env/local-demo-runbook.md`
- 对外演示脚本：`docs/env/external-demo-script.md`
- 正式演示前彩排记录：`docs/research/2026-07-13-formal-demo-rehearsal.md`
- Console 演示标识任务：`tasks/task-010d-console-demo-badges.md`
- Phase2 / Demo Sandbox 验收记录：`docs/09-verification.md` §10.21~10.27
- Product Sandbox（M11）验收记录：`docs/09-verification.md` §10.28
- task-011e 端到端彩排记录：`docs/research/2026-07-16-task-011e-product-sandbox-rehearsal.md`
