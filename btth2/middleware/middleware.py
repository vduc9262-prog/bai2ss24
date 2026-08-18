from enum import Enum
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, status
from fastapi.responses import JSONResponse


class UserRole(str, Enum):
    DISPATCHER = "DISPATCHER"
    DRIVER = "DRIVER"
    CUSTOMER_SUPPORT = "CUSTOMER_SUPPORT"


MANAGEMENT_ROLES = {

    ("POST", "/api/v1/orders/assign"): {
        UserRole.DISPATCHER
    },

    ("PATCH", "/api/v1/orders/status"): {
        UserRole.DISPATCHER,
        UserRole.DRIVER
    },

    ("GET", "/api/v1/orders/track"): {
        UserRole.DISPATCHER,
        UserRole.DRIVER,
        UserRole.CUSTOMER_SUPPORT
    }
}


class RBACMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        method = request.method

        path = request.url.path

        allowed_roles = MANAGEMENT_ROLES.get(
            (method, path)
        )


        if allowed_roles is None:
            return await call_next(request)

        role = request.headers.get("X-Role-Identity")

 
        if role is None:
            return JSONResponse(
                content={
                    "status": "Rejected",
                    "reason": "Unauthorized action for this role"
                },
                status_code=status.HTTP_403_FORBIDDEN
            )

        try:
            check_role = UserRole(role.upper())

        except ValueError:

            return JSONResponse(
                content={
                    "status": "Rejected",
                    "reason": "Unauthorized action for this role"
                },
                status_code=status.HTTP_403_FORBIDDEN
            )


        if check_role not in allowed_roles:

            return JSONResponse(
                content={
                    "status": "Rejected",
                    "reason": "Unauthorized action for this role"
                },
                status_code=status.HTTP_403_FORBIDDEN
            )

        return await call_next(request)