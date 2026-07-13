# TEMPLATE-UPGRADE：Codex sandbox 远端操作防卡死 SOP

> 来源：zhiyan-digital-cs-platform（emily8421/zhiyan-digital-cs-platform）派生项目回流
> 类型：模板优化提案草稿
> 状态：待提交模板仓 issue
> 关联：`ai/session-rules.md`、`ai/commands/README.md`、`git-guide.md`、`ai/prompts/git/*`、远端 PR / issue / merge / push 收口流程

## 背景

多个派生项目在 Codex CLI sandbox 环境中执行远端 Git / GitHub 操作时，反复遇到凭据、权限、askpass、网络或子进程执行差异。典型场景包括提交后推送、创建 PR、合并 PR、关闭 issue、查询远端 Actions 或启动需要子进程的前端工具。

这些问题通常不是项目代码失败，而是 sandbox 与宿主机凭据 / 进程权限 / 网络边界不一致导致。若 AI 未能及时识别，会出现反复重试、长时间无响应、误判用户未登录、误判远端不存在、或在操作已成功后仍继续排查的问题。

## 问题

- sandbox 内 `git push` 可能读取不到宿主机 Git 凭据，触发 `GIT_ASKPASS` / VS Code askpass 权限错误。
- sandbox 内 `gh auth status` 可能显示 token invalid，但宿主机 GitHub CLI 实际可用。
- sandbox 内远端操作可能返回 `Repository not found` / `Authentication failed`，实际根因是认证隔离而非仓库不存在。
- sandbox 内 Node / Vite / Git / shell 子进程可能出现 `spawn EPERM`、signal pipe、permission denied 等权限错误。
- AI 容易把“sandbox 权限 / 凭据 / 网络问题”当作“项目实现失败”或“用户未配置环境”，从而反复换命令、重复 push / gh 操作，形成卡住或长时间无输出。
- 提交、推送、PR 创建、合并、关闭 issue 等远端状态变更缺少统一的重试上限和停止规则。
- 成功的远端操作与后续 handoff / 状态刷新混在一起时，用户难以判断到底是 push 卡住、刷新卡住，还是 AI 仍在做别的检查。

## 建议改动

### 1. 增加 Codex sandbox 远端操作总原则

在 `ai/session-rules.md` 或 `git-guide.md` 中新增一节：Codex sandbox 下的远端操作治理。

建议口径：

- sandbox 内优先做本地只读检查：`git status --short --branch`、`git log --oneline -3`、`git diff --check`。
- 远端写操作包括 `git push`、`gh pr create`、`gh pr merge`、`gh issue close`、`gh release` 等；这些操作若依赖宿主机凭据，应允许 AI 直接说明风险并请求 sandbox 外执行。
- 远端只读但依赖认证的操作，如 `gh pr view`、`gh run watch`、私有仓 `gh issue list`，也应按认证敏感操作处理。
- AI 不得把 sandbox 内认证失败直接判定为用户未登录或仓库不存在，必须标注“sandbox 内凭据不可用 / 待宿主机复核”。

### 2. 增加疑似 sandbox 错误识别表

建议在 `git-guide.md` 或新增 Prompt / SOP 中加入分类表：

| 错误信号 | 默认判定 | AI 动作 |
|---|---|---|
| `Permission denied`、`askpass`、`GIT_ASKPASS`、VS Code askpass 路径失败 | sandbox / 凭据权限疑似问题 | 停止普通重试，请求 sandbox 外执行或让用户本机执行 |
| `token invalid` 但用户声称已登录 | sandbox 凭据隔离疑似问题 | 不要求用户重新登录；先用 sandbox 外只读认证检查 |
| `Repository not found` + 私有仓 / 已知可访问仓 | 认证失败可能伪装成仓库不存在 | 标注不确定，sandbox 外复核 |
| `spawn EPERM`、signal pipe、子进程创建失败 | sandbox 子进程权限问题 | 不改项目代码；请求 sandbox 外运行同一命令验证 |
| DNS / registry / network blocked | sandbox 网络限制疑似问题 | 不更换依赖方案；请求授权或停止记录 |

### 3. 增加重试上限

建议模板规则明确：

1. 同一远端动作最多两步：
   - sandbox 内尝试一次；
   - 若出现疑似 sandbox / 凭据 / 权限 / 网络错误，则请求 sandbox 外执行一次。
2. sandbox 外仍失败时，必须停止并报告，不得继续换参数反复重试。
3. 远端写操作失败后，必须立刻做一次只读事实核对：
   - `git status --short --branch`
   - `git log --oneline -3`
   - 对 `gh issue create` / `gh pr create`，用标题或分支搜索确认是否已创建半成品。
4. 若远端操作已经成功，后续 handoff / 文档刷新失败不得遮蔽成功事实；最终回复必须先说明“远端已完成”。

### 4. 增加远端操作前后固定输出

建议模板要求 AI 在执行 push / PR / merge / issue 操作前后输出最小状态摘要：

执行前：

```text
Git 状态：...
本地 HEAD：...
将执行的远端动作：...
是否可能需要 sandbox 外凭据：是 / 否
```

执行后：

```text
远端动作结果：成功 / 失败 / 不确定
本地 HEAD：...
远端状态：已同步 / ahead / 未复核
后续本地收尾：handoff / 文档 / 清理服务
```

### 5. 增加命令路由

建议在 `ai/commands/README.md` 增补远端收口类命令，或新增：

- `remote-git-ops`：提交后推送、PR 创建、PR merge、issue 关闭、Actions 检查。
- `pr-closure`：PR 检查、合并、删除分支、关闭 issue、刷新 handoff。

命令要求：

- 先区分本地 Git 事实与远端事实。
- 远端写操作必须说明是否需要 sandbox 外凭据。
- 遇到疑似 sandbox 错误立即切换到授权路径或停止，不进入循环。
- 输出“完成了什么 / 没完成什么 / 是否已推送 / 是否已合并”。

### 6. 增加 handoff 记录字段建议

建议 `.ai/session-handoff.md` 的远端任务记录增加：

- `Local HEAD`
- `Remote synced to`
- `Remote action status`
- `Sandbox issue encountered`
- `Escalated command result`

这样下次恢复时能一眼判断是 push 未完成，还是 push 已完成但后续刷新被中断。

### 7. 增加确认后 checkpoint 与长任务可见性规则

建议在 `ai/session-rules.md`、`ai/commands/README.md` 或通用执行规则中增加：当用户明确确认“是 / 按建议执行 / 继续 / 同意”等执行授权后，AI 必须在进入长命令、远端操作或复杂生成前，先完成一个可审计 checkpoint。

可接受的 checkpoint 包括：

- 更新 `.ai/session-handoff.md` 为 `active / executing`，写明任务目标、预计修改文件、下一步命令和阻塞项。
- 创建目标草稿文件，至少写入标题、来源标识、状态和待补章节。
- 输出 `git status --short --branch`、当前 HEAD 和“即将执行的第一步”。
- 对需要等待用户反馈的任务，先写明“等待哪一项反馈、当前已完成什么、服务 / 端口是否仍运行”。

建议禁止项：

- 用户确认后，不得长时间只做内部分析而没有任何可见状态变更。
- 不得在进入 `git push`、`gh issue create`、`gh pr merge`、`npm build`、服务启动等可能卡住的命令前，不记录当前 checkpoint。
- 工具调用被中断或用户下一轮质疑“为什么没执行”时，AI 必须先检查是否已有部分文件、提交、远端动作或运行进程，再继续；不得假设未执行或已完成。

该规则能降低“用户已经确认，但 AI 像没执行 / 卡住不出来”的体验问题，也能让跨 CLI 续接时快速判断任务卡在哪一步。

## 版本影响

- 类型：模板方法论 / Codex CLI 执行治理增强。
- 建议版本：MINOR。
- 影响范围：所有派生项目的 Git / GitHub / PR / issue / merge / demo build / frontend build 等依赖宿主机凭据或子进程权限的流程。
- 兼容性：不要求项目改代码；主要修改规则、SOP、命令路由和提示词。

## 影响面

- `ai/session-rules.md`：增加 sandbox 凭据 / 权限异常识别、重试上限、停止规则。
- `git-guide.md`：增加 Codex sandbox 下远端操作 SOP。
- `ai/commands/README.md`：增加远端操作路由和常见说法。
- `ai/prompts/git/*` 或新增 Prompt：规范 push / PR / merge / issue 收口输出。
- `template-docs/session-handoff.example.md`：可选增加远端同步字段样例。
- 通用执行规则 / 命令入口：增加用户确认后的 checkpoint 要求，避免长任务无可见进度。

## 验收建议

- 在 sandbox 内模拟 `git push` 触发 askpass / permission denied，AI 应停止普通重试并请求 sandbox 外执行。
- 在 sandbox 内模拟 `gh auth status` token invalid，但宿主机 `gh auth status` 正常，AI 应正确标注为 sandbox 凭据隔离。
- 在 sandbox 内模拟 Vite `spawn EPERM`，AI 不应修改代码或依赖，应请求 sandbox 外运行同一 build / dev 命令。
- 执行一次 push 成功但 handoff 刷新中断的场景，新会话应能从 Git 事实判断远端已同步。
- 用户等待期间，AI 应在关键远端动作完成后立即输出状态，避免用户误以为 push 卡住。
- 用户确认“按建议执行”后，AI 应先产生 checkpoint（handoff、草稿文件或状态输出），再进入长命令；若中断，下一轮能通过 checkpoint 判断执行进度。

## 禁止项

- 不得在认证 / askpass / permission / spawn 类错误上无限重试。
- 不得把 sandbox 内认证失败直接写成用户未登录、仓库不存在或远端状态失败。
- 不得为绕过 sandbox 问题修改项目业务代码、替换依赖或改变技术方案。
- 不得在远端写操作结果不明时继续执行 merge / close / delete branch 等后续动作。
- 不得在最终回复中模糊“本地提交完成”和“远端推送完成”。
- 不得在用户确认执行后长时间无 checkpoint、无文件变更、无状态输出。

## 后续处理建议

1. 将本提案提交到模板仓 issue，标签建议：`proposal`、`from:zhiyan-digital-cs-platform`。
2. 模板维护者合并时，优先改 `git-guide.md` 与 `ai/session-rules.md`，再考虑新增命令文件。
3. 下行同步后，派生项目可在远端操作中直接引用该 SOP，减少重复排查。
