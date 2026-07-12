from datetime import UTC, datetime
from uuid import uuid4

from app.schemas.conversations import ConversationData, MessageResponseData
from app.services.audit_service import record_audit_event, redact_sensitive_text
from app.services.console_service import create_handoff_record, create_knowledge_gap_record
from app.services.conversation_store import (
    PostgresConversationStoreError,
    append_message_to_postgres,
    create_conversation_in_postgres,
    get_conversation_from_postgres,
    list_conversations_from_postgres,
    should_use_postgres_conversation_store,
    update_conversation_in_postgres,
)
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
    if _use_postgres_conversation_store():
        _try_postgres_write(create_conversation_in_postgres, conversation)
    return conversation


def get_demo_conversation(conversation_id: str) -> ConversationData | None:
    if _use_postgres_conversation_store():
        conversation = _try_postgres_read(get_conversation_from_postgres, conversation_id)
        if conversation is not None:
            return conversation
    return _conversations.get(conversation_id)


def list_demo_conversations(
    status: str | None = None,
    scenario_pack_code: str | None = None,
    risk_level: str | None = None,
) -> list[ConversationData]:
    if _use_postgres_conversation_store():
        conversations = _try_postgres_read(
            list_conversations_from_postgres,
            status,
            scenario_pack_code,
            risk_level,
        )
        if conversations is not None:
            return conversations

    conversations = list(_seed_conversations()) + list(_conversations.values())
    return [
        conversation
        for conversation in conversations
        if _matches_filter(conversation.status, status)
        and _matches_filter(conversation.scenario_pack_code, scenario_pack_code)
        and _matches_filter(conversation.risk_level, risk_level)
    ]


def build_demo_message_response(conversation_id: str, content: str) -> MessageResponseData:
    conversation = get_demo_conversation(conversation_id)
    if conversation is None:
        raise KeyError(conversation_id)
    decision = decide_message_response(content, conversation.scenario_pack_code)
    handoff = _create_handoff_payload(conversation_id, conversation.scenario_pack_code, content, decision)
    knowledge_gap = _create_gap_payload(conversation_id, conversation.scenario_pack_code, decision)
    _apply_decision_to_conversation(conversation, content, decision)
    _conversations[conversation.conversation_id] = conversation
    record_audit_event(
        event_type="message_policy",
        content=content,
        outcome=decision.answer_type,
        risk_level=decision.risk_level,
        source_ref=decision.source_ref,
        conversation_id=conversation_id,
    )
    message_id = new_demo_id("msg")
    response = MessageResponseData(
        message_id=message_id,
        intent=decision.intent,
        answer_type=decision.answer_type,
        answer=decision.answer,
        source_ref=decision.source_ref,
        handoff=handoff,
        knowledge_gap=knowledge_gap,
        llm=decision.llm,
    )
    if _use_postgres_conversation_store():
        _persist_message_exchange(conversation, content, response)
    return response


def update_conversation_last_message(conversation_id: str, content: str) -> None:
    conversation = get_demo_conversation(conversation_id)
    if conversation is None:
        return
    conversation.last_message = content
    conversation.updated_at = _now_iso()
    _conversations[conversation.conversation_id] = conversation
    if _use_postgres_conversation_store():
        _try_postgres_write(update_conversation_in_postgres, conversation)


def _persist_message_exchange(
    conversation: ConversationData,
    content: str,
    response: MessageResponseData,
) -> None:
    safe_content = redact_sensitive_text(content)
    _try_postgres_write(
        append_message_to_postgres,
        new_demo_id("msg_customer"),
        conversation.conversation_id,
        "customer",
        safe_content,
    )
    _try_postgres_write(
        append_message_to_postgres,
        response.message_id,
        conversation.conversation_id,
        "assistant",
        response.answer,
        response.intent,
        response.answer_type,
        response.source_ref,
    )
    _try_postgres_write(update_conversation_in_postgres, conversation)


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


def _use_postgres_conversation_store() -> bool:
    try:
        return should_use_postgres_conversation_store()
    except Exception:
        return False


def _try_postgres_write(function, *args) -> None:
    try:
        function(*args)
    except PostgresConversationStoreError:
        return


def _try_postgres_read(function, *args):
    try:
        return function(*args)
    except PostgresConversationStoreError:
        return None
