"""控制台角色权限依赖（Phase2 MVP 试点，对应 WC-C-001）。

口径：Demo 级「请求头声明角色」(X-Console-Role)，由后端 Depends 强制；
非生产鉴权（无登录 / 无 token / 无密码），仅用于试点演示的角色可见性。
真实鉴权（账号 / 登录态 / 多租户）属 Phase4，不在本阶段实现。

默认角色为 viewer（只读）；未声明 X-Console-Role 时按只读处理，写操作返回 403。
"""

from fastapi import Header

from app.schemas.common import ApiError, ApiException, ErrorResponse, new_request_id

ADMIN_ROLE = "admin"
VIEWER_ROLE = "viewer"


def _forbidden_console_write_error() -> ApiException:
    return ApiException(
        status_code=403,
        response=ErrorResponse(
            request_id=new_request_id(),
            error=ApiError(
                code="FORBIDDEN_CONSOLE_WRITE",
                message="当前控制台角色无写权限，需要管理员角色",
                details={"required_role": ADMIN_ROLE},
            ),
        ),
    )


def require_console_admin(
    x_console_role: str = Header(default=VIEWER_ROLE, alias="X-Console-Role"),
) -> None:
    """控制台写操作依赖：仅 admin 角色放行，其余（含未声明）返回 403。

    后端执行角色校验，不依赖前端隐藏 / 禁用按钮；前端可见性仅作体验补充。
    """
    if x_console_role != ADMIN_ROLE:
        raise _forbidden_console_write_error()
