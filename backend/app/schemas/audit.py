from pydantic import BaseModel


class AuditLogRecord(BaseModel):
    audit_id: str
    event_type: str
    conversation_id: str | None = None
    input_summary: str
    outcome: str
    risk_level: str
    source_ref: str
    created_at: str
    mock: bool = True
