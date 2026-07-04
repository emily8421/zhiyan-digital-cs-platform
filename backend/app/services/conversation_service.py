from datetime import UTC, datetime
from uuid import uuid4

from app.schemas.conversations import ConversationData, MessageResponseData


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


def build_demo_message_response(content: str) -> MessageResponseData:
    return MessageResponseData(
        message_id=new_demo_id("msg"),
        intent="demo_echo",
        answer_type="mock_business",
        answer=f"这是 Mock 回复：已收到你的问题“{content}”。",
        source_ref="mock:sprint-1",
        handoff=None,
        knowledge_gap=None,
    )


def update_conversation_last_message(conversation_id: str, content: str) -> None:
    conversation = _conversations.get(conversation_id)
    if conversation is None:
        return
    conversation.last_message = content
    conversation.updated_at = _now_iso()


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
