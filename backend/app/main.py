from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.console import router as console_router
from app.api.conversations import router as conversations_router
from app.api.health import router as health_router
from app.api.mock_business import router as mock_business_router
from app.api.scenario_packs import router as scenario_packs_router
from app.api.source_mode import router as source_mode_router
from app.schemas.common import ApiError, ApiException, ErrorResponse, new_request_id


def create_app() -> FastAPI:
    app = FastAPI(title="Zhiyan Digital CS API", version="0.1.0")

    @app.exception_handler(ApiException)
    def handle_api_error(
        request: Request,
        error: ApiException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=error.status_code,
            content=error.response.model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    def handle_validation_error(
        request: Request,
        error: RequestValidationError,
    ) -> JSONResponse:
        response = ErrorResponse(
            request_id=new_request_id(),
            error=ApiError(
                code="VALIDATION_ERROR",
                message="请求参数不合法",
                details={"errors": error.errors()},
            ),
        )
        return JSONResponse(status_code=422, content=response.model_dump())

    app.include_router(health_router)
    app.include_router(console_router, prefix="/api/v1")
    app.include_router(conversations_router, prefix="/api/v1")
    app.include_router(mock_business_router, prefix="/api/v1")
    app.include_router(scenario_packs_router, prefix="/api/v1")
    app.include_router(source_mode_router, prefix="/api/v1")
    return app


app = create_app()
