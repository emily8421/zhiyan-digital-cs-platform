# TEMPLATE-UPGRADE: check-template 防文档滞后断言

> 类型：模板仓库内直接发起（去项目化）。
> 状态：已落地于 v1.18.2（2026-06-28）；随 PR #38 合并，从 `_proposals/` 归档到 `_archive/proposals/`。
> 关联：根目录文档审计（PR #37）发现的根因——脚本层已对 `_scaffold`/16 闭环有断言，但人读操作文档没有断言保护，导致 v1.17/v1.18 引入这些机制时操作文档滞后。

## 1. 现状与问题

v1.17.0（16 号审计）+ v1.18.0（`_scaffold` 镜像）落地时，脚本层与提示词层已自洽：`check-template.sh` 有断言强制 15→16 链接、sync 含 `_scaffold`、`check-derived-sync` 放行 `_scaffold`、`docs/README` 说明 `_scaffold`、16 提示词对照 `_scaffold`。但**根目录人读操作文档**（`git-guide §5` / `SOP` / `MAINTAINERS`）滞后——CHANGELOG v1.18.0 列了要改的脚本/文档，漏了操作权威 `git-guide.md §5`。

PR #37 事后补齐了文档内容，但**没有断言防止再次滞后**。根因：`check-template` 的 `require_contains` 断言覆盖了脚本/提示词/`docs/README` 引用 `_scaffold`，却**没要求 `git-guide`/`SOP`/`MAINTAINERS` 引用 `_scaffold`/16 闭环**。未来再引入类似机制并更新脚本时，人读文档可能再次漏更新，且自检无法捕获。

## 2. 拟改

在 `check-template.sh` 的 `_scaffold` 断言组后，加一组「防文档滞后」断言，要求根目录操作文档引用当前关键机制：

- `git-guide.md` 含 `docs/_scaffold`（§5.6 `_scaffold` 镜像说明）
- `git-guide.md` 含 `16-docs-system-audit`（§5.5 同步→15→16 闭环）
- `SOP.md` 含 `16-docs-system-audit`（场景索引 16 号审计行）
- `MAINTAINERS.md` 含 `require_scaffold_mirror`（自检章节 `_scaffold` 镜像自检说明）

关键词选稳定标识（`docs/_scaffold`、`16-docs-system-audit`、`require_scaffold_mirror`），不绑长文案——符合 MAINTAINERS「自检不过度绑定长文案，优先稳定关键词」。

## 3. 版本影响

**PATCH：v1.18.1 → v1.18.2。** 仅增强自检断言，不改方法论 / 编号 / 同步机制。`check-template.sh` 在同步清单内，派生项目下行同步会拿到新断言（断言只对模板仓库自检生效，不改变派生项目行为）。

## 4. 影响面

- `scripts/check-template.sh`（加 4 个断言）
- `VERSION` / `CHANGELOG.md` / `README.md` 摘要
- 不改任何文档内容（断言验证的是 #37 已补的文档引用，当前都满足）

## 5. 验收

- `bash scripts/check-template.sh` 通过（新断言对当前文档 pass，因为 #37 已补 `git-guide §5.6/§5.5`、SOP 16 行、MAINTAINERS `require_scaffold_mirror`）。
- 若有人删掉这些文档引用，自检会 fail（防护生效）。

## 6. 风险

低。断言用稳定关键词，不会因文案微调误报。唯一注意：未来若重构 `git-guide`/`SOP` 的 `_scaffold`/16 引用措辞，需同步更新断言模式——但这正是断言的目的（强制保持引用）。
