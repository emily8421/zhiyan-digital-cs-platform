# TEMPLATE-UPGRADE-beginner-ai-cli-onboarding

## 动机

当前新手入口已经补充了环境检查、环境安装、环境采集与文档生成顺序，但整体仍偏向“人工逐条敲命令”。模板的真实目标是让新手尽快打开 AI CLI 对话窗口，由 AI 读取规则、路由命令、解释每一步影响并辅助执行。若缺少 AI CLI 首次对话路径，新手容易把模板理解成命令清单，而不是 AI 协作工作流。

同时，本轮修改最初在本地 `main` 上开始，未先切维护分支、未先形成提案，偏离模板维护规范。已补救切换到维护分支 `change/beginner-ai-cli-onboarding`，并用本提案记录本轮模板优化范围。

## 拟改

- `README.md` 增加“推荐路径：先打开 AI CLI”，说明手动路径是兜底，推荐路径是尽快进入 AI CLI 引导模式。
- `README.md` 的 5 分钟路径在环境缺失时直接给出 `scripts/bootstrap-dev-env.ps1` 命令；常用命令区区分正式项目起步与模板烟测，避免把 `--local --no-remote` 烟测命令放在派生项目使用者默认入口。
- `template-docs/beginner-guide.md` 增加 AI CLI 引导路径，提供首次打开 AI CLI 后可复制的最小提示词，并说明哪些步骤仍需人工确认。
- `template-docs/ai-cli-setup.md` 补充安装完成后的“进入模板工作”启动语句。
- `scripts/new-project.sh` 生成的派生项目 README 同步提示 AI CLI 引导路径。
- `scripts/check-template.sh` / `scripts/check-template.ps1` 增加稳定关键词断言，防止 AI CLI 新手入口再次滞后。
- `VERSION` / `CHANGELOG.md` 记录版本变化。

## 版本影响

- 建议作为 `v1.21.1` 内同一轮新手入口优化继续落地；若需单独审计，也可提升到后续 patch 版本。
- 不改变模板核心文档生命周期规则，不修改 `ai/global-rules.md` 全局规则版本。

## 影响面

- 新手阅读路径：从“先看 README 后手敲命令”变为“README 明确推荐 AI CLI 引导模式，手动命令保留为兜底”。
- 派生项目 README 初始化内容：更贴近 AI CLI 实际使用方式。
- 自检断言：新增入口关键词检查，避免 README / beginner guide / ai-cli setup 文档漂移。

## 落地流程

1. 在维护分支上补充 AI CLI 推荐路径与首次提示词。
2. 同步更新派生 README 模板和防文档滞后断言。
3. 运行 `git diff --check` 与 `scripts/check-template.ps1`。
4. PR 合并后将本提案移动到 `_archive/proposals/`。
