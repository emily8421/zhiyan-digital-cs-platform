# Vision To Product（主样例）

本样例演示最常见的 AI 编程起点：**先有一份产品愿景文档，再让 AI 抽取工程文档并进入 Sprint 开发**。

## 样例项目

- 项目名：Knowledge Companion
- 形态：本地优先的个人知识助手
- Phase1：保存知识条目、生成摘要、按关键词检索、查看详情
- Phase2：标签、多项目知识库、导出、向量检索

## 为什么作为主样例

这个样例不是为了展示某个技术栈，而是展示完整工作流：

```text
产品愿景 → 00 场景 → 01 用户需求 → 02 SRS → 03 PRD → 04 架构
→ 05 技术方案 → 06 数据设计 → 07 接口契约 → 08 开发计划 → 09 验证计划
```

## 阅读顺序

1. 读 `docs/vision/product-vision.md`：这是人工输入的愿景，不直接驱动编码。
2. 读 `docs/00-scenario.md` ~ `docs/02-srs.md`：看愿景如何被抽取为需求事实。
3. 读 `docs/03-prd.md`：看 Phase 路线图如何成为阶段标签来源。
4. 读 `ai/project-rules.md`：看项目形态、技术栈、裁剪和禁区如何约束 AI。
5. 读 `docs/08-dev-plan.md` 与 `docs/09-verification.md`：看 Sprint 如何与验证闭环。

## 文档裁剪

- `docs/06-db-design.md`：保留。Phase1 使用本地 SQLite 持久化知识条目。
- `docs/07-api-spec.md`：保留。Phase1 用 CLI 命令契约描述对外接口。
- `docs/09-verification.md`：保留。所有项目必备，用 REQ → 用例矩阵定义“怎么算对”。

## 使用方式

新项目不要从本目录复制；应从模板根目录创建项目，再把自己的愿景放入 `docs/vision/product-vision.md`，先用 `ai/prompts/docs/01-review-inputs.md` 评审输入材料，再用 `ai/prompts/docs/00-generate-or-complete-docs.md` 生成项目文档体系。
