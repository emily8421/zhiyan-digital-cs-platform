# TEMPLATE-UPGRADE：Demo 端口占用与页面身份校验

> 来源：zhiyan-digital-cs-platform（emily8421/zhiyan-digital-cs-platform）派生项目回流
> 类型：模板优化提案草稿
> 状态：已提交模板仓 issue，待模板维护者处理
> 模板仓 issue：https://github.com/emily8421/ai-project-template/issues/184
> 关联：`template-docs/demo-runbook-template.md`、`ai/commands/show-demo.md`、Demo 启动 / 检查脚本模板、`docs/env/*demo*.md`

## 背景

派生项目执行本机 Demo smoke test 时，仅检查前端端口 HTTP 200 不足以证明访问的是当前项目页面。如果本机已有其他项目占用相同端口，检查脚本可能把“其他项目的页面”误判为当前 Demo 可用。

## 问题

- 前端开发服务常用端口（如 5173 / 5174）容易被其他本地项目占用。
- Vite 默认可能在端口占用时漂移到其他端口，导致启动脚本与检查脚本口径不一致。
- Demo 检查只看 HTTP 200 时，无法识别页面是否属于当前派生项目。
- 本地二维码、运行端口和进程信息缺少统一状态文件，不利于续接排查。
- 启动脚本允许后端改端口时，前端开发服务的 `/api` 代理仍可能硬编码到默认后端端口，造成页面可访问但 API 请求 `ECONNREFUSED`。
- 外部演示脚本或 runbook 如果把默认端口写成固定入口，会在使用备用端口时误导演示人员。

## 建议改动

### 1. Demo Runbook 模板

在 `template-docs/demo-runbook-template.md` 中补充：

- 启动前必须确认默认端口未被其他服务占用。
- 若端口被占用，应停止占用进程或显式指定备用端口。
- 前端页面应包含项目专属 identity marker，例如：
  - `meta name="<project>-demo-app" content="customer-h5"`
  - `meta name="<project>-demo-app" content="console"`
- 检查脚本必须校验 marker，而不是只检查 HTTP 200。
- 检查脚本应覆盖前端 `/api` 代理链路，避免“页面 HTML 可访问但接口代理失败”的误判。
- 文档应明确“默认端口只是示例，实际入口以启动脚本输出 / runtime 状态文件为准”。
- 手机二维码和 runtime 状态文件属于本地产物，不得提交。

### 2. show-demo 命令

在 `ai/commands/show-demo.md` 中补充执行边界：

- “检查 Demo”应包含页面身份校验。
- “检查 Demo”应包含 H5 / Console 到后端的代理 API 检查。
- 若端口返回 200 但身份不匹配，应报告端口被其他本地应用占用，而不是说 Demo ready。
- 启动服务时应启用 strict port 或等价机制，避免隐式端口漂移。
- 若使用备用端口，AI 输出应引用启动脚本实际输出的 URL，不应继续复述默认端口。

### 3. 脚本建议

若模板未来提供通用 demo 脚本模板，应包含：

- 端口占用预检：输出端口、PID、进程名和命令行。
- Vite / 前端开发服务使用 strict port。
- check 脚本对每个前端入口校验 identity marker。
- check 脚本对关键前端入口访问至少一个只读 API 代理路径，确认前端代理目标与后端端口一致。
- 启动脚本写入 `.ai/local-demo-runtime.json`，记录端口、URL、LAN URL、二维码路径和进程 ID。
- 启动脚本将后端实际地址注入前端开发服务，例如通过 `DEMO_BACKEND_PROXY_URL` / `PROJECT_BACKEND_PROXY_URL` 等项目化环境变量，默认仍可回落到标准后端端口。
- runbook / external demo script 中的访问入口表应区分“默认示例端口”和“本次运行实际端口”。

## 版本影响

- 类型：模板方法论 / Demo SOP 安全性增强。
- 建议版本：PATCH 或 MINOR，取决于是否只改文档 / Prompt，还是新增通用脚本模板。

## 验收建议

- 构造端口被其他页面占用的场景，检查脚本应失败并提示 identity marker 不匹配。
- 使用备用端口启动当前项目 Demo，检查脚本应通过。
- 后端使用非默认端口启动时，H5 / Console 的 `/api` 代理检查应通过，不应继续请求默认端口。
- 外部演示脚本中默认端口引用必须标明“默认示例 / 以启动输出为准”。
- 运行产物 `.ai/local-demo-runtime.json` 和二维码应被 `.gitignore` 忽略。
