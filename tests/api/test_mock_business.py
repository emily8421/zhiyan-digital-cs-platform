from fastapi.testclient import TestClient

from app.main import create_app


client = TestClient(create_app())


def test_get_mock_order_record() -> None:
    response = client.get("/api/v1/mock-business/order/HC-ORDER-001")

    assert response.status_code == 200
    body = response.json()
    assert body["meta"]["mock"] is True
    data = body["data"]
    assert data["record_type"] == "order"
    assert data["external_ref"] == "HC-ORDER-001"
    assert data["scenario_pack_code"] == "product_business"
    assert data["source_ref"] == "demo_erp:order:HC-ORDER-001"
    assert data["environment"] == "demo_sandbox"
    assert data["payload"]["schema_version"] == "demo_sandbox.v1"
    assert data["mock"] is True


def test_get_standard_demo_order_record() -> None:
    response = client.get("/api/v1/mock-business/order/DEMO-ORDER-202607-001")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["record_type"] == "order"
    assert data["external_ref"] == "DEMO-ORDER-202607-001"
    assert data["source_system"] == "demo_erp"
    assert data["environment"] == "demo_sandbox"
    assert data["stage"] == "in_production"
    assert data["source_ref"] == "demo_erp:order:DEMO-ORDER-202607-001"
    assert data["payload"]["customer"]["customer_id"] == "DEMO-CUST-GUJING-001"
    assert data["payload"]["business_object"]["order_id"] == "DEMO-ORDER-202607-001"
    assert data["payload"]["progress_nodes"]
    assert data["payload"]["redaction_applied"] is True
    assert data["mock"] is True


def test_get_mock_project_record() -> None:
    response = client.get("/api/v1/mock-business/project/XS-PROJ-001")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["record_type"] == "project"
    assert data["scenario_pack_code"] == "project_business"
    assert data["status"] == "方案开发阶段"


def test_get_mock_ticket_record() -> None:
    response = client.get("/api/v1/mock-business/ticket/XS-TICKET-001")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["record_type"] == "ticket"
    assert data["scenario_pack_code"] == "project_business"
    assert data["source_system"] == "demo_ticket"
    assert data["mock"] is True


def test_get_missing_mock_record_returns_error_contract() -> None:
    response = client.get("/api/v1/mock-business/order/UNKNOWN-001")

    assert response.status_code == 404
    body = response.json()
    assert body["request_id"]
    assert body["error"]["code"] == "MOCK_RECORD_NOT_FOUND"
    assert body["error"]["details"] == {
        "record_type": "order",
        "external_ref": "UNKNOWN-001",
    }


def test_list_mock_business_records() -> None:
    response = client.get("/api/v1/mock-business?scenario_pack_code=project_business")

    assert response.status_code == 200
    body = response.json()
    assert body["meta"]["mock"] is True
    assert body["data"]
    assert {record["scenario_pack_code"] for record in body["data"]} == {"project_business"}
    assert all(record["mock"] is True for record in body["data"])
