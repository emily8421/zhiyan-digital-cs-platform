from fastapi.testclient import TestClient

from app.main import create_app


client = TestClient(create_app())


def test_health_check_returns_mock_response() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["data"] == {"status": "ok"}
    assert body["meta"]["mock"] is True
    assert body["request_id"]


def test_create_conversation_returns_minimum_contract() -> None:
    response = client.post(
        "/api/v1/conversations",
        json={
            "channel": "h5",
            "scenario_pack_code": "product_business",
            "customer_alias": "demo_customer",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["meta"]["mock"] is True
    assert body["data"]["conversation_id"].startswith("conv_")
    assert body["data"]["status"] == "open"
    assert body["data"]["scenario_pack_code"] == "product_business"


def test_send_message_returns_mock_answer() -> None:
    create_response = client.post(
        "/api/v1/conversations",
        json={"channel": "h5", "scenario_pack_code": "product_business"},
    )
    conversation_id = create_response.json()["data"]["conversation_id"]

    response = client.post(
        f"/api/v1/conversations/{conversation_id}/messages",
        json={"content": "我想查一下 HC-ORDER-001 的生产进度"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["meta"]["mock"] is True
    assert body["data"]["message_id"].startswith("msg_")
    assert body["data"]["intent"] == "order_progress"
    assert body["data"]["answer_type"] == "mock_business"
    assert body["data"]["source_ref"] == "mock_business:HC-ORDER-001"
    assert body["data"]["handoff"] is None
    assert body["data"]["knowledge_gap"] is None


def test_send_message_for_missing_conversation_returns_error_contract() -> None:
    response = client.post(
        "/api/v1/conversations/conv_missing/messages",
        json={"content": "hello"},
    )

    assert response.status_code == 404
    body = response.json()
    assert body["request_id"]
    assert body["error"]["code"] == "CONVERSATION_NOT_FOUND"
    assert body["error"]["details"] == {"conversation_id": "conv_missing"}


def test_send_message_with_invalid_payload_returns_validation_error() -> None:
    create_response = client.post(
        "/api/v1/conversations",
        json={"channel": "h5", "scenario_pack_code": "product_business"},
    )
    conversation_id = create_response.json()["data"]["conversation_id"]

    response = client.post(
        f"/api/v1/conversations/{conversation_id}/messages",
        json={"content": ""},
    )

    assert response.status_code == 422
    body = response.json()
    assert body["request_id"]
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert "errors" in body["error"]["details"]
