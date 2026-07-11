from fastapi.testclient import TestClient

from app.main import create_app


client = TestClient(create_app())


def test_list_scenario_packs_returns_product_and_project() -> None:
    response = client.get("/api/v1/scenario-packs")

    assert response.status_code == 200
    body = response.json()
    assert body["meta"]["mock"] is True
    codes = {item["code"] for item in body["data"]}
    assert codes == {"product_business", "project_business"}
    assert all(item["knowledge_count"] > 0 for item in body["data"])
    assert all(item["mock_business_count"] > 0 for item in body["data"])


def test_get_scenario_pack_detail_returns_traceable_seed_data() -> None:
    response = client.get("/api/v1/scenario-packs/product_business")

    assert response.status_code == 200
    body = response.json()
    data = body["data"]
    assert data["code"] == "product_business"
    assert "SRC-SP-PRODUCT-001" in data["source_refs"]
    assert data["knowledge_items"]
    assert all(item["source_ref"] for item in data["knowledge_items"])
    assert data["mock_business_records"]
    assert all(record["is_mock"] is True for record in data["mock_business_records"])
    assert all(record["source_ref"] for record in data["mock_business_records"])
    assert all(record["environment"] == "demo_sandbox" for record in data["mock_business_records"])
    assert all(record["payload"]["schema_version"] == "demo_sandbox.v1" for record in data["mock_business_records"])


def test_get_missing_scenario_pack_returns_error_contract() -> None:
    response = client.get("/api/v1/scenario-packs/missing_pack")

    assert response.status_code == 404
    body = response.json()
    assert body["request_id"]
    assert body["error"]["code"] == "SCENARIO_PACK_NOT_FOUND"
    assert body["error"]["details"] == {"scenario_pack_id": "missing_pack"}
