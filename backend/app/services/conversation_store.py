import os
from datetime import datetime
from typing import Any

from app.schemas.conversations import ConversationData
from app.services.static_data_source import get_database_url


class ConversationStoreConfigError(Exception):
    def __init__(self, reason: str) -> None:
        self.reason = reason


class PostgresConversationStoreError(Exception):
    def __init__(self, reason: str) -> None:
        self.reason = reason


def get_conversation_store() -> str:
    value = os.getenv("ZYCS_CONVERSATION_STORE", "memory").strip().lower()
    if value in {"", "memory", "postgres"}:
        return value or "memory"
    raise ConversationStoreConfigError(
        "ZYCS_CONVERSATION_STORE must be unset, 'memory', or 'postgres'"
    )


def should_use_postgres_conversation_store() -> bool:
    return get_conversation_store() == "postgres"


def create_conversation_in_postgres(conversation: ConversationData) -> None:
    _execute(
        """
        INSERT INTO zycs_conversations (
          id, channel, scenario_pack_id, customer_alias, status, risk_level, is_mock, updated_at
        )
        VALUES (
          %s,
          %s,
          (SELECT id FROM zycs_scenario_packs WHERE code = %s),
          %s,
          %s,
          %s,
          %s,
          %s
        )
        ON CONFLICT (id) DO UPDATE SET
          channel = EXCLUDED.channel,
          scenario_pack_id = EXCLUDED.scenario_pack_id,
          customer_alias = EXCLUDED.customer_alias,
          status = EXCLUDED.status,
          risk_level = EXCLUDED.risk_level,
          is_mock = EXCLUDED.is_mock,
          updated_at = EXCLUDED.updated_at
        """,
        (
            conversation.conversation_id,
            conversation.channel,
            conversation.scenario_pack_code,
            conversation.customer_alias,
            conversation.status,
            conversation.risk_level,
            conversation.mock,
            conversation.updated_at,
        ),
    )


def get_conversation_from_postgres(conversation_id: str) -> ConversationData | None:
    rows = _fetch_all(
        _conversation_select_sql("WHERE c.id = %s"),
        (conversation_id,),
    )
    if not rows:
        return None
    return _conversation_from_row(rows[0])


def list_conversations_from_postgres(
    status: str | None = None,
    scenario_pack_code: str | None = None,
    risk_level: str | None = None,
) -> list[ConversationData]:
    where_clauses: list[str] = []
    params: list[str] = []
    if status is not None:
        where_clauses.append("c.status = %s")
        params.append(status)
    if scenario_pack_code is not None:
        where_clauses.append("sp.code = %s")
        params.append(scenario_pack_code)
    if risk_level is not None:
        where_clauses.append("c.risk_level = %s")
        params.append(risk_level)

    where_sql = ""
    if where_clauses:
        where_sql = "WHERE " + " AND ".join(where_clauses)
    rows = _fetch_all(_conversation_select_sql(where_sql), tuple(params))
    return [_conversation_from_row(row) for row in rows]


def update_conversation_in_postgres(conversation: ConversationData) -> None:
    _execute(
        """
        UPDATE zycs_conversations
        SET status = %s,
            risk_level = %s,
            updated_at = %s
        WHERE id = %s
        """,
        (
            conversation.status,
            conversation.risk_level,
            conversation.updated_at,
            conversation.conversation_id,
        ),
    )


def append_message_to_postgres(
    message_id: str,
    conversation_id: str,
    sender_type: str,
    content: str,
    intent: str | None = None,
    answer_type: str | None = None,
    source_ref: str | None = None,
) -> None:
    _execute(
        """
        INSERT INTO zycs_messages (
          id, conversation_id, sender_type, content, intent, answer_type, source_ref, is_mock
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, true)
        ON CONFLICT (id) DO NOTHING
        """,
        (
            message_id,
            conversation_id,
            sender_type,
            content,
            intent,
            answer_type,
            source_ref,
        ),
    )


def _conversation_select_sql(where_sql: str) -> str:
    return f"""
        SELECT
          c.id,
          c.channel,
          sp.code AS scenario_pack_code,
          c.customer_alias,
          c.status,
          c.risk_level,
          c.is_mock,
          c.updated_at,
          COALESCE(last_customer_message.content, '会话已创建，等待客户提问。') AS last_message
        FROM zycs_conversations c
        LEFT JOIN zycs_scenario_packs sp ON sp.id = c.scenario_pack_id
        LEFT JOIN LATERAL (
          SELECT content
          FROM zycs_messages m
          WHERE m.conversation_id = c.id AND m.sender_type = 'customer'
          ORDER BY m.created_at DESC
          LIMIT 1
        ) last_customer_message ON true
        {where_sql}
        ORDER BY c.updated_at DESC, c.id
        """


def _execute(sql: str, params: tuple[Any, ...]) -> None:
    try:
        import psycopg
    except ImportError as exc:
        raise PostgresConversationStoreError(
            "psycopg is required when ZYCS_CONVERSATION_STORE=postgres"
        ) from exc

    try:
        database_url = get_database_url()
        with psycopg.connect(database_url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
            connection.commit()
    except Exception as exc:
        raise PostgresConversationStoreError(f"failed to write conversation store: {exc}") from exc


def _fetch_all(sql: str, params: tuple[Any, ...]) -> list[dict[str, Any]]:
    try:
        import psycopg
        from psycopg.rows import dict_row
    except ImportError as exc:
        raise PostgresConversationStoreError(
            "psycopg is required when ZYCS_CONVERSATION_STORE=postgres"
        ) from exc

    try:
        database_url = get_database_url()
        with psycopg.connect(database_url, row_factory=dict_row) as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                return list(cursor.fetchall())
    except Exception as exc:
        raise PostgresConversationStoreError(f"failed to read conversation store: {exc}") from exc


def _conversation_from_row(row: dict[str, Any]) -> ConversationData:
    return ConversationData(
        conversation_id=str(row["id"]),
        channel=str(row["channel"]),
        scenario_pack_code=str(row["scenario_pack_code"] or ""),
        status=str(row["status"]),
        risk_level=str(row["risk_level"]),
        last_message=str(row["last_message"]),
        customer_alias=str(row["customer_alias"]) if row["customer_alias"] is not None else None,
        updated_at=_format_timestamp(row["updated_at"]),
        mock=bool(row["is_mock"]),
    )


def _format_timestamp(value: Any) -> str:
    if isinstance(value, datetime):
        return value.isoformat(timespec="seconds")
    return str(value)

