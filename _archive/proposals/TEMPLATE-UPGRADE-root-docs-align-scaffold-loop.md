# TEMPLATE-UPGRADE: 根目录文档追赶 `_scaffold` / 16 号审计闭环

> 类型：模板仓库内直接发起的文档同步修订提案（去项目化）。
> 状态：已落地于 v1.18.1（2026-06-28）；随 PR #37 合并，从 `_proposals/` 归档到 `_archive/proposals/`。
> 关联：补 v1.17.0（`16-docs-system-audit`）与 v1.18.0（`docs/_scaffold` 镜像）落地时遗漏的根目录人读文档更新。CHANGELOG v1.18.0 列了要改的文件（`sync-template` / `check-derived-sync` / `docs/README` / `check-template`），唯独漏了操作权威 `git-guide.md`。

## 1. 现状与问题

v1.17.0 + v1.18.0 在「脚本层 + 提示词层」已自洽建立闭环 `sync-template → 15-post-sync-cleanup → 16-docs-system-audit（对照 docs/_scaffold）`：

- `sync-template.sh` 镜像 `docs/00-09` → `docs/_scaffold/`；
- `check-derived-sync.sh:41` 放行 `docs/_scaffold/*`；
- `check-template.sh:246` 起有 `require_scaffold_mirror()` 自检；`:580-581` 断言强制 15→16 链接；
- `15-post-sync-cleanup.md` 指向 `16`；`16-docs-system-audit.md` 对照 `_scaffold`。

但「面向人读的根目录操作文档」没跟上脚本：

- **[H1]** `git-guide.md §5` 是下行同步的「操作 SOP 权威文档」，却完全没提 `_scaffold` 镜像。派生项目跑 `--dry-run` 会看到 `Δ docs/_scaffold/*`（新增规范镜像）条目，而 §5.2「不应出现」清单写「`docs/00-09` 不应出现」——用户极易把 `_scaffold/00-09` 误判为越界覆盖。
- **[M1]** `git-guide.md §5.5` 与 `SOP.md`「同步后项目整理」行只到 `15-post-sync-cleanup`，没接上 `15 → 16`（对照 `_scaffold`）。
- **[M2]** `MAINTAINERS.md` 自检/CI 与发布 Checklist 没提 `check-template.sh` 新增的 `_scaffold` 镜像自检。
- **[L1]** `MAINTAINERS.md` 文档分区列表漏 `inputs/`（`global-rules.md §5` 列了，`docs/` 实际有，sync 也同步它）。
- **[L2]** `README.md`「当前版本」历史条目仍用迁移前旧名（`BEGINNER-GUIDE.md` 等），v1.16.1 已迁到 `template-docs/` 并改名，与顶部导航现名自相矛盾。
- **[L3]** `CONTRIBUTING.md §8` 治理类变更记录停在 2026-06-23，且与 `CHANGELOG.md` 定位重叠，未说明是否继续维护。

## 2. 拟改（6 处，纯文档）

1. **[H1] `git-guide.md §5`** 新增 §5.6「`_scaffold` 规范镜像」小节：说明同步会新增只读 `docs/_scaffold/00-09`（模板撰写规范镜像）、不覆盖项目自己的 `docs/00-09`；dry-run 中 `docs/_scaffold/*` 的 Δ/新增是预期、不计越界，真正不能出现的是项目事实 `docs/00-09` 被改；该镜像供 `16-docs-system-audit.md` 做审计对照。§5.2 / §5.5「不应出现」清单旁补一句 `_scaffold` 例外。
2. **[M1]** `git-guide.md §5.5` 在提及 `15-post-sync-cleanup.md` 后补一句指向 `16-docs-system-audit.md`；`SOP.md`「同步后项目整理」行备注指向 16。
3. **[M2]** `MAINTAINERS.md`「自检与 CI」补一条说明 `check-template.sh` 现含 `_scaffold` 镜像自检（临时派生项目验证镜像生成、项目事实不变、边界检查通过）；发布 Checklist 加一条「若改了 `docs/00-09` 撰写规范，确认 `require_scaffold_mirror` 通过」。
4. **[L1]** `MAINTAINERS.md`「文档分区维护」补 `inputs/`（原始输入包）与 `archive/`。
5. **[L2]** `README.md` v1.16.1 条目标注现路径（`template-docs/`）。
6. **[L3]** `CONTRIBUTING.md §8` 顶部注明定位：治理类变更自 v1.6.5 起统一记入 `CHANGELOG.md`，本节保留早期基建记录、不再追加。

## 3. 版本影响

**PATCH：v1.18.0 → v1.18.1。** 改的都是 `template-sync.json` 同步清单内的文档文件（`git-guide` / `SOP` / `MAINTAINERS` / `README` / `CONTRIBUTING`），下行同步内容会变，派生项目应能通过 `VERSION` 感知。无编号体系 / 流程 / 同步机制变化。

## 4. 影响面

- 文档：`git-guide.md`、`SOP.md`、`MAINTAINERS.md`、`README.md`、`CONTRIBUTING.md`（均在同步清单）。
- 版本记录：`VERSION`、`CHANGELOG.md`、`README.md` 摘要。
- 不动任何脚本、`ai/` 规则文件、`ai/prompts/` 提示词、`template-sync.json` 清单。

## 5. 验收

- `bash scripts/check-template.sh` 通过（含 `_scaffold` 镜像自检等全部断言）。
- 人工核对上述 6 处修订到位，且 `VERSION` / CHANGELOG / README 三处版本一致。

## 6. 风险

纯文档修订，风险低。唯一需注意的是 [L3] 把 §8 定位改为「不再追加」属于治理约定调整，需在 PR 描述中点明。
