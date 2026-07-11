from typing import Any

from pydantic import BaseModel, Field


class MockBusinessRecordResponse(BaseModel):
    record_type: str
    external_ref: str
    scenario_pack_code: str
    status: str
    summary: str
    next_step: str
    eta: str | None = None
    source_ref: str
    source_system: str
    environment: str
    stage: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    mock: bool = True
