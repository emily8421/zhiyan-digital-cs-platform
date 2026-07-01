# TEMPLATE-UPGRADE-v1.6.6：README 瘦身与 docs 分区约束

## 状态

- 状态：已随本次模板改动落地，归档留痕
- 目标版本：v1.6.6
- 提案来源：模板易用性复盘与派生项目 docs 混杂问题反馈

## 背景

v1.6.5 后模板对新项目更易用，但 README 承载了过多维护者信息：同步清单、版本历史、治理细节和裁剪表都混在用户入口里。普通使用者只想快速启动项目，却需要浏览大量模板维护内容。

同时，派生项目在 AI 编程过程中出现了新问题：AI 需要新增文档时，常直接把文档放进 `docs/` 根目录，导致核心 `00-09` 文档、调研记录、详细设计、会议纪要和临时材料混在一起，长期演进后难以维护。

## 目标

1. 瘦身根 `README.md`，只保留 5 分钟路径、入口导航、常用命令、目录速览和最近版本摘要。
2. 新增 `MAINTAINERS.md`，承载模板维护原则、发布 checklist、同步清单维护和 CI / 自检说明。
3. 新增 `CHANGELOG.md`，承载完整版本记录，README 只保留最近摘要。
4. 新增 `docs/README.md`，定义派生项目文档分区规则。
5. 将子系统详细设计约定从 `docs/design-<子系统>.md` 调整为 `docs/design/<子系统>.md`。
6. 在 `ai/global-rules.md`、`ai/project-rules.md`、`INIT-PROMPT.md` 和自检脚本中约束 AI 不得把新增文档直接放到 `docs/` 根目录。

## 文档分区方案

`docs/` 根目录只放：

- `README.md`
- `00-scenario.md` ~ `09-verification.md`

新增文档按类型进入子目录：

- `docs/vision/`：愿景、叙事、业务背景等输入材料
- `docs/design/`：子系统 / 模块详细设计
- `docs/decisions/`：ADR 与重要取舍
- `docs/research/`：技术调研、竞品分析、实验结论
- `docs/env/`：本机环境、资源约束、服务器预案
- `docs/meetings/`：会议纪要、访谈记录、评审记录
- `docs/archive/`：废弃但需留痕的项目文档

AI 新增文档前必须先判断文档类型；不确定时先提出建议路径并等待人工确认。

## 拟改范围

- `VERSION`：升级到 `v1.6.6`。
- `README.md`：瘦身为普通使用者入口。
- `MAINTAINERS.md`：新增维护者说明。
- `CHANGELOG.md`：新增完整版本记录。
- `docs/README.md`：新增 docs 分区规则。
- `docs/design/`、`docs/decisions/`、`docs/research/`、`docs/meetings/`、`docs/archive/`：新增占位目录。
- `ai/global-rules.md`、`ai/project-rules.md`、`INIT-PROMPT.md`：更新 docs 分区和 `docs/design/` 约定。
- `scripts/new-project.sh`：派生项目 README 指向 `docs/README.md` 和 `docs/design/`。
- `template-sync.json`：新增 `MAINTAINERS.md`、`CHANGELOG.md`、`docs/README.md`。
- `scripts/check-template.sh`：新增分区、自检和版本断言。

## 版本影响

- 版本类型：PATCH。
- 理由：优化入口信息架构和文档组织约束，不改变核心开发流程和同步机制。

## 验证方式

- 运行 `git diff --check`。
- 运行 `powershell -ExecutionPolicy Bypass -File scripts/check-template.ps1`。
