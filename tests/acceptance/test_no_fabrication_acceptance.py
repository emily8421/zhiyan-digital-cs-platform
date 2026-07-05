from fastapi.testclient import TestClient

from app.main import create_app


client = TestClient(create_app())


def test_sensitive_input_is_redacted_in_audit_logs() -> None:
    create_response = client.post(
        "/api/v1/conversations",
        json={"channel": "h5", "scenario_pack_code": "product_business"},
    )
    conversation_id = create_response.json()["data"]["conversation_id"]

    response = client.post(
        f"/api/v1/conversations/{conversation_id}/messages",
        json={"content": "我的手机号是 13812345678，token=abc123，请处理赔偿"},
    )

    assert response.status_code == 200
    assert response.json()["data"]["answer_type"] == "handoff"

    audit_response = client.get("/api/v1/audit-logs")

    assert audit_response.status_code == 200
    logs = audit_response.json()["data"]
    assert logs
    latest = logs[-1]
    assert latest["mock"] is True
    assert latest["outcome"] == "handoff"
    assert "13812345678" not in latest["input_summary"]
    assert "abc123" not in latest["input_summary"]
    assert "[已脱敏]" in latest["input_summary"]


def test_handoff_and_gap_created_by_message_are_visible_in_console_lists() -> None:
    create_response = client.post(
        "/api/v1/conversations",
        json={"channel": "h5", "scenario_pack_code": "project_business"},
    )
    conversation_id = create_response.json()["data"]["conversation_id"]

    handoff_response = client.post(
        f"/api/v1/conversations/{conversation_id}/messages",
        json={"content": "这个合同违约责任你们能保证承担吗？"},
    )
    gap_response = client.post(
        f"/api/v1/conversations/{conversation_id}/messages",
        json={"content": "请说明月球项目售后流程"},
    )

    handoff_id = handoff_response.json()["data"]["handoff"]["handoff_id"]
    gap_id = gap_response.json()["data"]["knowledge_gap"]["gap_id"]

    handoff_list = client.get("/api/v1/handoffs").json()["data"]
    gap_list = client.get("/api/v1/knowledge-gaps").json()["data"]

    assert handoff_id in {item["handoff_id"] for item in handoff_list}
    assert gap_id in {item["gap_id"] for item in gap_list}
