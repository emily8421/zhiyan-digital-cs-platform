"""场景包数据源模式门禁服务（API-013，Phase2.5 / Phase3A）。

口径：默认 demo_sandbox 立即放行（读取场景包独立模拟数据）；
customer_sandbox_readonly / production_readonly / production_writeback 在本阶段
仅作门禁状态展示，未授权时返回 no_go 并保持 demo_sandbox，绝不调用真实系统。
依据：docs/07-api-spec.md §API-013、docs/design/integration-adapters.md
「Product Sandbox 数据源门禁增量」、docs/09-verification.md TC-066 / TC-070。
"""

from app.schemas.source_mode import AVAILABLE_SOURCE_MODES, GateStatus, SourceModeResponse
from app.services.scenario_pack_service import get_scenario_pack

DEMO_SANDBOX_MODE = "demo_sandbox"

# Phase2.5 / Phase3A 真实模式均未满足授权，统一门禁原因（解锁条件见
# docs/design/integration-adapters.md 门禁增量表）。
_REAL_MODE_GATE_REASONS: list[str] = [
    "missing_customer_authorization",
    "field_mapping_not_configured",
    "security_review_pending",
    "readonly_verification_pending",
]

# 内存态：每个场景包当前生效模式。Demo 性质，进程重启回到 demo_sandbox 默认，
# 不落库、不跨进程共享。
_effective_modes: dict[str, str] = {}


def _demo_source_ref(scenario_pack_id: str) -> str:
    return f"demo_dataset:{scenario_pack_id}:v1"


def _build_response(
    scenario_pack_id: str,
    source_mode: str,
    gate_status: GateStatus,
    gate_reasons: list[str],
) -> SourceModeResponse:
    source_ref = _demo_source_ref(scenario_pack_id) if source_mode == DEMO_SANDBOX_MODE else ""
    return SourceModeResponse(
        scenario_pack_id=scenario_pack_id,
        source_mode=source_mode,
        available_modes=list(AVAILABLE_SOURCE_MODES),
        gate_status=gate_status,
        gate_reasons=list(gate_reasons),
        source_ref=source_ref,
        mock=True,
    )


def get_source_mode(scenario_pack_id: str) -> SourceModeResponse:
    """查询场景包当前生效数据源模式。默认 demo_sandbox，gate_status=go。

    场景包不存在时由 get_scenario_pack 抛 ScenarioPackNotFoundError（API 层映射 404）。
    """
    get_scenario_pack(scenario_pack_id)
    effective_mode = _effective_modes.get(scenario_pack_id, DEMO_SANDBOX_MODE)
    return _build_response(scenario_pack_id, effective_mode, "go", [])


def update_source_mode(scenario_pack_id: str, requested_mode: str) -> SourceModeResponse:
    """评估切换到目标数据源模式的门禁结果。

    - demo_sandbox：立即放行（go），更新生效模式；
    - 真实模式：Phase2.5 / Phase3A 未授权，返回 no_go + 原因，保持 demo_sandbox，
      不调用真实系统。

    响应的 source_mode 为本次评估的目标模式，gate_status 反映该模式当前是否可用。
    """
    get_scenario_pack(scenario_pack_id)
    if requested_mode == DEMO_SANDBOX_MODE:
        _effective_modes[scenario_pack_id] = DEMO_SANDBOX_MODE
        return _build_response(scenario_pack_id, DEMO_SANDBOX_MODE, "go", [])

    return _build_response(
        scenario_pack_id,
        requested_mode,
        "no_go",
        _REAL_MODE_GATE_REASONS,
    )
