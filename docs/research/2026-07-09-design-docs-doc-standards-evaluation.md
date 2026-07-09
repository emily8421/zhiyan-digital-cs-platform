# 详细设计文档 doc-standards 合规评审报告(docs/design/*)

## 0. 文档元信息

| 项 | 内容 |
|---|---|
| 报告类型 | 只读评审留痕(不改任何项目文档) |
| 评审范围 | `docs/design/*` 共 7 份:backend-service / knowledge-and-policy / mock-integrations / scenario-packs / h5-dialog / web-console / frontend-interaction |
| 评审依据 | `ai/doc-standards/design-doc.md`(主)、`ai/doc-standards/frontend-interaction.md`(交互型补充)、`ai/document-lifecycle-rules.md` §5.1/§5.2/§7.1 |
| 上游核对 | `docs/02-srs.md`、`03-prd`、`04-architecture`、`05-tech-spec`、`06-db-design`、`07-api-spec`、`08-dev-plan`、`09-verification` |
| 评审日期 | 2026-07-09 |
| 当前阶段 | Phase2(MVP 试点,2026-07-09 Conditional Go);Phase1 本机 Demo 已验收 |
| 评审方式 | 7 份文档并行子评审 + 抽查上游 ID 存在性 + 汇总(本报告) |
| 关联 open item | DOC-C-007(`docs/design/*` v1.43.0 元信息)——本报告为其细化展开 |
| 下游影响 | 不直接改 `00-09` / `design/*`;结论供后续 design 回梳任务(DES-C-001~003)与 Phase2 Sprint-7 启动门禁参考 |

## 1. 评审范围与依据

- **范围裁定**:用户确认本次仅评审 `docs/design/*`(PLM §2 定义的"详细设计阶段"另含 `06/07`,但 `06/07` 已有 v1.43.0 前 Batch 3 评估,且 `docs/design/*` 是当前唯一未做 v1.43.0 合规评审的详细设计区,对应 DOC-C-007)。
- **标准对照关系**:
  - 全部 7 份 → `design-doc.md`(10 个必填结构 §4.1–4.11、§6 八项审计 checklist、§7 禁止项、§5 分类 checklist)。
  - 交互型(frontend-interaction / h5-dialog / web-console)→ 额外对照 `frontend-interaction.md`(页面/路由追溯、状态覆盖、权限边界、TC 追溯)。
- **评级口径(本报告统一)**:
  - **No Go**:同时命中"§0 元信息全缺(含无日期)"且"触发 §7 硬禁止项:纯 happy path(无失败/异常/降级/权限拒绝路径)"。
  - **Conditional Go**:无核心禁止项硬伤(未把候选/Mock/默认关闭写成当前可交付真实能力、未孤立新增 06/07 契约),但元信息/追溯链/必填结构不达标,需按 P0 补齐后放行。
- **行号说明**:文中 `文件:行号` 引自评审时文件状态,供后续回梳定位;修订前应以最新文件复核。

## 2. 总体结论

**整批复评:Conditional Go。**

7 份文档**全部守住了 Phase 红线**:未把 Mock/降级/默认关闭/候选能力写成当前可交付真实能力,未孤立新增 `06/07` 之外的表/接口/错误码,引用的 REQ/API/TC ID 经抽查均真实存在。因此作为 **Phase1 已验收事实的承载**,可继续服役。

但 7 份**全部不满足 v1.43.0 `design-doc.md` 结构合规**,系统性共性问题如下(根因:这些文档多在 Phase1 早期 Sprint-3~5 生成,早于 v1.43.0 doc-standards 与 04 P1 合规引入的 COMP/MOD/Flow ID 体系):

| # | 共性问题 | 涉及 | 对照条款 |
|---|---|---|---|
| C1 | **§0 文档元信息缺或部分缺**:全部缺"最后更新日期";多数全文无元信息表;交互型缺 UI 原型策略字段;阶段口径停留 Phase1 | 全部 7 份 | design-doc §4.1;DOC-C-007 |
| C2 | **追溯链中段断裂**:04 已把 COMP/MOD/Flow 指向各 design(04 P1 合规刚补),但 design 未反向引用;COMP/MOD/Flow → Table/Field → Sprint/Task 段普遍缺失 | 全部 7 份 | design-doc §4.3 |
| C3 | **纯 happy path**:缺失败/异常/降级/权限拒绝路径 | h5-dialog、web-console、scenario-packs、mock-integrations(程度不同) | design-doc §7 |
| C4 | **待确认项结构不合格或缺失**:无 §4.11 五元组(ID/AI建议/依据/备选/影响) | 全部 7 份 | design-doc §4.11、§7;doc-lifecycle §6.1 |
| C5 | **readiness gate + Mock/降级差异表缺失**:候选/默认关闭能力无解锁条件表;Mock 与真实能力无对照表 | 全部 7 份 | design-doc §4.6/§4.7 |
| C6 | **实现偏差/设计回写缺失**:Phase1 已实现/已验收但 design 未回写 | 全部 7 份 | design-doc §4.10 |
| C7 | **个别错引**:knowledge-and-policy 把知识缺口入库误引为 Sprint-4(应为 Sprint-9) | knowledge-and-policy | 追溯一致性 |

## 3. 分文档评审结论

### 3.1 评级总览

| 文档 | 类型 | 元信息 | 追溯链 | happy-path | 待确认项 | 评级 |
|---|---|---|---|---|---|---|
| backend-service.md | 服务型 | ❌全缺 | ❌断(COMP/MOD/Flow/Table/TC) | ⚠️有兜底分支,非纯 happy | ❌缺 | **Conditional Go** |
| knowledge-and-policy.md | 策略/规则+AI/RAG | ❌全缺 | ❌断 + Sprint-4 错引 | ✅有降级/转人工 | ❌缺 | **Conditional Go** |
| mock-integrations.md | 导入/异步/集成 | ❌全缺 | ⚠️中段断 | ⚠️缺状态机/幂等/重试 | ❌缺(bullet 未结构化) | **Conditional Go** |
| scenario-packs.md | 配置型 | ❌全缺 | ⚠️中段断 | ⚠️校验失败无处理 | ❌缺 | **Conditional Go** |
| h5-dialog.md | 页面/交互 | ❌全缺 | ⚠️COMP/MOD/Flow 断 | ❌纯 happy(仅回答分支) | ❌缺 | **No Go** |
| web-console.md | 页面/交互 | ❌全缺 | ⚠️Page/Flow 缺 | ❌纯 happy(写操作无错误分支) | ❌缺 | **No Go** |
| frontend-interaction.md | 页面/交互总览 | ⚠️部分(缺日期/UI原型策略) | ⚠️无统一矩阵 | ✅禁止项全未犯 | ❌结构不合格 | **Conditional Go** |

> 子评审原始评级与本表差异:backend-service 子评审判 No Go,本报告因其流程含 high_risk/mock_query/matched + gap/handoff 兜底分支(非纯 happy),按统一口径降为 Conditional Go;web-console 子评审判 Conditional Go,本报告因其写操作 PATCH/POST 无任何 404/409/500/无权限分支(纯 happy),按统一口径上调为 No Go。

### 3.2 backend-service.md(服务型 · Conditional Go)

- **合规项**:REQ-002~016、API-001~012、4 个错误码均真实有效;服务职责表与消息处理流程图覆盖服务型要点;明确"Mock 记录不存在不得编造""未预期错误不返回堆栈"(契合 REQ-005)。
- **问题项**:全文无 §0 元信息(`:1-3`);§1 职责边界只写"负责"无四列(`:5-9`);§3 服务职责表缺 API-ID/权限/错误码/契约状态列(`:29-42`);§4 流程无 Flow-D ID、缺状态机(`:44-64`);全文无追溯矩阵,未引 COMP-003~012/MOD-004~009/Flow-001~004/Table/TC(`:5-9`);§6 数据降级写成 Phase1 三选一,无 readiness gate(`:74-80`);§7 验收无 TC 映射(`:82-86`);缺 §4.9/§4.10/§4.11 三节。
- **风险项**:business_query_service(`:37`)、notification_service(`:40`)为 Mock 但无差异表,易误读为真实能力;数据降级未与 Demo/MVP/产品形态绑定;与 04 实现状态(COMP-005/006/011)脱节;无回写区。
- **P0**:补 §0 元信息(日期≥2026-07-09、[P1] Demo、状态 P1-已实现);补 §4.3 追溯矩阵闭合 COMP/MOD/Flow/Table/TC;补 §4.11 待确认项五元组。
- **P1**:§3 补 API-ID/权限/错误码列;§4 补 Flow-D ID + 状态机;补 §4.7 readiness gate + §4.6 Mock/降级差异表;补 §4.8 验收矩阵、§4.9 子系统交互、§4.10 回写。

### 3.3 knowledge-and-policy.md(策略/规则+AI/RAG · Conditional Go)

- **合规项**:明确 Phase1 不启用 LLM、规则/关键词降级(契合 05 RG-002/003);匹配策略给出明确规则优先级(高风险→进度→场景→缺口);不编造 + 高风险转人工有失败/降级路径;缺口状态机齐全;REQ/TC 上游真实。
- **问题项**:无 §0 元信息(`:1-3`);§1 边界未拆四列(`:5-9`);匹配策略缺 Flow-D ID 与规则冲突裁决(`:21-30`);未引 COMP-006/010、MOD-005、Flow-001/003/004、06 三表 + source_ref、API-002/005/006(全篇);**`:57` Sprint-4 错引应为 Sprint-9**;无 readiness gate 表;无 §4.6 差异表、§4.11 待确认项、§4.9/§4.10。
- **风险项**:Sprint-4 错引误导任务拆分;不编造策略未与 API-002 响应字段(source_ref/answer_type/knowledge_gap)挂钩;高风险规则未引 06 `zycs_rule_items`,若硬编码违反 project-rules §5.1。
- **P0**:补 §0 元信息;**修 `:57` Sprint-4→Sprint-9**;补 §4.3 追溯矩阵。
- **P1**:匹配策略补 Flow-D-001~004 + 冲突裁决;补 §4.5/§4.6/§4.7(引 RG-002/003)/§4.8/§4.11(LLM 启用、向量检索、accepted 入库时点入项)。

### 3.4 mock-integrations.md(导入/异步/集成 · Conditional Go)

- **合规项**:明确 Phase 不接真实 CRM/ERP/OA/飞书(`:7`);Mock 记录带 `mock:true`、通知 `send_status:mocked`,与 07 §1.3、06 `is_mock` 一致;`EXTERNAL_INTEGRATION_DISABLED` 引用正确;REQ/TC 真实。
- **问题项**:无 §0 元信息(无日期,`:1-9`);未引 COMP-008/011、MOD-006、Flow-002/003/004、API-007/008/009、`zycs_mock_business_records`/`zycs_notifications`(`:9-10`/`:29-34`/`:56-65`);**无状态机表**(本类型必需);缺幂等/重试/超时/限流(§5 仅把重试/限流/token 列为未来,`:74-75`);无 §4.6 失败/降级表与差异表;§5 升级条件为 bullet 非 readiness gate 表;§5 实质待确认项未结构化(`:67-75`);§4.8 空壳;停留 Phase1 口径。
- **风险项**:Mock 查询无幂等/重试基线,Phase2 换真实适配器易引入不可重入;真实集成 readiness gate 无阻塞判定;通知 payload 未与 06 表/07 API-009 逐字段对齐(契约漂移)。
- **P0**:补 §0 元信息;补 §4.3 追溯矩阵;补状态机表;补幂等/重试/超时/限流基线。
- **P1**:补 §4.6 失败/降级 + 差异表;§5 升级条件改造为 readiness gate 表(标 Phase3、阻塞判定);§5 bullet 转 §4.11 待确认项;补 §4.8 矩阵。

### 3.5 scenario-packs.md(配置型 · Conditional Go)

- **合规项**:REQ-007/014、TC-007/014 真实;字段模型与 06 `zycs_scenario_packs` 及 ADR-0003 一致;§5 校验抓住关键不变量(source_ref 必填、is_mock:true、高风险规则不可关闭、禁真实隐私/订单/合同);两包范围限定 P1 未越界。
- **问题项**:无 §0 元信息(无日期,`:1-69`);字段表未映射 06 表、未引 API-010/011(`:12-24`);追溯仅 REQ-007/014,缺 COMP-007/MOD-007/Flow-001/表/API/Sprint(`:5-9`);**校验规则无违反后系统行为(`:58-63`,触发 happy-path)**;§6 验收仅列 TC(`:65-69`);无 §4.9/§4.10/§4.11;跨大类复制(IN-C-003/005)未标候选/后续。
- **风险项**:校验无失败处理,与 TC-014/016 通过判定可能不一致;`mock_business_records` 与 mock-integrations 的 Mock 编号无关联(两处定义漂移);无版本/迁移策略。
- **P0**:补 §0 元信息;补追溯矩阵;补加载/校验失败处理(消除 happy-path)。
- **P1**:配置型补版本字段 + 加载/发布状态机 + 校验失败表;补 readiness gate(跨大类复制标后续阶段);补 §4.11/§4.9;字段表映射 06/07。

### 3.6 h5-dialog.md(页面/交互 · No Go)

- **合规项**:范围克制限 Phase1 Demo;Mock/Demo 标识清晰;API-001/002/010/011、TC-001/003/004/005/008、REQ 真实;§5 样例问题表质量好(含高风险不承诺与未知处理,契合 REQ-005/016);正确引用 frontend-interaction.md。
- **问题项(命中 No Go 硬门)**:无 §0 元信息(无日期,`:1-9`);**纯 happy path——时序图 alt 仅 handoff/knowledge_gap/正常回答三分支,无网络失败/超时/权限拒绝/降级(`:35-56`)**;§3 是前端状态变量非页面状态九态(`:20-31`,空/错误/禁用/无权限/降级五态 UI 文案缺);REQ/API 不一致(用 API-010/011 属 REQ-007,但 `:9` 覆盖列表未含 REQ-007);未引 COMP-001/MOD-001/Flow-001(04:226 已指向本文档);缺 §4.9/§4.10/§4.11/§4.7;权限边界未落后端(`:85-90` 仅谈数据隐私);API-011 列为依赖但流程未调用(`:83`)。
- **风险项**:happy-path 传导实现,失败路径无依据;无日期/状态易被误判,且 F-001=已验证未回写;`error` 状态字段存在但无 UI/恢复路径(口径漂移)。
- **P0**:补 §0 元信息;补 §4.6 失败/异常/降级表 + 时序图补 error 分支;补 §4.6 页面状态九态表。
- **P1**:补 §4.3 追溯矩阵(引 COMP-001/MOD-001/Flow-001 + 补 REQ-007);补 §4.9/§4.10(回写已验证)/§4.11/§4.7;补权限边界说明(Phase1 无鉴权 Demo 边界)。

### 3.7 web-console.md(页面/交互 · No Go)

- **合规项**:Mock/Demo 文案与状态词典一致(`:84-87`);API-003~012 全在 07;TC-006/009/010/011/012 在 09 且反向引用本文;§4 有 mermaid 时序图(契合 §13);正确声明 Phase1 不实现登录/权限/多租户(`:7`)。
- **问题项(命中 No Go 硬门)**:无 §0 元信息(无日期,`:1-9`);**纯 happy path——PATCH 转人工(`:44`)/PATCH 缺口(`:51`)/POST 知识候选(`:53`)无 404/409/500/校验失败/并发/无权限分支,mermaid(`:34-62`)无 alt 失败分支**;无待确认项章节;无追溯矩阵/Page-ID/Flow-ID(`:11-23`/`:32-80`);权限边界未结构化(写操作未声明"后端无鉴权 Demo 限" + Phase2 义务);状态九态仅命中风险/Mock-Demo 提示,缺 6 类;无 readiness gate/阶段增量/实现偏差;§1 覆盖 REQ 与 §2 实际触及不一致(`:9` vs `:15-23`,漏 REQ-007/008/014)、§6 漏 TC-007/008。
- **风险项**:写操作无后端边界声明,易被误读为"前端可更新即有权限",Phase2 试点越权风险;仅 happy + 6 类状态缺,空态/错误/降级无通过标准;无 Page/Flow-ID 致 08/09 无法稳定引用;停留 Phase1 与 07/09 的 Phase2 状态漂移。
- **P0**:补 §0 元信息;为 `:64`/`:70`/`:76` 关键流程补失败/异常/降级/无权限分支 + mermaid 补 alt;补 §4.11 待确认项(Phase2 后端权限口径、Mock→真实时点等)。
- **P1**:补追溯矩阵(Page-ID/Flow-ID + 引 04 COMP/MOD、05 Risk/RG、06 表、07 错误码);补角色-权限可见性表;补 §4.6 九态表;补 §4.7/§4.10。

### 3.8 frontend-interaction.md(页面/交互总览 · Conditional Go)

- **合规项**:**§7 禁止项全部未犯**(未定义 07 不存在接口、未用路由守卫替代权限、未把 Mock UI 写成真实能力、有验收路径、未越界);接口依赖(§8)与 07 一一对应;Mock/Demo/Risk 文案体系完整(§7)可直接落地;验收路径(§10)与 09 TC 双向闭合;已纳入 PX-R-002(§11 注脚)。
- **问题项**:§0 元信息(`:7-13`)缺最后更新日期、UI 原型策略字段、文档路径、交付物形态、下游影响;当前状态"Phase1 关键口径已确认"不符状态枚举且未升级 Phase2;§2 页面表缺 Phase/状态列(`:44-62`);§3 七条用户路径无 Flow-ID(`:80-134`);组件无 Component-ID;§12 待确认项结构不合格(无五元组,`:298-301`);缺实现偏差/回写章节、readiness gate 表、角色权限可见性表、统一追溯矩阵、UI 原型策略章节;§8 缺 Mock/降级差异列。
- **风险项**:阶段口径过期(锁 Phase1,项目已 Phase2),Phase2 权限/缺口流转/运营配置前端交互无权威索引;无 Flow-ID 致 04/09 难双向回溯;无实现偏差表,Phase1 验收事实漂移。
- **P0**:§0 补齐(日期=2026-07-09、UI 原型策略=代码原型引 project-rules §2.7、文档路径、交付物形态=Demo、状态枚举、下游影响);阶段口径升级覆盖 Phase2 增量或声明待补。
- **P1**:§2 补 Phase/状态列;§3 补 Flow-ID;§12 重写为五元组待确认项;新增实现偏差/回写表、readiness gate 表、角色权限可见性表、统一追溯矩阵(补 COMP/MOD 引用)。
- **P2**:组件补 Component-ID;§8 补 Mock/降级差异列;新增独立 UI 原型策略章节(声明 PX-R-001~003 覆盖);§5 状态补 success/degraded/no-permission。

## 4. 共性问题根因

1. **生成时序早于标准**:7 份文档多在 Phase1 Sprint-3~5 生成,早于 v1.43.0 doc-standards 与 04 P1 合规(COMP/MOD/Flow/TDR/Risk/RG ID 体系)。04 已反向指向 design,但 design 未正向引用,形成"04 → design 有、design → 04 无"的单向链(C2)。
2. **元信息规范未贯彻**:DOC-C-007 已知,本次证实 7 份全部不达标(含日期缺失),是 v1.43.0 合规的统一缺口(C1)。
3. **happy-path 习惯**:早期 Demo 文档侧重主流程演示,失败/降级/权限路径普遍薄弱(C3),与 design-doc §7 直接冲突。
4. **待确认项/回写机制缺位**:Phase1 以 Demo 交付为主,长期事实(已实现/已验证)多留代码与 08/09,design 未回写(C4/C6)。

## 5. 优先级修复路线

> 修复属"修改项目事实文档(design/*)"另一范围,需另起分支 + 用户确认后执行;本报告仅给出路线。

**P0(进入 Phase2 编码 / Sprint-7 前必做,全 7 份)**:
1. 补 §0 文档元信息:最后更新 ≥ 2026-07-09;Phase 双维度 `[P1]`/`[P2]`/`[愿景]`;交付物形态 Demo/MVP;当前状态用状态枚举;交互型补 UI 原型策略字段(引 project-rules §2.7);下游影响。
2. 补 §4.3 追溯矩阵:反向引用 04 COMP/MOD/Flow-ID + 06 Table/Field + 08 Sprint/Task + 09 TC-ID,闭合最低链。
3. 消除 happy-path:为关键流程补失败/异常/降级/权限拒绝分支(h5-dialog、web-console、scenario-packs、mock-integrations 优先)。
4. 补 §4.11 待确认项五元组(每份至少覆盖其类型相关项)。

**P1(实现/验收前)**:
5. 补 §4.6 Mock/降级 vs 真实能力差异表 + §4.7 readiness gate 表(候选/默认关闭能力标解锁条件)。
6. 补 §4.10 实现偏差/设计回写(回写 Phase1 已实现/已验收事实)。
7. 阶段增量补 Phase2(权限、缺口流转、运营配置落点)。
8. 交互型补 Page-ID / Flow-ID / Component-ID / 状态九态表 / 角色-权限可见性表。

**P2(文档完善,按需)**:
9. 命名规范(标题统一"详细设计:<子系统>(<slug>)")、a11y / 响应式、版本/迁移策略、子系统交互表。
10. 修正 scenario-packs 与 mock-integrations 的 Mock 编号关联。

## 6. 待确认项总览(本次评审新增,建议回填 open items)

| ID | 待确认项 | AI 建议 | 建议依据 | 备选 | 影响/阻塞 |
|---|---|---|---|---|---|
| DES-C-001 | 是否对 7 份 design 做统一 v1.43.0 合规回梳 | 做,分 P0 全量 + P1/P2 按需 | 本报告证实 7 份均不达标,且 Phase2 编码前 design 须可追溯 | 仅按需触碰时补 | 不阻塞 Phase1(已验收);**条件阻塞 Phase2 编码/Sprint-7** |
| DES-C-002 | 回梳批次与分支策略 | 单分支 `docs/design-p1-compliance`,7 份分 commit | 与 04/05 P1 合规(#30)同模式,便于审查 | 按文档类型分多分支 | 影响审查粒度,不阻塞 |
| DES-C-003 | knowledge-and-policy `:57` Sprint-4 错引修正 | 立即改 Sprint-9 | 08-dev-plan 明确 Sprint-4=Web 控制台、Sprint-9=知识运营 | 留待回梳一并改 | 不阻塞,但应随回梳闭合 |
| DES-C-004 | h5-dialog / web-console 的 No Go 是否先于整批回梳单独修 | 随 P0 统一回梳,不单独提级 | 二者 happy-path 与其余 P0 同批修复成本更低 | 单独紧急修 | 不阻塞(Phase1 已验收) |

## 7. 与既有 open items 的关系

- **DOC-C-007**(design/* v1.43.0 元信息):本报告是其细化展开,证实 7 份全部不达标,并扩展到追溯链/happy-path/待确认项等 design-doc 全维度。回梳后 DOC-C-007 可关闭。
- **DOC-C-006**(#148 模板仓)、**IN-C-003/005**、**ARCH-C-001 P2**:与本报告无直接耦合,回梳 design 时不涉及。
- **ARCH-C-001 P1 已完成**(04/05 COMP/MOD/Flow/TDR/Risk/RG):本次 design 回梳 P0 第 2 项(反向引用 04 ID)依赖该成果,二者衔接闭合 `REQ → Phase → COMP/MOD/Flow(04) ↔ Design → TC` 全链。

## 8. 附录:7 份 × design-doc §6 八项审计 checklist 矩阵

| 审计项(checklist) | backend | knowledge | mock-integ | scenario | h5 | web-console | frontend-int |
|---|---|---|---|---|---|---|---|
| 1. 触发详细设计/豁免理由 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2. 元信息/边界/追溯/流程/失败降级 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ⚠️ |
| 3. 正确引用 06/07 未孤立新增 | ✅ | ⚠️缺引用 | ⚠️缺引用 | ⚠️缺引用 | ⚠️缺引用 | ⚠️缺引用 | ✅ |
| 4. readiness gate + 候选/降级解锁 | ❌ | ⚠️口径对未落地 | ❌ | ❌ | ❌ | ❌ | ❌ |
| 5. 区分 Mock/降级/Demo 与真实 | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ✅ |
| 6. 输出到 08/09 Sprint/Task/TC | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ✅ |
| 7. 实现偏差/回写区 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 8. 待确认项含建议/依据/备选/影响 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

> 结论:除"触发详细设计"一项全过、"禁止项核心(未冒充真实能力)"全守住外,结构合规项(2/4/7/8)7 份均不达标,印证整批 Conditional Go、需 P0 回梳。
