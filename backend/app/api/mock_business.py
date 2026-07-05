from fastapi import APIRouter

from app.schemas.common import ApiError, ApiException, ApiResponse, ErrorResponse, ResponseMeta, new_request_id
from app.schemas.mock_business import MockBusinessRecordResponse
from app.services.mock_business_service import MockRecordNotFoundError, get_mock_business_record, list_mock_business_records

router = APIRouter(tags=["mock-business"])


@router.get(
    "/mock-business",
    response_model=ApiResponse[list[MockBusinessRecordResponse]],
)
def list_mock_business(
    record_type: str | None = None,
    scenario_pack_code: str | None = None,
) -> ApiResponse[list[MockBusinessRecordResponse]]:
    return ApiResponse(
        request_id=new_request_id(),
        data=list_mock_business_records(
            record_type=record_type,
            scenario_pack_code=scenario_pack_code,
        ),
        meta=ResponseMeta(mock=True),
    )


@router.get(
    "/mock-business/{record_type}/{external_ref}",
    response_model=ApiResponse[MockBusinessRecordResponse],
    responses={404: {"model": ErrorResponse}},
)
def get_mock_business(
    record_type: str,
    external_ref: str,
) -> ApiResponse[MockBusinessRecordResponse]:
    try:
        record = get_mock_business_record(record_type, external_ref)
    except MockRecordNotFoundError as error:
        raise ApiException(
            status_code=404,
            response=ErrorResponse(
                request_id=new_request_id(),
                error=ApiError(
                    code="MOCK_RECORD_NOT_FOUND",
                    message="Mock 业务记录不存在",
                    details={"record_type": error.record_type, "external_ref": error.external_ref},
                ),
            ),
        ) from error

    return ApiResponse(
        request_id=new_request_id(),
        data=record,
        meta=ResponseMeta(mock=True),
    )
