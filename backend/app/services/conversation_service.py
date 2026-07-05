from datetime import UTC, datetime
from uuid import uuid4

from app.schemas.conversations import ConversationData, MessageResponseData
from app.services.audit_service import record_audit_event, redact_sensitive_text
from app.services.console_service import create_handoff_record, create_knowledge_gap_record
from app.services.message_policy_service import MessageDecision, decide_message_response


_conversations: dict[str, ConversationData] = {}


def new_demo_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:8]}"


def create_demo_conversation(
    channel: str,
    scenario_pack_code: str,
    customer_alias: str | None,
) -> ConversationData:
    conversation = ConversationData(
        conversation_id=new_demo_id("conv"),
        channel=channel,
        scenario_pack_code=scenario_pack_code,
        status="open",
        risk_level="low",
        last_message="会话已创建，等待客户提问。",
        customer_alias=customer_alias or "demo_customer",
        updated_at=_now_iso(),
        mock=True,
    )
    _conversations[conversation.conversation_id] = conversation
    return conversation


def get_demo_conversation(conversation_id: str) -> ConversationData | None:
    return _conversations.get(conversation_id)


def list_demo_conversations(
    status: str | None = None,
    scenario_pack_code: str | None = None,
    risk_level: str | None = None,
) -> list[ConversationData]:
    conversations = list(_seed_conversations()) + list(_conversations.values())
    return [
        conversation
        for conversation in conversations
        if _matches_filter(conversation.status, status)
        and _matches_filter(conversation.scenario_pack_code, scenario_pack_code)
        and _matches_filter(conversation.risk_level, risk_level)
    ]


def build_demo_message_response(conversation_id: str, content: str) -> MessageResponseData:
    conversation = _conversations[conversation_id]
    decision = decide_message_response(content, conversation.scenario_pack_code)
    handoff = _create_handoff_payload(conversation_id, conversation.scenario_pack_code, content, decision)
    knowledge_gap = _create_gap_payload(conversation_id, conversation.scenario_pack_code, decision)
    _apply_decision_to_conversation(conversation, content, decision)
    record_audit_event(
        event_type="message_policy",
        content=content,
        outcome=decision.answer_type,
        risk_level=decision.risk_level,
        source_ref=decision.source_ref,
        conversation_id=conversation_id,
    )
    return MessageResponseData(
        message_id=new_demo_id("msg"),
        intent=decision.intent,
        answer_type=decision.answer_type,
        answer=decision.answer,
        source_ref=decision.source_ref,
        handoff=handoff,
        knowledge_gap=knowledge_gap,
    )


def update_conversation_last_message(conversation_id: str, content: str) -> None:
    conversation = _conversations.get(conversation_id)
    if conversation is None:
        return
    conversation.last_message = content
    conversation.updated_at = _now_iso()


def _create_handoff_payload(
    conversation_id: str,
    scenario_pack_code: str,
    content: str,
    decision: MessageDecision,
) -> dict[str, object] | None:
    if decision.answer_type != "handoff" or decision.handoff_reason is None:
        return None
    handoff = create_handoff_record(
        conversation_id=conversation_id,
        scenario_pack_code=scenario_pack_code,
        reason=decision.handoff_reason,
        summary=redact_sensitive_text(content),
        risk_level=decision.risk_level,
    )
    return {
        "handoff_id": handoff.handoff_id,
        "status": handoff.status,
        "reason": handoff.reason,
        "risk_level": handoff.risk_level,
    }


def _create_gap_payload(
    conversation_id: str,
    scenario_pack_code: str,
    decision: MessageDecision,
) -> dict[str, object] | None:
    if decision.answer_type != "gap" or decision.gap_question is None:
        return None
    gap = create_knowledge_gap_record(
        conversation_id=conversation_id,
        scenario_pack_code=scenario_pack_code,
        question=redact_sensitive_text(decision.gap_question),
        tags=["无依据", "待确认"],
    )
    return {
        "gap_id": gap.gap_id,
        "status": gap.status,
        "question": gap.question,
        "tags": gap.tags,
    }


def _apply_decision_to_conversation(
    conversation: ConversationData,
    content: str,
    decision: MessageDecision,
) -> None:
    conversation.last_message = redact_sensitive_text(content)
    conversation.risk_level = decision.risk_level
    conversation.updated_at = _now_iso()
    if decision.answer_type == "handoff":
        conversation.status = "handoff"


def _seed_conversations() -> list[ConversationData]:
    return [
        ConversationData(
            conversation_id="conv_demo_product_001",
            channel="h5",
            scenario_pack_code="product_business",
            status="open",
            risk_level="medium",
            last_message="客户询问 HC-ORDER-001 的生产进度。",
            customer_alias="demo_product_customer",
            updated_at="2026-07-05T09:30:00+08:00",
            mock=True,
        ),
        ConversationData(
            conversation_id="conv_demo_project_001",
            channel="h5",
            scenario_pack_code="project_business",
            status="handoff",
            risk_level="high",
            last_message="客户提到合同和上线承诺，需要人工确认。",
            customer_alias="demo_project_customer",
            updated_at="2026-07-05T10:10:00+08:00",
            mock=True,
        ),
    ]


def _matches_filter(value: str | None, expected: str | None) -> bool:
    return expected is None or value == expected


def _now_iso() -> str:
    return datetime.now(tz=UTC).astimezone().isoformat(timespec="seconds")
