# task-011e Product Sandbox 端到端彩排记录（M11 验收）

> 定位：task-011e 端到端彩排验收记录，归属 `docs/research/`。验收事实回写 `docs/09-verification.md` §10.28；不替代 `docs/08-dev-plan.md` 或 `docs/09-verification.md` 的正式记录。
> 日期：2026-07-16。关联：Sprint-10、M11、TC-066~TC-071、REQ-017~REQ-022、F-012~F-016、AC-008~AC-014。

## 1. 彩排目标

完成 Product Sandbox 可试用版端到端彩排，验证 M11 验收口径（TC-066~TC-071）：数据源模式、场景包独立模拟数据、Demo reset、虚拟客户资料完整展示、来源标识全链路。

## 2. 彩排环境

- 本机三端：`scripts/start-local-demo.ps1` → Backend `8000` / H5 `5173` / Console `5174`。
- 可达性：`scripts/check-local-demo.ps1` → **6 / 6 reachable**（Backend health/docs、H5/Console 页面 + 代理 API，identity marker 匹配）。
- 全量回归：`PYTHONPATH=backend python -m pytest tests/` → **87 passed / 6 skipped / 0 failed**（task-011a~d 合并进 main 后无回归；CI 仅跑 diff-check 未跑 pytest，本次补跑确认）。
- 工具版本：Python 3.14.3 / Node v22.17.1。端口 8000/5173/5174 全空闲。

## 3. API 全链路验证（阶段 1）

用 python urllib 发请求（规避 Windows Git Bash 下 curl 中文 body 编码问题），验证脚本 `.ai/task-011e-rehearse.py`（已 gitignore，保留作彩排证据）。

### 3.1 9 步闭环（全 http=200）

| 步骤 | 操作 | 来源标识结果 |
|---|---|---|
| 创建会话 | POST /conversations（产品型）| conversation_id=conv_xxx |
| 产品知识 | 「灯带有什么规格？」| answer_type=knowledge, source_ref=SRC-SP-PRODUCT-001 |
| 进度查询 | 「DEMO-ORDER-202607-001 生产进度」| answer_type=mock_business, source_ref=demo_erp:order:DEMO-ORDER-202607-001 |
| 高风险转人工 | 「合同违约责任能保证承担吗？」| answer_type=handoff, source_ref=rule:high_risk_handoff |
| 未知缺口 | 「火星基地联调验收流程」| answer_type=gap, source_ref=policy:knowledge_gap |
| 缺口入库 | PATCH /knowledge-gaps/{id} accepted（admin）| status=accepted → 生成 1 条 draft 知识条目 |
| Demo reset | POST /scenario-packs/{id}/demo-reset | scope=current_scenario_pack, source_mode=demo_sandbox, mock=true |

### 3.2 来源标识聚合（API-016，TC-071）

`GET /source-refs` → 17 条：knowledge×4 / rule×2 / mock_business×9 / demo_dataset×2，全部 `source_mode=demo_sandbox` + `mock=true`。

### 3.3 虚拟客户资料（API-014，TC-069）

`GET /scenario-packs/product_business/demo-dataset` → `source_mode=demo_sandbox`、`source_ref=demo_dataset:product_business:v1`、`mock=true`；`virtual_customer_profile`（company_name=明烁灯饰样例客户 / business_type / summary）+ stats（knowledge_items=2 / business_records=4 / historical_conversations=2 / knowledge_gaps=2 / summaries=1）。完整资料（产品目录 / FAQ / 订单 / 项目 / 售后 / 角色）存于 Demo Dataset 文件，由前端组装展示。

### 3.4 Console record 字段

- Mock 业务记录（/mock-business）：含 `source_ref` / `source_system` / `environment` / `stage` / `payload` / `mock`。
- handoff / knowledge-gap record：含 `mock:true`，本身不带 `source_ref` 字段（来源在触发消息 / 规则，设计如此）。
- daily summary：含 `content` + `mock:true`。

## 4. 前端人工验收（阶段 2，ABCD 全正常）

| 项 | 操作 | 结果 |
|---|---|---|
| A1/A2 TC-071 H5 徽章 | H5 发产品知识 / 进度消息 | 回复气泡显示「来源模式：Demo Sandbox」+「来源：{source_ref}」 ✅ |
| B1 TC-071 Console 抽样区 | Console「来源标识抽样（API-016）」专区 | 列出 knowledge/rule/mock_business/demo_dataset 来源 ✅ |
| B2 TC-071 Console 卡片 | Mock 业务卡片详情 | source_ref / source_system / environment 字段 ✅ |
| C TC-069 完整资料 | Console 各数据区 | Demo Sandbox banner + 知识条目（FAQ）+ Mock 业务（订单/项目/售后）+ 会话（历史）组装呈现完整虚拟客户资料，全程标识模拟 ✅ |
| D 演示主线 | 产品知识→进度→转人工→缺口→Console 闭环 | 5 步无报错、Console 联动 ✅ |

## 5. TC-066~TC-071 结论

| TC | 内容 | 结果 |
|---|---|---|
| TC-066 | 数据源模式门禁（task-011a）| ✅ |
| TC-067 | Demo Dataset 场景包独立（task-011b）| ✅ |
| TC-068 | Demo reset（task-011c）| ✅ |
| TC-069 | 完整虚拟客户资料展示（task-011b/011d）| ⚠️ → ✅ |
| TC-070 | 未授权真实模式 No-Go（task-011a）| ✅ |
| TC-071 | 来源标识全链路（task-011d）| ⚠️ → ✅ |

## 6. M11 验收结论

**TC-066~TC-071 全部通过，M11 Product Sandbox 可试用版验收通过（2026-07-16）。**

## 7. 边界（未解锁，Phase3 范围）

- 真实业务系统（CRM / ERP / OA / 工单）、生产飞书、真实客户数据、生产 LLM 自动答复：仍 No-Go。
- 通知 / 日报 record 不带 `source_ref` 字段为设计如此（来源在触发消息 / payload），不计为缺陷。
- 彩排为本机 Demo Sandbox，不等于生产上线。
