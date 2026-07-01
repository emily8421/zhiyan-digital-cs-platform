# 08 开发计划

> 轻量项目只拆一个 Sprint，避免过度计划。

## Sprint1：会议纪要清理脚本

### 目标

实现 Meeting Notes Cleaner 的全部 Phase1 功能：读取输入文件、执行三条清理规则、写入输出文件，并处理基础错误。

### 输入文档

- `docs/02-srs.md`：REQ-001~REQ-006
- `docs/03-prd.md`：F-001~F-004
- `docs/04-architecture.md`：CLI 层、清理规则层
- `docs/05-tech-spec.md`：命令参数约定、清理规则
- `docs/09-verification.md`：TC-001~TC-006

### 修改范围

- `backend/cleaner.py`
- `backend/cli.py`
- `tests/test_cleaner.py`
- `tests/test_cli.py`

### 验收标准

- `clean_text` 满足三条清理规则。
- CLI 可读取输入文件并写入输出文件。
- 输入文件不存在或参数缺失时返回非 0 退出码，并输出可理解错误。

### 禁止事项

- 不新增数据库、Web 服务、AI 模型调用。
- 不实现行动项提取、批量目录处理或配置文件系统。
- 不引入第三方依赖，除非先经人工确认。
