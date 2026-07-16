"""API-016 来源标识查询模型（Phase2.5 / Phase3A）。

口径：聚合场景包 knowledge / rule / mock_business 与 Demo Dataset 的来源标识，
统一 demo_sandbox / mock=true，供 Console 与验收抽样确认回答、通知、摘要和业务记录的来源。
依据：docs/07-api-spec.md §API-016、docs/design/frontend-interaction.md
「数据源模式显示」、docs/09-verification.md TC-071。
"""

from pydantic import BaseModel


class SourceRefItem(BaseModel):
    """单条来源标识记录。

    生产敏感字段必须脱敏或不返回；本阶段全部为 demo_sandbox 演示来源。
    """

    source_ref: str
    source_type: str
    scenario_pack_id: str
    source_mode: str
    mock: bool = True
    created_at: str


class SourceRefListData(BaseModel):
    items: list[SourceRefItem]
