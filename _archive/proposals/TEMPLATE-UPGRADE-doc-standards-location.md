# TEMPLATE-UPGRADE: 文档规范镜像迁移到 AI 标准区

> 类型：模板仓库内直接发起的模板优化提案。
> 状态：待评估 / 待落地。
> 关联：延续 v1.18.0 `docs/_scaffold` 规范镜像机制；优化其命名与目录语义，避免与项目事实区 `docs/` 混淆。

## 1. 背景与问题

v1.18.0 起，`sync-template` 会把模板 `docs/00-09` 的撰写规范镜像到派生项目 `docs/_scaffold/00-09`，用于 `16-docs-system-audit` 对照项目自己的 `docs/00-09`，同时避免覆盖项目事实文档。

该机制本身有效，但当前路径与命名存在语义问题：

- `docs/_scaffold/` 位于 `docs/` 项目事实区之下，容易削弱“`docs/` 只放项目事实与项目文档”的边界。
- `_scaffold` 容易被理解为“脚手架 / 初始化草稿”，而真实定位是“只读文档标准 / 审计基线 / AI 对照材料”。
- 派生项目用户在 dry-run 或文档审计时，仍可能误解 `docs/_scaffold/00-09` 与项目自己的 `docs/00-09` 的关系。

因此建议把该规范镜像迁移到 `ai/` 下的专门标准区，并同步调整脚本、提示词与人读文档。

## 2. 设计目标

- 让目录语义更准确：规范镜像属于 AI 方法论 / 标准材料，不属于项目事实文档。
- 保持 v1.18.0 已建立的价值：同步模板 `docs/00-09` 撰写规范，绝不覆盖派生项目 `docs/00-09`。
- 降低命名误解：避免使用 `_scaffold` 暗示“脚手架草稿”。
- 兼容已有派生项目：迁移期不因旧路径存在或缺失导致审计 / 同步检查断裂。
- 保持模板维护闭环：脚本层、提示词层、人读文档层与 CI 自检同步更新，避免文档滞后。

## 3. 建议方案

### 主推路径

将规范镜像目标路径从：

```text
docs/_scaffold/00-09
```

迁移为：

```text
ai/doc-standards/00-09
```

语义定义：`ai/doc-standards/00-09` 是模板 `docs/00-09` 撰写规范在派生项目中的只读镜像，供 AI 生成、审计、回梳项目文档时对照使用；它不是项目事实，不直接驱动开发，也不应由派生项目手改。

### 备选命名

- `ai/document-specs/00-09`：偏规范说明，语义准确但略长。
- `ai/reference-docs/00-09`：强调参考资料，但约束感弱于 `doc-standards`。
- `ai/docs-reference/00-09`：可读性尚可，但不如 `doc-standards` 直接。

当前建议采用 `ai/doc-standards/00-09`。

## 4. 迁移策略

建议分两阶段处理，避免对已同步到 v1.18.x 的派生项目造成突兀断裂。

### 阶段一：兼容迁移

- `sync-template` 开始生成 / 刷新 `ai/doc-standards/00-09`。
- `16-docs-system-audit` 优先读取 `ai/doc-standards/00-09`；若不存在，再 fallback 到旧的 `docs/_scaffold/00-09`。
- `check-derived-sync` 放行 `ai/doc-standards/*`；过渡期可继续放行 `docs/_scaffold/*`，避免旧同步提交或分支被误判。
- 人读文档统一说明新路径，同时标注旧路径为历史兼容路径。
- 不主动删除派生项目已有的 `docs/_scaffold/`，避免同步脚本承担清理项目历史文件的职责。

### 阶段二：清理旧路径

- 在后续版本确认派生项目基本完成过渡后，再考虑移除旧路径 fallback 与相关文案。
- 如需清理派生项目旧目录，应由同步后整理提示词给出人工确认的迁移 / 删除计划，而不是 `sync-template` 自动删除。

## 5. 拟改范围

### 脚本与自检

- `scripts/sync-template.sh`：将模板 `docs/00-09` 镜像目标改为 `ai/doc-standards/00-09`；同步调整变量名、注释、dry-run 输出、创建目录与 `git add` 路径。
- `scripts/check-derived-sync.sh`：同步边界允许 `ai/doc-standards/*`；迁移期保留 `docs/_scaffold/*` 兼容规则。
- `scripts/check-template.sh`：将 `require_scaffold_mirror` 改造 / 重命名为类似 `require_doc_standards_mirror`，验证新路径生成、镜像内容来自模板规范、项目 `docs/00-09` 不被覆盖、派生边界检查接受新路径。
- `scripts/check-template.sh`：更新防文档滞后断言，从强制引用 `_scaffold` 调整为强制引用 `ai/doc-standards` 与 `16-docs-system-audit` 闭环。

### 提示词

- `ai/prompts/review/16-docs-system-audit.md`：规范基线优先读取 `ai/doc-standards/00-09`，迁移期 fallback 到 `docs/_scaffold/00-09`。
- `ai/prompts/maintainers/15-post-sync-cleanup.md`：同步后整理说明改为对照 `ai/doc-standards/00-09`；如发现旧 `docs/_scaffold/`，仅提示人工确认是否清理。

### 人读文档

- `docs/README.md`：移除 `docs/_scaffold/` 作为 docs 分区的长期说明；改为说明规范镜像已属于 `ai/doc-standards/`，不再放在项目事实区。
- `git-guide.md`：更新同步 dry-run 例外、同步后审计闭环与专门说明小节。
- `SOP.md`：把“项目文档成型后回溯审计”的输入从 `docs/_scaffold/` 改为 `ai/doc-standards/`。
- `MAINTAINERS.md`：更新发布 checklist、自检说明、文档分区规则与防文档滞后说明。
- `README.md`：新增当前版本摘要，说明规范镜像路径迁移；旧历史版本条目不必回写。
- `CHANGELOG.md`：新增本次迁移记录；旧历史记录保留为历史事实，不批量改写。

### 可选新增文件

- `ai/doc-standards/README.md`：说明该目录只读、非项目事实、由 `sync-template` 刷新、供 AI 审计 / 生成对照使用。

是否新增该 README 需在落地前决定：若新增，它可能需要进入 `template-sync.json`；`00-09` 镜像文件本身仍建议由 `sync-template` 专用镜像逻辑生成，不逐项加入 `template-sync.json`。

## 6. 版本影响

建议作为 `v1.19.0` 落地。

理由：虽然功能行为仍是“同步 00-09 撰写规范镜像”，但目录语义与派生项目同步产物路径发生变化，影响脚本、审计提示词、人读 SOP 与派生项目文件布局，属于可见的模板方法论结构调整。

若维护者希望极小步兼容迁移，也可作为 `v1.18.4`，但需明确这是过渡版本，后续再安排旧路径清理。

## 7. 验收口径

- 派生项目运行 `sync-template --dry-run` 时，能看到模板 `docs/00-09` 将镜像到 `ai/doc-standards/00-09`，且不触碰项目自己的 `docs/00-09`。
- 派生项目执行同步后，`ai/doc-standards/00-09` 存在且内容来自模板规范。
- `check-derived-sync` 不把 `ai/doc-standards/*` 误判为同步越界。
- `check-template.sh` 通过，且覆盖新路径镜像生成、项目事实不被覆盖、边界检查通过。
- `16-docs-system-audit` 能优先对照 `ai/doc-standards/00-09`，并在过渡期兼容旧 `docs/_scaffold/00-09`。
- 根目录人读文档不再把 `docs/_scaffold/` 描述为长期主路径。

## 8. 风险与缓解

- **旧派生项目残留旧目录**：迁移期保留 fallback 与边界放行；清理旧目录交给人工确认后的同步后整理，不由脚本自动删除。
- **路径再次命名争议**：落地前先确认 `doc-standards` 是否为最终命名；若改名，仅替换路径，不改变迁移策略。
- **文档滞后**：同步更新 `check-template.sh` 的防文档滞后断言，要求脚本、提示词、`git-guide.md` / `SOP.md` / `MAINTAINERS.md` 关键入口引用新路径与 16 号审计闭环。
- **历史记录混淆**：`CHANGELOG.md` / `README.md` 的旧版本条目保留 `_scaffold` 历史事实，只在新版本记录中说明迁移。
