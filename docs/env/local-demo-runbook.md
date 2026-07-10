# 本机 Demo 查看效果手册

> 定位：本文件是 Phase1 本机 Demo 的固定运行手册，归属 `docs/env/`。它说明如何启动、检查和演示当前 H5 + FastAPI + Web 控制台闭环，不替代 `docs/08-dev-plan.md` 或 `docs/09-verification.md` 的验收记录。

## 1. 当前适用范围

- 适用阶段：Phase1 本机 Demo 已验收通过；Phase2 启动前仍可用本手册查看既有效果。
- 交付形态：H5 客户对话页 + FastAPI 后端 + Web 控制台 + Mock / Demo 数据。
- 验收依据：`docs/09-verification.md` §6 记录 Sprint-6 本机演示已通过，三端端口 `8000` / `5173` / `5174` 可访问。
- 边界：不接真实飞书、CRM / ERP / OA / 工单系统，不处理真实客户隐私、合同、订单、报价、联系方式或生产会话，不启用 LLM。

## 1.1 AI 场景：查看演示效果

当用户在 AI CLI 中说“我想看演示效果”“我想看 H5 演示效果”“帮我启动本机 Demo”“给我 H5 二维码”“检查 Demo 是否起来”等类似表达时，AI 应把本文件作为项目级演示 SOP，并按以下流程执行或引导用户执行。

### 触发词

- “我想看演示效果”
- “我想看 H5 演示效果”
- “帮我启动本机 Demo”
- “给我 H5 二维码”
- “检查 Demo 是否起来”
- “手机扫码看 H5”

### AI 执行流程

1. 先读取本文件，确认这是 Phase1 本机 Mock Demo，不接真实外部系统。
2. 如果用户只问“怎么看”，只输出启动命令、访问地址、二维码位置和演示路径，不运行命令。
3. 如果用户明确要求“启动 / 帮我启动”，运行 `scripts/start-local-demo.ps1`，并提示脚本会打开 3 个 PowerShell 窗口。
4. 启动后运行或引导用户运行 `scripts/check-local-demo.ps1`，确认后端、H5、Console 均可访问。
5. 输出电脑访问入口、手机扫码入口和 `.ai/local-demo-h5-qr.svg` 路径。
6. 若手机扫码失败，按 §6 常见问题检查同 Wi-Fi / 局域网、Windows 防火墙、`-LanHost <电脑局域网IP>`。
7. 不安装依赖、不引入新依赖、不启动 Docker / PostgreSQL / 外部 SaaS / LLM，不提交或推送代码。

### AI 输出模板

```text
本机 Demo 入口：
- H5 客户页（电脑）：http://127.0.0.1:5173
- H5 手机扫码：打开 .ai/local-demo-h5-qr.svg
- Web 控制台：http://127.0.0.1:5174
- 后端 API 文档：http://127.0.0.1:8000/docs

建议演示路径：
1. H5 提问产品咨询 / 项目咨询 / 售后 / 进度 / 未知问题。
2. 观察回答依据、Mock 口径、转人工、知识缺口。
3. 到 Web 控制台查看会话、待跟进、知识缺口、Mock 通知、日报摘要。
```

## 2. 启动前提

- 在仓库根目录执行命令。
- 本机可用 `python`、`node`、`npm.cmd`。
- 前端依赖已安装；如果缺少 `node_modules/`，先分别进入 `frontend/customer-h5` 与 `frontend/console` 执行 `npm.cmd install`，新增或升级依赖前仍需人工确认。
- Docker / PostgreSQL / pgvector 不是 Phase1 Demo 前置；当前 Demo 默认使用 Mock / 本地临时数据。
- PowerShell 如遇 `npm.ps1` 执行策略拦截，使用 `npm.cmd`。

## 3. 一键启动

在仓库根目录运行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/start-local-demo.ps1
```

脚本会分别打开 3 个 PowerShell 窗口：

| 服务 | 端口 | 地址 |
|---|---:|---|
| 后端 API | 8000 | `http://127.0.0.1:8000` |
| H5 客户页 | 5173 | `http://127.0.0.1:5173`；手机扫码用脚本输出的 `http://<电脑局域网IP>:5173` |
| Web 控制台 | 5174 | `http://127.0.0.1:5174` |

脚本会自动尝试识别电脑局域网 IP，并生成 H5 二维码 SVG：`.ai/local-demo-h5-qr.svg`。手机扫码前确保手机和电脑连接同一个 Wi-Fi / 局域网；若脚本未识别到正确 IP，可手动指定：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/start-local-demo.ps1 -LanHost 192.168.1.10
```

启动后检查：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check-local-demo.ps1
```

如果检查失败，通常是服务还在启动、端口被占用或某个窗口报错；先查看对应 PowerShell 窗口日志，再重新运行检查脚本。

## 4. 手动启动

如果不使用一键脚本，可以开 3 个 PowerShell 窗口分别执行。

### 4.1 后端 API

```powershell
$env:PYTHONPATH='backend'
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

检查地址：

- 健康检查：`http://127.0.0.1:8000/health`
- API 文档：`http://127.0.0.1:8000/docs`

### 4.2 H5 客户页

```powershell
cd frontend/customer-h5
npm.cmd run dev -- --host 0.0.0.0 --port 5173
```

电脑访问：`http://127.0.0.1:5173`。手机访问需要使用电脑局域网 IP，例如 `http://192.168.1.10:5173`。

### 4.3 Web 控制台

```powershell
cd frontend/console
npm.cmd run dev -- --port 5174
```

访问：`http://127.0.0.1:5174`。

## 5. 推荐演示路径

1. 打开 H5 客户页：电脑访问 `http://127.0.0.1:5173`；手机扫码访问 `.ai/local-demo-h5-qr.svg` 对应的局域网地址。
2. 选择或使用默认场景包，依次尝试产品咨询、项目咨询、售后、高风险问题、未知问题、进度查询。
3. 观察回答是否标明依据、Mock / Demo 口径、转人工或知识缺口。
4. 打开 Web 控制台：`http://127.0.0.1:5174`。
5. 查看会话列表、待跟进、知识缺口、Mock 通知、日报摘要。
6. 如需看接口响应，可打开 `http://127.0.0.1:8000/docs`，或访问下列只读 API：
   - `http://127.0.0.1:8000/api/v1/scenario-packs`
   - `http://127.0.0.1:8000/api/v1/conversations`
   - `http://127.0.0.1:8000/api/v1/handoffs`
   - `http://127.0.0.1:8000/api/v1/knowledge-gaps`
   - `http://127.0.0.1:8000/api/v1/notifications/mock`
   - `http://127.0.0.1:8000/api/v1/summaries/daily`

## 6. 常见问题

| 现象 | 处理 |
|---|---|
| `npm.ps1 cannot be loaded` | 使用 `npm.cmd`，不要直接用 `npm`。 |
| `address already in use` / 端口被占用 | 关闭旧服务窗口，或用脚本参数改端口：`-BackendPort`、`-H5Port`、`-ConsolePort`。 |
| H5 / Console 页面打不开 | 确认对应 Vite 窗口没有报错，再运行 `scripts/check-local-demo.ps1`。 |
| 手机扫码打不开 H5 | 确认手机和电脑在同一 Wi-Fi / 局域网；确认 H5 以 `--host 0.0.0.0` 启动；检查 Windows 防火墙是否拦截 Node / Vite；必要时用 `-LanHost <电脑局域网IP>` 重启。 |
| `.ai/local-demo-h5-qr.svg` 打不开 | 这是本地生成文件，可用浏览器打开；若不存在，重新运行 `scripts/start-local-demo.ps1`。 |
| 后端接口打不开 | 确认后端窗口显示 Uvicorn 已启动，并访问 `/health`。 |
| Docker 不可用 | Phase1 Demo 不依赖 Docker；保持 Mock / 本地临时数据即可。 |
| 看到 Mock 数据 | 这是预期行为；Phase1 不接真实业务系统。 |

## 7. 关闭服务

关闭一键脚本打开的 3 个 PowerShell 窗口，或在各窗口按 `Ctrl+C` 停止服务。
