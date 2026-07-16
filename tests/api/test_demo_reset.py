"""task-011c / API-015 场景包 Demo Sandbox 重置测试（TC-068）。

TC-068：在一个场景包产生会话 / 缺口 / 转人工 / 通知 / 摘要后执行 Demo reset，
当前场景包恢复初始演示态，其他场景包和真实数据配置不受影响。
"""

from fastapi.testclient import TestClient

from app.main import create_app
from app.services.console_service import (
    create_handoff_record,
    create_knowledge_gap_record,
    create_knowledge_item,
    create_mock_notification,
    list_handoffs,
    list_knowledge_gaps,
    list_knowledge_items,
    list_notifications,
)
from app.services.conversation_service import create_demo_conversation, list_demo_conversations

client = TestClient(create_app())

PRODUCT = "product_business"
PROJECT = "project_business"
UNKNOWN_PACK = "no_such_scenario_pack"


def _seed_product_runtime() -> dict[str, str]:
    """注入 product_business 运行时数据，返回创建的关键 ID。"""
    conversation = create_demo_conversation("h5", PRODUCT, "runtime_customer")
    handoff = create_handoff_record(
        conversation_id=conversation.conversation_id,
        scenario_pack_code=PRODUCT,
        reason="运行时转人工样例",
        summary="runtime handoff",
        risk_level="medium",
    )
    create_knowledge_gap_record(
        conversation_id=conversation.conversation_id,
        scenario_pack_code=PRODUCT,
        question="运行时缺口样例？",
        tags=["运行时"],
    )
    item = create_knowledge_item(
        scenario_pack_code=PRODUCT,
        title="运行时知识候选",
        content="runtime item",
        source_ref="runtime:test",
        tags=["运行时"],
        status="draft",
    )
    notification = create_mock_notification("handoff", handoff.handoff_id, "feishu")
    return {
        "conversation_id": conversation.conversation_id,
        "handoff_id": handoff.handoff_id,
        "item_id": item.item_id,
        "notification_id": notification.notification_id,
    }


def test_demo_reset_requires_confirm():
    response = client.post(
        f"/api/v1/scenario-packs/{PRODUCT}/demo-reset",
        headers={"X-Console-Role": "admin"},
        json={"runtime_scope": "current_scenario_pack", "confirm": False},
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_demo_reset_rejects_unsupported_scope():
    response = client.post(
        f"/api/v1/scenario-packs/{PRODUCT}/demo-reset",
        headers={"X-Console-Role": "admin"},
        json={"runtime_scope": "global", "confirm": True},
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_demo_reset_requires_admin_role():
    response = client.post(
        f"/api/v1/scenario-packs/{PRODUCT}/demo-reset",
        headers={"X-Console-Role": "viewer"},
        json={"runtime_scope": "current_scenario_pack", "confirm": True},
    )
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "FORBIDDEN_CONSOLE_WRITE"


def test_demo_reset_unknown_pack_returns_404():
    response = client.post(
        f"/api/v1/scenario-packs/{UNKNOWN_PACK}/demo-reset",
        headers={"X-Console-Role": "admin"},
        json={"runtime_scope": "current_scenario_pack", "confirm": True},
    )
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "SCENARIO_PACK_NOT_FOUND"


def test_demo_reset_clears_runtime_keeps_seed_and_other_pack():
    # TC-068：当前场景包恢复初始演示态，其他场景包与真实配置不受影响
    ids = _seed_product_runtime()

    response = client.post(
        f"/api/v1/scenario-packs/{PRODUCT}/demo-reset",
        headers={"X-Console-Role": "admin"},
        json={"runtime_scope": "current_scenario_pack", "confirm": True},
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["scenario_pack_id"] == PRODUCT
    assert data["reset_scope"] == "current_scenario_pack"
    assert data["source_mode"] == "demo_sandbox"
    assert data["mock"] is True
    assert data["reset_id"].startswith("demo_reset_")
    assert data["reset_at"]
    affected = data["affected_counts"]
    assert affected["conversations"] >= 1
    assert affected["handoffs"] >= 1
    assert affected["knowledge_gaps"] >= 1
    assert affected["knowledge_items"] >= 1

    # reset 后：product 运行时记录已清除
    product_conversations = list_demo_conversations(scenario_pack_code=PRODUCT)
    assert all(c.conversation_id != ids["conversation_id"] for c in product_conversations)
    product_handoffs = [h for h in list_handoffs() if h.scenario_pack_code == PRODUCT]
    assert all(h.handoff_id != ids["handoff_id"] for h in product_handoffs)
    product_gaps = list_knowledge_gaps(scenario_pack_code=PRODUCT)
    assert all(g.question != "运行时缺口样例？" for g in product_gaps)
    product_items = list_knowledge_items(scenario_pack_code=PRODUCT)
    assert all(i.item_id != ids["item_id"] for i in product_items)
    assert all(n.notification_id != ids["notification_id"] for n in list_notifications())

    # seed 初始演示态保留：product seed（handoff_002 / gap_001 / 会话 seed）仍在
    assert any(h.handoff_id == "handoff_002" for h in product_handoffs)
    assert any(g.gap_id == "gap_001" for g in product_gaps)
    assert any(c.conversation_id == "conv_demo_product_001" for c in product_conversations)
    # 知识条目无 seed，reset 后为空
    assert product_items == []

    # 其他场景包不受影响：project seed（handoff_001 / gap_002）仍在
    project_handoffs = [h for h in list_handoffs() if h.scenario_pack_code == PROJECT]
    assert any(h.handoff_id == "handoff_001" for h in project_handoffs)
    project_gaps = list_knowledge_gaps(scenario_pack_code=PROJECT)
    assert any(g.gap_id == "gap_002" for g in project_gaps)
