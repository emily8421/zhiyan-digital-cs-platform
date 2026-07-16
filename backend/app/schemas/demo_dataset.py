"""API-014 场景包 Demo Dataset 模型（Phase2.5 / Phase3A）。

口径：每个启用场景包绑定独立 Demo Dataset 与虚拟客户资料包，互不串用；
数据源模式默认 demo_sandbox，所有样例数据带 mock + source_ref 标识。
依据：docs/07-api-spec.md §API-014、docs/design/scenario-packs.md
「Product Sandbox 场景包数据集增量」、docs/09-verification.md TC-067 / TC-069 / TC-071。
"""

from typing import Any

from pydantic import BaseModel, Field


class VirtualCustomerProfileSummary(BaseModel):
    """API-014 响应中对外暴露的虚拟客户资料摘要。

    完整资料（公司背景、产品目录、FAQ、角色等）保留在 Demo Dataset 数据文件里，
    供前端展示消费，但不在本接口返回真实隐私或可联系信息。
    """

    company_name: str
    business_type: str
    summary: str


class DemoDatasetStats(BaseModel):
    knowledge_items: int
    business_records: int
    historical_conversations: int
    knowledge_gaps: int
    summaries: int


class DemoDatasetResponse(BaseModel):
    scenario_pack_id: str
    dataset_code: str
    source_mode: str
    source_ref: str
    virtual_customer_profile: VirtualCustomerProfileSummary
    stats: DemoDatasetStats
    mock: bool = True


# ---- 内部加载模型（校验 Demo Dataset 数据文件结构）----


class VirtualCustomerProfile(BaseModel):
    company_name: str
    business_type: str
    summary: str
    company_background: dict[str, Any] = Field(default_factory=dict)
    product_catalog: list[dict[str, Any]] = Field(default_factory=list)
    faq: list[dict[str, Any]] = Field(default_factory=list)
    roles: list[dict[str, Any]] = Field(default_factory=list)


class DemoConversationSample(BaseModel):
    conversation_id: str
    scenario_pack_id: str
    summary: str
    answer_type: str = "answer"
    mock: bool = True
    source_ref: str


class DemoDatasetData(BaseModel):
    scenario_pack_id: str
    dataset_code: str
    version: str
    source_mode: str
    virtual_customer_profile: VirtualCustomerProfile
    historical_conversations: list[DemoConversationSample] = Field(default_factory=list)
    knowledge_gaps: list[dict[str, Any]] = Field(default_factory=list)
    summaries: list[dict[str, Any]] = Field(default_factory=list)
    handoff_samples: list[dict[str, Any]] = Field(default_factory=list)
    notification_samples: list[dict[str, Any]] = Field(default_factory=list)
