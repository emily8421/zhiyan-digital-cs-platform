from pydantic import BaseModel


class MockBusinessRecordResponse(BaseModel):
    record_type: str
    external_ref: str
    scenario_pack_code: str
    status: str
    summary: str
    next_step: str
    eta: str | None = None
    mock: bool = True
