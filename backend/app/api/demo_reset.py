from fastapi import APIRouter, Depends

from app.core.permissions import require_console_admin
from app.schemas.common import ApiError, ApiException, ApiResponse, ErrorResponse, ResponseMeta, new_request_id
from app.schemas.demo_reset import DemoResetRequest, DemoResetResponse
from app.services.demo_reset_service import (
    DemoResetNotConfirmedError,
    DemoResetScopeError,
    reset_scenario_pack,
)
from app.services.scenario_pack_service import ScenarioPackNotFoundError

router = APIRouter(tags=["demo-reset"])


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


@router.post(
    "/scenario-packs/{scenario_pack_id}/demo-reset",
    response_model=ApiResponse[DemoResetResponse],
    responses={400: {"model": ErrorResponse}, 403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
def post_scenario_pack_demo_reset(
    scenario_pack_id: str,
    payload: DemoResetRequest,
    _: None = Depends(require_console_admin),
) -> ApiResponse[DemoResetResponse]:
    try:
        result = reset_scenario_pack(scenario_pack_id, payload.runtime_scope, payload.confirm)
    except ScenarioPackNotFoundError as error:
        raise _pack_not_found_error(error) from error
    except DemoResetScopeError as error:
        raise ApiException(
            status_code=400,
            response=ErrorResponse(
                request_id=new_request_id(),
                error=ApiError(
                    code="VALIDATION_ERROR",
                    message="不支持的 reset 作用域，仅支持 current_scenario_pack",
                    details={"runtime_scope": error.runtime_scope},
                ),
            ),
        ) from error
    except DemoResetNotConfirmedError as error:
        raise ApiException(
            status_code=400,
            response=ErrorResponse(
                request_id=new_request_id(),
                error=ApiError(
                    code="VALIDATION_ERROR",
                    message="需确认后才能重置演示运行态",
                    details={"confirm": False},
                ),
            ),
        ) from error

    return ApiResponse(
        request_id=new_request_id(),
        data=result,
        meta=ResponseMeta(mock=True),
    )
