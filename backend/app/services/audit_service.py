import re
from datetime import UTC, datetime
from uuid import uuid4

from app.schemas.audit import AuditLogRecord

_audit_logs: list[AuditLogRecord] = []

_SENSITIVE_PATTERNS = [
    re.compile(r"1[3-9]\d{9}"),
    re.compile(r"\d{17}[\dXx]"),
    re.compile(r"(?i)(token|api[_-]?key|secret)\s*[:=]\s*[^\s，。；,;]+"),
]


def record_audit_event(
    event_type: str,
    content: str,
    outcome: str,
    risk_level: str,
    source_ref: str,
    conversation_id: str | None = None,
) -> AuditLogRecord:
    record = AuditLogRecord(
        audit_id=f"audit_{uuid4().hex[:8]}",
        event_type=event_type,
        conversation_id=conversation_id,
        input_summary=redact_sensitive_text(content)[:120],
        outcome=outcome,
        risk_level=risk_level,
        source_ref=source_ref,
        created_at=_now_iso(),
        mock=True,
    )
    _audit_logs.append(record)
    return record


def list_audit_logs() -> list[AuditLogRecord]:
    return list(_audit_logs)


def redact_sensitive_text(content: str) -> str:
    redacted = content
    for pattern in _SENSITIVE_PATTERNS:
        redacted = pattern.sub("[已脱敏]", redacted)
    return redacted


def _now_iso() -> str:
    return datetime.now(tz=UTC).astimezone().isoformat(timespec="seconds")
