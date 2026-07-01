# docs/env 运行环境说明

本目录用于保存项目初始化阶段的本机运行环境与资源约束。

如果机器还没装好基础开发环境，先看 `template-docs/env-setup.md`，并先运行 `scripts/check-prereqs.ps1` / `scripts/bootstrap-dev-env.ps1`。

## 生成方式

在项目根目录运行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/collect-env.ps1
```

脚本会生成 `docs/env/local-env.md`，并保留需要人工确认的 Demo 资源边界、联网权限、服务器资源预案等字段。

## 使用要求

- 生成 `docs/04-architecture.md`、`docs/05-tech-spec.md`、`docs/09-verification.md` 前，应读取 `docs/env/local-env.md`。
- 技术方案必须判断本机 Demo 是否可运行；若不可运行，必须给出降级 / Mock 策略和公司服务器资源需求。
- `local-env.md` 可能包含计算机名、用户名、路径等本机信息；提交到公开仓库前需人工确认是否脱敏。

