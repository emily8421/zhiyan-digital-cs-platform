# TEMPLATE-UPGRADE-v1.6.3：修正下行同步 dry-run 差异方向

## 状态

- 状态：已随本次模板改动落地，归档留痕
- 目标版本：v1.6.3
- 提案来源：派生项目同步 dry-run 预览异常反馈

## 背景

派生项目运行 `bash scripts/sync-template.sh --dry-run` 时，预览统计出现“模板新增文件在派生项目中显示为删除”的反向结果，例如 `scripts/check-template.sh`、`scripts/collect-env.ps1` 被显示为 `0 ins / 全删除`。

原因是 dry-run 使用了 `git diff "$REF" -- "$f"` / `git diff --stat "$REF" -- "$f"`。该方向表示“从模板远端版本变成本地版本”，而下行同步真实动作是 `git checkout "$REF" -- "$f"`，即“从本地版本变成模板远端版本”。因此预览与实际同步方向相反。

## 目标

1. 修正 `scripts/sync-template.sh --dry-run` 的差异判断与统计方向。
2. 让 dry-run 预览表达“执行 --commit 后本地将变成什么”。
3. 避免将模板新增内容误显示为删除，降低派生项目同步误判风险。
4. 升级模板版本到 `v1.6.3`，作为脚本修复补丁。

## 拟改范围

- `VERSION`：升级到 `v1.6.3`。
- `README.md`：新增 `v1.6.3` 版本记录。
- `scripts/sync-template.sh`：dry-run 改用本地 → 模板方向的 diff。
- `scripts/check-template.sh`：检查同步脚本包含正确方向的 dry-run 逻辑。
- `_archive/proposals/TEMPLATE-UPGRADE-v1.6.3-sync-dry-run-direction.md`：本提案归档。

## 版本影响

- 版本类型：PATCH。
- 理由：修复同步脚本 dry-run 预览方向，不改变同步清单或核心流程。

## 验证方式

- 运行 `git diff --check`。
- 运行 `bash -n scripts/sync-template.sh scripts/check-template.sh`。
- 运行 `bash scripts/check-template.sh`。

