# 场景包详细设计

> **定位：详细设计。** 本文细化产品型客户和项目型客户场景包的配置模型。

## 0. 文档元信息

| 项 | 内容 |
|---|---|
| 设计对象 | 产品型 / 项目型客户场景包配置模型 |
| 文档路径 | docs/design/scenario-packs.md |
| 输入来源 | docs/02-srs.md / 03-prd.md / 04-architecture.md / 05-tech-spec.md / 06-db-design.md / 07-api-spec.md / docs/inputs/ |
| 覆盖 REQ / NFR | REQ-007、REQ-014、REQ-017、REQ-018、REQ-020、REQ-022 |
| 所属 Phase | [P1] Demo（跨大类复制属候选 / 后续阶段） |
| 交付物形态 | Demo / Product Sandbox |
| 当前状态 | P1-已实现；Product Sandbox 场景包数据集增量待实现 |
| 最后更新 | 2026-07-15 |
| 下游影响 | docs/08-dev-plan.md（Sprint-2）、docs/09-verification.md（TC-007/014）、backend/app/data/、tests/ |

## 1. 目标与范围

场景包用于把不同客户业务形态的知识、规则、意图样例和 Mock 业务数据从代码中分离出来。Phase1 至少提供产品型客户与项目型客户两个场景包。

覆盖需求：REQ-007、REQ-014。

## 2. 场景包结构

| 字段 | 说明 |
|---|---|
| `code` | 唯一编码，如 `product_business` |
| `name` | 场景包名称 |
| `description` | 适用客户类型 |
| `source_refs` | 输入材料来源 |
| `intents` | 意图定义和样例 |
| `knowledge_items` | 知识条目 |
| `rule_items` | 规则条目 |
| `mock_business_records` | 订单 / 项目 / 售后 Mock 数据 |
| `handoff_rules` | 转人工策略 |
| `demo_questions` | H5 快捷演示问题 |

## 3. 产品型客户场景包

来源：`SRC-SP-PRODUCT-001`、`SRC-PRD-001`。

覆盖：灯饰 / 制造 / 标准或半标准产品销售企业。

核心对象：产品、规格、参数、定制询盘、订单、售后规则。

Phase1 样例：

- 产品参数咨询。
- 定制尺寸 / 颜色 / 批量询盘。
- 订单生产进度 Mock。
- 售后退换货规则。
- 投诉 / 舆情高风险转人工。

## 4. 项目型客户场景包

来源：`SRC-SP-PROJECT-001`、`SRC-PRD-001`。

覆盖：智能家居方案商、项目交付型企业、方案开发与生产交付并存客户。

核心对象：项目、阶段、里程碑、交付物、技术资料、项目进度、问题跟进、售后工单。

Phase1 样例：

- 方案开发流程咨询。
- 技术资料获取说明。
- 项目阶段 Mock 查询。
- 售后工单 Mock 查询。
- 复杂技术 / 合同问题转人工。

## 5. 校验规则

- 每个知识条目必须有 `source_ref`。
- 每个 Mock 业务记录必须有 `is_mock: true`。
- 高风险规则不可被场景包关闭，只能追加更严格规则。
- 场景包中不得包含真实客户隐私、真实订单、真实合同。

## 6. 验收

- TC-007、TC-014 通过。
- 新增或切换场景包不需要改动意图路由核心逻辑。

## 上游依据与追溯

最低追溯链：`REQ/NFR → Phase → COMP/MOD/Flow → Table/Field → API → Design Point → Sprint/Task → TC`。

| 来源 | 章节 / ID | 本设计承接内容 | 下游影响 |
|---|---|---|---|
| docs/02-srs.md / 03-prd.md | REQ-007/014 | 场景包、配置与 Mock 数据可替换 | 08 / 09 |
| docs/04-architecture.md | COMP-007（Scenario Pack）；MOD-007（backend/app/data）+ MOD-005；Flow-001（客户问答）、Flow-002（进度 Mock 查询） | 场景包加载、与意图路由解耦 | 05 / 06 / 07 |
| docs/06-db-design.md | zycs_scenario_packs、zycs_mock_business_records（含 source_ref / is_mock 字段） | 配置模型数据对象 | seed |
| docs/07-api-spec.md | API-010 场景包列表、API-011 场景包详情（API-008 Mock 数据列表共享 mock_business_records） | 场景包接口契约 | 代码 / 测试 |
| docs/08-dev-plan.md | Sprint-2（场景包 / Mock） | 实现范围 | tasks |
| docs/09-verification.md | TC-007 场景包切换、TC-014 配置与 Mock 数据可替换（经 REQ-007/014 推断；09 §3 未显式反向引用本文） | 验收入口 | 验收记录 |

错误码（07 §5，按 API-010/011 归属推断）：`SCENARIO_PACK_NOT_FOUND`。

## 校验失败处理

| 场景 | 触发条件 | 系统行为 | 用户可见信息 | 记录 / 日志 | 是否阻塞验收 | 关联 TC |
|---|---|---|---|---|---|---|
| source_ref 缺失 | 知识条目无来源 | 拒绝加载该条目并记录 | 加载警告 | 审计 | 否 | TC-014 |
| is_mock 缺失 | Mock 记录未标记 | 拒绝加载并记录 | 加载警告 | 审计 | 否 | TC-014 |
| 含真实隐私 / 订单 / 合同 | 场景包数据违规 | 拒绝加载整包并告警 | 加载失败 | 审计 | 是（阻断加载） | TC-016 |
| 场景包不存在 | code 无效 | 返回 `SCENARIO_PACK_NOT_FOUND` | 提示场景包不可用 | — | 否 | TC-007 |
| 高风险规则被关闭 | risk 规则 enabled=false | 拒绝关闭，只允许追加更严规则 | 规则保留 | 审计 | 否 | TC-005 |

## 待人工确认项

| ID | 待确认项 | AI 建议 | 建议依据 | 备选方案 | 取舍影响 / 阻塞关系 |
|---|---|---|---|---|---|
| SP-C-001 | 跨大类场景包复制（古镇其他标准品制造 / 服务型 / 渠道代理型） | 登记为候选 / 后续阶段，当前不投入 | docs/inputs 场景包可复制性评估（推测未验证） | 立即扩展 | 不阻塞；Phase2 / 3 再评估 |
| SP-C-002 | 场景包版本与迁移策略 | 引入 version 字段 + 向后兼容约定 | Phase2 知识库强化可能改结构 | 无版本管理 | 不阻塞；结构变更前确认 |
| SP-C-003 | mock_business_records 编号与 mock-integrations 对齐 | 统一编号来源（HC-ORDER / XS-PROJ / XS-TICKET） | 当前两处独立定义 | 各自维护 | 不阻塞；存在漂移风险 |

## Product Sandbox 场景包数据集增量（Phase2.5 / Phase3A，2026-07-15）

每个启用场景包需绑定独立 Demo Dataset，至少覆盖：知识 / FAQ、订单或项目记录、售后工单、历史会话、知识缺口、转人工样例、通知样例、日报摘要和虚拟客户资料包。

| 数据块 | 要求 | 关联 REQ / TC |
|---|---|---|
| `data_source_mode` | 默认 `demo_sandbox`，预留真实只读模式门禁字段。 | REQ-017、REQ-021；TC-066、TC-070 |
| `demo_dataset` | 场景包独立维护，不与其他场景包共享运行态。 | REQ-018；TC-067 |
| `virtual_customer_profile` | 公司背景、产品目录、FAQ、角色和历史会话摘要。 | REQ-020；TC-069 |
| `source_refs` | 每条关键数据有可展示来源引用。 | REQ-022；TC-071 |

禁止把真实客户资料、真实订单或真实合同复制进场景包数据。
