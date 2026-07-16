"""场景包 Demo Dataset 服务（API-014，Phase2.5 / Phase3A）。

口径：每个启用场景包绑定独立 Demo Dataset 与虚拟客户资料包，互不串用；
默认 demo_sandbox，stats 聚合场景包知识 / 业务记录计数与 Demo Dataset 预置样例计数。
依据：docs/07-api-spec.md §API-014、docs/design/scenario-packs.md
「Product Sandbox 场景包数据集增量」、docs/09-verification.md TC-067 / TC-069 / TC-071。
"""

import json
from functools import lru_cache
from pathlib import Path

from app.schemas.demo_dataset import (
    DemoDatasetData,
    DemoDatasetResponse,
    DemoDatasetStats,
    VirtualCustomerProfileSummary,
)
from app.services.scenario_pack_service import get_scenario_pack

_DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "demo_datasets"


@lru_cache
def load_demo_datasets() -> dict[str, DemoDatasetData]:
    datasets: dict[str, DemoDatasetData] = {}
    for path in sorted(_DATA_DIR.glob("*.json")):
        raw_data = json.loads(path.read_text(encoding="utf-8-sig"))
        data = DemoDatasetData.model_validate(raw_data)
        datasets[data.scenario_pack_id] = data
    return datasets


def _demo_source_ref(scenario_pack_id: str) -> str:
    return f"demo_dataset:{scenario_pack_id}:v1"


def get_demo_dataset(scenario_pack_id: str) -> DemoDatasetResponse:
    """查询场景包 Demo Dataset 摘要。

    场景包不存在时由 get_scenario_pack 抛 ScenarioPackNotFoundError（API 层映射 404）。
    若场景包存在但缺少独立 Demo Dataset 数据文件，则基于场景包返回降级摘要
    （历史会话 / 缺口 / 摘要计数为 0），保证接口稳定可用。
    """
    pack = get_scenario_pack(scenario_pack_id)
    data = load_demo_datasets().get(scenario_pack_id)

    if data is not None:
        profile = data.virtual_customer_profile
        profile_summary = VirtualCustomerProfileSummary(
            company_name=profile.company_name,
            business_type=profile.business_type,
            summary=profile.summary,
        )
        dataset_code = data.dataset_code
        source_mode = data.source_mode
        historical_conversations = len(data.historical_conversations)
        knowledge_gaps = len(data.knowledge_gaps)
        summaries = len(data.summaries)
    else:
        # 降级：无独立 Demo Dataset 文件时，用场景包基本信息构造摘要。
        profile_summary = VirtualCustomerProfileSummary(
            company_name=pack.name,
            business_type=scenario_pack_id,
            summary=pack.description,
        )
        dataset_code = f"{scenario_pack_id}_demo_v1"
        source_mode = "demo_sandbox"
        historical_conversations = 0
        knowledge_gaps = 0
        summaries = 0

    stats = DemoDatasetStats(
        knowledge_items=len(pack.knowledge_items),
        business_records=len(pack.mock_business_records),
        historical_conversations=historical_conversations,
        knowledge_gaps=knowledge_gaps,
        summaries=summaries,
    )
    return DemoDatasetResponse(
        scenario_pack_id=scenario_pack_id,
        dataset_code=dataset_code,
        source_mode=source_mode,
        source_ref=_demo_source_ref(scenario_pack_id),
        virtual_customer_profile=profile_summary,
        stats=stats,
        mock=True,
    )
