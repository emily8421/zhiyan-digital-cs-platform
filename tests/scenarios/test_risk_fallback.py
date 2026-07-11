from fastapi.testclient import TestClient

from app.main import create_app


client = TestClient(create_app())


def _create_conversation(scenario_pack_code: str = "product_business") -> str:
    response = client.post(
        "/api/v1/conversations",
        json={"channel": "h5", "scenario_pack_code": scenario_pack_code},
    )
    assert response.status_code == 200
    return response.json()["data"]["conversation_id"]


def test_high_risk_question_creates_handoff_without_commitment() -> None:
    conversation_id = _create_conversation()

    response = client.post(
        f"/api/v1/conversations/{conversation_id}/messages",
        json={"content": "如果客户投诉并要求赔偿，你们能保证赔多少钱？"},
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["answer_type"] == "handoff"
    assert data["source_ref"] == "rule:high_risk_handoff"
    assert "不会给出承诺性答复" in data["answer"]
    assert data["handoff"]["handoff_id"].startswith("handoff_")
    assert data["handoff"]["status"] == "open"
    assert data["knowledge_gap"] is None


def test_unknown_question_creates_knowledge_gap() -> None:
    conversation_id = _create_conversation("project_business")

    response = client.post(
        f"/api/v1/conversations/{conversation_id}/messages",
        json={"content": "请说明火星基地联调验收流程"},
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["answer_type"] == "gap"
    assert data["source_ref"] == "policy:knowledge_gap"
    assert "没有可追溯依据" in data["answer"]
    assert data["handoff"] is None
    assert data["knowledge_gap"]["gap_id"].startswith("gap_")
    assert data["knowledge_gap"]["status"] == "new"


def test_missing_mock_record_does_not_fabricate_progress() -> None:
    conversation_id = _create_conversation()

    response = client.post(
        f"/api/v1/conversations/{conversation_id}/messages",
        json={"content": "帮我查一下 HC-ORDER-999 的生产进度"},
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["answer_type"] == "gap"
    assert data["source_ref"] == "mock_business:HC-ORDER-999:missing"
    assert "避免编造进度" in data["answer"]


def test_known_mock_record_returns_traceable_mock_answer() -> None:
    conversation_id = _create_conversation()

    response = client.post(
        f"/api/v1/conversations/{conversation_id}/messages",
        json={"content": "我想查一下 HC-ORDER-001 的生产进度"},
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["answer_type"] == "mock_business"
    assert data["source_ref"] == "demo_erp:order:HC-ORDER-001"
    assert "Mock 进度" in data["answer"]
    assert data["handoff"] is None
    assert data["knowledge_gap"] is None
