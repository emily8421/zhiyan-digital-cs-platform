from fastapi import APIRouter

from app.schemas.common import ApiError, ApiException, ApiResponse, ErrorResponse, ResponseMeta, new_request_id
from app.schemas.scenario_packs import ScenarioPack, ScenarioPackSummary
from app.services.scenario_pack_service import (
    ScenarioPackNotFoundError,
    get_scenario_pack,
    list_scenario_pack_summaries,
)

router = APIRouter(tags=["scenario-packs"])


@router.get("/scenario-packs", response_model=ApiResponse[list[ScenarioPackSummary]])
def list_scenario_packs() -> ApiResponse[list[ScenarioPackSummary]]:
    return ApiResponse(
        request_id=new_request_id(),
        data=list_scenario_pack_summaries(),
        meta=ResponseMeta(mock=True),
    )


@router.get(
    "/scenario-packs/{scenario_pack_id}",
    response_model=ApiResponse[ScenarioPack],
    responses={404: {"model": ErrorResponse}},
)
def get_scenario_pack_detail(scenario_pack_id: str) -> ApiResponse[ScenarioPack]:
    try:
        pack = get_scenario_pack(scenario_pack_id)
    except ScenarioPackNotFoundError as error:
        raise ApiException(
            status_code=404,
            response=ErrorResponse(
                request_id=new_request_id(),
                error=ApiError(
                    code="SCENARIO_PACK_NOT_FOUND",
                    message="场景包不存在",
                    details={"scenario_pack_id": error.scenario_pack_code},
                ),
            ),
        ) from error

    return ApiResponse(
        request_id=new_request_id(),
        data=pack,
        meta=ResponseMeta(mock=True),
    )
