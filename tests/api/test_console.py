from fastapi.testclient import TestClient

from app.main import create_app


client = TestClient(create_app())


def test_list_conversations_returns_console_fields() -> None:
    response = client.get("/api/v1/conversations")

    assert response.status_code == 200
    body = response.json()
    assert body["meta"]["mock"] is True
    assert body["data"]
    assert body["data"][0]["conversation_id"].startswith("conv_")
    assert "last_message" in body["data"][0]
    assert body["data"][0]["mock"] is True


def test_update_handoff_status() -> None:
    response = client.patch(
        "/api/v1/handoffs/handoff_001",
        json={"status": "processing", "resolution_note": "已分配给售前方案负责人"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["meta"]["mock"] is True
    assert body["data"]["handoff_id"] == "handoff_001"
    assert body["data"]["status"] == "processing"
    assert body["data"]["resolution_note"] == "已分配给售前方案负责人"


def test_update_handoff_with_invalid_status_returns_error() -> None:
    response = client.patch(
        "/api/v1/handoffs/handoff_001",
        json={"status": "done", "resolution_note": "invalid"},
    )

    assert response.status_code == 400
    body = response.json()
    assert body["error"]["code"] == "INVALID_CONSOLE_STATUS"


def test_update_knowledge_gap_status() -> None:
    response = client.patch(
        "/api/v1/knowledge-gaps/gap_001",
        json={"status": "reviewing", "resolution_note": "等待业务确认答案"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["meta"]["mock"] is True
    assert body["data"]["gap_id"] == "gap_001"
    assert body["data"]["status"] == "reviewing"


def test_create_and_list_mock_notification() -> None:
    create_response = client.post(
        "/api/v1/notifications/mock",
        json={"event_type": "handoff", "related_id": "handoff_001", "target_type": "feishu"},
    )

    assert create_response.status_code == 200
    created = create_response.json()["data"]
    assert created["notification_id"].startswith("notif_")
    assert created["send_status"] == "mocked"
    assert created["mock"] is True
    assert created["payload"]["mock"] is True

    list_response = client.get("/api/v1/notifications/mock")

    assert list_response.status_code == 200
    notification_ids = {item["notification_id"] for item in list_response.json()["data"]}
    assert created["notification_id"] in notification_ids


def test_daily_summary_returns_counts() -> None:
    response = client.get("/api/v1/summaries/daily?date=2026-07-05")

    assert response.status_code == 200
    body = response.json()
    assert body["meta"]["mock"] is True
    assert body["data"]["summary_date"] == "2026-07-05"
    assert body["data"]["conversation_count"] >= 2
    assert body["data"]["handoff_count"] >= 2
    assert body["data"]["gap_count"] >= 2
    assert body["data"]["mock"] is True
