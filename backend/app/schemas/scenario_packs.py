from pydantic import BaseModel, Field


class IntentItem(BaseModel):
    code: str
    name: str
    examples: list[str] = Field(default_factory=list)


class KnowledgeItem(BaseModel):
    id: str
    title: str
    content: str
    source_ref: str


class RuleItem(BaseModel):
    id: str
    rule_type: str
    pattern: str
    action: str
    source_ref: str


class HandoffRule(BaseModel):
    code: str
    description: str


class MockBusinessRecord(BaseModel):
    record_type: str
    external_ref: str
    status: str
    summary: str
    next_step: str
    eta: str | None = None
    is_mock: bool = True


class ScenarioPack(BaseModel):
    code: str
    name: str
    description: str
    source_refs: list[str]
    intents: list[IntentItem]
    knowledge_items: list[KnowledgeItem]
    rule_items: list[RuleItem]
    mock_business_records: list[MockBusinessRecord]
    handoff_rules: list[HandoffRule]
    demo_questions: list[str]


class ScenarioPackSummary(BaseModel):
    code: str
    name: str
    description: str
    source_refs: list[str]
    knowledge_count: int
    rule_count: int
    mock_business_count: int
    demo_questions: list[str]


def to_summary(pack: ScenarioPack) -> ScenarioPackSummary:
    return ScenarioPackSummary(
        code=pack.code,
        name=pack.name,
        description=pack.description,
        source_refs=pack.source_refs,
        knowledge_count=len(pack.knowledge_items),
        rule_count=len(pack.rule_items),
        mock_business_count=len(pack.mock_business_records),
        demo_questions=pack.demo_questions,
    )
