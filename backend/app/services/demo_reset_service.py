"""场景包 Demo Sandbox 重置服务（API-015，Phase2.5 / Phase3A）。

口径：仅重置当前场景包演示运行态，保留 seed 初始演示态、场景包配置、
Demo Dataset、真实数据门禁配置与其他场景包数据。
依据：docs/07-api-spec.md §API-015、docs/09-verification.md TC-068。
"""

from datetime import UTC, datetime
from uuid import uuid4

from app.schemas.demo_reset import DemoResetResponse
from app.services.console_service import reset_console_runtime_for_pack
from app.services.conversation_service import reset_conversations_for_pack
from app.services.scenario_pack_service import get_scenario_pack
from app.services.source_mode_service import DEMO_SANDBOX_MODE, get_source_mode

_RUNTIME_SCOPE = "current_scenario_pack"


class DemoResetScopeError(Exception):
    def __init__(self, runtime_scope: str) -> None:
        self.runtime_scope = runtime_scope


class DemoResetNotConfirmedError(Exception):
    pass


def reset_scenario_pack(
    scenario_pack_code: str,
    runtime_scope: str,
    confirm: bool,
) -> DemoResetResponse:
    """重置当前场景包演示运行态。

    场景包不存在时由 get_scenario_pack 抛 ScenarioPackNotFoundError（API 层映射 404）。
    runtime_scope 必须为 current_scenario_pack；confirm 必须为 True。
    """
    get_scenario_pack(scenario_pack_code)
    if runtime_scope != _RUNTIME_SCOPE:
        raise DemoResetScopeError(runtime_scope)
    if not confirm:
        raise DemoResetNotConfirmedError()

    conversations_removed = reset_conversations_for_pack(scenario_pack_code)
    console_counts = reset_console_runtime_for_pack(scenario_pack_code)
    affected_counts = {"conversations": conversations_removed, **console_counts}

    source_mode_value = DEMO_SANDBOX_MODE
    try:
        source_mode_value = get_source_mode(scenario_pack_code).source_mode
    except Exception:
        pass

    return DemoResetResponse(
        scenario_pack_id=scenario_pack_code,
        reset_id=f"demo_reset_{uuid4().hex[:8]}",
        reset_at=datetime.now(tz=UTC).astimezone().isoformat(timespec="seconds"),
        reset_scope=runtime_scope,
        affected_counts=affected_counts,
        source_mode=source_mode_value,
        mock=True,
    )
