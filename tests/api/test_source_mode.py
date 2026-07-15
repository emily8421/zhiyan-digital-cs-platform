"""task-011a / API-013 场景包数据源模式门禁测试（TC-066 / TC-070）。"""

from fastapi.testclient import TestClient

from app.main import create_app

client = TestClient(create_app())

# 动态取一个真实存在的场景包，避免硬编码 pack code 导致用例脆弱。
_AVAILABLE_PACKS = client.get("/api/v1/scenario-packs").json()["data"]
DEFAULT_PACK = _AVAILABLE_PACKS[0]["code"] if _AVAILABLE_PACKS else "product_business"
UNKNOWN_PACK = "no_such_scenario_pack"


def test_get_source_mode_defaults_to_demo_sandbox():
    response = client.get(f"/api/v1/scenario-packs/{DEFAULT_PACK}/source-mode")
    assert response.status_code == 200
    body = response.json()
    data = body["data"]
    assert data["scenario_pack_id"] == DEFAULT_PACK
    assert data["source_mode"] == "demo_sandbox"
    assert data["gate_status"] == "go"
    assert data["available_modes"] == [
        "demo_sandbox",
        "customer_sandbox_readonly",
        "production_readonly",
        "production_writeback",
    ]
    assert data["source_ref"] == f"demo_dataset:{DEFAULT_PACK}:v1"
    assert body["meta"]["mock"] is True


def test_patch_real_mode_returns_no_go_without_calling_real_system():
    response = client.patch(
        f"/api/v1/scenario-packs/{DEFAULT_PACK}/source-mode",
        headers={"X-Console-Role": "admin"},
        json={"source_mode": "customer_sandbox_readonly"},
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["source_mode"] == "customer_sandbox_readonly"
    assert data["gate_status"] == "no_go"
    assert data["gate_reasons"], "门禁未通过必须记录原因"
    assert data["source_ref"] == ""  # 真实来源未配置

    # 生效模式仍为 demo_sandbox：真实模式不切换、不调用真实系统
    follow = client.get(f"/api/v1/scenario-packs/{DEFAULT_PACK}/source-mode")
    follow_data = follow.json()["data"]
    assert follow_data["source_mode"] == "demo_sandbox"
    assert follow_data["gate_status"] == "go"


def test_patch_demo_mode_is_go():
    response = client.patch(
        f"/api/v1/scenario-packs/{DEFAULT_PACK}/source-mode",
        headers={"X-Console-Role": "admin"},
        json={"source_mode": "demo_sandbox"},
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["source_mode"] == "demo_sandbox"
    assert data["gate_status"] == "go"
    assert data["gate_reasons"] == []
    assert data["source_ref"] == f"demo_dataset:{DEFAULT_PACK}:v1"


def test_patch_source_mode_requires_admin_role():
    response = client.patch(
        f"/api/v1/scenario-packs/{DEFAULT_PACK}/source-mode",
        headers={"X-Console-Role": "viewer"},
        json={"source_mode": "demo_sandbox"},
    )
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "FORBIDDEN_CONSOLE_WRITE"


def test_get_source_mode_unknown_pack_returns_404():
    response = client.get(f"/api/v1/scenario-packs/{UNKNOWN_PACK}/source-mode")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "SCENARIO_PACK_NOT_FOUND"
