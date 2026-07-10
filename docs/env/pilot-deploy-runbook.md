# 试点部署预案（Phase2 MVP）

> 定位：本文件是 Phase2 Sprint-7「试点部署与运营配置」的本机部署预案，归属 `docs/env/`。它面向单个试点客户演示，说明如何在本机以「单实例 + 双场景包」形态部署、演示和验收；不替代 `docs/08-dev-plan.md` Sprint-7 验收标准与 `docs/09-verification.md` §10.4 验证用例。Phase1 通用 Demo 启动见 `docs/env/local-demo-runbook.md`。

## 0. 文档元信息

| 项 | 内容 |
|---|---|
| 上游输入 | `docs/08-dev-plan.md` Sprint-7、`docs/09-verification.md` §10.4（TC-017~TC-020）、`docs/design/web-console.md`（WC-C-001） |
| 当前状态 | Phase2 Sprint-7 部署预案（本机演示优先），2026-07-10 |
| 交付物形态 | MVP 试点（本机演示） |
| 关联 REQ | REQ-010、REQ-011、REQ-012（运营控制台）、REQ-015（本机运行）、REQ-016（权限 / 安全） |

## 1. 适用范围与边界

- 适用阶段：Phase2 MVP 试点，面向单个试点客户演示。
- 部署形态：**单实例 + 双场景包**——同一本机实例同时承载古晶（产品型，签约目标）与乐式（项目型，数据 / 验证来源）两个场景包，验证「统一架构 + 场景包可复制」。
- 部署环境：**本机演示优先**（后端 `8000` / H5 `5173` / Console `5174`），不使用公司服务器、不部署到客户侧、不触发新依赖或安全评审。
- 明确不做：多租户 / 客户级数据隔离（Phase4）、真实登录鉴权（Phase4）、真实 CRM / ERP / OA / 飞书 / 工单（Phase3）、LLM 默认启用、知识库 / 规则编辑（Sprint-9）。

## 2. 启动（本机三端）

启动方式与 `docs/env/local-demo-runbook.md` 一致，复用一键脚本或手动启动。

### 2.1 一键启动

```powershell
powershell -ExecutionPolicy Bypass -File scripts/start-local-demo.ps1
```

| 服务 | 端口 | 地址 |
|---|---:|---|
| 后端 API | 8000 | `http://127.0.0.1:8000`（`/health`、`/docs`） |
| H5 客户页 | 5173 | `http://127.0.0.1:5173`；手机扫码见 `local-demo-runbook.md` §3 |
| Web 控制台 | 5174 | `http://127.0.0.1:5174` |

启动后检查：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check-local-demo.ps1
```

### 2.2 手动启动

后端：

```powershell
$env:PYTHONPATH='backend'
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

H5：`cd frontend/customer-h5; npm.cmd run dev -- --host 0.0.0.0 --port 5173`
控制台：`cd frontend/console; npm.cmd run dev -- --port 5174`

## 3. 试点演示路径

### 3.1 双场景包主链路（TC-017）

1. 打开 H5：`http://127.0.0.1:5173`。
2. 分别用**产品型（古晶）**与**项目型（乐式）**两个场景包创建会话，依次发送产品咨询、项目咨询、售后规则、进度查询、高风险 / 未知问题。
3. 期望：两个场景包主链路（问答 / 转人工 / 知识缺口）均跑通，回答标明依据与 Mock，`scenario_pack_code` 正确区分。

### 3.2 运营配置入口（TC-019）

1. 打开控制台：`http://127.0.0.1:5174`。
2. 顶部「当前演示场景包」选择器切换「全部 / 产品型 / 项目型」：会话、待跟进、知识缺口、Mock 数据列表按所选场景包过滤。
3. 顶部「管理员 / 只读」角色切换器切换角色，查看日报摘要与各列表。

### 3.3 控制台角色权限（TC-018）

- 切到「管理员」：可更新转人工状态、知识缺口状态、生成 Mock 通知（写操作可用）。
- 切到「只读」：写操作按钮禁用；即便绕过前端直接调用 `PATCH /api/v1/handoffs/{id}`、`PATCH /api/v1/knowledge-gaps/{id}`、`POST /api/v1/notifications/mock`（不带 `X-Console-Role: admin`），后端返回 `403 FORBIDDEN_CONSOLE_WRITE`。
- 只读接口（`GET` 会话 / 转人工 / 缺口 / 通知 / 日报）对所有角色开放。

## 4. 角色与权限说明（重要口径）

- 控制台权限采用 **Demo 级「请求头声明角色」**：前端在顶部切换「管理员 / 只读」，角色写入浏览器 `localStorage`，写操作请求携带 `X-Console-Role` 头；后端 `app/core/permissions.py` 的 `require_console_admin` 依赖强制校验，非 `admin` 写操作返回 `403`。
- **这是演示用角色机制，不是生产级鉴权**：没有账号、密码、登录态或 token，角色可由前端切换；它满足「后端执行角色校验、不依赖前端隐藏按钮」的底线（WC-C-001），但不抵御恶意伪造。
- 真实登录、多租户、用户体系属 Phase4；本阶段不实现。任何对外正式演示须同步说明此口径，避免被误读为生产级安全能力。

## 5. Mock / 降级边界

- 所有外部业务数据（订单 / 项目 / 售后 / 通知）均为 Mock，响应 `meta.mock = true`；不接真实 CRM / ERP / OA / 飞书 / 工单。
- 飞书通知只记录 payload，`send_status = mocked`，不真实发送。
- LLM 默认关闭；回答来自规则 / 知识 / Mock，无依据或高风险转人工，不编造。
- 存储使用内存 / Mock 降级；PostgreSQL / pgvector 不作为本阶段前置（DOC-C-004，Sprint-8 技术验证）。

## 6. 试点验收检查点

对应 `docs/09-verification.md` §10.4：

| TC-ID | 检查点 | 自动化 / 手工 |
|---|---|---|
| TC-017 | 单实例双场景包主链路跑通 | 手工（§3.1） |
| TC-018 | 后端按角色放行写操作（admin 可写 / 其余只读 / 前端绕过无效） | 自动化 `tests/api/test_console.py` + 手工（§3.3） |
| TC-019 | 运营配置入口可切换场景包、查看双场景包数据 | 手工（§3.2） |
| TC-020 | 本机三端部署预案可复现 | 手工（§2 + `check-local-demo.ps1`） |

自动化验证命令：

```powershell
$env:PYTHONPATH='backend'; python -m pytest -p no:cacheprovider tests/api tests/scenarios tests/acceptance
cd frontend/console; npm.cmd run build
cd ../customer-h5; npm.cmd run build
```

## 7. 关闭服务

关闭一键脚本打开的 3 个 PowerShell 窗口，或在各窗口按 `Ctrl+C`。
