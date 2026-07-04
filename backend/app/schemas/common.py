from typing import Generic, TypeVar
from uuid import uuid4

from pydantic import BaseModel, Field

DataT = TypeVar("DataT")


class ResponseMeta(BaseModel):
    mock: bool = True


class ApiError(BaseModel):
    code: str
    message: str
    details: dict[str, object] = Field(default_factory=dict)


class ApiResponse(BaseModel, Generic[DataT]):
    request_id: str
    data: DataT
    meta: ResponseMeta = Field(default_factory=ResponseMeta)


class ErrorResponse(BaseModel):
    request_id: str
    error: ApiError


class ApiException(Exception):
    def __init__(self, status_code: int, response: ErrorResponse) -> None:
        self.status_code = status_code
        self.response = response


def new_request_id() -> str:
    return f"req_{uuid4().hex[:12]}"
