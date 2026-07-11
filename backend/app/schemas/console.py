from pydantic import BaseModel, Field


class StatusUpdateRequest(BaseModel):
    status: str
    resolution_note: str | None = None


class HandoffRecord(BaseModel):
    handoff_id: str
    conversation_id: str
    scenario_pack_code: str
    reason: str
    suggested_owner: str
    status: str
    risk_level: str
    summary: str
    resolution_note: str | None = None
    updated_at: str
    mock: bool = True


class KnowledgeGapRecord(BaseModel):
    gap_id: str
    conversation_id: str
    scenario_pack_code: str
    question: str
    tags: list[str] = Field(default_factory=list)
    status: str
    resolution_note: str | None = None
    updated_at: str
    mock: bool = True


class KnowledgeItemRecord(BaseModel):
    item_id: str
    scenario_pack_code: str
    title: str
    content: str
    tags: list[str] = Field(default_factory=list)
    source_ref: str
    status: str
    origin_gap_id: str | None = None
    updated_at: str
    mock: bool = True


class KnowledgeItemCreateRequest(BaseModel):
    scenario_pack_code: str
    title: str
    content: str
    source_ref: str
    tags: list[str] = Field(default_factory=list)
    status: str = "draft"


class MockNotificationRequest(BaseModel):
    event_type: str
    related_id: str
    target_type: str = "feishu"


class MockNotificationRecord(BaseModel):
    notification_id: str
    event_type: str
    related_id: str
    target_type: str
    payload: dict[str, object]
    send_status: str = "mocked"
    created_at: str
    mock: bool = True


class DailySummaryData(BaseModel):
    summary_date: str
    conversation_count: int
    auto_answer_count: int
    handoff_count: int
    gap_count: int
    open_item_count: int
    notification_count: int
    content: str
    mock: bool = True
