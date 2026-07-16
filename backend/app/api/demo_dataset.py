from fastapi import APIRouter

from app.schemas.common import ApiError, ApiException, ApiResponse, ErrorResponse, ResponseMeta, new_request_id
from app.schemas.demo_dataset import DemoDatasetResponse
from app.services.demo_dataset_service import get_demo_dataset
from app.services.scenario_pack_service import ScenarioPackNotFoundError

router = APIRouter(tags=["demo-dataset"])


@router.get(
    "/scenario-packs/{scenario_pack_id}/demo-dataset",
    response_model=ApiResponse[DemoDatasetResponse],
    responses={404: {"model": ErrorResponse}},
)
def get_scenario_pack_demo_dataset(
    scenario_pack_id: str,
) -> ApiResponse[DemoDatasetResponse]:
    try:
        dataset = get_demo_dataset(scenario_pack_id)
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
        data=dataset,
        meta=ResponseMeta(mock=True),
    )
