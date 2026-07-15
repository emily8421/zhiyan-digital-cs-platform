# TEMPLATE-UPGRADE：sync-template PowerShell fallback 提交 pathspec 过长风险

> 来源：zhiyan-digital-cs-platform（emily8421/zhiyan-digital-cs-platform）派生项目回流
> 类型：模板优化提案草稿
> 状态：已提交模板仓 issue，待模板维护者处理
> 模板仓 issue：https://github.com/emily8421/ai-project-template/issues/217
> 关联：`scripts/sync-template.ps1`、派生项目同步 `--commit --preserve-project-version`、PowerShell fallback、A13 同步闭环

## 1. 背景

派生项目同步到模板 v1.52.4 时，本机 Git Bash 因 `couldn't create signal pipe, Win32 error 5` 无法启动，脚本按预期进入 PowerShell fallback。

`--dry-run --no-stat --preserve-project-version` 已正常完成，风险路径为 none；`--commit --preserve-project-version` 也成功覆盖并 stage 了同步清单文件，但在执行内部 `git commit -q -m ... -- <大量路径>` 时失败，输出显示很长的文件 pathspec 被展开并最终报 `failed with exit code 1`。

工作区检查显示所有同步文件已正确 staged、无 unstaged 差异，因此本次采用等价安全动作：手动执行 `git commit -m "sync template v1.52.4 from ai-project-template"`，随后 `scripts/check-derived-sync.ps1 <sync-commit>` 通过。

## 2. 问题

- PowerShell fallback 在同步文件数量较多时，把全部已更新文件作为 pathspec 传给 `git commit`，容易触发命令行长度、参数展开或 PowerShell / Git pathspec 兼容问题。
- 失败发生在文件已覆盖、已 stage 之后；如果 AI 不先检查 index 状态，可能误判为同步失败并重复执行，增加混乱风险。
- A13 同步闭环要求记录真实命令，但当前脚本无法自动完成 commit，派生项目需要人工等价替代。

## 3. 建议改动

### 3.1 commit 阶段避免传超长 pathspec

在 PowerShell fallback 的 `--commit` 路径中，完成文件覆盖和 `git add` 后，优先使用：

```powershell
git commit -q -m "sync template $version from ai-project-template"
```

而不是把全部 `$updatedFiles` 作为 pathspec 传入。前置条件是脚本已经要求工作区干净，并且只 stage 自己同步的文件；此时不传 pathspec 更稳妥。

### 3.2 如仍需限制 pathspec，使用 pathspec 文件

若维护者认为必须限定提交文件，可考虑生成临时 pathspec 文件，再使用 Git 支持的 pathspec-from-file 机制，避免命令行参数过长。

### 3.3 失败提示增加恢复步骤

当 commit 阶段失败但存在 staged 同步文件时，脚本应提示：

1. 运行 `git status --short --branch`。
2. 确认仅同步清单文件 staged。
3. 可手动执行 `git commit -m "sync template vX.Y.Z from ai-project-template"` 作为等价替代。
4. 随后运行 `scripts/check-derived-sync.ps1 <sync-commit>`。

## 4. 验收建议

- 在 Windows PowerShell fallback 环境中模拟 Git Bash 不可用。
- 使用包含 50+ 变更文件的同步清单执行 `--commit --preserve-project-version`。
- 确认脚本能自动创建同步提交，且 `check-derived-sync` 通过。
- 确认失败路径不会重复覆盖、不会误改项目专属文件，并输出可恢复指引。

## 5. 非目标

- 不改变同步清单范围。
- 不要求修复 Git Bash / MSYS 本机权限问题；fallback 本来就是该场景的替代路径。
- 不改变派生项目双版本语义。

## 6. 影响范围

- 所有在 Windows PowerShell fallback 下执行派生项目模板同步的普通派生项目。
- 模板同步版本差异较大、变更文件数量较多时风险更高。
