# task-009d-console-knowledge-tab

## 目标

在 Console 前端新增「知识条目」Tab（独立 Tab），让运营通过 UI 管理知识库：查看列表（draft/active/archived）、转正（draft→active）、归档、手动新增 draft 知识候选；接 API-006 GET/POST/PATCH；admin 可写、viewer 只读。补齐知识闭环的运营 UI 最后一公里。

## 输入文档

- `docs/design/web-console.md` §4.4（知识条目管理设计）、§5（文案）。
- `docs/design/frontend-interaction.md` §8（接口依赖）。
- `docs/07-api-spec.md` API-006。

## 修改范围

- `frontend/shared/types.ts`：加 `KnowledgeItemRecord`。
- `frontend/shared/apiClient.ts`：加 `listKnowledgeItems` / `createKnowledgeItem` / `updateKnowledgeItemStatus`。
- `frontend/console/src/App.tsx`：加 Tab + `KnowledgeItemList` 组件（列表 / 转正 / 归档 / 新增表单）+ handler。
- `frontend/console/src/styles.css`：加 success/neutral badge 颜色 + 表单样式。
- 更新 `docs/env/local-demo-runbook.md`、`docs/08-dev-plan.md`、`docs/09-verification.md`。

## 验收标准

- Console 出现「知识条目」Tab。
- 列表展示知识条目，状态颜色区分（active 绿「已生效·问答可命中」/ draft、archived 灰）。
- admin 可转正（draft→active）、归档（active→archived）、表单新增 draft；viewer 只读。
- `npm run build` 通过。
- 真实闭环：缺口 accepted → 知识条目 Tab 看到 draft → 转正 active → H5 再问命中。

## 禁止事项

- 不启用 LLM，不接外部系统。
- 不改后端 API（task-009b/009c 已完成）。
- 不引入新前端依赖。

## 完成记录

- 2026-07-11：Console 新增「知识条目」Tab（独立），列表 + 转正 + 归档 + 新增表单（admin），viewer 只读；状态颜色区分（success/neutral）。
- 改动文件：`frontend/shared/types.ts`、`frontend/shared/apiClient.ts`、`frontend/console/src/App.tsx`、`frontend/console/src/styles.css`。
- 验证通过：`npm run build`（tsc + vite build）通过，17 modules transformed；TC-055 人工浏览器验收暂未发现问题。
- 边界：未改后端；未引入新依赖；LLM 默认关闭未变。
- 后置项：暂无。若后续需要提升操作体验，可单独评估缺口状态中文化、accepted 后提示 draft 入库和跳转知识条目页。
