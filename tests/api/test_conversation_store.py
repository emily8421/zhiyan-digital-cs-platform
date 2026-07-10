import importlib.util
import os

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


def test_default_conversation_store_uses_memory(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ZYCS_CONVERSATION_STORE", raising=False)
    monkeypatch.delenv("ZYCS_DATABASE_URL", raising=False)

    client = TestClient(create_app())
    create_response = client.post(
        "/api/v1/conversations",
        json={
            "channel": "h5",
            "scenario_pack_code": "product_business",
            "customer_alias": "memory_store_smoke",
        },
    )
    conversation_id = create_response.json()["data"]["conversation_id"]

    message_response = client.post(
        f"/api/v1/conversations/{conversation_id}/messages",
        json={"content": "灯带有什么规格？"},
    )

    assert create_response.status_code == 200
    assert message_response.status_code == 200
    assert message_response.json()["data"]["answer_type"] == "knowledge"


def test_postgres_conversation_store_without_url_falls_back_to_memory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ZYCS_CONVERSATION_STORE", "postgres")
    monkeypatch.delenv("ZYCS_DATABASE_URL", raising=False)

    client = TestClient(create_app())
    create_response = client.post(
        "/api/v1/conversations",
        json={"channel": "h5", "scenario_pack_code": "product_business"},
    )
    conversation_id = create_response.json()["data"]["conversation_id"]

    message_response = client.post(
        f"/api/v1/conversations/{conversation_id}/messages",
        json={"content": "灯带有什么规格？"},
    )

    assert create_response.status_code == 200
    assert message_response.status_code == 200
    assert message_response.json()["data"]["answer_type"] == "knowledge"


@pytest.mark.skipif(
    importlib.util.find_spec("psycopg") is None,
    reason="psycopg is not installed",
)
def test_postgres_conversation_store_persists_conversation_and_messages(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database_url = os.getenv("ZYCS_TEST_DATABASE_URL")
    if not database_url:
        pytest.skip("ZYCS_TEST_DATABASE_URL is not set")

    import psycopg
    from psycopg.rows import dict_row

    monkeypatch.setenv("ZYCS_CONVERSATION_STORE", "postgres")
    monkeypatch.setenv("ZYCS_DATABASE_URL", database_url)

    client = TestClient(create_app())
    customer_alias = "pg_store_smoke"
    create_response = client.post(
        "/api/v1/conversations",
        json={
            "channel": "h5",
            "scenario_pack_code": "product_business",
            "customer_alias": customer_alias,
        },
    )
    assert create_response.status_code == 200
    conversation_id = create_response.json()["data"]["conversation_id"]

    message_response = client.post(
        f"/api/v1/conversations/{conversation_id}/messages",
        json={"content": "灯带有什么规格？"},
    )
    assert message_response.status_code == 200
    assert message_response.json()["data"]["answer_type"] == "knowledge"

    list_response = client.get("/api/v1/conversations", params={"scenario_pack_code": "product_business"})
    assert list_response.status_code == 200
    assert conversation_id in {item["conversation_id"] for item in list_response.json()["data"]}

    with psycopg.connect(database_url, row_factory=dict_row) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT c.id, c.customer_alias, c.status, sp.code AS scenario_pack_code
                FROM zycs_conversations c
                JOIN zycs_scenario_packs sp ON sp.id = c.scenario_pack_id
                WHERE c.id = %s
                """,
                (conversation_id,),
            )
            conversation = cursor.fetchone()
            cursor.execute(
                """
                SELECT sender_type, answer_type, source_ref
                FROM zycs_messages
                WHERE conversation_id = %s
                ORDER BY created_at, sender_type
                """,
                (conversation_id,),
            )
            messages = cursor.fetchall()

    assert conversation is not None
    assert conversation["customer_alias"] == customer_alias
    assert conversation["scenario_pack_code"] == "product_business"
    assert {message["sender_type"] for message in messages} == {"customer", "assistant"}
    assistant_messages = [message for message in messages if message["sender_type"] == "assistant"]
    assert assistant_messages[0]["answer_type"] == "knowledge"
    assert assistant_messages[0]["source_ref"] == "SRC-SP-PRODUCT-001"


@pytest.mark.skipif(
    importlib.util.find_spec("psycopg") is None,
    reason="psycopg is not installed",
)
def test_postgres_conversation_store_updates_handoff_status(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database_url = os.getenv("ZYCS_TEST_DATABASE_URL")
    if not database_url:
        pytest.skip("ZYCS_TEST_DATABASE_URL is not set")

    import psycopg

    monkeypatch.setenv("ZYCS_CONVERSATION_STORE", "postgres")
    monkeypatch.setenv("ZYCS_DATABASE_URL", database_url)

    client = TestClient(create_app())
    create_response = client.post(
        "/api/v1/conversations",
        json={"channel": "h5", "scenario_pack_code": "product_business"},
    )
    conversation_id = create_response.json()["data"]["conversation_id"]

    message_response = client.post(
        f"/api/v1/conversations/{conversation_id}/messages",
        json={"content": "如果客户投诉并要求赔偿，你们能保证赔多少钱？"},
    )
    assert message_response.status_code == 200
    assert message_response.json()["data"]["answer_type"] == "handoff"

    with psycopg.connect(database_url) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT status, risk_level FROM zycs_conversations WHERE id = %s",
                (conversation_id,),
            )
            status, risk_level = cursor.fetchone()

    assert status == "handoff"
    assert risk_level == "high"
