import importlib.util
import os

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


def test_postgres_console_store_without_url_falls_back_to_memory(
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
        json={"content": "如果客户投诉并要求赔偿，你们能保证赔多少钱？"},
    )

    assert create_response.status_code == 200
    assert message_response.status_code == 200
    assert message_response.json()["data"]["answer_type"] == "handoff"

    handoff_id = message_response.json()["data"]["handoff"]["handoff_id"]
    list_response = client.get("/api/v1/handoffs")

    assert list_response.status_code == 200
    assert handoff_id in {item["handoff_id"] for item in list_response.json()["data"]}


@pytest.mark.skipif(
    importlib.util.find_spec("psycopg") is None,
    reason="psycopg is not installed",
)
def test_postgres_console_store_persists_handoff_and_gap(
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
    handoff_conversation_id = _create_conversation(client)
    handoff_response = client.post(
        f"/api/v1/conversations/{handoff_conversation_id}/messages",
        json={"content": "如果客户投诉并要求赔偿，你们能保证赔多少钱？"},
    )
    assert handoff_response.status_code == 200
    handoff = handoff_response.json()["data"]["handoff"]

    gap_conversation_id = _create_conversation(client)
    gap_response = client.post(
        f"/api/v1/conversations/{gap_conversation_id}/messages",
        json={"content": "火星基地土豆种植方案是什么？"},
    )
    assert gap_response.status_code == 200
    gap = gap_response.json()["data"]["knowledge_gap"]

    handoff_list = client.get("/api/v1/handoffs", params={"status": "open"})
    gap_list = client.get("/api/v1/knowledge-gaps", params={"status": "new", "tag": "待确认"})

    assert handoff["handoff_id"] in {
        item["handoff_id"] for item in handoff_list.json()["data"]
    }
    assert gap["gap_id"] in {item["gap_id"] for item in gap_list.json()["data"]}

    handoff_patch = client.patch(
        f"/api/v1/handoffs/{handoff['handoff_id']}",
        headers={"X-Console-Role": "admin"},
        json={"status": "processing", "resolution_note": "PG 模式已分配处理"},
    )
    gap_patch = client.patch(
        f"/api/v1/knowledge-gaps/{gap['gap_id']}",
        headers={"X-Console-Role": "admin"},
        json={"status": "reviewing", "resolution_note": "PG 模式等待知识运营确认"},
    )

    assert handoff_patch.status_code == 200
    assert handoff_patch.json()["data"]["status"] == "processing"
    assert gap_patch.status_code == 200
    assert gap_patch.json()["data"]["status"] == "reviewing"

    with psycopg.connect(database_url, row_factory=dict_row) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT h.id, h.status, h.risk_level, sp.code AS scenario_pack_code
                FROM zycs_human_handoffs h
                JOIN zycs_conversations c ON c.id = h.conversation_id
                JOIN zycs_scenario_packs sp ON sp.id = c.scenario_pack_id
                WHERE h.id = %s
                """,
                (handoff["handoff_id"],),
            )
            handoff_row = cursor.fetchone()
            cursor.execute(
                """
                SELECT g.id, g.status, g.resolution_note, g.suggested_tags, sp.code AS scenario_pack_code
                FROM zycs_knowledge_gaps g
                JOIN zycs_conversations c ON c.id = g.conversation_id
                JOIN zycs_scenario_packs sp ON sp.id = c.scenario_pack_id
                WHERE g.id = %s
                """,
                (gap["gap_id"],),
            )
            gap_row = cursor.fetchone()

    assert handoff_row is not None
    assert handoff_row["status"] == "processing"
    assert handoff_row["risk_level"] == "high"
    assert handoff_row["scenario_pack_code"] == "product_business"
    assert gap_row is not None
    assert gap_row["status"] == "reviewing"
    assert gap_row["resolution_note"] == "PG 模式等待知识运营确认"
    assert "待确认" in gap_row["suggested_tags"]
    assert gap_row["scenario_pack_code"] == "product_business"


@pytest.mark.skipif(
    importlib.util.find_spec("psycopg") is None,
    reason="psycopg is not installed",
)
def test_postgres_console_store_persists_notifications(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database_url = os.getenv("ZYCS_TEST_DATABASE_URL")
    if not database_url:
        pytest.skip("ZYCS_TEST_DATABASE_URL is not set")

    import psycopg
    from psycopg.rows import dict_row

    monkeypatch.setenv("ZYCS_CONVERSATION_STORE", "postgres")
    monkeypatch.setenv("ZYCS_DATABASE_URL", database_url)
    monkeypatch.delenv("ZYCS_FEISHU_NOTIFY_MODE", raising=False)
    monkeypatch.delenv("ZYCS_FEISHU_WEBHOOK_URL", raising=False)
    monkeypatch.delenv("ZYCS_FEISHU_WEBHOOK_SECRET", raising=False)

    client = TestClient(create_app())
    create_response = client.post(
        "/api/v1/notifications/mock",
        headers={"X-Console-Role": "admin"},
        json={
            "event_type": "handoff",
            "related_id": "handoff_pg_notification",
            "target_type": "feishu",
        },
    )
    assert create_response.status_code == 200
    notification = create_response.json()["data"]

    list_response = client.get(
        "/api/v1/notifications/mock",
        params={"event_type": "handoff", "send_status": "mocked"},
    )
    assert list_response.status_code == 200
    assert notification["notification_id"] in {
        item["notification_id"] for item in list_response.json()["data"]
    }

    with psycopg.connect(database_url, row_factory=dict_row) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, event_type, related_id, target_type, send_status, is_mock, payload
                FROM zycs_notifications
                WHERE id = %s
                """,
                (notification["notification_id"],),
            )
            row = cursor.fetchone()

    assert row is not None
    assert row["event_type"] == "handoff"
    assert row["related_id"] == "handoff_pg_notification"
    assert row["target_type"] == "feishu"
    assert row["send_status"] == "mocked"
    assert row["is_mock"] is True
    assert row["payload"]["notify_mode"] == "mock"


def _create_conversation(client: TestClient) -> str:
    response = client.post(
        "/api/v1/conversations",
        json={"channel": "h5", "scenario_pack_code": "product_business"},
    )
    assert response.status_code == 200
    return str(response.json()["data"]["conversation_id"])
