from datetime import date

from fastapi import APIRouter, Depends, Query

from app.core.permissions import require_console_admin
from app.schemas.common import ApiError, ApiException, ApiResponse, ErrorResponse, ResponseMeta, new_request_id
from app.schemas.audit import AuditLogRecord
from app.schemas.console import (
    DailySummaryData,
    HandoffRecord,
    KnowledgeGapRecord,
    MockNotificationRecord,
    MockNotificationRequest,
    StatusUpdateRequest,
)
from app.services.audit_service import list_audit_logs
from app.services.console_service import (
    ConsoleRecordNotFoundError,
    InvalidConsoleStatusError,
    build_daily_summary,
    create_mock_notification,
    list_handoffs,
    list_knowledge_gaps,
    list_notifications,
    update_handoff_status,
    update_knowledge_gap_status,
)

router = APIRouter(tags=["console"])


@router.get("/handoffs", response_model=ApiResponse[list[HandoffRecord]])
def get_handoffs(
    status: str | None = None,
    risk_level: str | None = None,
    suggested_owner: str | None = None,
) -> ApiResponse[list[HandoffRecord]]:
    return ApiResponse(
        request_id=new_request_id(),
        data=list_handoffs(
            status=status,
            risk_level=risk_level,
            suggested_owner=suggested_owner,
        ),
        meta=ResponseMeta(mock=True),
    )


@router.patch(
    "/handoffs/{handoff_id}",
    response_model=ApiResponse[HandoffRecord],
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
def patch_handoff(
    handoff_id: str,
    payload: StatusUpdateRequest,
    _: None = Depends(require_console_admin),
) -> ApiResponse[HandoffRecord]:
    try:
        handoff = update_handoff_status(
            handoff_id=handoff_id,
            status=payload.status,
            resolution_note=payload.resolution_note,
        )
    except ConsoleRecordNotFoundError as error:
        raise _not_found_error(error) from error
    except InvalidConsoleStatusError as error:
        raise _invalid_status_error(error) from error
    return ApiResponse(
        request_id=new_request_id(),
        data=handoff,
        meta=ResponseMeta(mock=True),
    )


@router.get("/knowledge-gaps", response_model=ApiResponse[list[KnowledgeGapRecord]])
def get_knowledge_gaps(
    status: str | None = None,
    scenario_pack_code: str | None = None,
    tag: str | None = None,
) -> ApiResponse[list[KnowledgeGapRecord]]:
    return ApiResponse(
        request_id=new_request_id(),
        data=list_knowledge_gaps(
            status=status,
            scenario_pack_code=scenario_pack_code,
            tag=tag,
        ),
        meta=ResponseMeta(mock=True),
    )


@router.patch(
    "/knowledge-gaps/{gap_id}",
    response_model=ApiResponse[KnowledgeGapRecord],
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
def patch_knowledge_gap(
    gap_id: str,
    payload: StatusUpdateRequest,
    _: None = Depends(require_console_admin),
) -> ApiResponse[KnowledgeGapRecord]:
    try:
        gap = update_knowledge_gap_status(
            gap_id=gap_id,
            status=payload.status,
            resolution_note=payload.resolution_note,
        )
    except ConsoleRecordNotFoundError as error:
        raise _not_found_error(error) from error
    except InvalidConsoleStatusError as error:
        raise _invalid_status_error(error) from error
    return ApiResponse(
        request_id=new_request_id(),
        data=gap,
        meta=ResponseMeta(mock=True),
    )


@router.get("/notifications/mock", response_model=ApiResponse[list[MockNotificationRecord]])
def get_mock_notifications(
    event_type: str | None = None,
    send_status: str | None = None,
) -> ApiResponse[list[MockNotificationRecord]]:
    return ApiResponse(
        request_id=new_request_id(),
        data=list_notifications(event_type=event_type, send_status=send_status),
        meta=ResponseMeta(mock=True),
    )


@router.post("/notifications/mock", response_model=ApiResponse[MockNotificationRecord])
def post_mock_notification(
    payload: MockNotificationRequest,
    _: None = Depends(require_console_admin),
) -> ApiResponse[MockNotificationRecord]:
    return ApiResponse(
        request_id=new_request_id(),
        data=create_mock_notification(
            event_type=payload.event_type,
            related_id=payload.related_id,
            target_type=payload.target_type,
        ),
        meta=ResponseMeta(mock=True),
    )


@router.get("/summaries/daily", response_model=ApiResponse[DailySummaryData])
def get_daily_summary(
    summary_date: date | None = Query(default=None, alias="date"),
) -> ApiResponse[DailySummaryData]:
    return ApiResponse(
        request_id=new_request_id(),
        data=build_daily_summary(summary_date),
        meta=ResponseMeta(mock=True),
    )


@router.get("/audit-logs", response_model=ApiResponse[list[AuditLogRecord]])
def get_audit_logs() -> ApiResponse[list[AuditLogRecord]]:
    return ApiResponse(
        request_id=new_request_id(),
        data=list_audit_logs(),
        meta=ResponseMeta(mock=True),
    )


def _not_found_error(error: ConsoleRecordNotFoundError) -> ApiException:
    return ApiException(
        status_code=404,
        response=ErrorResponse(
            request_id=new_request_id(),
            error=ApiError(
                code="CONSOLE_RECORD_NOT_FOUND",
                message="控制台 Demo 记录不存在",
                details={"record_type": error.record_type, "record_id": error.record_id},
            ),
        ),
    )


def _invalid_status_error(error: InvalidConsoleStatusError) -> ApiException:
    return ApiException(
        status_code=400,
        response=ErrorResponse(
            request_id=new_request_id(),
            error=ApiError(
                code="INVALID_CONSOLE_STATUS",
                message="控制台 Demo 状态不合法",
                details={"record_type": error.record_type, "status": error.status},
            ),
        ),
    )
