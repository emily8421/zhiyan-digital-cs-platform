from uuid import uuid4

from fastapi import APIRouter

from app.schemas.common import ApiError, ApiException, ApiResponse, ErrorResponse, ResponseMeta, new_request_id
from app.schemas.conversations import (
    ConversationData,
    CreateConversationRequest,
    MessageResponseData,
    SendMessageRequest,
)

router = APIRouter(tags=["conversations"])

_conversations: dict[str, ConversationData] = {}


def _new_demo_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:8]}"


@router.post("/conversations", response_model=ApiResponse[ConversationData])
def create_conversation(
    payload: CreateConversationRequest,
) -> ApiResponse[ConversationData]:
    conversation = ConversationData(
        conversation_id=_new_demo_id("conv"),
        status="open",
        scenario_pack_code=payload.scenario_pack_code,
    )
    _conversations[conversation.conversation_id] = conversation
    return ApiResponse(
        request_id=new_request_id(),
        data=conversation,
        meta=ResponseMeta(mock=True),
    )


@router.post(
    "/conversations/{conversation_id}/messages",
    response_model=ApiResponse[MessageResponseData],
    responses={404: {"model": ErrorResponse}},
)
def send_message(
    conversation_id: str,
    payload: SendMessageRequest,
) -> ApiResponse[MessageResponseData]:
    if conversation_id not in _conversations:
        raise ApiException(
            status_code=404,
            response=ErrorResponse(
                request_id=new_request_id(),
                error=ApiError(
                    code="CONVERSATION_NOT_FOUND",
                    message="会话不存在",
                    details={"conversation_id": conversation_id},
                ),
            ),
        )

    answer = MessageResponseData(
        message_id=_new_demo_id("msg"),
        intent="demo_echo",
        answer_type="mock_business",
        answer=f"这是 Mock 回复：已收到你的问题“{payload.content}”。",
        source_ref="mock:sprint-1",
        handoff=None,
        knowledge_gap=None,
    )
    return ApiResponse(
        request_id=new_request_id(),
        data=answer,
        meta=ResponseMeta(mock=True),
    )
