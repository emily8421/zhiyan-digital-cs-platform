from collections import defaultdict
from typing import Any

from app.schemas.scenario_packs import (
    HandoffRule,
    IntentItem,
    KnowledgeItem,
    MockBusinessRecord,
    RuleItem,
    ScenarioPack,
)
from app.services.static_data_source import get_database_url


class PostgresStaticDataError(Exception):
    def __init__(self, reason: str) -> None:
        self.reason = reason


def load_scenario_packs_from_postgres() -> dict[str, ScenarioPack]:
    try:
        import psycopg
        from psycopg.rows import dict_row
    except ImportError as exc:
        raise PostgresStaticDataError(
            "psycopg is required when ZYCS_STATIC_DATA_SOURCE=postgres"
        ) from exc

    try:
        database_url = get_database_url()
    except Exception as exc:
        raise PostgresStaticDataError(str(exc)) from exc

    try:
        with psycopg.connect(database_url, row_factory=dict_row) as connection:
            scenario_pack_rows = _fetch_all(
                connection,
                """
                SELECT id, code, name, description, source_ref
                FROM zycs_scenario_packs
                WHERE status = 'active'
                ORDER BY code
                """,
            )
            knowledge_rows = _fetch_all(
                connection,
                """
                SELECT id, scenario_pack_id, title, content, source_ref
                FROM zycs_knowledge_items
                WHERE status = 'active'
                ORDER BY id
                """,
            )
            rule_rows = _fetch_all(
                connection,
                """
                SELECT id, scenario_pack_id, rule_type, pattern, action, source_ref
                FROM zycs_rule_items
                WHERE enabled = true
                ORDER BY priority, id
                """,
            )
            mock_rows = _fetch_all(
                connection,
                """
                SELECT record_type, external_ref, scenario_pack_id, status, summary, next_step, eta, payload, is_mock
                FROM zycs_mock_business_records
                ORDER BY external_ref
                """,
            )
    except Exception as exc:
        raise PostgresStaticDataError(f"failed to load static data from PostgreSQL: {exc}") from exc

    return _build_scenario_packs(scenario_pack_rows, knowledge_rows, rule_rows, mock_rows)


def _fetch_all(connection: Any, sql: str) -> list[dict[str, Any]]:
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return list(cursor.fetchall())


def _build_scenario_packs(
    scenario_pack_rows: list[dict[str, Any]],
    knowledge_rows: list[dict[str, Any]],
    rule_rows: list[dict[str, Any]],
    mock_rows: list[dict[str, Any]],
) -> dict[str, ScenarioPack]:
    knowledge_by_pack = _group_by_pack(knowledge_rows)
    rules_by_pack = _group_by_pack(rule_rows)
    mocks_by_pack = _group_by_pack(mock_rows)

    packs: dict[str, ScenarioPack] = {}
    for row in scenario_pack_rows:
        pack_id = str(row["id"])
        pack = ScenarioPack(
            code=str(row["code"]),
            name=str(row["name"]),
            description=str(row["description"]),
            source_refs=[str(row["source_ref"])],
            intents=_build_intents(row, knowledge_by_pack[pack_id], mock_rows=mocks_by_pack[pack_id]),
            knowledge_items=[_build_knowledge_item(item) for item in knowledge_by_pack[pack_id]],
            rule_items=[_build_rule_item(item) for item in rules_by_pack[pack_id]],
            mock_business_records=[_build_mock_business_record(item) for item in mocks_by_pack[pack_id]],
            handoff_rules=[_build_handoff_rule(row, rules_by_pack[pack_id])],
            demo_questions=_build_demo_questions(row, mocks_by_pack[pack_id]),
        )
        packs[pack.code] = pack
    return packs


def _group_by_pack(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        scenario_pack_id = row.get("scenario_pack_id")
        if scenario_pack_id is not None:
            grouped[str(scenario_pack_id)].append(row)
    return grouped


def _build_knowledge_item(row: dict[str, Any]) -> KnowledgeItem:
    return KnowledgeItem(
        id=str(row["id"]),
        title=str(row["title"]),
        content=str(row["content"]),
        source_ref=str(row["source_ref"]),
    )


def _build_rule_item(row: dict[str, Any]) -> RuleItem:
    return RuleItem(
        id=str(row["id"]),
        rule_type=str(row["rule_type"]),
        pattern=str(row["pattern"]),
        action=str(row["action"]),
        source_ref=str(row["source_ref"]),
    )


def _build_mock_business_record(row: dict[str, Any]) -> MockBusinessRecord:
    payload = row.get("payload") or {}
    if not isinstance(payload, dict):
        payload = {}
    return MockBusinessRecord(
        record_type=str(row["record_type"]),
        external_ref=str(row["external_ref"]),
        status=str(row["status"]),
        summary=str(row["summary"]),
        next_step=str(row["next_step"]),
        eta=str(row["eta"]) if row["eta"] is not None else None,
        is_mock=bool(row["is_mock"]),
        source_ref=str(payload.get("source_ref") or f"demo_sandbox:{row['record_type']}:{row['external_ref']}"),
        source_system=str(payload.get("source_system") or "demo_sandbox"),
        environment=str(payload.get("environment") or "demo_sandbox"),
        stage=str(payload["stage"]) if payload.get("stage") is not None else None,
        payload=payload,
    )


def _build_intents(
    scenario_pack_row: dict[str, Any],
    knowledge_rows: list[dict[str, Any]],
    mock_rows: list[dict[str, Any]],
) -> list[IntentItem]:
    code = str(scenario_pack_row["code"])
    first_mock_ref = str(mock_rows[0]["external_ref"]) if mock_rows else "MOCK-REF-001"
    if code == "project_business":
        return [
            IntentItem(
                code="project_consultation",
                name="方案咨询",
                examples=_knowledge_examples(knowledge_rows),
            ),
            IntentItem(
                code="project_progress",
                name="项目进度",
                examples=[f"{first_mock_ref} 到哪个阶段了"],
            ),
        ]
    return [
        IntentItem(
            code="product_consultation",
            name="产品咨询",
            examples=_knowledge_examples(knowledge_rows),
        ),
        IntentItem(
            code="order_progress",
            name="订单进度",
            examples=[f"我想查一下 {first_mock_ref} 的生产进度"],
        ),
    ]


def _knowledge_examples(knowledge_rows: list[dict[str, Any]]) -> list[str]:
    return [str(row["title"]) for row in knowledge_rows]


def _build_handoff_rule(
    scenario_pack_row: dict[str, Any],
    rule_rows: list[dict[str, Any]],
) -> HandoffRule:
    code = f"{scenario_pack_row['code']}_high_risk"
    description = "高风险问题必须转人工。"
    if rule_rows:
        description = f"命中规则 {rule_rows[0]['pattern']} 时必须转人工。"
    return HandoffRule(code=code, description=description)


def _build_demo_questions(
    scenario_pack_row: dict[str, Any],
    mock_rows: list[dict[str, Any]],
) -> list[str]:
    code = str(scenario_pack_row["code"])
    questions = ["灯带有什么规格？"] if code == "product_business" else ["项目开发有哪些阶段？"]
    if mock_rows:
        external_ref = str(mock_rows[0]["external_ref"])
        if code == "product_business":
            questions.append(f"我想查一下 {external_ref} 的生产进度")
        else:
            questions.append(f"{external_ref} 到哪个阶段了？")
    questions.append("如果客户要赔偿怎么办？")
    return questions
