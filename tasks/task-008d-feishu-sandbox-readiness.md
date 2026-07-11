# task-008d-feishu-sandbox-readiness

## 目标

完成 Sprint-8 / RG-001 飞书通知沙箱的启动前评估：明确出站通知凭据清单、配置开关、payload 最小化、错误降级、日志脱敏与回调边界，给出 Go / Conditional Go / No-Go 判断；本任务不真实发送飞书通知、不写真实凭据、不接真实组织数据。

## 输入文档

- `docs/05-tech-spec.md`：RG-001、RISK-P2-002、依赖与配置表。
- `docs/design/mock-integrations.md`：Mock 通知 payload、真实集成升级条件。
- `docs/08-dev-plan.md`：Sprint-8 飞书沙箱联调 + DB 技术验证。
- `docs/09-verification.md`：Phase2 readiness gate 验证项。
- `docs/research/2026-07-09-docs-open-items.md`：DOC-C-003 飞书通知沙箱 / 试点评估。

## 修改范围

- 新增 `docs/research/2026-07-10-tech-env-evaluation-feishu-sandbox.md`：RG-001 技术环境评估与边界清单。
- 更新 `docs/05-tech-spec.md`：RG-001 状态从待评估推进到 Conditional Go。
- 更新 `docs/08-dev-plan.md`：Sprint-8 增加 8D 启动前评估记录。
- 更新 `docs/09-verification.md`：新增 TC-036~039 与 RG-001 验证状态。

## 验收标准

- 明确 `ZYCS_FEISHU_NOTIFY_MODE`、`ZYCS_FEISHU_WEBHOOK_URL`、`ZYCS_FEISHU_WEBHOOK_SECRET` 等出站通知配置边界。
- 明确回调 / 事件订阅不纳入本任务，后续启用前必须补验签 / 解密 / 去重 / 限流 / 脱敏日志。
- 明确默认 Mock、显式 sandbox、失败降级、不提交密钥、不接真实组织数据。
- `docs/05-tech-spec.md`、`docs/08-dev-plan.md`、`docs/09-verification.md` 回写 RG-001 Conditional Go 状态。
- `git diff --check` 通过。

## 禁止事项

- 不写入真实 webhook、token、secret、用户 ID、组织 ID 或生产数据。
- 不联网调用飞书 API，不真实发送消息。
- 不实现真实 Feishu adapter 代码，不新增依赖。
- 不启用事件回调，不暴露公网回调地址。
- 不改变现有 H5 / Console 默认 Mock 演示链路。

## 完成记录

- 2026-07-10：已新增 RG-001 飞书沙箱技术环境评估，结论为 Conditional Go。
- 验证通过：TC-036~TC-038（凭据清单、出站通知边界、回调边界）。
- 验证通过：TC-039 沙箱实发（2026-07-11），用户本机配置沙箱 webhook URL / secret 后触发 API-009，接口返回 `send_status=sent`、`mock=False`、`notify_mode=sandbox`，且飞书测试群收到通知。
- 边界确认：本任务未提交任何密钥，未接真实生产群 / 生产组织数据，未启用事件回调。
