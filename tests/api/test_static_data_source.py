import importlib.util
import os

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.services.scenario_pack_service import load_scenario_packs


@pytest.fixture(autouse=True)
def clear_scenario_pack_cache() -> None:
    load_scenario_packs.cache_clear()
    yield
    load_scenario_packs.cache_clear()


def test_default_static_data_source_uses_json(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ZYCS_STATIC_DATA_SOURCE", raising=False)
    monkeypatch.delenv("ZYCS_DATABASE_URL", raising=False)

    client = TestClient(create_app())
    response = client.get("/api/v1/scenario-packs")

    assert response.status_code == 200
    codes = {item["code"] for item in response.json()["data"]}
    assert codes == {"product_business", "project_business"}


def test_postgres_static_data_source_without_url_falls_back_to_json(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ZYCS_STATIC_DATA_SOURCE", "postgres")
    monkeypatch.delenv("ZYCS_DATABASE_URL", raising=False)

    client = TestClient(create_app())
    response = client.post(
        "/api/v1/conversations",
        json={"channel": "h5", "scenario_pack_code": "product_business"},
    )
    conversation_id = response.json()["data"]["conversation_id"]

    message_response = client.post(
        f"/api/v1/conversations/{conversation_id}/messages",
        json={"content": "灯带有什么规格？"},
    )

    assert message_response.status_code == 200
    assert message_response.json()["data"]["answer_type"] == "knowledge"


@pytest.mark.skipif(
    importlib.util.find_spec("psycopg") is None,
    reason="psycopg is not installed",
)
def test_postgres_static_data_source_reads_seed_data(monkeypatch: pytest.MonkeyPatch) -> None:
    database_url = os.getenv("ZYCS_TEST_DATABASE_URL")
    if not database_url:
        pytest.skip("ZYCS_TEST_DATABASE_URL is not set")

    monkeypatch.setenv("ZYCS_STATIC_DATA_SOURCE", "postgres")
    monkeypatch.setenv("ZYCS_DATABASE_URL", database_url)

    client = TestClient(create_app())

    packs_response = client.get("/api/v1/scenario-packs")
    assert packs_response.status_code == 200
    assert {item["code"] for item in packs_response.json()["data"]} == {
        "product_business",
        "project_business",
    }

    mock_response = client.get("/api/v1/mock-business/order/HC-ORDER-001")
    assert mock_response.status_code == 200
    assert mock_response.json()["data"]["scenario_pack_code"] == "product_business"

    create_response = client.post(
        "/api/v1/conversations",
        json={"channel": "h5", "scenario_pack_code": "product_business"},
    )
    conversation_id = create_response.json()["data"]["conversation_id"]
    message_response = client.post(
        f"/api/v1/conversations/{conversation_id}/messages",
        json={"content": "灯带有什么规格？"},
    )
    assert message_response.status_code == 200
    assert message_response.json()["data"]["answer_type"] == "knowledge"
