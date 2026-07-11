# 2026-07-10 飞书沙箱通知技术环境评估（RG-001）

## 0. 文档元信息

| 项 | 内容 |
|---|---|
| 评估对象 | 飞书通知沙箱 / 试点评估（RG-001） |
| 当前状态 | Go：出站通知沙箱已通过；事件回调、真实生产群和生产组织数据后置 |
| 最后更新 | 2026-07-11 |
| 当前 Phase | Phase2：MVP 试点 |
| 上游输入 | `docs/05-tech-spec.md`、`docs/design/mock-integrations.md`、`docs/08-dev-plan.md`、`docs/09-verification.md` |
| 下游影响 | `backend/app/adapters/`、`docs/05-tech-spec.md`、`docs/08-dev-plan.md`、`docs/09-verification.md`、`tasks/task-008d-feishu-sandbox-readiness.md` |

## 1. 评估结论

| Gate | 结论 | 可进入范围 | 不可进入范围 | 下一步 |
|---|---|---|---|---|
| RG-001 | Go（出站通知沙箱） | 默认 Mock / 显式 sandbox 的 Feishu 通知适配器骨架；本地配置校验、payload 脱敏、失败降级和测试 | 不接真实生产群 / 生产组织数据；不启用事件回调；不提交任何 token / secret | 后续若要生产化，另行确认生产群、审批、安全审计和回调边界 |

结论说明：当前项目已具备 Mock 通知 payload、控制台通知记录、DB 地基和默认 Mock / 显式 sandbox 的 Feishu 通知适配器。2026-07-11 用户在本机 PowerShell 配置沙箱 webhook URL / secret 后触发 API-009，接口返回 `send_status=sent`、`mock=False`、`notify_mode=sandbox`，且飞书测试群收到通知。因此 RG-001 对“出站通知沙箱”结论为 **Go**。真实生产群、生产组织数据和事件回调仍需另拆任务。

## 2. 当前项目基线

| 能力 | 当前状态 | 依据 |
|---|---|---|
| Mock 通知 payload | 已实现，`send_status=mocked` | `docs/design/mock-integrations.md` |
| 通知记录表 | 已设计并 seed Mock 通知 | `docs/06-db-design.md`、`docker/postgres/init/002_seed.sql` |
| 控制台通知接口 | 已支持 Mock 创建 / 列表 | `docs/07-api-spec.md`、`backend/app/api/console.py` |
| 真实飞书通知 | 未启用 | `docs/05-tech-spec.md` RG-001 |
| 飞书事件回调 | 未设计为当前 Sprint 必需项 | `docs/05-tech-spec.md`、`docs/design/mock-integrations.md` |

## 2.1 官方资料核对（2026-07-10）

| 资料 | 核对结论 | 对本项目影响 |
|---|---|---|
| 飞书自定义机器人使用指南 | 自定义机器人通过 webhook 单向向当前群推送消息，不具备数据访问权限；支持关键词、IP 白名单和签名三类安全设置；签名校验基于时间戳与密钥计算。 | 本项目可优先采用“群自定义机器人 webhook”做出站通知沙箱，不需要在本任务接入组织数据或通讯录权限。 |
| 飞书自定义机器人使用指南 | 自定义机器人有频率与请求体大小限制；官方建议妥善保管 webhook 地址，避免公开泄露。 | 本项目必须保留密钥不提交、payload 最小化、失败降级和限流 / 重试后置策略。 |
| 飞书事件订阅回调文档 | Webhook 模式事件回调需要开发者提供公网可访问地址。 | 本机开发阶段不默认启用事件回调；如后续启用，需先确认公网入口、验签 / 解密、重放防护和关闭时点。 |

官方资料链接：飞书自定义机器人使用指南 `https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot?lang=zh-CN`；飞书事件订阅回调 `https://open.feishu.cn/document/event-subscription-guide/callback-subscription/step-1-choose-a-subscription-mode/send-callbacks-to-developers-server`。

## 3. 凭据与配置边界

### 3.1 最小出站通知凭据

| 配置项 | 用途 | 敏感性 | 存放建议 | 是否本轮需要 |
|---|---|---|---|---|
| `ZYCS_FEISHU_NOTIFY_MODE` | `mock` / `sandbox` / `disabled` 三态开关 | 非密钥 | `.env.local` 或运行环境变量 | 是 |
| `ZYCS_FEISHU_WEBHOOK_URL` | 沙箱群机器人 webhook URL | secret | 仅本机 `.env.local` / CI secret；不得提交 | 真实发送前需要 |
| `ZYCS_FEISHU_WEBHOOK_SECRET` | webhook 签名密钥 | secret | 仅本机 `.env.local` / CI secret；不得提交 | 真实发送前需要 |
| `ZYCS_FEISHU_REQUEST_TIMEOUT_SECONDS` | 出站请求超时 | 非密钥 | 默认配置即可 | 可选 |

### 3.2 回调 / 事件订阅凭据（后置）

| 配置项 | 用途 | 敏感性 | 是否纳入当前 Sprint |
|---|---|---|---|
| `ZYCS_FEISHU_APP_ID` | 应用机器人 / 事件订阅标识 | secret-like | 后置，除非明确要接事件回调 |
| `ZYCS_FEISHU_APP_SECRET` | 应用密钥 | secret | 后置 |
| `ZYCS_FEISHU_VERIFICATION_TOKEN` | 回调校验 | secret | 后置 |
| `ZYCS_FEISHU_ENCRYPT_KEY` | 回调加密解密 | secret | 后置 |
| `ZYCS_FEISHU_CALLBACK_PATH` | 本机 / 沙箱回调路径 | 非密钥 | 后置 |

本轮建议只推进出站通知沙箱；事件回调属于更高风险入口，需另行确认公网回调地址、验签 / 解密、重放防护、幂等和日志脱敏后再进入实现。

## 4. 出站通知边界

| 边界项 | 约束 |
|---|---|
| 默认模式 | `mock`，任何未配置 / 配置错误 / 网络失败均回退为 Mock 记录，不影响 Demo |
| 显式启用 | 只有 `ZYCS_FEISHU_NOTIFY_MODE=sandbox` 且 webhook URL / secret 均存在时才允许真实发送 |
| Payload 最小化 | 仅发送转人工 / 知识缺口摘要、关联 ID、风险等级、Mock 标识；不发送客户联系方式、合同、订单隐私或完整对话原文 |
| 日志 | 不记录 webhook URL、secret、原始敏感 payload；只记录脱敏后的 `event_type`、`related_id`、`send_status` |
| 错误处理 | 超时 / 4xx / 5xx 不阻塞主链路，写入 `failed` 或保持 Mock 降级 |
| 重试 | MVP 默认不自动重试；如需重试，最多 3 次指数退避，并要求幂等键 |
| 幂等 | 建议使用 `event_type + related_id + target_type` 作为本地去重基线 |

## 5. 回调边界

| 边界项 | 当前结论 |
|---|---|
| 是否需要回调 | 不作为本次出站通知沙箱验证前置；真实通知只需出站 webhook |
| 若后续启用 | 必须先定义 challenge 校验、签名 / 加密校验、事件去重、重放防护、限流和脱敏日志 |
| 数据范围 | 只接收沙箱事件，不接真实组织通讯录、用户消息原文或生产会话 |
| 网络入口 | 本机开发不得直接暴露公网；如需公网回调，必须先确认临时隧道 / 服务器、访问控制和关闭时点 |
| 失败处理 | 回调失败不影响 H5 / Console 主链路；事件只用于通知状态回写或审计候选 |

## 6. 验证计划

| TC-ID | 验证项 | 前置 | 通过标准 | 当前结果 |
|---|---|---|---|---|
| TC-036 | RG-001 凭据清单 | 无 | 出站通知与回调凭据分层，密钥不落库不提交 | 通过（2026-07-10） |
| TC-037 | 出站通知边界 | 无 | 默认 Mock；sandbox 需显式开关 + URL + secret；失败回退 | 通过（2026-07-10） |
| TC-038 | 回调边界 | 无 | 回调后置，需验签 / 解密 / 去重 / 限流 / 脱敏后才能启用 | 通过（2026-07-10） |
| TC-039 | 沙箱实发 | 沙箱 webhook 与签名密钥 | 飞书沙箱群收到转人工 / 知识缺口通知，且日志无密钥 | 通过（2026-07-11） |

## 7. Go / No-Go 判断

| 条件 | 结论 |
|---|---|
| 是否可继续设计 Feishu 通知适配器骨架 | 已完成 |
| 是否可默认开启真实发送 | No-Go，默认仍必须 Mock |
| 是否可在无凭据情况下宣称沙箱联调通过 | No-Go；本次通过依赖用户本机沙箱凭据，凭据未入库未提交 |
| 是否可接入事件回调 | No-Go，需另拆任务 |
| 是否可保留 Mock / 降级路径 | 必须保留 |

## 8. 后续任务建议

1. 新增 Feishu 通知适配器骨架：默认 `mock`，显式 `sandbox`，失败降级。
2. 新增配置校验：缺 webhook URL / secret 时返回配置错误并保持 Mock。
3. 新增沙箱实发测试手册：由人工在本机 `.env.local` 设置凭据后执行，不把凭据写入仓库。
4. 若后续要接事件回调，另建 `channel-adapters` / callback 专项任务，不与出站通知混合。

## 9. 报告落盘

- 路径：`docs/research/2026-07-10-tech-env-evaluation-feishu-sandbox.md`（本文件）。
- 本文件不包含真实 webhook、token、secret、用户 ID、组织 ID 或生产数据。
- 本文件不替代 `docs/05-tech-spec.md`、`docs/08-dev-plan.md`、`docs/09-verification.md`；这些文档仅记录 gate 状态与追溯。
