# TEMPLATE-UPGRADE-v1.6.9：区分旧派生同步流程并新增派生边界检查

## 状态

- 状态：已随本次模板改动落地，归档留痕
- 目标版本：v1.6.9
- 提案来源：派生项目同步模板方法论时误用模板仓库完整性自检的问题复盘

## 背景

`scripts/check-template.sh` / `scripts/check-template.ps1` 是模板仓库完整性自检，会检查 `_examples/`、模板 PR 模板、模板归档区和完整样例结构。旧派生项目同步模板方法论后，如果把它作为同步成功判断，会因为派生项目本来不应具备这些模板仓库内容而大量失败，造成误导。

同时，v1.6.8 之前的旧派生项目通常缺少 `scripts/sync-template.ps1`、`template-sync.json` 或新版 `sync-template.sh`，首次同步不能直接走 v1.6.8+ 的 PowerShell 入口。

## 目标

1. 在 `git-guide.md` §5 明确区分旧派生项目首次同步路径与 v1.6.8+ 后续同步路径。
2. 在 `INIT-PROMPT.md` §12 同步更新可复制 Prompt，要求先做路径判定。
3. 明确派生项目同步后不运行模板仓库自检，只检查同步边界和最近提交。
4. 新增 `scripts/check-derived-sync.sh` / `scripts/check-derived-sync.ps1`，只校验最近同步提交是否限定在 `template-sync.json` 清单内。
5. 更新 README、SOP、MAINTAINERS、CHANGELOG、VERSION、`template-sync.json` 和模板自检断言。

## 拟改范围

- `VERSION`：升级到 `v1.6.9`。
- `CHANGELOG.md`：新增 v1.6.9 记录。
- `git-guide.md`：拆分派生项目同步路径，禁止用模板自检验收派生同步。
- `INIT-PROMPT.md`：更新 §12 同步 Prompt。
- `SOP.md` / `README.md` / `MAINTAINERS.md`：更新入口说明和命令。
- `scripts/check-derived-sync.sh` / `scripts/check-derived-sync.ps1`：新增派生同步边界检查入口。
- `template-sync.json` / `scripts/sync-template.sh`：纳入新增检查脚本。
- `scripts/check-template.sh`：新增 v1.6.9 自检断言。

## 版本影响

- 版本类型：PATCH。
- 理由：修正同步流程说明并新增派生同步边界检查脚本，不改变 docs 00-09 编号体系，也不改变项目专属文件的同步边界。

## 验证方式

- 运行 `git diff --check`。
- 运行 `powershell -ExecutionPolicy Bypass -File scripts/check-template.ps1`。
