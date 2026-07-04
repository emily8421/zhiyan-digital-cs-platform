from pydantic import BaseModel, Field


class CreateConversationRequest(BaseModel):
    channel: str = Field(default="h5")
    scenario_pack_code: str = Field(default="product_business")
    customer_alias: str | None = None


class ConversationData(BaseModel):
    conversation_id: str
    channel: str = "h5"
    scenario_pack_code: str
    status: str
    risk_level: str = "low"
    last_message: str = ""
    customer_alias: str | None = None
    updated_at: str = ""
    mock: bool = True


class ConversationListItem(BaseModel):
    conversation_id: str
    channel: str
    scenario_pack_code: str
    status: str
    risk_level: str
    last_message: str
    updated_at: str
    mock: bool = True


class SendMessageRequest(BaseModel):
    content: str = Field(min_length=1)


class MessageResponseData(BaseModel):
    message_id: str
    intent: str
    answer_type: str
    answer: str
    source_ref: str
    handoff: dict[str, object] | None = None
    knowledge_gap: dict[str, object] | None = None
