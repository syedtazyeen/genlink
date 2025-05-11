from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException 
from http import HTTPStatus

# Global exception handler
async def global_exception_handler(_: Request, exc: Exception):
    """Handles global exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "error": HTTPStatus(500).name,
            "message": str(exc),
        },
    )

# HTTP exception handler
async def http_exception_handler(_: Request, exc: HTTPException):
    """Handles HTTP exceptions."""
    status_phrase = HTTPStatus(exc.status_code).name if exc.status_code in HTTPStatus._value2member_map_ else exc.__class__.__name__
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": status_phrase,
            "message": str(exc.detail),
        },
    )


# Validation exception handler
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    """Handles validation errors."""
    errors = []
    for error in exc.errors():
        error_msg = f"{error['loc'][-1]}: {error['msg']}"
        errors.append(error_msg)

    return JSONResponse(
        status_code=422,
        content={
            "message": "Request validation error",
            "data": errors,
            "error": HTTPStatus(422).name,
        },
    )
