import json
from datetime import datetime
from typing import Any

from app.schemas.console import HandoffRecord, KnowledgeGapRecord
from app.services.static_data_source import get_database_url


class PostgresConsoleStoreError(Exception):
    def __init__(self, reason: str) -> None:
        self.reason = reason


def create_handoff_in_postgres(record: HandoffRecord) -> None:
    _execute(
        """
        INSERT INTO zycs_human_handoffs (
          id, conversation_id, reason, risk_level, suggested_owner, status, updated_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
          conversation_id = EXCLUDED.conversation_id,
          reason = EXCLUDED.reason,
          risk_level = EXCLUDED.risk_level,
          suggested_owner = EXCLUDED.suggested_owner,
          status = EXCLUDED.status,
          updated_at = EXCLUDED.updated_at
        """,
        (
            record.handoff_id,
            record.conversation_id,
            record.reason,
            record.risk_level,
            record.suggested_owner,
            record.status,
            record.updated_at,
        ),
    )


def list_handoffs_from_postgres(
    status: str | None = None,
    risk_level: str | None = None,
    suggested_owner: str | None = None,
) -> list[HandoffRecord]:
    where_clauses: list[str] = []
    params: list[str] = []
    if status is not None:
        where_clauses.append("h.status = %s")
        params.append(status)
    if risk_level is not None:
        where_clauses.append("h.risk_level = %s")
        params.append(risk_level)
    if suggested_owner is not None:
        where_clauses.append("h.suggested_owner = %s")
        params.append(suggested_owner)

    where_sql = ""
    if where_clauses:
        where_sql = "WHERE " + " AND ".join(where_clauses)
    rows = _fetch_all(_handoff_select_sql(where_sql), tuple(params))
    return [_handoff_from_row(row) for row in rows]


def update_handoff_status_in_postgres(
    handoff_id: str,
    status: str,
    resolution_note: str | None,
) -> HandoffRecord | None:
    row = _fetch_one(
        f"""
        WITH updated AS (
          UPDATE zycs_human_handoffs
          SET status = %s,
              updated_at = now()
          WHERE id = %s
          RETURNING *
        )
        {_handoff_select_sql("", table_name="updated")}
        """,
        (status, handoff_id),
    )
    if row is None:
        return None
    return _handoff_from_row(row, resolution_note=resolution_note)


def create_knowledge_gap_in_postgres(record: KnowledgeGapRecord) -> None:
    _execute(
        """
        INSERT INTO zycs_knowledge_gaps (
          id, conversation_id, question, suggested_tags, status, resolution_note, updated_at
        )
        VALUES (%s, %s, %s, %s::jsonb, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
          conversation_id = EXCLUDED.conversation_id,
          question = EXCLUDED.question,
          suggested_tags = EXCLUDED.suggested_tags,
          status = EXCLUDED.status,
          resolution_note = EXCLUDED.resolution_note,
          updated_at = EXCLUDED.updated_at
        """,
        (
            record.gap_id,
            record.conversation_id,
            record.question,
            json.dumps(record.tags, ensure_ascii=False),
            record.status,
            record.resolution_note,
            record.updated_at,
        ),
    )


def list_knowledge_gaps_from_postgres(
    status: str | None = None,
    scenario_pack_code: str | None = None,
    tag: str | None = None,
) -> list[KnowledgeGapRecord]:
    where_clauses: list[str] = []
    params: list[str] = []
    if status is not None:
        where_clauses.append("g.status = %s")
        params.append(status)
    if scenario_pack_code is not None:
        where_clauses.append("sp.code = %s")
        params.append(scenario_pack_code)

    where_sql = ""
    if where_clauses:
        where_sql = "WHERE " + " AND ".join(where_clauses)
    records = [
        _knowledge_gap_from_row(row)
        for row in _fetch_all(_knowledge_gap_select_sql(where_sql), tuple(params))
    ]
    if tag is None:
        return records
    return [record for record in records if tag in record.tags]


def update_knowledge_gap_status_in_postgres(
    gap_id: str,
    status: str,
    resolution_note: str | None,
) -> KnowledgeGapRecord | None:
    row = _fetch_one(
        f"""
        WITH updated AS (
          UPDATE zycs_knowledge_gaps
          SET status = %s,
              resolution_note = %s,
              updated_at = now()
          WHERE id = %s
          RETURNING *
        )
        {_knowledge_gap_select_sql("", table_name="updated")}
        """,
        (status, resolution_note, gap_id),
    )
    if row is None:
        return None
    return _knowledge_gap_from_row(row)


def _handoff_select_sql(where_sql: str, table_name: str = "zycs_human_handoffs") -> str:
    return f"""
        SELECT
          h.id,
          h.conversation_id,
          COALESCE(sp.code, '') AS scenario_pack_code,
          h.reason,
          h.suggested_owner,
          h.status,
          h.risk_level,
          h.updated_at
        FROM {table_name} h
        LEFT JOIN zycs_conversations c ON c.id = h.conversation_id
        LEFT JOIN zycs_scenario_packs sp ON sp.id = c.scenario_pack_id
        {where_sql}
        ORDER BY h.updated_at DESC, h.id
        """


def _knowledge_gap_select_sql(where_sql: str, table_name: str = "zycs_knowledge_gaps") -> str:
    return f"""
        SELECT
          g.id,
          g.conversation_id,
          COALESCE(sp.code, '') AS scenario_pack_code,
          g.question,
          g.suggested_tags,
          g.status,
          g.resolution_note,
          g.updated_at
        FROM {table_name} g
        LEFT JOIN zycs_conversations c ON c.id = g.conversation_id
        LEFT JOIN zycs_scenario_packs sp ON sp.id = c.scenario_pack_id
        {where_sql}
        ORDER BY g.updated_at DESC, g.id
        """


def _execute(sql: str, params: tuple[Any, ...]) -> None:
    try:
        import psycopg
    except ImportError as exc:
        raise PostgresConsoleStoreError(
            "psycopg is required when ZYCS_CONVERSATION_STORE=postgres"
        ) from exc

    try:
        database_url = get_database_url()
        with psycopg.connect(database_url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
            connection.commit()
    except Exception as exc:
        raise PostgresConsoleStoreError(f"failed to write console store: {exc}") from exc


def _fetch_one(sql: str, params: tuple[Any, ...]) -> dict[str, Any] | None:
    rows = _fetch_all(sql, params)
    if not rows:
        return None
    return rows[0]


def _fetch_all(sql: str, params: tuple[Any, ...]) -> list[dict[str, Any]]:
    try:
        import psycopg
        from psycopg.rows import dict_row
    except ImportError as exc:
        raise PostgresConsoleStoreError(
            "psycopg is required when ZYCS_CONVERSATION_STORE=postgres"
        ) from exc

    try:
        database_url = get_database_url()
        with psycopg.connect(database_url, row_factory=dict_row) as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                return list(cursor.fetchall())
    except Exception as exc:
        raise PostgresConsoleStoreError(f"failed to read console store: {exc}") from exc


def _handoff_from_row(
    row: dict[str, Any],
    resolution_note: str | None = None,
) -> HandoffRecord:
    reason = str(row["reason"])
    return HandoffRecord(
        handoff_id=str(row["id"]),
        conversation_id=str(row["conversation_id"] or ""),
        scenario_pack_code=str(row["scenario_pack_code"] or ""),
        reason=reason,
        suggested_owner=str(row["suggested_owner"]),
        status=str(row["status"]),
        risk_level=str(row["risk_level"]),
        summary=reason,
        resolution_note=resolution_note,
        updated_at=_format_timestamp(row["updated_at"]),
        mock=True,
    )


def _knowledge_gap_from_row(row: dict[str, Any]) -> KnowledgeGapRecord:
    return KnowledgeGapRecord(
        gap_id=str(row["id"]),
        conversation_id=str(row["conversation_id"] or ""),
        scenario_pack_code=str(row["scenario_pack_code"] or ""),
        question=str(row["question"]),
        tags=_tags_from_jsonb(row["suggested_tags"]),
        status=str(row["status"]),
        resolution_note=(
            str(row["resolution_note"]) if row["resolution_note"] is not None else None
        ),
        updated_at=_format_timestamp(row["updated_at"]),
        mock=True,
    )


def _tags_from_jsonb(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, str):
        try:
            loaded = json.loads(value)
        except json.JSONDecodeError:
            return []
        if isinstance(loaded, list):
            return [str(item) for item in loaded]
    return []


def _format_timestamp(value: Any) -> str:
    if isinstance(value, datetime):
        return value.isoformat(timespec="seconds")
    return str(value)
