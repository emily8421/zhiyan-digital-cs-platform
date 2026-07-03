# 输入材料评审记录 · zhiyan-digital-cs-platform

> **定位**：输入评审记录（`docs/meetings/`）。本记录是新项目生成 `docs/00-09` 前的输入评审与关键决策落点，属长期事实。
> **评审日期**：2026-07-01
> **评审依据**：`ai/prompts/docs/01-review-inputs.md`
> **评审输入**：`docs/inputs/` 下 `platform-vision-brief.md`、`ZY_PRD01_产品构想_产品方案_知衍数字客服_V1.0_20260627.md`、`产品型客户_工作日想定_V4.0.md`、`项目型客户_工作日想定_XS_V2.0.md`、`agent-delivery-modes.md`
> **关联**：旧项目 `digital-cs-demo` 已软冻结（标签 `product-demo-sample-2026-07-01`，已 push），作为产品型客户场景包 POC 参考（见 `platform-vision-brief.md` §2.2、§7）。

---

## 1. 输入类型判断

- **主入口**：Vision-first（`platform-vision-brief.md` 全景愿景总纲 + 产品构想愿景级叙事）。
- **辅助输入**：External-input（两份工作日想定 = 产品型/项目型场景叙事；agent-delivery-modes = 交付决策输入）；Existing-system（`digital-cs-demo` 作为产品型场景包 POC，跨项目引用）。
- 混合输入，主入口清晰，材料互补不冲突。

## 2. 推荐文档剖面

**Full**：有持久化 + 对外接口/多入口 + 外部系统集成 + 运营闭环 → `00-09` 全保留（含 `06/07`）+ `vision/product-vision.md` + `docs/design/*`（7 层架构子系统）+ `docs/decisions/`。与 `platform-vision-brief.md` §6.1 一致。

## 3. 生成准备度

**Conditionally Ready** —— 可铺 `vision` + `00-09` 完整骨架（含阶段标签）；`03` 路线图 / `04-05` 架构技术栈 / `08` 计划要写细，依赖下方决策。

## 4. 已确认决策（本次评审 · 2026-07-01，人工拍板）

| 决策项 | 结论 |
|---|---|
| 第一阶段主打场景包 | **产品型 + 项目型 两者最小样例**（体现"统一平台 + 多场景包"价值） |
| 客户侧第一入口 | **H5 对话页**（零安装、扫码即用，Demo 阶段最快验证闭环） |
| 员工侧入口 | **飞书机器人（通知/转交）+ Web 控制台（运营/日报/知识确认）并存** |
| 售中能力（订单/项目进度查询） | **Mock 数据演示**（架构预留集成层，Demo 阶段不接真实系统） |

## 5. 采用默认值（待人工最终确认，AI 据此起草 `project-rules` 草稿）

| 项 | 默认值 | 依据 |
|---|---|---|
| 售后能力 | 规则内引导 + 高风险一律转人工，**AI 不做高风险裁决** | 沿用 Demo 红线 + brief §4.4 |
| 技术栈 | 沿用 `digital-cs-demo`：Python + FastAPI + PostgreSQL/pgvector + Docker TEI；**LLM Demo 阶段不启用**（保"不编造"红线） | brief 未指定；Demo 已验证可行 |
| Demo 复用 | `digital-cs-demo` 作为产品型场景包参考实现，迁移**经验 + 部分设计**，不直接改造 | brief §7 |
| 阶段路线 | 新路线 P0–P4（brief §6.6），当前细化 P0/P1；交付物形态 Demo | brief §6.6 |

## 6. 待确认缺口

| 级别 | 项 | 说明 |
|---|---|---|
| 🟡 | 本机运行环境/资源约束 | 需 `scripts/collect-env.ps1` 采集 `docs/env/local-env.md` |
| 🟡 | `ai/project-rules.md` §0–§3 | 项目名/Phase 边界/技术栈/形态裁剪待填（AI 可基于本评审起草草稿） |
| 🟡 | 合规前提阶段化 | 双链路中"监控链路（企微会话存档）"依赖企业认证 + 客户同意，**Demo 阶段不依赖，仅做对话链路（H5）**；监控链路留 MVP |

> ✅ **已澄清（2026-07-01）**：两份工作日想定是**两个独立场景**，非版本替换——
> - `产品型客户_工作日想定_V4.0.md`（汇辰灯饰/灯带采购，对应 brief §2.2 产品型客户场景包，也是 `digital-cs-demo` Demo 场景来源）
> - `项目型客户_工作日想定_XS_V2.0.md`（星栎科技/智能家居方案商，对应 brief §2.3 项目型客户场景包）
> 两份均已纳入并按场景类型重命名。

## 7. inputs 归属建议

| 输入 | 归属 |
|---|---|
| `platform-vision-brief.md` | 留 `docs/inputs/` 作总纲 |
| 产品构想 | → `docs/vision/product-vision.md` 主骨架来源 |
| `产品型客户_工作日想定_V4.0.md` | → 产品型场景包（`docs/vision/scenarios/product-business.md` 或 `docs/inputs/scenario-packs/product-business.md`） |
| `项目型客户_工作日想定_XS_V2.0.md` | → 项目型场景包（`docs/vision/scenarios/project-business.md` 或 `docs/inputs/scenario-packs/project-business.md`） |
| agent-delivery-modes | → `docs/decisions/delivery-entry-selection.md`（H5 / 飞书+Web 已初定，其余形态留远期） |

## 8. 横切权威源建议（`docs/decisions/`）

- **DEC**：微信客户群自动回复已证伪（继承 `digital-cs-demo` Sprint-0 结论，`sprint-0-wework-findings.md`）。
  - ⚠️ **与 V4.0 想定前提冲突**：`产品型客户_工作日想定_V4.0.md` §13 以"企微客户群机器人对外自动回复"为前提叙事，该能力已被 Sprint-0 证伪。新项目客户入口已决策用 **H5**（不依赖群内自动回复），V4.0 的群内场景仅作"产品型客户期望形态"参考，不作为 Demo 通道实现。
- **DEC**：售后高风险不 AI 裁决。
- **DEC**：无外部数据转人工不编造（业务进度查询无数据时降级转人工）。
- **DEC**：交付入口（客户=H5，员工=飞书+Web 控制台）。

## 9. 生成 `00-09` 的下一步计划（建议在本项目新会话执行）

1. 新会话先读 `ai/index.md` 列出的全部规则 + 本评审记录 + `docs/inputs/`。
2. 填 `ai/project-rules.md` §0–§3（AI 起草草稿，基于第 4、5 节决策与默认）。
3. 运行 `scripts/collect-env.ps1`，补 `docs/env/local-env.md`。
4. 按 `ai/prompts/docs/00-generate-or-complete-docs.md` 分阶段生成（建议顺序）：
   `vision/product-vision.md` → `00` → `01` → `02` → `03`（P0/P1 细化）→ `04`（7 层架构）→ `05` → `06` → `07` → `08` → `09` → `docs/design/*`（7 层子系统）→ `docs/decisions/*`（第 8 节）→ 改写根 `README.md`。
5. 阶段标签：当前 P0/P1，交付物形态 Demo（v1.7.0 双维度）。

## 10. 给新会话的启动提示

参考 `docs/inputs/platform-vision-brief.md` §9 提示词，并将本记录第 4、5 节决策作为已确认约束代入；第 6 节缺口作为待确认项标注。
