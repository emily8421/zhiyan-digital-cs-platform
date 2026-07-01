# TEMPLATE-UPGRADE: 00-09 撰写规范同步机制（规范与项目事实分离）

> 类型：派生项目起草的模板优化提案（去项目化）。
> 状态：已落地于 v1.18.0（2026-06-28），并于 v1.20.0 迁移主路径为 `ai/doc-standards/00-09`；从 `_proposals/` 归档到 `_archive/proposals/`。
> 关联：补 sync-template 的规范同步缺口；与 `document-lifecycle-rules.md` §5（生成矩阵）、review 类提示词、`TEMPLATE-UPGRADE-docs-system-audit-prompt.md` 互补。

## 1. 现状与问题（已 fetch 模板核对）

- **模板 `docs/00-09` 是规范样板**：每份含「文档定位 / 上游输入 / 下游输出」+ §0 文档元信息表 + 各章「撰写提要」+ 骨架表格 + 占位（`ACT-001` / `YYYY-MM-DD` / 空单元格），**不含项目事实**。
- **`template-sync.json` 不含 `docs/00-09`**（只含 `docs/README.md` + `docs/inputs/README.md`）。这是**正确**的——派生项目的 `docs/00-09` 是项目事实，不能被覆盖。

**矛盾**：模板 `00-09` 承担双重角色——模板侧是「规范样板」，派生侧是「项目事实占位」。sync 不同步它们 → 模板对 00-09 撰写规范的演进（新增章节、调整撰写提要、补质量标准）**传不到派生项目** → 派生项目重评审/重生成 00-09 时**缺规范基准**，只能凭提示词的零散描述，易偏离或漏新规范。

**派生项目实证**：v1.9.0 同步后想「按最新规范重审 00-09」，发现模板的撰写提要（如 00-scenario 的 §0 文档元信息表、§2 `ACT-ID` 角色规范、§3 `SC-ID` 场景规范）无法对照——派生项目的 00-09 是早期生成的，未必含这些新结构，且没有基准可查。

## 2. 设计目标

- 把模板 `00-09` 的**撰写规范**同步到派生项目。
- **绝不覆盖**派生项目的 `docs/00-09` 项目事实。
- 评审/重生成时，AI 能对照规范基准梳理 00-09。
- 最小侵入模板现有结构。

## 3. 拟改（两套方案，主推 B'）

### 方案 B'（主推·最小侵入）：模板 docs/00-09 骨架镜像到派生项目只读目录

- sync-template 增加一步：把模板 `docs/00-09` 复制到派生项目 `docs/_scaffold/00-09`（下划线前缀＝模板规范镜像，**只读、非项目事实**）。
- 派生项目自己的 `docs/00-09` **完全不动**；物理路径分离保证不覆盖。
- `docs/README.md` 增加 `_scaffold/` 分区说明：模板 00-09 撰写规范镜像，随模板版本刷新，**不作为项目事实、不直接驱动开发**；改动须走 `_proposals/` 回流模板。
- `template-sync.json` + `check-derived-sync`：把 `docs/_scaffold/*` 纳入同步清单与边界允许范围（属模板同步件，非项目事实）。
- **评审用法**：AI 读 `docs/_scaffold/00-09`（规范）+ `docs/00-09`（项目现状），按 `document-lifecycle-rules.md` §5/§10 对照，输出「偏离/缺失规范项 + 回梳建议」。

### 方案 A（备选·长期更干净）：规范 / 实例分离

- 模板把 00-09 的「撰写规范」（定位/元信息/撰写提要/必备章节/质量标准）提取到 `ai/doc-specs/00-09.md`，纯规范、无完整骨架表格。
- `template-sync.json` 纳入 `ai/doc-specs/*`。
- 模板 `docs/00-09` 保留为模板自己的实例（或改为引用 spec）。
- 评审对照 `doc-specs` 的「必备章节 + 质量标准」。
- 成本：模板需重构抽取；好处：规范与实例彻底分离，无镜像冗余。

> **建议**：先落地 B'（零模板重构、立即解渴），待模板侧有重构窗口再演进到 A。两者评审用法一致。

## 4. 评审闭环（与 review 类提示词联动）

- 配合 `TEMPLATE-UPGRADE-docs-system-audit-prompt.md`（已起草）：审计提示词增加一步「对照 `docs/_scaffold` 规范，核查项目 00-09 的章节完整性与撰写质量」。
- 或增强 `review/10-docs-checklist.md`：B 段补「对照 `docs/_scaffold/00-09`，核查项目 00-09 是否含必备章节（文档元信息表 / 撰写提要对应内容 / 追溯矩阵）」。

## 5. 版本影响

B' 可作 v1.9.x / v1.10.0 增量；A 作后续大版本。依赖现有 sync-template 机制（加镜像步骤）。

## 6. 影响面

- `scripts/sync-template.sh` / `.ps1`：增加 `docs/00-09` → `docs/_scaffold/` 镜像步骤。
- `template-sync.json`：纳入 `docs/_scaffold/*`。
- `docs/README.md`：增加 `_scaffold/` 分区说明。
- `scripts/check-derived-sync.*`：允许 `docs/_scaffold/*` 在同步提交内。
- 评审提示词 / checklist：增加「对照 scaffold」步骤。
- 派生项目：获得 `docs/_scaffold/00-09` 规范镜像；自己的 `docs/00-09` 不变。

## 7. 验收口径

- sync 后派生项目有 `docs/_scaffold/00-09`（模板规范），且自己的 `docs/00-09` 逐字未变。
- `check-derived-sync` 不把 `docs/_scaffold` 误判为项目事实越界。
- 评审时 AI 能用 scaffold 对照项目 00-09，输出章节缺失 / 规范偏离清单。
- 模板更新 00-09 撰写提要后，下次 sync 能刷新 scaffold，派生项目获知。

## 8. 风险

- scaffold 与项目 00-09 主题相似，可能混淆「规范 vs 事实」→ 靠 `_scaffold/` 前缀 + README 说明 + 文件头标注缓解。
- 镜像增加派生项目文件数（+10）→ 可接受（只读规范，且能被 .gitignore 之外正常跟踪）。
