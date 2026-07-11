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
        headers={"X-Console-Role": "admin"},
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
        headers={"X-Console-Role": "admin"},
        json={"status": "done", "resolution_note": "invalid"},
    )

    assert response.status_code == 400
    body = response.json()
    assert body["error"]["code"] == "INVALID_CONSOLE_STATUS"


def test_update_knowledge_gap_status() -> None:
    response = client.patch(
        "/api/v1/knowledge-gaps/gap_001",
        headers={"X-Console-Role": "admin"},
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
        headers={"X-Console-Role": "admin"},
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


def test_create_mock_notification_sandbox_without_secret_falls_back_to_mock(
    monkeypatch,
) -> None:
    monkeypatch.setenv("ZYCS_FEISHU_NOTIFY_MODE", "sandbox")
    monkeypatch.setenv("ZYCS_FEISHU_WEBHOOK_URL", "https://example.invalid/hook")
    monkeypatch.delenv("ZYCS_FEISHU_WEBHOOK_SECRET", raising=False)

    response = client.post(
        "/api/v1/notifications/mock",
        headers={"X-Console-Role": "admin"},
        json={"event_type": "handoff", "related_id": "handoff_001", "target_type": "feishu"},
    )

    assert response.status_code == 200
    created = response.json()["data"]
    assert created["send_status"] == "mocked"
    assert created["mock"] is True
    assert created["payload"]["notify_mode"] == "mock"
    assert "fallback_reason" in created["payload"]
    assert "https://example.invalid/hook" not in str(created["payload"])


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


# --- Sprint-7 控制台角色权限（WC-C-001，TC-018） ---


def test_update_handoff_requires_admin_role() -> None:
    # 未声明角色 = viewer（只读），写操作被后端拒绝
    response = client.patch(
        "/api/v1/handoffs/handoff_001",
        json={"status": "processing", "resolution_note": "尝试越权更新"},
    )

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "FORBIDDEN_CONSOLE_WRITE"


def test_update_handoff_viewer_role_forbidden() -> None:
    response = client.patch(
        "/api/v1/handoffs/handoff_001",
        headers={"X-Console-Role": "viewer"},
        json={"status": "processing", "resolution_note": "viewer 尝试写"},
    )

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "FORBIDDEN_CONSOLE_WRITE"


def test_update_knowledge_gap_requires_admin_role() -> None:
    response = client.patch(
        "/api/v1/knowledge-gaps/gap_001",
        json={"status": "reviewing", "resolution_note": "尝试越权更新"},
    )

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "FORBIDDEN_CONSOLE_WRITE"


def test_create_mock_notification_requires_admin_role() -> None:
    response = client.post(
        "/api/v1/notifications/mock",
        json={"event_type": "handoff", "related_id": "handoff_001", "target_type": "feishu"},
    )

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "FORBIDDEN_CONSOLE_WRITE"


def test_read_endpoints_open_without_admin_role() -> None:
    # 只读接口对 viewer / 未声明角色开放
    for path in (
        "/api/v1/handoffs",
        "/api/v1/knowledge-gaps",
        "/api/v1/knowledge-items",
        "/api/v1/notifications/mock",
        "/api/v1/summaries/daily",
    ):
        response = client.get(path, headers={"X-Console-Role": "viewer"})
        assert response.status_code == 200, path


# --- Sprint-9 知识运营强化（缺口 accepted 入库 + API-006，TC-050~052） ---


def test_create_and_list_knowledge_items() -> None:
    # TC-050：POST 新增知识候选，GET 可查回
    create_response = client.post(
        "/api/v1/knowledge-items",
        headers={"X-Console-Role": "admin"},
        json={
            "scenario_pack_code": "project_business",
            "title": "项目验收资料清单",
            "content": "Mock 知识：项目验收需提供资料清单（Demo 样例）。",
            "source_ref": "SRC-SP-PROJECT-DEMO",
            "tags": ["项目交付"],
            "status": "draft",
        },
    )

    assert create_response.status_code == 200
    created = create_response.json()["data"]
    assert created["item_id"].startswith("ki_")
    assert created["status"] == "draft"
    assert created["source_ref"] == "SRC-SP-PROJECT-DEMO"
    assert created["mock"] is True

    list_response = client.get("/api/v1/knowledge-items?scenario_pack_code=project_business")

    assert list_response.status_code == 200
    item_ids = {item["item_id"] for item in list_response.json()["data"]}
    assert created["item_id"] in item_ids


def test_accept_knowledge_gap_creates_draft_item() -> None:
    # TC-051：缺口 accepted 自动入库为 draft 知识条目
    response = client.patch(
        "/api/v1/knowledge-gaps/gap_002",
        headers={"X-Console-Role": "admin"},
        json={"status": "accepted", "resolution_note": "已补充标准模板，入库为知识候选"},
    )

    assert response.status_code == 200
    gap = response.json()["data"]
    assert gap["gap_id"] == "gap_002"
    assert gap["status"] == "accepted"

    list_response = client.get("/api/v1/knowledge-items?status=draft")

    assert list_response.status_code == 200
    items = list_response.json()["data"]
    matching = [item for item in items if item["source_ref"] == "knowledge_gap:gap_002"]
    assert matching, "accepted 缺口应自动生成 draft 知识条目"
    assert matching[0]["status"] == "draft"
    assert matching[0]["origin_gap_id"] == "gap_002"


def test_reject_knowledge_gap_does_not_create_item() -> None:
    # TC-052：缺口 rejected 不生成知识条目
    before = client.get("/api/v1/knowledge-items?status=draft").json()["data"]
    before_count = sum(1 for item in before if item["source_ref"] == "knowledge_gap:gap_001")

    response = client.patch(
        "/api/v1/knowledge-gaps/gap_001",
        headers={"X-Console-Role": "admin"},
        json={"status": "rejected", "resolution_note": "不属于知识范围，拒绝"},
    )

    assert response.status_code == 200
    assert response.json()["data"]["status"] == "rejected"

    after = client.get("/api/v1/knowledge-items?status=draft").json()["data"]
    after_count = sum(1 for item in after if item["source_ref"] == "knowledge_gap:gap_001")
    assert after_count == before_count, "rejected 缺口不应生成知识条目"


def test_create_knowledge_item_requires_admin_role() -> None:
    response = client.post(
        "/api/v1/knowledge-items",
        json={
            "scenario_pack_code": "product_business",
            "title": "尝试越权新增",
            "content": "x",
            "source_ref": "SRC-X",
        },
    )

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "FORBIDDEN_CONSOLE_WRITE"


def test_create_knowledge_item_invalid_status_returns_error() -> None:
    response = client.post(
        "/api/v1/knowledge-items",
        headers={"X-Console-Role": "admin"},
        json={
            "scenario_pack_code": "product_business",
            "title": "非法状态",
            "content": "x",
            "source_ref": "SRC-X",
            "status": "published",
        },
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "INVALID_CONSOLE_STATUS"
