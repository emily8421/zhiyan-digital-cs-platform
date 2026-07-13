# Token Hotspot 观察记录：task-010c Demo Sandbox 演示彩排

> 本文件为 AI 协作观察记录，不替代 `.ai/session-handoff.md`、`docs/08-dev-plan.md` 或 `docs/09-verification.md`。
> 本记录不包含 token、密钥、完整对话、客户敏感数据或隐私事实。

## 元数据

- 日期：2026-07-13
- 任务：执行 `task-010c-demo-sandbox-demo-rehearsal`，完成 Demo Sandbox 对外演示彩排收口。
- 触发原因：从快速续接进入分析 / 写入任务后，按规则完整读取 `ai/index.md` 及其规则清单；随后执行 Demo 启动、验证、正式文档回写和续接刷新。
- 状态：已记录

## Hotspot 来源

1. **快速续接升级为执行任务**
   - 本轮先按快速续接读取 handoff，随后用户确认继续执行推荐方案。
   - 按 `ai/session-rules.md` 要求，进入分析 / 写入任务前必须完整读取规则清单。

2. **规则文件与项目事实文档较长**
   - `ai/document-lifecycle-rules.md`、`docs/08-dev-plan.md`、`docs/09-verification.md` 内容较长。
   - 为避免终端输出截断影响判断，规则文件曾按窗口分段读取；项目文档按 Phase2 / Demo Sandbox 锚点聚焦检索。

3. **Demo 验证跨 sandbox / 本机运行边界**
   - CLI sandbox 内 Vite 启动出现 `spawn EPERM`，需要识别为执行环境限制而非产品功能失败。
   - 经用户确认后，在 sandbox 外运行官方启动脚本，健康检查通过。

4. **验证证据需要压缩归档**
   - 启动脚本、健康检查、聚焦 pytest、HTTP 抽样、手机人工验收记录均可作为证据。
   - 正式记录只保留命令、退出结果、关键通过项和边界，不粘贴完整日志。

## 质量影响

- 正面：完整规则读取确保写入 `tasks/`、`docs/research/`、`08/09` 和 handoff 时不越过 Phase2 / Demo Sandbox 边界。
- 成本：规则补读、文档锚点检索、sandbox 启动失败排查和验证重试增加了上下文与命令轮次。
- 风险：若未识别 Vite `spawn EPERM` 属于 sandbox 限制，可能误判 H5 / Console 不可演示。

## 优化建议

1. **Demo 命令分层**
   - 在后续 runbook 或命令入口中明确：Vite dev server 在受限 sandbox 中可能需要 sandbox 外启动。
   - 健康检查仍可在普通 CLI 中运行，减少提权范围。

2. **验证命令固化**
   - 聚焦 API 测试建议统一写为 `$env:PYTHONPATH='backend'; python -m pytest -p no:cacheprovider ...`，避免 PATH 与 `.pytest_cache` 权限噪声。
   - 对 Demo Sandbox 彩排保留固定四类 HTTP 抽样：知识、标准 Mock 进度、高风险转人工、未知缺口。

3. **长文档读取摘要化**
   - 对已完成 M10 后的后续演示收口任务，优先检索 `TC-060~TC-063`、`task-010*`、`Demo Sandbox`、`external-demo-script` 等锚点。
   - 收尾时只记录关键事实路径和验证命令，避免重复携带完整 `08/09` 内容。

## 本轮关键结果摘要

- 新增任务：`tasks/task-010c-demo-sandbox-demo-rehearsal.md`
- 演示彩排记录：`docs/research/2026-07-13-demo-sandbox-demo-rehearsal.md`
- 健康检查：`scripts/check-local-demo.ps1 -BackendPort 8021 -H5Port 5195 -ConsolePort 5196`，`6 / 6 reachable`
- 聚焦回归：`17 passed, 1 warning`
- HTTP 抽样：知识、标准 Demo 订单、高风险转人工、未知缺口四类主路径符合预期
- 残留边界：真实 CRM / ERP / OA / 工单、生产飞书、真实客户数据和真实 LLM 自动答复仍未解锁。
