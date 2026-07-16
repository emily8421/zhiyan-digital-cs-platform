"""API-015 场景包 Demo Sandbox 重置模型（Phase2.5 / Phase3A）。

口径：仅重置当前场景包演示运行态（会话 / 缺口 / 转人工 / 通知 / 知识条目），
保留场景包基础配置、Demo Dataset、真实数据门禁配置与其他场景包数据。
依据：docs/07-api-spec.md §API-015、docs/09-verification.md TC-068。
"""

from pydantic import BaseModel, Field


class DemoResetRequest(BaseModel):
    runtime_scope: str = "current_scenario_pack"
    confirm: bool = False


class DemoResetResponse(BaseModel):
    scenario_pack_id: str
    reset_id: str
    reset_at: str
    reset_scope: str
    affected_counts: dict[str, int] = Field(default_factory=dict)
    source_mode: str
    mock: bool = True
