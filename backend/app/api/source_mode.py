from fastapi import APIRouter, Depends

from app.core.permissions import require_console_admin
from app.schemas.common import ApiError, ApiException, ApiResponse, ErrorResponse, ResponseMeta, new_request_id
from app.schemas.source_mode import SourceModeResponse, SourceModeUpdateRequest
from app.services.scenario_pack_service import ScenarioPackNotFoundError
from app.services.source_mode_service import get_source_mode, update_source_mode

router = APIRouter(tags=["source-mode"])


def _pack_not_found_error(error: ScenarioPackNotFoundError) -> ApiException:
    return ApiException(
        status_code=404,
        response=ErrorResponse(
            request_id=new_request_id(),
            error=ApiError(
                code="SCENARIO_PACK_NOT_FOUND",
                message="场景包不存在",
                details={"scenario_pack_id": error.scenario_pack_code},
            ),
        ),
    )


@router.get(
    "/scenario-packs/{scenario_pack_id}/source-mode",
    response_model=ApiResponse[SourceModeResponse],
    responses={404: {"model": ErrorResponse}},
)
def get_scenario_pack_source_mode(
    scenario_pack_id: str,
) -> ApiResponse[SourceModeResponse]:
    try:
        source_mode = get_source_mode(scenario_pack_id)
    except ScenarioPackNotFoundError as error:
        raise _pack_not_found_error(error) from error

    return ApiResponse(
        request_id=new_request_id(),
        data=source_mode,
        meta=ResponseMeta(mock=True),
    )


@router.patch(
    "/scenario-packs/{scenario_pack_id}/source-mode",
    response_model=ApiResponse[SourceModeResponse],
    responses={400: {"model": ErrorResponse}, 403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
def patch_scenario_pack_source_mode(
    scenario_pack_id: str,
    payload: SourceModeUpdateRequest,
    _: None = Depends(require_console_admin),
) -> ApiResponse[SourceModeResponse]:
    try:
        source_mode = update_source_mode(scenario_pack_id, payload.source_mode)
    except ScenarioPackNotFoundError as error:
        raise _pack_not_found_error(error) from error

    return ApiResponse(
        request_id=new_request_id(),
        data=source_mode,
        meta=ResponseMeta(mock=True),
    )
