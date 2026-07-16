"""task-011b / API-014 场景包 Demo Dataset 测试（TC-067 / TC-069 / TC-071）。

- TC-067（REQ-018）：切换场景包读取各自独立 Demo Dataset，不串用。
- TC-069（REQ-020）：虚拟客户资料摘要可展示，并标识为模拟数据。
- TC-071（REQ-022）：响应带 source_mode / source_ref / mock 来源标识。
"""

from fastapi.testclient import TestClient

from app.main import create_app

client = TestClient(create_app())

# 动态取真实场景包，避免硬编码导致用例脆弱。
_AVAILABLE_PACKS = client.get("/api/v1/scenario-packs").json()["data"]
PACK_CODES = [pack["code"] for pack in _AVAILABLE_PACKS]
UNKNOWN_PACK = "no_such_scenario_pack"


def test_get_demo_dataset_returns_summary_with_source_markers():
    # TC-069 / TC-071：摘要字段齐全 + 来源标识
    pack = PACK_CODES[0] if PACK_CODES else "product_business"
    response = client.get(f"/api/v1/scenario-packs/{pack}/demo-dataset")
    assert response.status_code == 200
    body = response.json()
    data = body["data"]
    assert data["scenario_pack_id"] == pack
    assert data["source_mode"] == "demo_sandbox"
    assert data["source_ref"] == f"demo_dataset:{pack}:v1"
    assert data["dataset_code"] == f"{pack}_demo_v1"
    assert data["mock"] is True
    assert body["meta"]["mock"] is True

    profile = data["virtual_customer_profile"]
    assert profile["business_type"] == pack
    assert profile["company_name"]
    assert profile["summary"]

    stats = data["stats"]
    for key in (
        "knowledge_items",
        "business_records",
        "historical_conversations",
        "knowledge_gaps",
        "summaries",
    ):
        assert isinstance(stats[key], int)


def test_demo_datasets_isolated_between_scenario_packs():
    # TC-067：不同场景包的 Demo Dataset 与虚拟客户不串用
    if len(PACK_CODES) < 2:
        return  # 仅一个场景包时无法验证隔离
    first = client.get(f"/api/v1/scenario-packs/{PACK_CODES[0]}/demo-dataset").json()["data"]
    second = client.get(f"/api/v1/scenario-packs/{PACK_CODES[1]}/demo-dataset").json()["data"]
    assert first["scenario_pack_id"] != second["scenario_pack_id"]
    assert first["source_ref"] != second["source_ref"]
    assert first["dataset_code"] != second["dataset_code"]
    assert (
        first["virtual_customer_profile"]["company_name"]
        != second["virtual_customer_profile"]["company_name"]
    )
    # 业务记录计数随场景包独立，证明不共享运行态
    assert first["stats"]["business_records"] != second["stats"]["business_records"]


def test_demo_dataset_stats_reflect_scenario_pack():
    # TC-067：stats 按场景包独立聚合（product 业务记录 4 / project 5）
    product = client.get("/api/v1/scenario-packs/product_business/demo-dataset").json()["data"]
    assert product["stats"]["knowledge_items"] == 2
    assert product["stats"]["business_records"] == 4
    assert product["stats"]["historical_conversations"] == 2
    assert product["stats"]["knowledge_gaps"] == 2
    assert product["stats"]["summaries"] == 1

    project = client.get("/api/v1/scenario-packs/project_business/demo-dataset").json()["data"]
    assert project["stats"]["knowledge_items"] == 2
    assert project["stats"]["business_records"] == 5


def test_demo_dataset_uses_virtual_customer_names():
    # 确认演示数据用虚拟客户名（合规：不含真实公司名）
    product = client.get("/api/v1/scenario-packs/product_business/demo-dataset").json()["data"]
    assert product["virtual_customer_profile"]["company_name"] == "明烁灯饰样例客户"
    project = client.get("/api/v1/scenario-packs/project_business/demo-dataset").json()["data"]
    assert project["virtual_customer_profile"]["company_name"] == "云栖智能样例客户"


def test_get_demo_dataset_unknown_pack_returns_404():
    response = client.get(f"/api/v1/scenario-packs/{UNKNOWN_PACK}/demo-dataset")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "SCENARIO_PACK_NOT_FOUND"
