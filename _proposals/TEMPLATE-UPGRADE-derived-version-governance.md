# TEMPLATE-UPGRADE：派生项目版本管理机制默认启用与存量迁移

> 来源：zhiyan-digital-cs-platform（emily8421/zhiyan-digital-cs-platform）派生项目回流
> 类型：模板优化提案草稿
> 状态：已提交模板仓 issue，待模板维护者处理
> 模板仓 issue：https://github.com/emily8421/ai-project-template/issues/221
> 关联：`VERSION`、`CHANGELOG.md`、`TEMPLATE-BASE.md`、`scripts/new-project.sh`、`.github/workflows/project-check.yml`、`ai/project-rules.md`、`scripts/check-derived-sync.*`、`scripts/check-template.*`、双版本机制（v1.46.0）

## 1. 背景

模板已建立双版本机制：派生项目 `VERSION` 记录项目自有版本，`TEMPLATE-BASE.md` 记录继承的模板版本（v1.46.0 起）。但模板只提供了「版本骨架」（文件 + 双版本分离声明），没有提供「版本机制」（递增规则 + 一致性校验 + 启用路径）。

在一个已推进到 MVP 验收阶段的派生项目中复盘发现：`VERSION` 自双版本迁移后长期停滞、`CHANGELOG.md` 项目版本段只有基线一条、CI 不校验版本、`ai/project-rules.md` 无任何版本规则。这是结构性缺口，而非单个项目疏忽。

## 2. 问题

### 2.1 新建派生项目不启用版本机制

`scripts/new-project.sh` 生成的派生项目：

- `.github/workflows/project-check.yml` 只有空白检查 + 同步边界检查，**不含版本一致性校验**。
- `ai/project-rules.md` 的「首次必填 checklist」不含版本管理项；种子无版本规则 section。
- `VERSION` 初始为**模板当时版本号**（继承语义遗留，见 `new-project.sh` `Project version at sync time: $TEMPLATE_VERSION`），不是项目自有的干净起点（如 `v0.1.0`）。

### 2.2 存量派生项目同步新模板后无启用路径

版本机制的部件（`ai/project-rules.md` 版本 section、`project-check.yml` 校验 step、`VERSION` 自有语义）多为**项目自有文件，不随 `sync-template` 自动下行**（`project-rules.md`、`project-check.yml` 不在同步清单；`VERSION` / `CHANGELOG.md` 受 `--preserve-project-version` 保护）。因此早期派生项目同步新模板方法论后，不会自动获得版本机制，也没有启用 / 迁移引导。

### 2.3 模板无通用默认

没有「派生项目自有版本 bump 规则」的通用默认，每个派生项目重新发明一套，违背模板沉淀复用经验的初衷。

## 3. 沿现有实现（可复用）

- `scripts/check-template.sh:122-135` `require_changelog_current_version`：读 `VERSION`、要求 `CHANGELOG.md` 含 `## {版本}（`、要求顶部版本 == `VERSION` 的成熟逻辑，可直接作为派生 CI 校验参考。
- `readme-version-check`（v1.24.3，回流自派生）：`scripts/check-derived-sync.*` 已有「非阻断告警」模式（读 VERSION + 扫文档版本声明，不一致告警、不计入失败），可作为存量启用状态检测的先例。
- 双版本机制（v1.46.0）：`sync-template` 的 `--preserve-project-version` 已保护项目自有 `VERSION` / `CHANGELOG.md` 不被覆盖；`TEMPLATE-BASE.md` 已分离模板继承版本。

## 4. 建议改动

### 4.1 模板提供派生版本 bump 规则的通用默认（半通用，派生可改）

在 `TEMPLATE-BASE.md` 的 Version Semantics 或 `new-project.sh` 生成的 `ai/project-rules.md` 种子中，提供通用语义化默认：

- **PATCH**：bug 修复、文档 / 配置 / 重构，不新增可演示能力、不破坏对外契约。
- **MINOR**：可感知的能力增强或里程碑交付，向后兼容。
- **MAJOR**：不兼容变更、对外契约破坏、首上线。

明确标注「派生项目可按自身交付节奏覆盖」，不绑定具体阶段 / Sprint 概念。

### 4.2 new-project 默认启用版本机制

- 生成的 `.github/workflows/project-check.yml` 增加 `Check project version consistency` step：`VERSION` 三段式 + `CHANGELOG.md` 顶部第一个 `## vX.Y.Z（` 标题等于 `VERSION`。逻辑借鉴 `require_changelog_current_version`，但**不做全文档降序检查**（派生 CHANGELOG 顶部项目版本下方接数值更大的模板历史版本，降序不适用）。
- 生成的 `ai/project-rules.md` 种子增加「项目版本管理」section（通用默认 + 可改提示）；首次必填 checklist 增加「版本规则」项。
- `VERSION` 初始改为项目自有 `v0.1.0`（修正继承模板版本号的遗留），`TEMPLATE-BASE.md` 仍记录模板继承版本。

### 4.3 存量派生项目启用路径（迁移）

- **检测**：在 `scripts/check-derived-sync.*` 增加非阻断告警（仿 `readme-version-check` 先例）：检测 VERSION 是否仍为继承语义、`project-rules.md` 是否缺版本 section、`project-check.yml` 是否缺版本校验 step；未启用即提示，不计入同步失败。
- **引导**：`post-sync-cleanup` 或同步后整理步骤引导一次性启用：VERSION 重定义为项目自有语义、补 `project-rules.md` 版本 section、补 CI 校验 step、`CHANGELOG.md` 补「项目版本」段。
- **一次性人工确认**：参照双版本机制（v1.46.0）迁移先例，版本基线重定义需人工确认，不自动改写。

### 4.4 模板落地与防回归

- `scripts/check-template.*` 增加断言：`new-project.sh` 生成的派生 CI 含版本校验 step、`project-rules` 种子含版本 section、`VERSION` 初始 `v0.1.0`。
- `template-docs/scenario-guides.md`、`MAINTAINERS.md`、`CONTRIBUTING.md`、`TEMPLATE-BASE.md` 配套说明派生版本机制启用与迁移。

## 5. 验收建议

- **新建烟测**：`new-project.sh` 生成派生项目后，确认 `VERSION=v0.1.0`、`project-check.yml` 含版本校验、`ai/project-rules.md` 含版本 section；故意改错 VERSION 验证 CI 红。
- **存量迁移烟测**：用一个 `VERSION`=继承语义、无版本 section 的早期派生项目，同步新模板后确认检测告警 + 引导启用成功、CI 校验通过。
- `scripts/check-template.sh` 自检全过。

## 6. 非目标

- 不规定派生项目具体 bump 触发业务语义（留给派生），只给通用默认。
- 不强制 git tag / release workflow（保持可选）。
- 不改双版本语义（VERSION / TEMPLATE-BASE 分离不变）。
- 不改同步清单范围（`ai/project-rules.md`、`project-check.yml` 仍为项目自有）。

## 7. 影响范围

- 所有普通派生项目（新建 + 存量）。
- 模板：`scripts/new-project.sh`、`project-check.yml` 生成逻辑、`ai/project-rules.md` 种子、`scripts/check-derived-sync.*`、`post-sync-cleanup`、`scripts/check-template.*`、`TEMPLATE-BASE.md` 及相关文档。

## 8. 版本影响（供模板维护者判断）

- 建议按模板版本规则判断为 **MINOR**：新增模板能力（派生版本机制默认启用 + 存量迁移路径），向后兼容，不影响已同步派生项目的现有行为（存量为非阻断检测 + 人工确认引导）。
- 不兼容点：`new-project.sh` 生成的 `VERSION` 初始值从「继承模板版本号」改为 `v0.1.0`——仅影响**新建**派生项目，对已存在项目无影响。
