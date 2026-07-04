from pydantic import BaseModel, Field


class CreateConversationRequest(BaseModel):
    channel: str = Field(default="h5")
    scenario_pack_code: str = Field(default="product_business")
    customer_alias: str | None = None


class ConversationData(BaseModel):
    conversation_id: str
    status: str
    scenario_pack_code: str


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
