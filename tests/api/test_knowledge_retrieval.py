from fastapi.testclient import TestClient

from app.main import create_app


client = TestClient(create_app())


def _create_knowledge_item(status: str, title: str, content: str, source_ref: str) -> str:
    response = client.post(
        "/api/v1/knowledge-items",
        headers={"X-Console-Role": "admin"},
        json={
            "scenario_pack_code": "product_business",
            "title": title,
            "content": content,
            "source_ref": source_ref,
            "status": status,
        },
    )
    assert response.status_code == 200
    return str(response.json()["data"]["item_id"])


def _send_message(content: str) -> dict:
    conversation_id = client.post(
        "/api/v1/conversations",
        json={"channel": "h5", "scenario_pack_code": "product_business"},
    ).json()["data"]["conversation_id"]
    response = client.post(
        f"/api/v1/conversations/{conversation_id}/messages",
        json={"content": content},
    )
    return dict(response.json()["data"])


def test_active_knowledge_item_is_retrieved() -> None:
    # TC-054：active 知识被检索命中
    _create_knowledge_item(
        status="active",
        title="激光功率规格",
        content="Mock：激光功率规格说明（active 知识 Demo）。",
        source_ref="SRC-ACTIVE-RETRIEVAL",
    )
    data = _send_message("激光功率规格是什么？")

    assert data["answer_type"] == "knowledge"
    assert data["source_ref"] == "SRC-ACTIVE-RETRIEVAL"


def test_draft_knowledge_item_not_retrieved() -> None:
    # TC-054：draft 知识不参与检索
    _create_knowledge_item(
        status="draft",
        title="量子灯带规格",
        content="Mock：量子灯带规格（draft 不应命中）。",
        source_ref="SRC-DRAFT-NO",
    )
    data = _send_message("量子灯带规格是什么？")

    assert data["source_ref"] != "SRC-DRAFT-NO"


def test_no_active_knowledge_seed_still_matches() -> None:
    # 无新增 active 时，seed 知识仍正常命中（行为不变）
    data = _send_message("灯带有什么规格？")

    assert data["answer_type"] == "knowledge"
    assert data["source_ref"] == "SRC-SP-PRODUCT-001"
