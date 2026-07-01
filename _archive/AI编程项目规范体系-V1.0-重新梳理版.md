# AI编程项目规范体系 V1.0（重新梳理版）

**文档定位：** 本文档是规范体系的**设计源文档**，回答"规则的内容是什么、为什么这样分类"。
它与另外两类文档的关系是：

```text
本文档（设计源）
   ↓ 拆解分发
ai-project-template/（实际模板文件：global-rules.md / project-rules.md / index.md / docs / tasks / 入口文件）
   ↑ 使用说明
《AI编程规范体系说明》（操作手册，给人看，解释模板怎么用）
```

本文档不进入AI每次任务的阅读清单（那是 `ai/index.md` 指向的文件的职责），它的作用是：当需要新增/调整某条规则时，先在这里判断这条规则属于哪一类、该落到模板的哪个文件里。

---

## 一、设计理念

整套体系只服务于一个目标：

> **让AI遵守项目，而不是让项目迁就AI。**

为此遵循三条核心设计原则：

1. **规则分层**：区分"跨项目永久通用"的规则和"单项目专属"的规则，避免每新建一个项目都要重写一整套约束。
2. **入口指针化**：所有AI工具的入口文件（AGENTS.md / CLAUDE.md / .cursor rules）内容固定不变，只指向一份路由表，规则的增减不触碰入口文件。
3. **只增不改**：无论是规则文件还是代码目录，演进方式永远是"新增文件"或"在已有文件里加章节"，不允许"重命名已有路径"或"推翻已有结构"。

---

## 二、规则分层架构

| 层级 | 文件 | 内容 | 是否跨项目复用 |
|---|---|---|---|
| 通用层 | `ai/global-rules.md` | AI编程总体原则、代码生成规范、任务体系规则、审查体系、通用目录标准 | 是，逐字复用 |
| 项目层 | `ai/project-rules.md` | 本项目Phase边界、技术栈允许/禁止清单、目录规范的项目特例 | 否，每个项目重新填写 |
| 路由层 | `ai/index.md` | 列出当前生效的规则文件清单 | 模板自带，按需扩展 |

**分类判断标准**：一条规则写下来后，自问"换到另一个完全不同的项目（比如把KnowledgeBase换成数字客服）上，这条规则还成立吗？"——成立，放进 `global-rules.md`；不成立（涉及具体技术栈、具体功能、具体Phase定义），放进 `project-rules.md`。

---

## 三、项目目录标准

所有项目统一采用：

```text
ProjectName/
├─ docs/                          # 项目事实：需求、设计、计划
├─ ai/                             # AI行为规范
│  ├─ index.md
│  ├─ global-rules.md
│  └─ project-rules.md
├─ tasks/                          # AI任务单（按需启用）
├─ frontend/  backend/  tests/  scripts/  docker/
├─ AGENTS.md
├─ CLAUDE.md
├─ .cursor/rules/project-rules.mdc
├─ README.md
└─ .gitignore
```

### docs/ 命名规则

核心9份文档固定编号 `00-08`，不因项目而变：

```text
00-scenario.md            人工提供：项目背景与场景
01-user-requirements.md   人工提供：用户需求
02-srs.md                 人工提供：需求规格说明
03-prd.md                 AI生成：产品需求
04-architecture.md        AI生成：系统架构
05-tech-spec.md           AI生成：技术方案
06-db-design.md           AI生成：数据库设计
07-api-spec.md            AI生成：API设计
08-dev-plan.md            AI生成：开发计划
```

若项目需要额外专属文档（如数字客服的"对话流程设计.md"），使用**语义化命名**直接追加在 `docs/` 下，不占用、不挪动 `00-08` 编号，避免插入新文档导致后续编号连锁重排。

---

## 四、ai/ 目录设计

### 4.1 index.md（路由表）

AI每次开始任务前必读的第一个文件，作用是声明"当前项目生效的规则文件有哪些"。

Phase1阶段：

```markdown
# 当前生效的规则文件

请按顺序阅读以下文件，再开始任何分析或编码：

- ai/global-rules.md
- ai/project-rules.md
```

规则膨胀需要拆分时，仅扩展这个列表（见第十二节演进路径），其他文件不变：

```markdown
- ai/global-rules.md
- ai/project-rules.md
- ai/coding-rules.md
- ai/phase-boundary.md
- ai/directory-standard.md
- ai/review-checklist.md
```

### 4.2 global-rules.md 内容清单

该文件包含第五至第八节的全部内容（AI编程总体原则、代码生成规范、任务体系规则、审查体系），以及本节的通用目录标准说明。所有项目逐字复用。

### 4.3 project-rules.md 模板

```markdown
# 项目专属规则

## 1. Phase边界

当前阶段：Phase1

允许：
- （本项目当前阶段允许使用的技术/功能）

禁止：
- （本项目当前阶段禁止使用的技术/功能）

下一阶段预告：
- （Phase2大致会开放什么）

## 2. 技术栈约束

（本项目确定使用的前端/后端/数据库/AI模型等，及禁止引入的替代品）

## 3. 目录规范的项目特例

（如本项目目录结构与global-rules的通用骨架有差异，在此说明；
 没有差异则写"无，遵循global-rules通用目录标准"）
```

---

## 五、AI编程总体原则

### 5.1 文档驱动开发

开发顺序：

```text
Scenario → 用户需求 → SRS → PRD → 架构 → 技术方案 → 数据库设计 → API设计 → 开发计划 → 代码
```

禁止直接从想法生成代码。

### 5.2 小步快跑

```text
一个功能 = 一个任务 = 一次提交
```

禁止一次实现整个系统。

### 5.3 先设计后实现

任何模块开发前必须先有设计说明，再允许代码生成。

### 5.4 AI不可自主扩展需求

AI只能实现文档中已定义的功能，不得自主新增功能或"顺手"优化未被要求的部分。

---

## 六、AI代码生成规范

| 阶段 | 要求 |
|---|---|
| 生成前 | 必须先阅读 `ai/index.md` 列出的全部规则文件及相关 `docs/` 文档 |
| 生成时 | 必须先用文字说明实现方案，再输出代码 |
| 生成后 | 必须列出新增/修改的文件清单，并说明如何验证 |

---

## 七、AI任务体系

### 7.1 基本规则

- 所有开发通过任务单进行
- 一个任务单对应一个功能模块
- 禁止一个任务单实现整个系统

### 7.2 Phase1的轻量用法

不强制建立 `tasks/` 下的独立文件，`docs/08-dev-plan.md` 中每个Sprint按以下五个字段书写即可：

```markdown
## Sprint-X：功能名

### 目标
（这个任务要实现什么）

### 输入文档
（需要参考哪些 docs/ 文件的哪些章节）

### 修改范围
（预计新增/修改哪些文件，限制在1~3个文件/模块）

### 验收标准
（如何判断这个任务完成）

### 禁止事项
（明确不允许做的事，例如不允许引入新依赖、不允许改动其他模块）
```

当某个Sprint复杂到需要拆成多个独立任务时，将对应内容原样复制为 `tasks/task-00X-xxx.md`，格式完全一致，无需重新设计。

---

## 八、AI审查体系

### 8.1 审查维度

```text
需求审查   —— 是否符合PRD
架构审查   —— 是否符合架构设计
技术审查   —— 是否符合技术方案
数据库审查 —— 是否符合DB设计
API审查    —— 是否符合API设计
边界审查   —— 是否超出当前Phase范围
```

### 8.2 统一输出格式

```text
1. 合规项
2. 问题项
3. 风险项
4. 修复建议
```

---

## 九、Phase边界管理

### 9.1 必须定义阶段

```text
Phase1  个人/单功能 Demo
Phase2  功能完善
Phase3  团队协作 / 多用户
```

### 9.2 边界写法

在 `ai/project-rules.md` 的"Phase边界"一节中，用"允许/禁止/下一阶段预告"三段式描述，例如：

```text
当前阶段：Phase1

允许：SQLite / 单用户 / 本地运行
禁止：多用户 / 权限系统 / PostgreSQL / Qdrant

下一阶段预告：Phase2将开放富文本编辑、文档版本历史
```

进入下一Phase时，只更新这一个状态块，不需要在PRD、coding-rules、各工具入口文件里逐处修改。

---

## 十、多AI工具适配

| 工具 | 入口文件 |
|---|---|
| Cursor | `.cursor/rules/project-rules.mdc` |
| Claude Code | `CLAUDE.md` |
| Codex / AGENTS标准 | `AGENTS.md` |

**统一原则**：不同工具的入口文件**内容完全相同、只有一句话**——

```text
本项目的全部AI行为规范见 ai/index.md，
开发前必须先阅读该文件列出的全部文件，不得跳过。
```

不同工具读取入口不同，但指向的规范体系相同；这三个入口文件创建后永久不变，规则的增减只发生在 `ai/index.md`。

---

## 十一、跨项目复用与同步机制

### 11.1 新项目启动流程

```text
1. 复制 ai-project-template/ → NewProject/
2. 人工填写 docs/00-02（Scenario / 用户需求 / SRS）
3. 用初始化Prompt（附录B）让AI阅读00-02 + global-rules.md，
   生成 docs/03-08
4. 人工审核03-08后，填写 ai/project-rules.md
   （Phase边界 + 技术栈约束 + 目录特例）
5. ai/index.md、ai/global-rules.md、AGENTS.md/CLAUDE.md/.cursor rules
   直接使用，不需修改
6. 进入Sprint1
```

除 `project-rules.md` 一个文件外，其余所有AI约束文件对任意新项目都是**零修改即用**。

### 11.2 global-rules 更新同步

`global-rules.md` 在每个项目里是独立副本（不使用 git submodule）。当某条通用规则需要修改时：

```text
1. 先改 ai-project-template/ai/global-rules.md（源头）
2. 覆盖复制到其他正在进行的项目的 ai/global-rules.md
3. 在对应项目提交记录中注明：
   "sync global-rules from template vX"
```

因为是单一自包含文件，覆盖复制是无歧义的整体替换。`project-rules.md` 是项目专属内容，不参与跨项目同步。

---

## 十二、从轻量到规范化的演进路径

本体系刻意设计为"只增不改"：

| 阶段 | 变化内容 | 是否改动入口文件 | 是否改动代码路径 |
|---|---|---|---|
| Phase1（起步） | `ai/index.md` 只列2个文件；`tasks/` 不启用 | 不变 | 不变 |
| Phase2（规则增多） | `global-rules.md` 按章节拆分为多个独立文件，`index.md` 列表增加 | 不变 | 不变（新模块归入已有分类） |
| Phase2（功能复杂） | 开始使用 `tasks/`，从dev-plan复制Sprint内容 | 不变 | 不变 |
| Phase3（多用户/团队） | `docs/` 新增权限设计、多租户设计等文档（语义命名追加） | 不变 | 仅新增models/schemas，不改现有结构 |

关键约束：任何阶段的演进，都是"新增文件"或"在已有文件内增加章节"，不允许"重命名已有路径"或"重新设计已有结构"。

---

## 十三、最佳实践流程总览

```text
Scenario
↓
用户需求
↓
SRS
↓
PRD
↓
架构设计
↓
技术方案
↓
数据库设计
↓
API设计
↓
开发计划
↓
任务单/Sprint
↓
AI编码
↓
人工审查
↓
Git提交
```

避免：

```text
想法 → AI → 代码
```

---

## 附录A：本规范章节 → 模板落地文件映射表

| 本文档章节 | 落地位置 |
|---|---|
| 一、设计理念 / 二、规则分层架构 | 《AI编程规范体系说明》的架构说明部分 |
| 三、项目目录标准 | 模板根目录的实际骨架 + global-rules.md 目录规范条款 |
| 四、ai/目录设计 | `ai/index.md`、`ai/global-rules.md`、`ai/project-rules.md` 本身 |
| 五～八、十二节内容 | `ai/global-rules.md` 主体 |
| 九节 Phase边界 | `ai/project-rules.md` 的"Phase边界"填空模板 |
| 十节 多工具适配 | `AGENTS.md` / `CLAUDE.md` / `.cursor/rules/project-rules.mdc` 实际内容 |
| 十一节 复用与同步机制 | 《AI编程规范体系说明》的使用流程章节 |
| 附录B 初始化Prompt | 模板根目录 `INIT-PROMPT.md` |
| 附录C 任务单模板 | `tasks/README.md` 中的任务单格式 |

---

## 附录B：项目初始化Prompt

```text
请先阅读：
- docs/00-scenario.md
- docs/01-user-requirements.md
- docs/02-srs.md
- ai/global-rules.md

然后依次生成：
- docs/03-prd.md
- docs/04-architecture.md
- docs/05-tech-spec.md
- docs/06-db-design.md
- docs/07-api-spec.md
- docs/08-dev-plan.md

要求：
1. 严格遵循 ai/global-rules.md 中的文档驱动开发原则
2. 不增加00-02中没有提及的功能
3. 明确标注当前Phase允许和禁止的技术/功能边界
4. 每份文档生成前先用1-2句话说明本文档的结构安排
```

---

## 附录C：单任务执行Prompt

```text
请执行以下任务：

docs/08-dev-plan.md 中的 Sprint-X

执行前请先阅读：
- ai/index.md 列出的全部规则文件
- docs/03-prd.md（相关章节）
- docs/07-api-spec.md（相关接口）

要求：
1. 先说明实现方案
2. 列出将新增或修改的文件（限制1~3个）
3. 确认不超出本任务范围
4. 再开始生成代码
5. 完成后说明修改了哪些文件，以及如何验证
```

---

## 附录D：项目审查Prompt

```text
请根据 ai/index.md 列出的全部规则文件及 docs/03-08，审查当前项目，输出：

1. 合规项
2. 问题项（是否超出当前Phase范围 / 是否存在技术栈偏离 / 是否存在未按API或DB设计实现的部分）
3. 风险项
4. 修复建议
```
