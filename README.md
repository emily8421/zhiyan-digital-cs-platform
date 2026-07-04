# 知衍数字客服统一平台

知衍数字客服统一平台面向古镇产业带及类似中小企业，解决“靠微信做生意、靠人盯群”的客户沟通问题。当前目标是先完成本机 Demo：客户通过 H5 提问，系统基于场景包、知识、规则和 Mock 数据回答；高风险或无依据问题转人工；员工侧 Web 控制台查看会话、缺口、待跟进和摘要。

## 当前阶段

- 当前阶段：Phase1（本机 Demo，已人工确认）
- 交付物形态：H5 客户对话页 + FastAPI 后端 + Web 控制台 + Mock 数据
- 阶段目标：演示产品型客户和项目型客户的数字客服闭环
- 非目标：不接真实企业微信、飞书组织、CRM / ERP / OA / 工单系统，不处理真实客户数据，不启用本地大模型或生产级向量索引

## 当前能力规划

- H5 客户对话入口，支持产品咨询、项目咨询、售后、进度查询和未知问题兜底。
- 产品型 / 项目型场景包，知识、规则和 Mock 业务数据配置化。
- Mock 订单 / 项目 / 售后进度查询，明确标记演示数据。
- 高风险和无依据问题转人工，不编造价格、交期、赔付、合同等承诺。
- Web 控制台查看会话、待跟进、知识缺口、Mock 通知和日报摘要。

## 快速开始

当前仓库已完成文档基线回梳，可从 Sprint-1 开始小步开发。建议流程：

1. 阅读并确认 `docs/03-prd.md` 的 Phase 路线图和 `docs/08-dev-plan.md` 的 Sprint 拆分。
2. 按已确认口径执行：React + Vite + TypeScript；存储优先 JSON / SQLite / 内存 Mock；飞书仅 Mock payload；LLM 默认关闭；Docker / PostgreSQL 不强制纳入 Phase1。
3. 从 `docs/08-dev-plan.md` 的 Sprint-1 开始开发，写代码或安装依赖前仍需说明范围并确认。

本机环境记录见 `docs/env/local-env.md`。当前记录显示 Docker 已安装但不可用，Phase1 默认允许使用 Mock / 本地临时数据降级。

## 文档入口

- `docs/vision/product-vision.md`：产品愿景和长期边界
- `docs/00-scenario.md`：项目背景、角色与场景
- `docs/01-user-requirements.md`：用户需求全集
- `docs/02-srs.md`：系统需求规格
- `docs/03-prd.md`：产品范围与 Phase 路线图
- `docs/04-architecture.md`：总体架构与模块划分
- `docs/05-tech-spec.md`：技术栈、资源约束与降级策略
- `docs/06-db-design.md`：目标数据库设计
- `docs/07-api-spec.md`：REST API 契约
- `docs/08-dev-plan.md`：Phase1 Sprint 计划
- `docs/09-verification.md`：验证计划与验收用例
- `docs/design/`：H5、Web 控制台、后端、知识规则、场景包、Mock 集成详细设计
- `docs/decisions/`：入口选择、Mock 优先、场景包配置化、不编造与转人工 ADR

## 重要边界

- Phase1 只使用 Mock / Demo 数据，不使用真实客户隐私、合同、订单、报价、联系方式或生产会话。
- 外部 API、飞书真实通知、LLM、Docker 镜像和新依赖默认关闭；如需引入，必须单独人工确认。
- 企业微信客户群自动对外回复不进入 Phase1，客户侧入口默认 H5。
- 所有回答必须能回溯到知识、规则、场景包或 Mock 数据；否则转人工或记录知识缺口。

## 开发计划

当前建议从 `docs/08-dev-plan.md` 的 Sprint-1 开始：

1. 后端 API 骨架。
2. 场景包与 Mock 服务。
3. H5 客户对话闭环。
4. Web 控制台。
5. 不编造与风险兜底。
6. 本机演示与文档回填。

文档链路与 Phase1 关键口径已确认；进入每个 Sprint 前仍需确认本次修改范围。

## 验证方式

验证计划见 `docs/09-verification.md`，覆盖 TC-001 到 TC-016。Phase1 以接口验证、场景样例和手工端到端演示为主，后续再按 Sprint 增加自动化测试。

## 模板关系

- 本项目由 `ai-project-template` 派生，通用 AI 行为规范在 `ai/`。
- 项目专属规则在 `ai/project-rules.md`。
- 根 `README.md` 是项目说明，不参与模板下行同步。
- 如需修改模板方法论，应在 `_proposals/` 起草提案，不直接修改模板同步文件。
