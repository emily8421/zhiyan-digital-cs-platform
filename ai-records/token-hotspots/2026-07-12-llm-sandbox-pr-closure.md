# Token Hotspot 观察记录：LLM Sandbox PR 收口

> 本文件为 AI 协作观察记录，不替代 `.ai/session-handoff.md`、`docs/08-dev-plan.md` 或 `docs/09-verification.md`。
> 本记录不包含 token、密钥、完整对话、客户敏感数据或隐私事实。

## 元数据

- 日期：2026-07-12
- 任务：续接 `feat/llm-sandbox-adapter-mock` 分支的提交 / 推送 / PR 创建收口
- 触发原因：从中断续接进入远端 PR 收口；按项目规则完整读取 `ai/index.md` 及其规则清单；随后执行 Git / GitHub 状态复核与 PR 创建。
- 状态：已记录

## Hotspot 来源

1. **规则读取成本较高**
   - 本轮从中断日志恢复后进入提交 / 推送 / PR 创建等状态变更任务，需完整读取 `ai/index.md` 指向的规则文件。
   - `ai/document-lifecycle-rules.md` 内容较长，且终端输出曾发生截断，需要分段补读以确保规则门禁完整。

2. **续接信息与 Git 事实不一致**
   - `.ai/session-handoff.md` 指向旧的 PR #40 闭环任务。
   - 当前 Git HEAD 与用户贴出的中断日志指向新任务 `feat/llm-sandbox-adapter-mock`，因此需以 Git 事实重建上下文。

3. **沙箱内外 GitHub CLI 凭据差异**
   - 沙箱内 `gh auth status` 显示 token invalid。
   - 沙箱外提权只读检查显示 GitHub CLI 已正常登录。
   - 该差异导致需要额外复核认证状态，并使用沙箱外认证完成 `gh pr create`。

4. **远端收口输出需要最小化摘要**
   - GitHub 预检、推送、PR 创建、PR 查看均产生可审计输出。
   - 收尾时只保留 PR 编号、URL、分支、状态与关键阻塞原因，避免重复携带长日志。

## 质量影响

- 正面：完整规则读取避免了在旧 handoff 误导下继续错误任务；Git 事实优先的恢复路径正确识别了当前提交与远端分支状态。
- 成本：规则分段读取、凭据差异排查与 PR 状态确认增加上下文与命令轮次。
- 风险：若未区分沙箱内外凭据，可能误判为用户未登录 GitHub CLI，从而中断可继续的 PR 创建流程。

## 优化建议

1. **续接文件更新**
   - PR 创建后可在后续收尾中刷新 `.ai/session-handoff.md`，避免继续保留旧 PR #40 作为最新 handoff。
   - 若只做一次性 PR 创建，可在最终回复中明确 Git 事实已覆盖旧 handoff。

2. **凭据诊断提示**
   - 当沙箱内 `gh auth status` 失败但用户声明已登录时，优先用提权只读 `gh auth status` 区分“真实未登录”和“沙箱凭据隔离”。
   - 输出中避免展示 token 明文，仅说明认证来源和状态。

3. **长规则读取摘要化**
   - 对必须完整读取但输出易截断的规则文件，保留“已分段补读”的执行事实即可，不在收尾重复粘贴规则正文。
   - 后续若频繁触发同类任务，可考虑在模板层补充更明确的 PR 收口快捷命令，减少重复上下文装载。

## 本轮关键结果摘要

- 本地提交：`117386f feat: add LLM Sandbox adapter (mock-first) for evidence-backed answer rewriting`
- 远端分支：`origin/feat/llm-sandbox-adapter-mock`
- PR：`https://github.com/emily8421/zhiyan-digital-cs-platform/pull/41`
- PR 状态：`OPEN`
- 残留边界：真实 LLM 调用仍受 `RG-003` / `DOC-C-005` / 安全与成本授权约束，当前仅为 mock-first sandbox adapter 收口。
