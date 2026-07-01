# 参考样例

本目录存放**填好的参考样例项目**，帮助理解“从愿景文档到 AI 编程交付”的完整路径。

新项目应从**模板根目录**复制或用 `scripts/new-project.sh` 创建；本目录仅供学习对照，不作为新项目起点。

## 我该看哪个样例？

| 你的起点 / 项目形态 | 推荐样例 | 重点看什么 |
|---|---|---|
| 先有一份产品愿景，希望 AI 生成工程文档并进入开发 | `vision-to-product/` | 愿景文档如何抽取为 `docs/00-09`，以及 Phase1 如何进入 Sprint |
| 项目很小，只是脚本 / 小工具 | `quick-script/` | 如何走轻量路径，保留最少文档但仍有验收口径 |
| 有数据库 + 对外 API，需要完整闭环 | `todo-api/` | `docs/06-db-design.md`、`docs/07-api-spec.md`、`docs/09-verification.md` 如何联动 |

## 推荐阅读顺序

1. 先看 `vision-to-product/OVERVIEW.md`，理解主流程。
2. 再看 `vision-to-product/docs/vision/product-vision.md`，它是项目起点。
3. 对照 `vision-to-product/docs/00-09`，理解 AI 如何把愿景拆成工程文档。
4. 最后看 `vision-to-product/ai/project-rules.md`，理解 Phase、技术栈、裁剪与禁区如何约束 AI。
