"""task-011d / API-016 来源标识查询测试（TC-071）。

- TC-071（REQ-022）：聚合 knowledge / rule / mock_business / demo_dataset 来源标识，
  统一 source_mode=demo_sandbox / mock=true；支持 scenario_pack_id / source_mode 过滤；
  真实模式未授权时返回空（TC-070 门禁口径）。
"""

from fastapi.testclient import TestClient

from app.main import create_app

client = TestClient(create_app())

_AVAILABLE_PACKS = client.get("/api/v1/scenario-packs").json()["data"]
PACK_CODES = [pack["code"] for pack in _AVAILABLE_PACKS]


def test_list_source_refs_aggregates_all_types():
    # TC-071：聚合覆盖 knowledge / rule / mock_business / demo_dataset
    response = client.get("/api/v1/source-refs")
    assert response.status_code == 200
    body = response.json()
    items = body["data"]["items"]
    assert items  # 非空

    source_types = {item["source_type"] for item in items}
    assert {"knowledge", "rule", "mock_business", "demo_dataset"}.issubset(source_types)

    # 全部 demo_sandbox / mock=true，来源标识齐全
    for item in items:
        assert item["source_mode"] == "demo_sandbox"
        assert item["mock"] is True
        assert item["source_ref"]
        assert item["scenario_pack_id"] in PACK_CODES
        assert item["created_at"]
    assert body["meta"]["mock"] is True


def test_list_source_refs_filter_by_scenario_pack():
    # 按 scenario_pack_id 过滤：只返回该场景包的来源标识，不串用
    if len(PACK_CODES) < 2:
        return  # 仅一个场景包时无法验证隔离
    target = PACK_CODES[0]
    response = client.get(f"/api/v1/source-refs?scenario_pack_id={target}")
    assert response.status_code == 200
    items = response.json()["data"]["items"]
    assert items
    assert all(item["scenario_pack_id"] == target for item in items)

    # demo_dataset 来源标识按场景包区分（demo_dataset:{pack}:v1）；知识 / 规则
    # source_ref 跨包可能复用同一资料来源（如 SRC-PRD-001），属正常来源引用，不算串用。
    target_demo = next(item for item in items if item["source_type"] == "demo_dataset")
    assert target_demo["source_ref"] == f"demo_dataset:{target}:v1"
    other = client.get(
        f"/api/v1/source-refs?scenario_pack_id={PACK_CODES[1]}"
    ).json()["data"]["items"]
    other_demo = next(item for item in other if item["source_type"] == "demo_dataset")
    assert other_demo["source_ref"] != target_demo["source_ref"]


def test_list_source_refs_filter_by_demo_sandbox_mode():
    # source_mode=demo_sandbox 返回全部来源标识
    response = client.get("/api/v1/source-refs?source_mode=demo_sandbox")
    assert response.status_code == 200
    assert response.json()["data"]["items"]


def test_list_source_refs_unauthorized_mode_returns_empty():
    # 真实模式未授权：返回空 items（TC-070 门禁口径，不调用真实系统）
    response = client.get("/api/v1/source-refs?source_mode=production_readonly")
    assert response.status_code == 200
    assert response.json()["data"]["items"] == []


def test_list_source_refs_includes_demo_dataset_ref():
    # demo_dataset 来源标识存在（API-014 可追溯 source_ref）
    response = client.get("/api/v1/source-refs")
    items = response.json()["data"]["items"]
    demo_refs = [item for item in items if item["source_type"] == "demo_dataset"]
    assert demo_refs
    for item in demo_refs:
        assert item["source_ref"] == f"demo_dataset:{item['scenario_pack_id']}:v1"
