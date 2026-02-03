"""Custom exception classes and handlers."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AppException(Exception):
    """Base application exception."""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundException(AppException):
    """Resource not found exception."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)


class ConflictException(AppException):
    """Conflict exception for duplicate resources."""

    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, status_code=409)


class ValidationException(AppException):
    """Validation error exception."""

    def __init__(self, message: str = "Validation error"):
        super().__init__(message, status_code=400)


def register_exception_handlers(app: FastAPI) -> None:
    """Register custom exception handlers with the FastAPI app."""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )
