# TEMPLATE-UPGRADE-v1.6.4：新增 SOP 索引

## 状态

- 状态：已随本次模板改动落地，归档留痕
- 目标版本：v1.6.4
- 提案来源：标准操作流程分散度评估

## 背景

模板已经沉淀了多类标准操作流程：新建派生项目、初始化文档、采集环境、执行 Sprint、审查、同步模板、模板优化回流、版本发布等。当前这些流程分布在 `README.md`、`git-guide.md`、`INIT-PROMPT.md`、`CONTRIBUTING.md` 等文件中。

虽然职责划分已经明确：

- `git-guide.md`：操作 SOP 权威文档。
- `INIT-PROMPT.md`：可复制给 AI 的 Prompt。
- `CONTRIBUTING.md`：模板治理规则。
- `README.md`：快速入口与版本记录。

但缺少一张“当前场景应该看哪个 SOP”的总索引，导致用户和 AI 容易在多个文件之间跳转时迷路。

## 目标

1. 新增 `SOP.md`，作为标准操作流程导航索引。
2. 不在 `SOP.md` 中重复完整命令，只提供场景 → 权威操作文档 → 可复制 Prompt → 备注。
3. 在 `README.md` 中加入 `SOP.md` 入口与版本记录。
4. 在 `scripts/check-template.sh` 中检查 SOP 索引存在且覆盖关键场景。
5. 版本升级为 `v1.6.4`，作为文档导航补丁。

## 拟改范围

- `VERSION`：升级到 `v1.6.4`。
- `SOP.md`：新增 SOP 索引。
- `README.md`：目录说明和版本记录加入 `SOP.md`。
- `scripts/check-template.sh`：检查 `SOP.md` 存在并包含新建项目、派生同步、环境采集、模板回流等关键场景。
- `_archive/proposals/TEMPLATE-UPGRADE-v1.6.4-sop-index.md`：本提案归档。

## 版本影响

- 版本类型：PATCH。
- 理由：新增文档导航，不改变模板核心流程和同步机制。

## 验证方式

- 运行 `git diff --check`。
- 运行 `bash scripts/check-template.sh`。

