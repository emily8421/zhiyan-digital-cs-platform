"""来源标识聚合服务（API-016，Phase2.5 / Phase3A）。

口径：聚合场景包 knowledge / rule / mock_business 与 Demo Dataset 的 source_ref，
统一标记 source_mode=demo_sandbox / mock=true，供 Console 与验收抽样确认
回答、通知、摘要和业务记录的来源；真实数据模式未授权，不返回真实来源标识。
依据：docs/07-api-spec.md §API-016、docs/design/frontend-interaction.md
「数据源模式显示」、docs/09-verification.md TC-071。
"""

from app.schemas.source_ref import SourceRefItem, SourceRefListData
from app.services.scenario_pack_service import load_scenario_packs

DEMO_SANDBOX_MODE = "demo_sandbox"

# Demo seed 来源标识的统一创建时间（演示性质，非运行时时间戳，便于稳定抽样与回归）。
_DEMO_SEED_CREATED_AT = "2026-07-16T00:00:00Z"


def _demo_dataset_source_ref(scenario_pack_id: str) -> str:
    return f"demo_dataset:{scenario_pack_id}:v1"


def list_source_refs(
    scenario_pack_id: str | None = None,
    source_mode: str | None = None,
) -> SourceRefListData:
    """聚合来源标识。

    - scenario_pack_id：限定单个场景包；None 表示全部场景包。
    - source_mode：限定数据源模式；当前仅 demo_sandbox 有来源标识，
      传其他模式返回空 items（真实模式未授权，符合 TC-070 门禁口径）。
    """
    if source_mode is not None and source_mode != DEMO_SANDBOX_MODE:
        return SourceRefListData(items=[])

    items: list[SourceRefItem] = []
    for pack_code, pack in load_scenario_packs().items():
        if scenario_pack_id is not None and pack_code != scenario_pack_id:
            continue

        for knowledge_item in pack.knowledge_items:
            items.append(_build_item(knowledge_item.source_ref, "knowledge", pack_code))
        for rule_item in pack.rule_items:
            items.append(_build_item(rule_item.source_ref, "rule", pack_code))
        for mock_record in pack.mock_business_records:
            if not mock_record.source_ref:
                continue
            items.append(_build_item(mock_record.source_ref, "mock_business", pack_code))
        items.append(_build_item(_demo_dataset_source_ref(pack_code), "demo_dataset", pack_code))

    return SourceRefListData(items=items)


def _build_item(source_ref: str, source_type: str, scenario_pack_id: str) -> SourceRefItem:
    return SourceRefItem(
        source_ref=source_ref,
        source_type=source_type,
        scenario_pack_id=scenario_pack_id,
        source_mode=DEMO_SANDBOX_MODE,
        mock=True,
        created_at=_DEMO_SEED_CREATED_AT,
    )
