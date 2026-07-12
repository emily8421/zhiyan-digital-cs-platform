import pytest
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
    assert body["data"]["source_ref"] == "demo_erp:order:HC-ORDER-001"
    assert body["data"]["handoff"] is None
    assert body["data"]["knowledge_gap"] is None


def test_send_message_returns_standard_demo_sandbox_answer() -> None:
    create_response = client.post(
        "/api/v1/conversations",
        json={"channel": "h5", "scenario_pack_code": "product_business"},
    )
    conversation_id = create_response.json()["data"]["conversation_id"]

    response = client.post(
        f"/api/v1/conversations/{conversation_id}/messages",
        json={"content": "我想查一下 DEMO-ORDER-202607-001 的生产进度"},
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["intent"] == "order_progress"
    assert data["answer_type"] == "mock_business"
    assert data["source_ref"] == "demo_erp:order:DEMO-ORDER-202607-001"
    assert "Demo 订单" in data["answer"]
    assert data["handoff"] is None
    assert data["knowledge_gap"] is None


def test_send_message_with_demo_question_matches_knowledge() -> None:
    cases = [
        ("product_business", "灯带有什么规格？", "SRC-SP-PRODUCT-001"),
        ("project_business", "项目开发有哪些阶段？", "SRC-SP-PROJECT-001"),
    ]

    for scenario_pack_code, content, source_ref in cases:
        create_response = client.post(
            "/api/v1/conversations",
            json={"channel": "h5", "scenario_pack_code": scenario_pack_code},
        )
        conversation_id = create_response.json()["data"]["conversation_id"]

        response = client.post(
            f"/api/v1/conversations/{conversation_id}/messages",
            json={"content": content},
        )

        assert response.status_code == 200
        body = response.json()
        assert body["data"]["answer_type"] == "knowledge"
        assert body["data"]["source_ref"] == source_ref
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


def test_send_message_returns_llm_sandbox_answer_in_mock_mode(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ZYCS_LLM_MODE", "mock")
    create_response = client.post(
        "/api/v1/conversations",
        json={"channel": "h5", "scenario_pack_code": "product_business"},
    )
    conversation_id = create_response.json()["data"]["conversation_id"]

    response = client.post(
        f"/api/v1/conversations/{conversation_id}/messages",
        json={"content": "我想查一下 DEMO-ORDER-202607-001 的生产进度"},
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["answer_type"] == "llm_sandbox"
    assert data["source_ref"] == "demo_erp:order:DEMO-ORDER-202607-001"
    assert "LLM Sandbox 改写" in data["answer"]
    assert data["llm"]["mode"] == "mock"
    assert data["llm"]["base_answer_type"] == "mock_business"
    assert "demo_erp:order:DEMO-ORDER-202607-001" in data["llm"]["evidence"]
    assert data["handoff"] is None
    assert data["knowledge_gap"] is None
