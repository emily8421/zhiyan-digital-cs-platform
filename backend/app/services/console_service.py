from copy import deepcopy
from datetime import UTC, date, datetime
from uuid import uuid4

from app.schemas.console import (
    DailySummaryData,
    HandoffRecord,
    KnowledgeGapRecord,
    MockNotificationRecord,
)

_HANDOFF_STATUSES = {"open", "processing", "closed"}
_GAP_STATUSES = {"new", "reviewing", "accepted", "rejected", "closed"}

_handoffs: dict[str, HandoffRecord] = {
    "handoff_001": HandoffRecord(
        handoff_id="handoff_001",
        conversation_id="conv_demo_project_001",
        scenario_pack_code="project_business",
        reason="客户提到合同、上线承诺等高风险事项，需要人工确认。",
        suggested_owner="售前方案负责人",
        status="open",
        risk_level="high",
        summary="项目型客户询问合同和上线承诺，Demo 阶段不自动承诺。",
        updated_at="2026-07-05T10:12:00+08:00",
        mock=True,
    ),
    "handoff_002": HandoffRecord(
        handoff_id="handoff_002",
        conversation_id="conv_demo_product_001",
        scenario_pack_code="product_business",
        reason="客户询问赔偿和最低价，需要人工确认。",
        suggested_owner="售后值班同事",
        status="processing",
        risk_level="medium",
        summary="产品型客户售后问题已进入人工跟进。",
        resolution_note="已分配给售后同事跟进。",
        updated_at="2026-07-05T09:45:00+08:00",
        mock=True,
    ),
}

_knowledge_gaps: dict[str, KnowledgeGapRecord] = {
    "gap_001": KnowledgeGapRecord(
        gap_id="gap_001",
        conversation_id="conv_demo_product_001",
        scenario_pack_code="product_business",
        question="客户询问定制灯带是否支持特殊防水等级。",
        tags=["产品规格", "待确认"],
        status="new",
        updated_at="2026-07-05T09:50:00+08:00",
        mock=True,
    ),
    "gap_002": KnowledgeGapRecord(
        gap_id="gap_002",
        conversation_id="conv_demo_project_001",
        scenario_pack_code="project_business",
        question="客户询问项目验收资料清单模板。",
        tags=["项目交付", "知识候选"],
        status="reviewing",
        resolution_note="等待交付同事补充标准模板。",
        updated_at="2026-07-05T10:20:00+08:00",
        mock=True,
    ),
}

_notifications: dict[str, MockNotificationRecord] = {}


class ConsoleRecordNotFoundError(Exception):
    def __init__(self, record_type: str, record_id: str) -> None:
        self.record_type = record_type
        self.record_id = record_id


class InvalidConsoleStatusError(Exception):
    def __init__(self, record_type: str, status: str) -> None:
        self.record_type = record_type
        self.status = status


def list_handoffs(
    status: str | None = None,
    risk_level: str | None = None,
    suggested_owner: str | None = None,
) -> list[HandoffRecord]:
    return [
        deepcopy(record)
        for record in _handoffs.values()
        if _matches_filter(record.status, status)
        and _matches_filter(record.risk_level, risk_level)
        and _matches_filter(record.suggested_owner, suggested_owner)
    ]


def update_handoff_status(
    handoff_id: str,
    status: str,
    resolution_note: str | None,
) -> HandoffRecord:
    if status not in _HANDOFF_STATUSES:
        raise InvalidConsoleStatusError("handoff", status)
    record = _handoffs.get(handoff_id)
    if record is None:
        raise ConsoleRecordNotFoundError("handoff", handoff_id)
    record.status = status
    record.resolution_note = resolution_note
    record.updated_at = _now_iso()
    return deepcopy(record)


def create_handoff_record(
    conversation_id: str,
    scenario_pack_code: str,
    reason: str,
    summary: str,
    risk_level: str,
) -> HandoffRecord:
    handoff = HandoffRecord(
        handoff_id=f"handoff_{uuid4().hex[:8]}",
        conversation_id=conversation_id,
        scenario_pack_code=scenario_pack_code,
        reason=reason,
        suggested_owner="人工客服值班同事",
        status="open",
        risk_level=risk_level,
        summary=summary,
        updated_at=_now_iso(),
        mock=True,
    )
    _handoffs[handoff.handoff_id] = handoff
    return deepcopy(handoff)


def list_knowledge_gaps(
    status: str | None = None,
    scenario_pack_code: str | None = None,
    tag: str | None = None,
) -> list[KnowledgeGapRecord]:
    return [
        deepcopy(record)
        for record in _knowledge_gaps.values()
        if _matches_filter(record.status, status)
        and _matches_filter(record.scenario_pack_code, scenario_pack_code)
        and (tag is None or tag in record.tags)
    ]


def update_knowledge_gap_status(
    gap_id: str,
    status: str,
    resolution_note: str | None,
) -> KnowledgeGapRecord:
    if status not in _GAP_STATUSES:
        raise InvalidConsoleStatusError("knowledge_gap", status)
    record = _knowledge_gaps.get(gap_id)
    if record is None:
        raise ConsoleRecordNotFoundError("knowledge_gap", gap_id)
    record.status = status
    record.resolution_note = resolution_note
    record.updated_at = _now_iso()
    return deepcopy(record)


def create_knowledge_gap_record(
    conversation_id: str,
    scenario_pack_code: str,
    question: str,
    tags: list[str] | None = None,
) -> KnowledgeGapRecord:
    gap = KnowledgeGapRecord(
        gap_id=f"gap_{uuid4().hex[:8]}",
        conversation_id=conversation_id,
        scenario_pack_code=scenario_pack_code,
        question=question,
        tags=tags or ["待确认"],
        status="new",
        updated_at=_now_iso(),
        mock=True,
    )
    _knowledge_gaps[gap.gap_id] = gap
    return deepcopy(gap)


def list_notifications(
    event_type: str | None = None,
    send_status: str | None = None,
) -> list[MockNotificationRecord]:
    records = list(_seed_notifications().values()) + list(_notifications.values())
    return [
        deepcopy(record)
        for record in records
        if _matches_filter(record.event_type, event_type)
        and _matches_filter(record.send_status, send_status)
    ]


def create_mock_notification(
    event_type: str,
    related_id: str,
    target_type: str,
) -> MockNotificationRecord:
    notification = MockNotificationRecord(
        notification_id=f"notif_{uuid4().hex[:8]}",
        event_type=event_type,
        related_id=related_id,
        target_type=target_type,
        payload=_build_notification_payload(event_type, related_id, target_type),
        created_at=_now_iso(),
        mock=True,
    )
    _notifications[notification.notification_id] = notification
    return deepcopy(notification)


def build_daily_summary(summary_date: date | None = None) -> DailySummaryData:
    from app.services.conversation_service import list_demo_conversations

    resolved_date = summary_date or date.today()
    conversations = list_demo_conversations()
    handoffs = list_handoffs()
    gaps = list_knowledge_gaps()
    notifications = list_notifications()
    open_item_count = sum(1 for item in handoffs if item.status != "closed") + sum(
        1 for item in gaps if item.status not in {"accepted", "rejected", "closed"}
    )
    return DailySummaryData(
        summary_date=resolved_date.isoformat(),
        conversation_count=len(conversations),
        auto_answer_count=max(len(conversations) - len(handoffs), 0),
        handoff_count=len(handoffs),
        gap_count=len(gaps),
        open_item_count=open_item_count,
        notification_count=len(notifications),
        content="Demo 日报：今日已生成会话、转人工、知识缺口和 Mock 通知摘要，未接入真实飞书或业务系统。",
        mock=True,
    )


def _seed_notifications() -> dict[str, MockNotificationRecord]:
    return {
        "notif_demo_001": MockNotificationRecord(
            notification_id="notif_demo_001",
            event_type="handoff",
            related_id="handoff_001",
            target_type="feishu",
            payload=_build_notification_payload("handoff", "handoff_001", "feishu"),
            created_at="2026-07-05T10:13:00+08:00",
            mock=True,
        ),
        "notif_demo_002": MockNotificationRecord(
            notification_id="notif_demo_002",
            event_type="knowledge_gap",
            related_id="gap_001",
            target_type="feishu",
            payload=_build_notification_payload("knowledge_gap", "gap_001", "feishu"),
            created_at="2026-07-05T09:51:00+08:00",
            mock=True,
        ),
    }


def _build_notification_payload(event_type: str, related_id: str, target_type: str) -> dict[str, object]:
    payload: dict[str, object] = {
        "event_type": event_type,
        "related_id": related_id,
        "target_type": target_type,
        "send_status": "mocked",
        "mock": True,
    }
    if event_type == "handoff" and related_id in _handoffs:
        record = _handoffs[related_id]
        payload.update(
            {
                "conversation_id": record.conversation_id,
                "reason": record.reason,
                "suggested_owner": record.suggested_owner,
            }
        )
    if event_type == "knowledge_gap" and related_id in _knowledge_gaps:
        record = _knowledge_gaps[related_id]
        payload.update(
            {
                "gap_id": record.gap_id,
                "question": record.question,
                "tags": record.tags,
            }
        )
    return payload


def _matches_filter(value: str, expected: str | None) -> bool:
    return expected is None or value == expected


def _now_iso() -> str:
    return datetime.now(tz=UTC).astimezone().isoformat(timespec="seconds")
