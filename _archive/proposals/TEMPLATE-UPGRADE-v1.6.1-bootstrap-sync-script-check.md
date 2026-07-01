# TEMPLATE-UPGRADE-v1.6.1：下行同步脚本 bootstrap 与自检保护

## 状态

- 状态：已随本次模板改动落地，归档留痕
- 目标版本：v1.6.1
- 提案来源：派生项目同步 SOP 风险复盘

## 背景

派生项目执行下行同步时，通常依赖本地已有的 `scripts/sync-template.sh` 判断需要更新哪些文件。但如果该脚本本身不是最新版，就可能产生以下问题：

- `SYNC_FILES` 漏掉新增模板文件，例如 `VERSION` 或 `scripts/collect-env.ps1`。
- 版本解析仍使用旧规则，例如从 `ai/global-rules.md` 读取两段式版本，而不是从 `VERSION` 读取三段式版本。
- 旧版 `--dry-run` 行为可能不是真 dry-run，存在修改工作区或 stage 文件的风险。

因此，派生项目不能无条件信任本地旧版同步脚本，需要在同步前先 bootstrap / 对比模板远端最新版脚本。

## 目标

1. 增强 `scripts/sync-template.sh`：执行前抓取模板远端后，先对比远端最新版脚本与本地脚本。
2. 若脚本不同，停止同步，提示用户先用远端脚本覆盖本地脚本并单独提交。
3. 更新 `git-guide.md` 和 `INIT-PROMPT.md`，把 bootstrap 最新同步脚本作为派生项目同步 SOP。
4. 更新 `scripts/check-template.sh`，将同步脚本自检和 SOP 文档纳入模板自检。
5. 将模板版本从 `v1.6.0` 升级到 `v1.6.1`，作为补丁级治理增强。

## 拟改范围

- `VERSION`：升级到 `v1.6.1`。
- `README.md`：新增 `v1.6.1` 版本记录。
- `scripts/sync-template.sh`：增加远端自身脚本对比；旧脚本时停止并提示 bootstrap 步骤。
- `scripts/check-template.sh`：检查同步脚本包含自身更新保护，文档包含 bootstrap 步骤。
- `git-guide.md`：更新下行同步标准流程，明确先 bootstrap 最新脚本。
- `INIT-PROMPT.md`：更新 §12 下行同步 Prompt，要求先抓取 / 对比最新版 `sync-template.sh`。
- `_archive/proposals/TEMPLATE-UPGRADE-v1.6.1-bootstrap-sync-script-check.md`：本提案归档。

## 版本影响

- 版本类型：PATCH。
- 理由：不改变模板核心结构；增强已有同步流程的安全性与兼容性。

## 验证方式

- 运行 `git diff --check`。
- 运行 `bash -n scripts/sync-template.sh scripts/check-template.sh scripts/new-project.sh`。
- 运行 `bash scripts/check-template.sh`。

