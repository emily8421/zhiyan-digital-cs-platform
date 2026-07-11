# 2026-07-11 LLM 专项技术环境评估（RG-003）

## 0. 文档元信息

| 项 | 内容 |
|---|---|
| 评估对象 | LLM 专项评估（RG-003） |
| 当前状态 | Conditional Go：评估完成，RG-003 可从「待评估」推进；LLM 默认仍关闭，真实接入后置 |
| 最后更新 | 2026-07-11 |
| 当前 Phase | Phase2：MVP 试点 |
| 上游输入 | `docs/05-tech-spec.md`、`docs/08-dev-plan.md`、`docs/09-verification.md`、`docs/design/knowledge-and-policy.md`、`docs/decisions/ADR-0004-no-fabrication-and-human-handoff.md`、`docs/env/local-env.md` |
| 下游影响 | `docs/05-tech-spec.md`（RG-003 / RISK-P2-003 / §3.1 LLM 行 / DOC-C-005 / 新增 RISK-P2-007~010）、`docs/08-dev-plan.md`（Sprint-9）、`docs/09-verification.md`（§10.2 + TC-047~049）、`docs/design/knowledge-and-policy.md`（KP-C-001） |

## 1. 评估结论

| Gate | 结论 | 可进入范围 | 不可进入范围 | 下一步 |
|---|---|---|---|---|
| RG-003 | Conditional Go（评估完成） | Sprint-9 的 LLM 评估交付物（本报告）+ 知识运营强化；任何不触发真实 LLM 调用的工作 | LLM 自动答复默认启用；接真实 LLM API；提交 API key；发送真实客户隐私给 LLM | 真实启用需另拆授权任务（Phase3 或单独安全评审），先解 DOC-C-005 + 不编造 / 成本 / 兜底 / 隐私四条硬约束 |

结论说明：RG-003 的进入标准是「证据约束 / 不编造 / 成本 / 兜底**评估完成**」。本次评估已完成这四项的边界盘点（见 §4 / §8），因此 RG-003 可从「待评估」推进到 **Conditional Go**。但「评估完成」不等于「LLM 可启用」——`ai/project-rules.md` §1 / §2 与 DOC-C-005 明确 Phase2 仅评估、不默认启用；真实接入仍受 Phase 边界、安全评审和成本授权三重约束。当前「规则 / 关键词匹配 + 高风险转人工 + 知识缺口」降级链路已验证可用（Phase1 已实现），LLM 不接入不阻塞 Sprint-9 知识运营强化推进。

## 2. 评估范围与依据

- 规范依据：`ai/prompts/review/20-tech-env-evaluation.md`；`ai/document-lifecycle-rules.md` §2 / §5.4；`ai/implementation-lifecycle-rules.md` §3 / §5；`ai/project-rules.md` §1 / §2 / §6。
- 项目事实依据：`docs/05-tech-spec.md` §1 / §3.1 / §9 / §11.2 / §13 / §14；`docs/08-dev-plan.md` Sprint-9；`docs/09-verification.md` §10.2 / §10.3；`docs/design/knowledge-and-policy.md`（KP-C-001~004、候选能力表）；`docs/decisions/ADR-0004-no-fabrication-and-human-handoff.md`；`docs/env/local-env.md`。
- 未读取 / 不适用：未联网核实具体 LLM 厂商定价 / 模型版本（属于「若未来启用」的待验证项，且 `ai/project-rules.md` 限定联网仅限依赖安装）；未执行任何安装 / 导入 / 最小运行（本次禁止接真实 API）。

## 3. 本机 / 团队环境事实

摘要引用 `docs/env/local-env.md`（采集 2026-07-03，环境采集 ≠ 评估通过）：

- Windows 10 / PowerShell 5.1，约 31.73 GB 内存，Python 3.14.3，Node.js 22.17.1。
- 未检测到 GPU；`ai/project-rules.md` §2.5 禁止本机运行本地大模型推理、模型训练、生产规模向量索引。
- 联网默认不允许；真实外部 API / SaaS / LLM 调用需另行确认。
- Docker 已安装（`docs/05-tech-spec.md` §13 RISK-P2-001 记录 Docker Desktop 4.76.0 已可用；local-env 旧采集仍标「不可用」，以 05 为准）。

## 4. LLM 路线候选与决策

| 候选 | 方案 | 评估 | 决策 |
|---|---|---|---|
| A | 不启用 LLM，保持规则 / 关键词匹配 + 高风险转人工 + 知识缺口 | 现状，Phase1 已实现并验证；满足 ADR-0004 不编造 | 当前采用（Phase2 保持） |
| B | 受控外部 LLM API（RAG + 证据约束 + 不编造 + 成本上限 + 兜底） | 技术可行，但需解四条硬约束（见 §8）+ 安全评审 + 成本授权 | 候选，Phase3 或单独授权任务后再评估启用；未来 LLM 启用走此路线 |
| C | 本地小模型 CPU 推理（ollama + 量化小模型） | 技术可行（CPU 可跑 0.5B~3B 量化模型，本机内存充足），但能力弱易误导判断、引大依赖、违反 §2.5 | 不采用（用户决策 2026-07-11：未来 LLM 启用走外部 API；当前若需验证骨架优先用 Mock LLM） |

与向量检索 / Embedding 的关系：Embedding / 向量检索由 `docs/05-tech-spec.md` RISK-P2-005 / 006 和 `docs/design/knowledge-and-policy.md` KP-C-002 单独跟踪，默认关闭。若未来走候选 B（RAG），Embedding 方案需同步确定（RISK-P2-006 解锁），但本次不混淆两件事。

## 5. 依赖与工具支撑矩阵

| 名称 | 目标版本 / 方案 | 环境要求 | 启用阶段 | 当前状态 | 配置来源 | 密钥 / 敏感性 | 验证方式 | 风险 |
|---|---|---|---|---|---|---|---|---|
| LLM adapter | 待定（OpenAI 兼容协议或国内厂商 SDK） | 联网 + API key | Phase3 / 授权后 | 未引入，默认关闭 | `.env.local`（待） | API key（secret） | 未来启用前另做导入 / 最小调用验证 | 厂商锁定、版本漂移、限流 |
| LLM 配置开关 | `ZYCS_LLM_MODE` = `disabled` / `mock` / `sandbox`（建议三态，对齐飞书 RG-001 模式） | 非密钥 | Phase2 评估 | 建议草案 | `.env.local` / 环境变量 | 非密钥 | 配置校验 + 缺配置降级 | 误启用 |
| 成本 / 限流配置 | 预算上限、RPM / TPM、超时秒 | 非密钥 | Phase3 / 授权后 | 待定 | `.env.local` | 非密钥 | 未来启用前验证 | 成本失控 |
| 审计日志 | LLM 调用记录（模型 / 耗时 / 成本 / 是否命中证据，脱敏） | 非密钥 | Phase3 / 授权后 | `zycs_audit_logs` 已设计未启用 | DB | 需脱敏 prompt 摘要 | 未来启用前验证 | 隐私泄露 |

## 6. 安装 / 导入 / 最小运行验证

本次不执行任何实机验证（禁止接真实 LLM API、不装依赖、不写 key）。以下为「若未来启用候选 B」时的待验证命令清单，不在本轮执行：

- 安装 LLM SDK（需先人工确认包名 / 用途 / 影响，`ai/project-rules.md` §6）。
- 配置 `ZYCS_LLM_MODE=sandbox` + API key（仅本机 `.env.local`，不提交）后最小调用。
- 验证证据回溯：LLM 回答必须挂 `source_ref`，无证据转人工 / 缺口。
- 验证降级：超时 / 限流 / 失败时回退规则匹配，不阻塞主链路。

骨架验证优先用 Mock LLM（见 §8），不真跑本地小模型。

## 7. 资源、网络、权限与成本验证

| 维度 | 本次结论 |
|---|---|
| 联网 | 需外网访问 LLM API；Phase2 默认不允许，需另行确认 |
| 代理 / 权限 | 可能需代理或内网中转；API key 需管理员权限管理 |
| GPU / 大内存 | 候选 C 需 GPU → 不采用；候选 B 走外部 API，不占本机 GPU |
| 成本 | 按 token 计费，需预算上限 + 告警 + 缓存；Phase2 不纳入成本 |
| 数据驻留 / 合规 | 云端 LLM 涉及数据出境合规，需安全评审 |

## 8. 风险项与降级策略

| Risk-ID | 优先级 | 风险 | 触发条件 | 影响 | 当前状态 | 建议降级 / Mock / 服务器预案 | 对应用例 / Sprint | 解锁条件 |
|---|---|---|---|---|---|---|---|---|
| RISK-P2-003 | P1 | LLM 不编造 / 成本 / 兜底边界未评估 | Sprint-9 LLM 评估 | 阻塞 LLM 启用决策 | 已评估（2026-07-11）→ Conditional Go；启用仍阻塞 | 规则 / 关键词匹配 + 转人工 / 缺口（已实现） | Sprint-9 / RG-003 | 评估完成（已满足）；真实启用另需 DOC-C-005 解锁 + Phase 升级 + 安全评审 |
| RISK-P2-007 | P1 | LLM 幻觉承诺（价格 / 合同 / 赔付 / 交期） | LLM 启用后绕过高风险规则 | 业务承诺风险 | 候选，未启用 | 高风险关键词强制转人工，LLM 不得覆盖；温度调低 + system prompt 约束 | Phase3 LLM 启用前 | ADR-0004 在 LLM 链路强制执行 + 测试覆盖 |
| RISK-P2-008 | P1 | LLM 成本失控 | 无预算上限 / 缓存 | 费用超支 | 候选，未启用 | 预算上限 + 告警 + 缓存 + 限流 | Phase3 LLM 启用前 | 成本授权 + 预算配置 |
| RISK-P2-009 | P1 | 客户隐私泄露给 LLM | 真实隐私 / 订单 / 合同入 prompt | 合规风险 | 候选，未启用 | PII 脱敏 + 不发送真实隐私 / 合同 / 订单 / 联系方式 | Phase3 LLM 启用前 | 隐私脱敏 + 安全评审 |
| RISK-P2-010 | P2 | LLM 超时 / 限流致主链路阻塞 | API 延迟或限流 | 体验下降 | 候选，未启用 | 超时降级回规则匹配 / 转人工，不阻塞 | Phase3 LLM 启用前 | 超时配置 + 降级测试 |

骨架验证策略：未来验证 LLM adapter / 证据回溯 / 兜底降级等骨架时，优先用 Mock LLM（按预设规则模拟 LLM 响应，零依赖、不违反 `ai/project-rules.md` §2.5 / §5.2、不引大模型文件），不真跑本地小模型。本地小模型 CPU 推理虽技术可行，但不作为启用路线（见 §4 候选 C 决策）。

## 9. Readiness Gate

| Gate | 进入标准 | 必需证据 | 状态 | 阻塞项 / 下一步 |
|---|---|---|---|---|
| RG-003 | 证据约束 / 不编造 / 成本 / 兜底评估完成 | LLM 专项评估报告（本文件） | Conditional Go（2026-07-11，评估完成） | 评估完成可推进；LLM 真实启用仍阻塞，需 DOC-C-005 解锁 + Phase 升级 + 安全评审 + 成本授权 |

回填关系：RG-003 Conditional Go → `docs/05-tech-spec.md` §14 RG-003 行状态 + §13 RISK-P2-003 状态 + 新增 RISK-P2-007~010；`docs/09-verification.md` §10.2 RG-003 行状态 + 新增 TC-047~049（评估类用例，非实发）；`docs/08-dev-plan.md` Sprint-9 进度记录。

## 10. Go / Conditional Go / No-Go 结论

Conditional Go。

- 可进入范围：Sprint-9 的 LLM 评估交付物（本报告）+ 知识运营强化（缺口流转 / 审核）；任何不触发真实 LLM 调用的工作。
- 必须满足的条件：LLM 默认保持 `disabled`；不接真实 LLM API、不写真实 key、不发送真实客户隐私；评估结论不写成「已启用」。
- 不可进入范围：LLM 自动答复启用、真实 LLM API 接入、API key 提交入库。
- 若 No-Go 触发：本次无 No-Go 项（候选 C 本地小模型不采用，非 No-Go；候选 B 后置，非 No-Go）。

## 11. 对 docs/05、docs/09、docs/08 和依赖文件的修改建议

本报告落盘时同步回写以下内容（用户确认 2026-07-11）：

| 文件 | 章节 | 修改内容 |
|---|---|---|
| `docs/05-tech-spec.md` | §0 当前状态 | 补 RG-003 Conditional Go（2026-07-11） |
| `docs/05-tech-spec.md` | §3.1 LLM 行 | 当前状态更新为「Phase2 评估完成（Conditional Go），默认关闭」；验证方式补本报告路径 |
| `docs/05-tech-spec.md` | §13 RISK-P2-003 | 状态从「待评估」→「已评估（Conditional Go），启用仍阻塞」；解锁条件细化 |
| `docs/05-tech-spec.md` | §13 | 新增 RISK-P2-007~010（LLM 启用前专项风险，状态 = 候选 / 未启用） |
| `docs/05-tech-spec.md` | §14 RG-003 | 状态「待评估」→「Conditional Go（2026-07-11，评估完成）」；阻塞项更新 |
| `docs/05-tech-spec.md` | §11.2 DOC-C-005 | 取舍影响更新为「已评估（Conditional Go），启用仍条件阻塞」 |
| `docs/09-verification.md` | §10.2 RG-003 | 状态「待评估（Sprint-9）」→「Conditional Go（2026-07-11）」；证据补本报告路径 |
| `docs/09-verification.md` | §10 新增 §10.13 | 新增 TC-047~TC-049（LLM 评估类：评估完成 / 默认关闭 / 边界已定义），结果 = 通过（评估类，非实发） |
| `docs/08-dev-plan.md` | Sprint-9 | 状态从「草案，待细化（DOC-C-005）」→「LLM 评估部分已完成（Conditional Go），知识运营强化待细化」 |
| `docs/08-dev-plan.md` | §6 进度记录 | 新增 2026-07-11 RG-003 LLM 评估完成行 |
| `docs/design/knowledge-and-policy.md` | KP-C-001 | 取舍影响补「Phase2 评估完成（Conditional Go），启用仍阻塞」 |

## 12. 待人工确认项

| ID | 待确认项 | AI 建议 | 建议依据 | 备选方案 | 取舍影响 / 阻塞关系 |
|---|---|---|---|---|---|
| LLM-C-001 | RG-003 是否推进到 Conditional Go（评估完成） | 推进 | 评估已完成四项边界盘点 | 维持「待评估」 | 不阻塞 Sprint-9 知识运营强化；推进后 RG-003 gate 闭环 |
| LLM-C-002 | 新增 RISK-P2-007~010（LLM 启用前专项风险） | 新增，状态标「候选 / 未启用」 | 避免启用时才补风险 | 暂不新增，启用时再评 | 不阻塞当前；新增可让未来启用有明确门槛 |
| LLM-C-003 | 新增 TC-047~049（评估类用例） | 新增，结果 = 通过（评估类非实发） | 09 需有 RG-003 评估证据 TC | 仅在报告留痕，不进 09 | 不阻塞；进 09 可让 gate 证据可追溯 |
| LLM-C-004 | LLM 配置开关命名 `ZYCS_LLM_MODE` 三态 | 采用三态（disabled / mock / sandbox），对齐飞书 RG-001 模式 | 项目已有三态模式惯例 | 二态或延后定 | 不阻塞当前；启用前需定 |
| LLM-C-005 | LLM 真实启用时点 | Phase3 或单独授权任务后 | DOC-C-005 Phase2 仅评估 | Phase2 末尾试点 | 阻塞 LLM 上线，不阻塞 Sprint-9 |
| LLM-C-006 | 本地小模型是否作为启用路线 | 不采用；未来走外部 LLM API | 用户决策 2026-07-11；能力弱易误导、引大依赖、违反 §2.5 | 真跑小模型验证 | 不阻塞当前；骨架验证优先 Mock LLM |

## 13. 报告落盘

- 路径：`docs/research/2026-07-11-tech-env-evaluation-llm.md`（本文件）。
- 本文件不含真实 API key、客户隐私、订单 / 合同数据。
- 本文件不替代 `docs/05-tech-spec.md`、`docs/08-dev-plan.md`、`docs/09-verification.md`；这些文档仅记录 gate 状态与追溯。
