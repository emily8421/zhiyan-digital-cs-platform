# Quick Script（轻量愿景样例）

本样例演示：**项目很小，也可以从愿景文档开始，但不需要保留完整重型文档**。

## 样例项目

- 项目名：Meeting Notes Cleaner
- 形态：本地 Python CLI 小脚本
- Phase1：读取一份会议纪要文本，清理空白、统一项目符号、输出整理后的文本
- 文档裁剪：无数据库、无对外 API，因此省略 `docs/06-db-design.md` 与 `docs/07-api-spec.md`

## 轻量路径重点

轻量项目不是跳过设计，而是把设计压缩到最小可验证闭环：

```text
愿景 → 00 场景 → 01 需求 → 02 SRS → 03 PRD → 04 架构 → 05 技术方案 → 08 开发计划 → 09 验证计划
```

## 阅读顺序

1. 读 `docs/vision/product-vision.md`：看一个很小的愿景如何表达。
2. 读 `ai/project-rules.md` §3：看为什么省略 `docs/06` 和 `docs/07`。
3. 读 `docs/08-dev-plan.md`：看如何只拆一个 Sprint。
4. 读 `docs/09-verification.md`：看小脚本如何定义验收口径。

## 适用场景

- 一次性脚本
- 本地自动化小工具
- 无数据库、无公开 API、无长期复杂演进的小项目

如果项目后来增长为长期产品，应补充缺失设计，并重新评估是否需要 `docs/06`、`docs/07`。
