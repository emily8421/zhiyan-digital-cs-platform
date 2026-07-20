import re
from dataclasses import dataclass, replace

from app.adapters.llm_adapter import generate_llm_answer
from app.schemas.mock_business import MockBusinessRecordResponse
from app.schemas.scenario_packs import IntentItem, KnowledgeItem, RuleItem
from app.services.mock_business_service import MockRecordNotFoundError, get_mock_business_record
from app.services.scenario_pack_service import ScenarioPackNotFoundError, get_scenario_pack


@dataclass(frozen=True)
class MessageDecision:
    intent: str
    answer_type: str
    answer: str
    source_ref: str
    risk_level: str
    handoff_reason: str | None = None
    gap_question: str | None = None
    mock_record: MockBusinessRecordResponse | None = None
    llm: dict[str, object] | None = None


_HIGH_RISK_PATTERNS = [
    ("high_risk_complaint", "投诉|曝光|抖音|维权", "投诉舆情问题必须人工确认。", "high"),
    ("high_risk_compensation", "赔钱|补偿|赔偿|赔付", "赔付承诺问题必须人工确认。", "high"),
    ("high_risk_contract", "合同|违约|法律责任|责任", "合同责任问题必须人工确认。", "high"),
    ("high_risk_price", "最低价|报价|打折|价格", "价格承诺问题必须人工确认。", "medium"),
    ("high_risk_delivery", "保证交期|一定到货|交期承诺", "交期承诺问题必须人工确认。", "medium"),
    ("privacy_data", "手机|身份证|地址|账号|token|api[_-]?key|secret", "疑似隐私或凭据内容不得自动处理。", "high"),
]

_MOCK_REF_PATTERN = re.compile(r"\b(HC-ORDER-\d+|XS-PROJ-\d+|XS-TICKET-\d+|DEMO-ORDER-\d{6}-\d+|DEMO-PROJ-\d{6}-\d+|DEMO-TICKET-\d{6}-\d+)\b", re.IGNORECASE)

_MOCK_REF_TYPES = {
    "HC-ORDER": "order",
    "XS-PROJ": "project",
    "XS-TICKET": "ticket",
    "DEMO-ORDER": "order",
    "DEMO-PROJ": "project",
    "DEMO-TICKET": "ticket",
}


_LLM_ELIGIBLE_ANSWER_TYPES = {"mock_business", "knowledge", "rule"}


def decide_message_response(content: str, scenario_pack_code: str) -> MessageDecision:
    stripped_content = content.strip()
    high_risk_decision = _match_high_risk(stripped_content)
    if high_risk_decision is not None:
        return high_risk_decision

    decision = _match_mock_business(stripped_content)
    if decision is None:
        decision = _match_knowledge_or_rule(stripped_content, scenario_pack_code)
    if decision is None:
        decision = _default_gap(stripped_content)
    return _maybe_llm_rewrite(decision, stripped_content)


def _default_gap(content: str) -> MessageDecision:
    return MessageDecision(
        intent="unknown_question",
        answer_type="gap",
        answer="这个问题当前知识库没有可追溯依据，我已记录为知识缺口，等待人工确认后再回复。",
        source_ref="policy:knowledge_gap",
        risk_level="medium",
        gap_question=content,
    )


def _maybe_llm_rewrite(decision: MessageDecision, question: str) -> MessageDecision:
    # 高风险 handoff 在 decide_message_response 入口短路，不会到达这里；
    # 无依据 gap 不属于证据型，也不进入 LLM，避免编造业务事实。
    if decision.answer_type not in _LLM_ELIGIBLE_ANSWER_TYPES:
        return decision
    llm_result = generate_llm_answer(
        question=question,
        base_answer_type=decision.answer_type,
        base_answer=decision.answer,
        source_ref=decision.source_ref,
    )
    if llm_result is None:
        return decision
    return replace(
        decision,
        answer_type="llm_sandbox",
        answer=llm_result.answer,
        source_ref=llm_result.source_ref,
        llm={
            "mode": llm_result.mode_used,
            "base_answer_type": llm_result.base_answer_type,
            "mock": llm_result.mock,
            "evidence": list(llm_result.evidence),
            "fallback_reason": llm_result.fallback_reason,
        },
    )


def _match_high_risk(content: str) -> MessageDecision | None:
    for intent, pattern, reason, risk_level in _HIGH_RISK_PATTERNS:
        if re.search(pattern, content, flags=re.IGNORECASE):
            return MessageDecision(
                intent=intent,
                answer_type="handoff",
                answer="这个问题需要人工确认，我已记录为待跟进事项；在人工确认前不会给出承诺性答复。",
                source_ref="rule:high_risk_handoff",
                risk_level=risk_level,
                handoff_reason=reason,
            )
    return None


def _match_mock_business(content: str) -> MessageDecision | None:
    match = _MOCK_REF_PATTERN.search(content)
    if match is None:
        return None
    external_ref = match.group(1).upper()
    record_type = _record_type_for_ref(external_ref)
    if record_type is None:
        return None
    try:
        record = get_mock_business_record(record_type, external_ref)
    except MockRecordNotFoundError:
        return MessageDecision(
            intent="missing_mock_business",
            answer_type="gap",
            answer="这个编号当前没有可查询的业务记录，我已记录为知识缺口，避免编造进度。",
            source_ref=f"mock_business:{external_ref}:missing",
            risk_level="medium",
            gap_question=f"缺少 Mock 业务记录：{external_ref}",
        )
    return MessageDecision(
        intent=f"{record.record_type}_progress",
        answer_type="mock_business",
        answer=f"{record.summary} 下一步：{record.next_step}",
        source_ref=record.source_ref,
        risk_level="low",
        mock_record=record,
    )


def _match_knowledge_or_rule(content: str, scenario_pack_code: str) -> MessageDecision | None:
    try:
        scenario_pack = get_scenario_pack(scenario_pack_code)
    except ScenarioPackNotFoundError:
        return None

    rule = _find_answer_rule(content, scenario_pack.rule_items)
    if rule is not None:
        return MessageDecision(
            intent=rule.rule_type,
            answer_type="rule",
            answer="当前问题命中场景包规则，涉及承诺或风险事项时以人工确认结果为准。",
            source_ref=rule.source_ref,
            risk_level="low",
        )

    knowledge_candidates = list(scenario_pack.knowledge_items) + _load_active_knowledge_items(
        scenario_pack_code
    )
    knowledge_item = _find_knowledge_item(content, knowledge_candidates, scenario_pack.intents)
    if knowledge_item is not None:
        return MessageDecision(
            intent="knowledge_lookup",
            answer_type="knowledge",
            answer=knowledge_item.content,
            source_ref=knowledge_item.source_ref,
            risk_level="low",
        )
    return None


def _load_active_knowledge_items(scenario_pack_code: str) -> list[KnowledgeItem]:
    from app.services.console_service import list_knowledge_items

    try:
        records = list_knowledge_items(scenario_pack_code=scenario_pack_code, status="active")
    except Exception:
        return []
    return [
        KnowledgeItem(
            id=record.item_id,
            title=record.title,
            content=record.content,
            source_ref=record.source_ref,
        )
        for record in records
    ]


def _find_answer_rule(content: str, rules: list[RuleItem]) -> RuleItem | None:
    for rule in rules:
        if rule.action == "answer" and re.search(rule.pattern, content, flags=re.IGNORECASE):
            return rule
    return None


def _find_knowledge_item(
    content: str,
    knowledge_items: list[KnowledgeItem],
    intents: list[IntentItem],
) -> KnowledgeItem | None:
    best_match: KnowledgeItem | None = None
    best_score = 0
    for knowledge_item in knowledge_items:
        score = _text_match_score(content, knowledge_item.title)
        if score > best_score:
            best_match = knowledge_item
            best_score = score
    if best_score >= 2:
        return best_match

    matched_intent = _find_intent_by_example(content, intents)
    if matched_intent is None:
        return None
    return _find_knowledge_item_for_intent(matched_intent, knowledge_items)


def _find_intent_by_example(content: str, intents: list[IntentItem]) -> IntentItem | None:
    best_match: IntentItem | None = None
    best_score = 0
    for intent in intents:
        references = [intent.name, *intent.examples]
        score = max((_text_match_score(content, reference) for reference in references), default=0)
        if score > best_score:
            best_match = intent
            best_score = score
    if best_score >= 2:
        return best_match
    return None


def _find_knowledge_item_for_intent(
    intent: IntentItem,
    knowledge_items: list[KnowledgeItem],
) -> KnowledgeItem | None:
    intent_reference = " ".join([intent.name, *intent.examples])
    best_match: KnowledgeItem | None = None
    best_score = 0
    for knowledge_item in knowledge_items:
        knowledge_reference = f"{knowledge_item.title} {knowledge_item.content}"
        score = _text_match_score(intent_reference, knowledge_reference)
        if score > best_score:
            best_match = knowledge_item
            best_score = score
    if best_score >= 2:
        return best_match
    return None


def _text_match_score(content: str, reference: str) -> int:
    normalized_content = _normalize_text(content)
    normalized_reference = _normalize_text(reference)
    if not normalized_content or not normalized_reference:
        return 0
    if normalized_reference in normalized_content or normalized_content in normalized_reference:
        return 4
    content_grams = _character_ngrams(normalized_content)
    reference_grams = _character_ngrams(normalized_reference)
    return len(content_grams & reference_grams)


def _normalize_text(value: str) -> str:
    return re.sub(r"[^0-9a-zA-Z\u4e00-\u9fff]+", "", value).lower()


def _character_ngrams(value: str, size: int = 2) -> set[str]:
    if len(value) < size:
        return {value} if value else set()
    return {value[index : index + size] for index in range(len(value) - size + 1)}


def _record_type_for_ref(external_ref: str) -> str | None:
    for prefix, record_type in _MOCK_REF_TYPES.items():
        if external_ref.startswith(prefix):
            return record_type
    return None
