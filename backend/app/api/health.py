from fastapi import APIRouter

from app.schemas.common import ApiResponse, ResponseMeta

router = APIRouter(tags=["health"])


@router.get("/health", response_model=ApiResponse[dict[str, str]])
def health_check() -> ApiResponse[dict[str, str]]:
    return ApiResponse(
        request_id="req_health",
        data={"status": "ok"},
        meta=ResponseMeta(mock=True),
    )
