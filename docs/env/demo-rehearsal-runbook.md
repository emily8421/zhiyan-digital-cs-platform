# 正式演示前彩排 SOP

> 定位：本文件是正式对外演示前的**彩排演练流程**，归属 `docs/env/`。它编排「启动 → 演示主线 → 检查 → 收尾」的彩排步骤；详细演示话术指向 `external-demo-script.md`，详细检查项指向 `formal-demo-checklist.md`，启动细节指向 `local-demo-runbook.md`。它不替代这三份文档，也不替代 `docs/09-verification.md` 的验收记录。
> 适用：每次正式对外演示前、里程碑（Mxx）发布后、或演示脚本 / 功能 / 环境变更后，都应照本 SOP 彩排一次。

## 1. 什么时候彩排

- 正式对外演示（客户沟通 / 内部评审 / 售前预演）前一天或当天开始前。
- 里程碑（Mxx）验收通过、演示脚本或功能有变更后。
- 演示环境（网络 / IP / 端口 / 防火墙）可能变化时。

## 2. 彩排前置：启动与可达性

1. 确认端口空闲；正式演示建议用演示端口 `8021` / `5195` / `5196`，避开开发常用端口（`8000` / `5173` / `5174`）。
2. 启动三端（详见 `local-demo-runbook.md`）：

   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts/start-local-demo.ps1 -BackendPort 8021 -H5Port 5195 -ConsolePort 5196
   ```

3. 健康检查（详见 `formal-demo-checklist.md` §4）：

   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts/check-local-demo.ps1 -BackendPort 8021 -H5Port 5195 -ConsolePort 5196
   ```

   通过标准：`6 / 6 reachable`，且 H5 / Console identity marker 匹配本项目。不通过则先排查端口占用 / 前端代理目标 / 启动窗口日志，**不要继续彩排**。

## 3. 彩排步骤（照演示脚本走一遍）

入口（以启动脚本实际输出为准）：H5 `http://127.0.0.1:5195` ｜ Console `http://127.0.0.1:5196`。

### 3.1 开场话术（约 30 秒）

照 `external-demo-script.md` §2，确认讲清：本机 Demo / Mock 数据 / 有依据回答 / 可追溯不编造 / 真实系统未接入。

### 3.2 H5 演示主线

照 `external-demo-script.md` §3.1~§3.4 依次走：产品知识 → 进度查询 → 高风险转人工 → 未知缺口。
- 每条回复后确认**来源徽章**显示正常（来源模式 + `source_ref`）。

### 3.3 Console 演示主线

照 `external-demo-script.md` §3.5~§3.6 走：运营闭环（会话 / 待跟进 / 缺口 / 通知 / 日报 / 角色权限）+ Product Sandbox 新卖点（虚拟客户资料 / 来源标识全链路 / 数据源模式门禁 / 一键重置）。

### 3.4 手机扫码复核

照 `formal-demo-checklist.md` §6：扫码打开 H5，发一个问题确认收到回答，Console 看到联动数据。

## 4. 彩排检查点

照 `formal-demo-checklist.md` §8 逐项确认。当前（M11）必看点：

- 顶部 `Demo Sandbox` / `真实系统未接入` / `LLM 默认关闭` 标识。
- Mock 数据列表带 `environment` / `source_system` / `source_ref`。
- **虚拟客户资料**：场景包切换后完整画像可见，全程标识模拟。
- **来源标识抽样区（API-016）**：来源列表全 `demo_sandbox` / `mock=true`；H5 回复带来源徽章。
- **数据源模式门禁**：admin 试切真实模式显式 No-Go。
- **一键重置**：当前场景包运行态可重置。
- 角色权限：admin 可写、viewer 写操作禁用。

> 演示前可用 Console「重置演示运行态」清干净当前场景包运行态，确保演示数据处于初始态。

## 5. 彩排反馈与问题记录

彩排中记录：

- 哪些演示点不顺 / 话术别扭 / 报错。
- 是否所有必看点都正常展示。
- 演示总时长是否可控（建议主线 5~8 分钟）。

发现的问题分类处理：

- **脚本 / 清单问题**（话术别扭、漏点）→ 更新 `external-demo-script.md` / `formal-demo-checklist.md`。
- **功能 / 数据问题**（报错、展示缺失）→ 走 bug 修复流程；演示前修复，或记录为已知限制并准备话术。
- **环境问题**（网络 / 端口 / 防火墙）→ 按 `local-demo-runbook.md` §6 排查。

## 6. 收尾

1. 关闭 3 个服务窗口（或各窗口 `Ctrl+C`）；可选核对端口释放（见 `formal-demo-checklist.md` §9）。
2. 把彩排结果落盘成 `docs/research/YYYY-MM-DD-demo-rehearsal-*.md`：环境、走完的步骤、发现的问题、是否通过、后续动作。
3. 若改了演示脚本 / 清单，提交并同步本 SOP 的检查点（§4）。

## 7. 关联文档

- 启动手册：`docs/env/local-demo-runbook.md`
- 对外演示脚本（话术）：`docs/env/external-demo-script.md`
- 正式演示检查清单：`docs/env/formal-demo-checklist.md`
- 最近彩排记录：`docs/research/2026-07-13-formal-demo-rehearsal.md`、`docs/research/2026-07-16-task-011e-product-sandbox-rehearsal.md`
