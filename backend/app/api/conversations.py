from fastapi import APIRouter

from app.schemas.common import ApiError, ApiException, ApiResponse, ErrorResponse, ResponseMeta, new_request_id
from app.schemas.conversations import (
    ConversationData,
    ConversationListItem,
    CreateConversationRequest,
    MessageResponseData,
    SendMessageRequest,
)
from app.services.conversation_service import (
    build_demo_message_response,
    create_demo_conversation,
    get_demo_conversation,
    list_demo_conversations,
    update_conversation_last_message,
)

router = APIRouter(tags=["conversations"])


@router.get("/conversations", response_model=ApiResponse[list[ConversationListItem]])
def list_conversations(
    status: str | None = None,
    scenario_pack_code: str | None = None,
    risk_level: str | None = None,
) -> ApiResponse[list[ConversationListItem]]:
    conversations = list_demo_conversations(
        status=status,
        scenario_pack_code=scenario_pack_code,
        risk_level=risk_level,
    )
    return ApiResponse(
        request_id=new_request_id(),
        data=[ConversationListItem.model_validate(conversation.model_dump()) for conversation in conversations],
        meta=ResponseMeta(mock=True),
    )


@router.post("/conversations", response_model=ApiResponse[ConversationData])
def create_conversation(
    payload: CreateConversationRequest,
) -> ApiResponse[ConversationData]:
    conversation = create_demo_conversation(
        channel=payload.channel,
        scenario_pack_code=payload.scenario_pack_code,
        customer_alias=payload.customer_alias,
    )
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
    if get_demo_conversation(conversation_id) is None:
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

    update_conversation_last_message(conversation_id, payload.content)
    answer = build_demo_message_response(payload.content)
    return ApiResponse(
        request_id=new_request_id(),
        data=answer,
        meta=ResponseMeta(mock=True),
    )
