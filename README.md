# 知衍数字客服统一平台

知衍数字客服统一平台面向古镇产业带及类似中小企业，解决“靠微信做生意、靠人盯群”的客户沟通问题。Phase1 已完成本机 Demo：客户通过 H5 提问，系统基于场景包、知识、规则和 Mock 数据回答；高风险或无依据问题转人工；员工侧 Web 控制台查看会话、缺口、待跟进和摘要。Phase2 MVP 已通过 M10 验收，当前仍处于 Phase2 收尾与 Demo Sandbox / Phase3 准备规划阶段，不解锁真实业务系统集成。

## 当前阶段

- 当前阶段：Phase2（MVP 已验收，M10，2026-07-11）；Phase3 仅进入准备规划，真实集成仍 No-Go
- 已有交付物：H5 客户对话页 + FastAPI 后端 + Web 控制台 + Mock 数据
- Phase1 已验证目标：演示产品型客户和项目型客户的数字客服闭环
- 非目标：不接真实企业微信、飞书组织、CRM / ERP / OA / 工单系统，不处理真实客户数据，不启用本地大模型或生产级向量索引

## 当前能力规划

- H5 客户对话入口，支持产品咨询、项目咨询、售后、进度查询和未知问题兜底。
- 产品型 / 项目型场景包，知识、规则和 Mock 业务数据配置化。
- Mock 订单 / 项目 / 售后进度查询，明确标记演示数据。
- 高风险和无依据问题转人工，不编造价格、交期、赔付、合同等承诺。
- Web 控制台查看会话、待跟进、知识缺口、Mock 通知和日报摘要。

## 快速开始

当前仓库已完成文档基线回梳，并已合并 Sprint-1 到 Sprint-9：Phase1 本机 Demo 已通过验收，Phase2 Sprint-7/8/9 已完成，M10 里程碑已验收。RG-001 飞书出站通知沙箱与 RG-002 PostgreSQL / pgvector 为 Go，RG-003 LLM 为 Conditional Go；真实业务系统、生产飞书、真实客户数据和生产 LLM 自动答复仍保持 No-Go。

固定运行手册见 `docs/env/local-demo-runbook.md`。

AI 场景触发：后续可直接说“我想看演示效果”“帮我启动本机 Demo”“给我 H5 二维码”或“检查 Demo 是否起来”，AI 会按 `docs/env/local-demo-runbook.md` 的固定流程执行或引导操作。

### 一键启动本机 Demo

```powershell
powershell -ExecutionPolicy Bypass -File scripts/start-local-demo.ps1
```

启动后检查：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check-local-demo.ps1
```

访问入口：

- H5 客户页：`http://127.0.0.1:5173`
- H5 手机扫码：启动脚本会输出 `http://<电脑局域网IP>:5173`，并生成 `.ai/local-demo-h5-qr.svg`
- Web 控制台：`http://127.0.0.1:5174`
- 后端健康检查：`http://127.0.0.1:8000/health`
- 后端 API 文档：`http://127.0.0.1:8000/docs`

### 手动启动

#### 启动后端

```powershell
$env:PYTHONPATH='backend'
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

健康检查：`http://127.0.0.1:8000/health`。

#### 启动 H5 客户页

```powershell
cd frontend/customer-h5
npm.cmd run dev -- --host 0.0.0.0 --port 5173
```

电脑访问：`http://127.0.0.1:5173`；手机扫码访问需使用启动脚本输出的局域网地址。

#### 启动 Web 控制台

```powershell
cd frontend/console
npm.cmd run dev -- --port 5174
```

访问：`http://127.0.0.1:5174`。

本机环境记录见 `docs/env/local-env.md`。Docker 已完成 PostgreSQL / pgvector 技术验证并解除 RG-002 阻塞；当前演示默认仍可使用 Mock / 本地临时数据，按 Sprint-8 开关可验证 PostgreSQL 可选持久化路径。PowerShell 下如遇 `npm.ps1` 执行策略拦截，使用 `npm.cmd`。完整演示路径、常见问题和关闭方式见 `docs/env/local-demo-runbook.md`。

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
- `docs/08-dev-plan.md`：Phase / Sprint 计划
- `docs/09-verification.md`：验证计划与验收用例
- `docs/env/local-demo-runbook.md`：本机 Demo 启动、检查和演示手册
- `docs/design/`：H5、Web 控制台、后端、知识规则、场景包、Mock 集成详细设计
- `docs/decisions/`：入口选择、Mock 优先、场景包配置化、不编造与转人工 ADR

## 重要边界

- Phase1 只使用 Mock / Demo 数据，不使用真实客户隐私、合同、订单、报价、联系方式或生产会话。
- 外部 API、生产飞书、生产 LLM、Docker 镜像和新依赖默认关闭；PostgreSQL / pgvector 已完成技术验证与可选持久化路径验证，生产或客户侧启用仍需单独任务和人工确认。
- 企业微信客户群自动对外回复不进入 Phase1，客户侧入口默认 H5。
- 所有回答必须能回溯到知识、规则、场景包或 Mock 数据；否则转人工或记录知识缺口。

## 开发计划

当前开发进度：Sprint-1 到 Sprint-9 已完成并合并；Phase1 本机 Demo 已跑通，Phase2 M10 已验收；Sprint-8 飞书出站通知沙箱 + DB 技术验证已完成，Sprint-9 LLM 评估 + 知识运营强化已完成。后续优先围绕 Demo Sandbox、LLM Sandbox 适配器、客户演示脚本或 Phase3 准备规划拆独立任务。

1. 后端 API 骨架：已完成。
2. 场景包与 Mock 服务：已完成。
3. H5 客户对话闭环：已完成。
4. Web 控制台：已完成。
5. 不编造与风险兜底：已完成。
6. 本机演示与文档回填：已完成。

文档链路与 Phase1 关键口径已确认；Phase2 Conditional Go 已确认。进入每个 Sprint 前仍需确认本次修改范围。

## 验证方式

验证计划见 `docs/09-verification.md`，覆盖 TC-001 到 TC-060。Phase2 M10 已验收，RG-001 飞书出站通知沙箱与 RG-002 PostgreSQL / pgvector 为 Go，RG-003 LLM 为 Conditional Go；Demo Sandbox 标准模拟业务数据包已通过 TC-060。后续真实集成、生产飞书、生产 LLM 或产品化能力需另补验证层级。

## 模板关系

- 本项目由 `ai-project-template` 派生，通用 AI 行为规范在 `ai/`。
- 项目专属规则在 `ai/project-rules.md`。
- 项目自身版本见 `VERSION` 与 `CHANGELOG.md`；继承模板版本见 `TEMPLATE-BASE.md`。
- 根 `README.md` 是项目说明，不参与模板下行同步。
- 如需修改模板方法论，应在 `_proposals/` 起草提案，不直接修改模板同步文件。
