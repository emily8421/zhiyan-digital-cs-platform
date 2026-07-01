# TEMPLATE-UPGRADE-v1.6.7：同步边界说明与派生 README 标准化

## 状态

- 状态：已随本次模板改动落地，归档留痕
- 目标版本：v1.6.7
- 提案来源：模板同步边界与派生项目 README 规范补齐

## 背景

模板已经通过 `template-sync.json` 定义了下行同步方法论文件，也明确根 `README.md`、`ai/project-rules.md` 和项目 `docs/` 是项目专属内容。但派生项目使用者仍可能不清楚：哪些 Markdown 文件会在同步时被覆盖，哪些文件应该留给项目自行维护。

此外，派生项目根 `README.md` 不参与模板同步，但需要一个统一的推荐结构，避免项目 README 过于随意，缺少当前阶段、运行环境、验证方式和模板关系说明。

## 目标

1. 为同步 Markdown 方法论文件补充同步覆盖说明。
2. 明确派生项目不要直接修改同步方法论文件；通用改进应通过 `_proposals/` 回流模板。
3. 明确根 `README.md` 是项目专属文档，不参与模板下行同步。
4. 标准化 `scripts/new-project.sh` 生成的派生 README 版块。
5. 补齐 `_examples/` 的 docs 分区结构，使样例与 v1.6.6 规则一致。
6. 增强自检，覆盖同步说明、派生 README 模板和样例分区。

## 拟改范围

- `VERSION`：升级到 `v1.6.7`。
- `CHANGELOG.md`：新增 v1.6.7 记录。
- `SOP.md`、`git-guide.md`、`MAINTAINERS.md`：补充同步边界与 README 不同步说明。
- `SOP.md`、`INIT-PROMPT.md`、`CONTRIBUTING.md`、`MAINTAINERS.md`、`CHANGELOG.md`、`git-guide.md`、`docs/README.md`：顶部补同步覆盖说明。
- `AGENTS.md`、`CLAUDE.md`、`.cursor/rules/project-rules.mdc`：补简短入口同步说明。
- `scripts/new-project.sh`：标准化派生项目 README 版块。
- `_examples/*/docs/README.md` 与 docs 分区目录：补齐样例结构。
- `_examples/*/ai/project-rules.md`：补文档分区初始化检查。
- `scripts/check-template.sh`：新增自检断言。

## 版本影响

- 版本类型：PATCH。
- 理由：补充同步边界说明和样例一致性，不改变核心流程、同步机制或文档编号。

## 验证方式

- 运行 `git diff --check`。
- 运行 `powershell -ExecutionPolicy Bypass -File scripts/check-template.ps1`。
