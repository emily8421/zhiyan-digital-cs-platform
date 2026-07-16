from fastapi import APIRouter

from app.schemas.common import ApiResponse, ResponseMeta, new_request_id
from app.schemas.source_ref import SourceRefListData
from app.services.source_ref_service import list_source_refs

router = APIRouter(tags=["source-refs"])


@router.get(
    "/source-refs",
    response_model=ApiResponse[SourceRefListData],
)
def list_source_refs_endpoint(
    scenario_pack_id: str | None = None,
    source_mode: str | None = None,
) -> ApiResponse[SourceRefListData]:
    data = list_source_refs(scenario_pack_id=scenario_pack_id, source_mode=source_mode)
    return ApiResponse(
        request_id=new_request_id(),
        data=data,
        meta=ResponseMeta(mock=True),
    )
