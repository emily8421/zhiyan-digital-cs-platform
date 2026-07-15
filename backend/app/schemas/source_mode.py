from typing import Literal

from pydantic import BaseModel, Field

# API-013 场景包数据源模式（docs/07-api-spec.md §API-013）。
# Phase2.5 / Phase3A：仅 demo_sandbox 立即可用；customer_sandbox_readonly /
# production_readonly / production_writeback 仅作门禁状态展示，未授权时 No-Go。
SourceMode = Literal[
    "demo_sandbox",
    "customer_sandbox_readonly",
    "production_readonly",
    "production_writeback",
]

GateStatus = Literal["go", "no_go"]

AVAILABLE_SOURCE_MODES: list[str] = [
    "demo_sandbox",
    "customer_sandbox_readonly",
    "production_readonly",
    "production_writeback",
]


class SourceModeResponse(BaseModel):
    scenario_pack_id: str
    source_mode: str
    available_modes: list[str]
    gate_status: GateStatus
    gate_reasons: list[str] = Field(default_factory=list)
    source_ref: str
    mock: bool = True


class SourceModeUpdateRequest(BaseModel):
    source_mode: SourceMode
